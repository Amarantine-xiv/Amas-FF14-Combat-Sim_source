import copy
import math
import numpy as np

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.stat_fns import StatFns
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.timeline_builders.skill_timing_info import (
    SkillTimingInfo,
)
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.timeline_builders.timeline_utils import TimelineUtils
from ama_xiv_combat_sim.simulator.trackers.channeling_tracker import ChannelingTracker
from ama_xiv_combat_sim.simulator.trackers.combo_tracker import ComboTracker
from ama_xiv_combat_sim.simulator.trackers.job_resource_tracker import (
    JobResourceTracker,
)
from ama_xiv_combat_sim.simulator.trackers.status_effect_tracker import (
    StatusEffectTracker,
)
from ama_xiv_combat_sim.simulator.utils import Utils


class RotationBuilder:
    """A utility class used to turn 1) a series of button (skills) pressed and optionally the specific time they were pressed, and 2) proc application times into a series of damage instances and applicable buffs/debuffs."""

    def __init__(
        self,
        stats,
        skill_library,
        snap_dots_to_server_tick_starting_at=None,
        enable_autos=False,
        ignore_trailing_dots=False,
        fight_start_time=None,
        # downtime_windows can either be: 1) a tuple of tuples, containing downtime windows, or
        # 2) a dict of tuples, keyed by the name of the target for which the downtime window applies to.
        # Each downtime window is a tuple of the form (start, end, optional damage_class) which is
        # interpreted as a downtime window of the half-open interval [start, end). All damage of type
        # damage_class (assumed to be of type DamageClass) will be disabled in this window. If
        # damage_class is not specified, ALL damage that otherwise could've applied in the given
        # window will be removed. Example:
        # downtime_windows={'Default Target': ((5.2, 9.3), (102.1, 120.2, DamageClass.AUTO),)}
        # to indicate downtimes for the target named "Default Target", where the boss cannot
        # be damaged in the interval [5.2, 9.3), and the player simply does not auto-attack
        # the boss in the interval [102.1, 120.2)- eg, the player had to disengage from the boss,
        # but the boss was still targetable and still generally takes damage.
        downtime_windows=(),
        default_target=SimConsts.DEFAULT_TARGET,
        use_strict_skill_naming=True,
    ):
        self.__stats = stats
        # snap_dots_to_server_tick_starting_at is in SECONDS
        self.__snap_dots_to_server_tick_starting_at = (
            snap_dots_to_server_tick_starting_at
        )
        self._skill_library = skill_library
        self.set_fight_start_time(fight_start_time)
        self._q_others = []  # (time, skill, skill_modifier, job_class, targets)
        self._q_self = []  # (time, skill, skill_modifier, job_class, targets)

        self._q_dot_skills = {}  # this is a map
        self.__q_button_press_timing = []
        self._q_snapshot_and_applications = SnapshotAndApplicationEvents()
        self.__enable_autos = enable_autos
        self.__ignore_trailing_dots = ignore_trailing_dots

        self.__status_effect_priority = None
        self.__timestamps_and_main_target = []
        assert isinstance(
            default_target, str
        ), "Default target should be a string- did you accidentally make it a tuple?"
        # save original for idempotency
        self.__original_downtime_windows = RotationBuilder.__init_downtime_windows(
            downtime_windows
        )
        self.__downtime_windows = None
        self.__default_target = default_target
        self.__use_strict_skill_naming = use_strict_skill_naming
        self.__all_targets = set()
        self.__non_auto_periods = []

    def get_skill_library(self):
        return self._skill_library

    @staticmethod
    def __do_init_downtime_windows(downtime_windows):
        downtime_windows = list(downtime_windows)

        # convert to ms
        for i, downtime_window in enumerate(downtime_windows):
            downtime_window = list(downtime_window)
            downtime_window[0] *= 1000
            downtime_window[1] *= 1000
            if len(downtime_window) < 3:
                downtime_window.append(None)

            downtime_windows[i] = tuple(downtime_window)
        return tuple(downtime_windows)

    @staticmethod
    def __init_downtime_windows(downtime_windows):
        if isinstance(downtime_windows, tuple):
            downtime_windows = RotationBuilder.__do_init_downtime_windows(
                downtime_windows
            )
        else:
            for target, downtime_windows_use in downtime_windows.items():
                downtime_windows[target] = RotationBuilder.__do_init_downtime_windows(
                    downtime_windows_use
                )
        return downtime_windows

    def __process_downtime_windows(self):
        # save original for idempotency
        if isinstance(self.__original_downtime_windows, tuple):
            res = {}
            for k in self.__all_targets:
                res[k] = copy.deepcopy(self.__original_downtime_windows)
            self.__downtime_windows = res
        else:
            self.__downtime_windows = self.__original_downtime_windows.copy()

    def get_button_press_timing(self):
        # NOTE: deprecate, but alias to appropriately.
        # users use this function!
        res = copy.deepcopy(self.__q_button_press_timing)
        res.sort(key=lambda x: x[0])
        return res

    def set_fight_start_time(self, fight_start_time):
        if fight_start_time is None:
            self.__fight_start_time = None
        else:
            # convert to ms
            self.__fight_start_time = 1000 * fight_start_time

    def set_stats(self, stats):
        if self.__stats is not None:
            print(f"Overwriting stats in RotationBuilder object with: {stats}")
        self.__stats = stats

    def set_downtime_windows(self, downtime_windows):
        self.__original_downtime_windows = RotationBuilder.__init_downtime_windows(
            downtime_windows
        )

    def set_use_strict_skill_naming(self, use_strict_skill_naming):
        self.__use_strict_skill_naming = use_strict_skill_naming

    def set_ignore_trailing_dots(self, ignore_trailing_dots):
        self.__ignore_trailing_dots = ignore_trailing_dots

    def set_enable_autos(self, enable_autos):
        self.__enable_autos = enable_autos

    def __process_and_check_targets(self, targets):
        if targets is None:
            targets = self.__default_target
        assert isinstance(
            targets, str
        ), "'targets' must be specified as a comma-separate string. Perhaps you made it a tuple? Got: {targets}"
        all_targets = tuple(x.strip() for x in targets.split(","))
        for target in all_targets:
            self.__all_targets.add(target)
        return all_targets

    @staticmethod
    def _print_q(q):
        q.sort(key=lambda x: x[0])
        for time, skill in q:
            print(f"{time}: {skill.name}")

    def get_default_skill_modifier(self, skill, job_class):
        job_class_provided = (job_class is not None) or (job_class != "")
        if job_class_provided and (job_class != self.__stats.job_class):
            return SkillModifier(with_condition=skill.off_class_default_condition)
        return SkillModifier()

    def add_next(
        self,
        skill_name,
        skill_modifier=None,
        job_class=None,
        num_times=1,
        targets=None,
    ):
        targets = self.__process_and_check_targets(targets)

        job_class = self.__stats.job_class if job_class is None else job_class
        try:
            skill = self._skill_library.get_skill(skill_name, job_class)
        except KeyError as e:
            if self.__use_strict_skill_naming:
                raise (e)
            else:
                print(
                    f"Skill naming warning: {e}. Skill cannot be added. Typo in skill name?"
                )
                return

        if skill_modifier is None:
            skill_modifier = self.get_default_skill_modifier(skill, job_class)

        if job_class != self.__stats.job_class:
            for _ in range(num_times):
                self._q_others.append((None, skill, skill_modifier, job_class, targets))
        else:
            for _ in range(num_times):
                self._q_self.append((None, skill, skill_modifier, job_class, targets))

    def add(
        self,
        t,
        skill_name,
        skill_modifier=None,
        job_class=None,
        targets=None,
        time_is_in_ms=False,
    ):
        targets = self.__process_and_check_targets(targets)

        job_class = self.__stats.job_class if job_class is None else job_class
        try:
            skill = self._skill_library.get_skill(skill_name, job_class)
        except KeyError as e:
            if self.__use_strict_skill_naming:
                raise (e)
            else:
                print(
                    f"Skill naming warning: {e}. Skill cannot be added. Typo in skill name?"
                )
                return

        if skill_modifier is None:
            skill_modifier = self.get_default_skill_modifier(skill, job_class)
        t_use = t if time_is_in_ms else int(1000 * t)  # else time is assumed to be in s

        if job_class != self.__stats.job_class:
            self._q_others.append((t_use, skill, skill_modifier, job_class, targets))
        else:
            self._q_self.append((t_use, skill, skill_modifier, job_class, targets))

    def add_external(self, t, skill, skill_modifier=None, targets=None):
        targets = self.__process_and_check_targets(targets)
        job_class = ""
        if skill_modifier is None:
            skill_modifier = self.get_default_skill_modifier(skill, job_class)
        self._q_others.append((t, skill, skill_modifier, job_class, targets))

    @staticmethod
    def __follow_up_is_dot(follow_up_skill):
        return follow_up_skill.dot_duration is not None

    def __get_cast_time(self, timing_spec, skill_modifier, curr_buffs):
        if skill_modifier.ignore_cast_times:
            return 0

        trait_haste_time_mult = (
            1 - self.__stats.processed_stats.trait_haste_time_reduction
        )
        cast_time = (
            StatFns.get_time_using_speed_stat(
                timing_spec.base_cast_time,
                self.__stats.speed_stat,
                self.__stats.version,
                self.__stats.level,
            )
            if timing_spec.affected_by_speed_stat
            else timing_spec.base_cast_time
        )
        cast_time = (
            Utils.truncate_to_digit(
                cast_time * curr_buffs.haste_time_mult * trait_haste_time_mult,
                2,
            )
            if timing_spec.affected_by_haste_buffs
            else cast_time
        )
        cast_time -= curr_buffs.flat_cast_time_reduction
        cast_time = max(0, cast_time)
        return cast_time

    def __process_dot_follow_up_skill(
        self,
        follow_up_dot_skill,
        priority_modifier,
        parent_snapshot_time,
        parent_application_time,
        targets,
    ):
        for target in targets:
            if target not in self._q_dot_skills:
                self._q_dot_skills[target] = {}
            if follow_up_dot_skill not in self._q_dot_skills[target]:
                self._q_dot_skills[target][follow_up_dot_skill] = []

            self._q_dot_skills[target][follow_up_dot_skill].append(
                (
                    parent_snapshot_time,
                    parent_application_time,
                    priority_modifier,
                )
            )

    def __process_non_dot_follow_up_skill(
        self,
        follow_up_skill,
        priority_modifier,
        parent_snapshot_time,
        parent_application_time,
        se_tracker,
        job_resource_tracker,
        targets,
    ):
        skill = follow_up_skill.skill
        application_time = (
            parent_application_time + follow_up_skill.delay_after_parent_application
        )

        if (
            follow_up_skill.snapshot_buffs_with_parent
            or follow_up_skill.snapshot_debuffs_with_parent
        ):
            snapshot_time = parent_snapshot_time
            snapshot_status = [
                follow_up_skill.snapshot_buffs_with_parent,
                follow_up_skill.snapshot_debuffs_with_parent,
            ]
        else:
            snapshot_time = application_time
            snapshot_status = [True, True]
        priority = Utils.transform_time_to_prio(snapshot_time)

        if follow_up_skill.primary_target_only:
            targets = (targets[0],)

        self._q_snapshot_and_applications.add(
            priority + priority_modifier,
            snapshot_time,
            application_time,
            skill,
            SkillModifier(),
            snapshot_status,
            targets=targets,
        )
        se_tracker.add_to_status_effects(
            application_time, skill, SkillModifier(), targets
        )
        job_resource_tracker.add_resource(application_time, skill, SkillModifier())

    def _process_follow_up_skills(
        self,
        follow_up_skills,
        parent_snapshot_time,
        parent_application_time,
        se_tracker,
        job_resource_tracker,
        targets,
    ):
        for i, follow_up_skill in enumerate(follow_up_skills):
            # priority modifier is used to ensure follow up skills is such that it happens after its parent, and in order of follow up skills specified
            priority_modifier = i + 1
            if RotationBuilder.__follow_up_is_dot(follow_up_skill):
                self.__process_dot_follow_up_skill(
                    follow_up_skill,
                    priority_modifier,
                    parent_snapshot_time,
                    parent_application_time,
                    targets,
                )
            else:
                self.__process_non_dot_follow_up_skill(
                    follow_up_skill,
                    priority_modifier,
                    parent_snapshot_time,
                    parent_application_time,
                    se_tracker,
                    job_resource_tracker,
                    targets,
                )

    def __get_base_dot_timings(self, target, follow_up_dot_skill):
        app_times = []
        dot_times = self._q_dot_skills[target][follow_up_dot_skill]
        for (
            parent_snapshot_time,
            parent_application_time,
            priority_modifier,
        ) in dot_times:
            dot_max_end_time = (
                parent_application_time + follow_up_dot_skill.dot_duration
            )
            # dots may start ticking once the parent skill has been applied
            app_times.append(
                (
                    parent_application_time,
                    dot_max_end_time,
                    parent_snapshot_time,
                    priority_modifier,
                )
            )
        return sorted(app_times, key=lambda x: x[0])

    def __get_consolidated_dot_timing(self, base_dot_times):
        consolidated_dots = []
        for i, base_dot_time in enumerate(base_dot_times):
            curr_start_time, curr_end_time, parent_snapshot_time, priority_modifier = (
                base_dot_time
            )
            if i == len(base_dot_times) - 1:
                possible_end_time = math.inf
            else:
                # We make the current dot end here and don't merge in, because the new
                # dot may snapshot a different set of buffs/debuffs.
                possible_end_time = base_dot_times[i + 1][0]
            end_time = min(curr_end_time, possible_end_time)
            consolidated_dots.append(
                (curr_start_time, end_time, parent_snapshot_time, priority_modifier)
            )
        return consolidated_dots

    def __process_all_dots(self, last_event_time):
        # target_num
        for target, all_follow_up_dot_skills in self._q_dot_skills.items():
            for follow_up_dot_skill in all_follow_up_dot_skills:
                base_dot_times = self.__get_base_dot_timings(
                    target, follow_up_dot_skill
                )
                consolidated_dot_times = self.__get_consolidated_dot_timing(
                    base_dot_times
                )
                dot_skill = follow_up_dot_skill.skill

                # We use the priority modifier to ensure dot skills 1) are processed after their parent, and
                # 2) a dot tick will be processed after the early dot ticks, even if they snapshot at different times.
                dot_num = 0
                for (
                    _dot_start_time,
                    dot_end_time,
                    parent_snapshot_time,
                    priority_modifier,
                ) in consolidated_dot_times:
                    if self.__snap_dots_to_server_tick_starting_at is None:
                        dot_start_time = _dot_start_time
                    else:
                        shave_off = (
                            _dot_start_time
                            - 1000 * self.__snap_dots_to_server_tick_starting_at
                        ) % GameConsts.DOT_TICK_INTERVAL
                        if (
                            shave_off <= 1e-6
                        ):  # allow some tolerance for floating point precision
                            dot_start_time = _dot_start_time
                        else:
                            dot_start_time = int(
                                _dot_start_time
                                - shave_off
                                + GameConsts.DOT_TICK_INTERVAL
                            )
                    for application_time in range(
                        dot_start_time, dot_end_time, GameConsts.DOT_TICK_INTERVAL
                    ):
                        if (last_event_time) and (application_time > last_event_time):
                            continue
                        priority = Utils.transform_time_to_prio(
                            parent_snapshot_time
                        ) + (priority_modifier + dot_num)
                        snapshot_status = [
                            follow_up_dot_skill.snapshot_buffs_with_parent,
                            follow_up_dot_skill.snapshot_debuffs_with_parent,
                        ]
                        self._q_snapshot_and_applications.add(
                            priority,
                            parent_snapshot_time,
                            application_time,
                            dot_skill,
                            SkillModifier(),
                            snapshot_status,
                            targets=(target,),
                        )
                        dot_num += 1

    def __process_skill(
        self,
        t,
        skill,
        skill_modifier,
        se_tracker,
        job_resource_tracker,
        curr_buffs,
        targets,
    ):
        timing_spec = skill.get_timing_spec(skill_modifier)

        cast_time = self.__get_cast_time(timing_spec, skill_modifier, curr_buffs)
        snapshot_time = t + max(
            0, cast_time - GameConsts.DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES
        )

        application_time = t + cast_time

        if not skill_modifier.ignore_application_delay:
            if cast_time > 1e-6:
                application_delay = max(
                    0,
                    -GameConsts.DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES
                    + skill.get_timing_spec(skill_modifier).application_delay,
                )
            else:
                application_delay = skill.get_timing_spec(
                    skill_modifier
                ).application_delay
            application_time += application_delay

        priority = Utils.transform_time_to_prio(snapshot_time)
        self._q_snapshot_and_applications.add(
            priority,
            snapshot_time,
            application_time,
            skill,
            skill_modifier,
            [True, True],
            targets=targets,
        )

        se_tracker.add_to_status_effects(
            application_time, skill, skill_modifier, targets
        )
        job_resource_tracker.add_resource(snapshot_time, skill, skill_modifier)

        follow_up_skills = skill.get_follow_up_skills(skill_modifier)
        if follow_up_skills:
            self._process_follow_up_skills(
                follow_up_skills,
                snapshot_time,
                application_time,
                se_tracker,
                job_resource_tracker,
                targets,
            )

    def __process_q_others(self):
        # assume to be all timed
        q_others = copy.deepcopy(self._q_others)
        q_others.sort(key=lambda x: x[0])
        self.__process_q(q_others)

    def __process_q(self, q):
        se_tracker = StatusEffectTracker(self.__status_effect_priority)
        c_tracker = ChannelingTracker()
        job_resource_tracker = JobResourceTracker(
            self._skill_library.get_all_resource_settings(self.__stats.job_class)
        )
        combo_tracker = ComboTracker(
            self._skill_library.get_all_combo_breakers(self.__stats.job_class)
        )

        cast_periods = []
        next_gcd_time = -math.inf
        curr_t = (
            0 if self.__fight_start_time is None else self.__fight_start_time
        )  # this represents the next time we could possibly use any skill button

        for maybe_curr_t, skill, skill_modifier, job_class, targets in q:
            if maybe_curr_t is not None:
                curr_t = maybe_curr_t
            else:
                if skill.is_GCD:
                    curr_t = max(curr_t, next_gcd_time)

            self.__q_button_press_timing.append(
                [
                    curr_t,
                    skill.name,
                    job_class if job_class != self.__stats.job_class else "",
                    ",".join(skill_modifier.with_condition),
                ]
            )

            se_tracker.expire_status_effects(curr_t)
            if (
                job_class == self.__stats.job_class
            ):  # assume it is this player if job class matches
                c_tracker.process_channeling(curr_t, skill, skill_modifier)
            curr_buffs_and_skill_modifier = se_tracker.compile_buffs(curr_t, skill)
            curr_debuffs_and_skill_modifier = se_tracker.compile_debuffs(curr_t, skill)

            curr_buffs, skill_modifier_from_buffs = (
                curr_buffs_and_skill_modifier[0],
                curr_buffs_and_skill_modifier[1],
            )
            curr_debuffs, skill_modifier_from_debuffs = (
                curr_debuffs_and_skill_modifier[0],
                curr_debuffs_and_skill_modifier[1],
            )
            job_resource_conditional = job_resource_tracker.compile_job_resources(
                curr_t, skill
            )

            skill_modifier = copy.deepcopy(skill_modifier)
            skill_modifier.add_to_condition(skill_modifier_from_buffs)
            skill_modifier.add_to_condition(skill_modifier_from_debuffs)
            skill_modifier.add_to_condition(job_resource_conditional)

            combo_conditional = combo_tracker.compile_and_update_combo(
                curr_t, skill, skill_modifier
            )
            skill_modifier.add_to_condition(combo_conditional)

            cast_time = self.__get_cast_time(
                skill.get_timing_spec(skill_modifier), skill_modifier, curr_buffs
            )
            if cast_time > 0:
                cast_periods.append((curr_t, curr_t + cast_time))

            try:
                skill_modifier.add_to_condition(
                    Utils.get_positional_condition(skill, skill_modifier)
                )
            except ValueError as v:
                print(str(v))

            self.__timestamps_and_main_target.append((curr_t, targets[0]))
            self.__process_skill(
                curr_t,
                skill,
                skill_modifier,
                se_tracker,
                job_resource_tracker,
                curr_buffs,
                targets,
            )

            # compute next timing spec
            next_gcd_time_delta, curr_t_delta = self.__compute_next_skill_time_deltas(
                skill, skill_modifier, curr_buffs, curr_debuffs
            )
            next_gcd_time = (
                curr_t + next_gcd_time_delta if skill.is_GCD else next_gcd_time
            )
            curr_t += curr_t_delta

        c_tracker.finalize()
        self.__non_auto_periods = list(c_tracker.get_channeling_windows())
        self.__non_auto_periods.extend(cast_periods)
        self.__non_auto_periods.sort()

    def __compute_next_skill_time_deltas(
        self, skill, skill_modifier, curr_buffs, curr_debuffs
    ):
        timing_spec = skill.get_timing_spec(skill_modifier)
        if timing_spec is None:
            print(f"Timing spec is none for: {skill.name}")
            return (0, 0)
        if skill.is_GCD:
            trait_haste_time_mult = (
                1 - self.__stats.processed_stats.trait_haste_time_reduction
            )
            recast_time = (
                StatFns.get_time_using_speed_stat(
                    timing_spec.gcd_base_recast_time,
                    self.__stats.speed_stat,
                    self.__stats.version,
                    self.__stats.level,
                )
                if timing_spec.affected_by_speed_stat
                else timing_spec.gcd_base_recast_time
            )
            recast_time = (
                Utils.truncate_to_digit(
                    recast_time
                    * curr_buffs.haste_time_mult
                    * curr_debuffs.haste_time_mult
                    * trait_haste_time_mult,
                    2,
                )
                if timing_spec.affected_by_haste_buffs
                else recast_time
            )
            recast_time -= curr_buffs.flat_gcd_recast_time_reduction
            # default (2500 ms, at the time of writing) gcd recasts are hard
            # stopped by a particular recast time.
            if timing_spec.gcd_base_recast_time == GameConsts.GCD_RECAST_TIME:
                recast_time = max(recast_time, GameConsts.MIN_GCD_RECAST_TIME)

            next_gcd_time_delta = recast_time
            cast_time = self.__get_cast_time(timing_spec, skill_modifier, curr_buffs)
            curr_t_delta = cast_time + timing_spec.animation_lock
        else:
            next_gcd_time_delta = 0
            curr_t_delta = timing_spec.animation_lock

        return next_gcd_time_delta, curr_t_delta

    @staticmethod
    def __divide_into_chunks(q):
        curr = []
        idx = 0

        all_chunks = {}
        for i, val in enumerate(q):
            if val[0] is None:
                curr.append(val)
            else:
                if len(curr) > 0:
                    all_chunks[idx] = curr
                idx = i
                curr = [val]
        if len(curr) > 0:
            all_chunks[idx] = curr
        return all_chunks

    def __process_q_self(self):
        has_timestamps = False
        has_nexts = False

        for _, val in enumerate(self._q_self):
            if val[0] is None:
                has_nexts = True
            else:
                has_timestamps = True

        if has_timestamps and not has_nexts:
            q_self = copy.deepcopy(self._q_self)
            q_self.sort(key=lambda x: x[0])
            self.__process_q(q_self)
        elif not has_timestamps and has_nexts:
            q_self = copy.deepcopy(self._q_self)
            self.__process_q(q_self)
        else:  # a mix
            chunks = self.__divide_into_chunks(self._q_self)

            times = []
            for i, tmp in enumerate(self._q_self):
                if tmp[0] is not None:
                    times.append((tmp[0], i))
            perm_inds = list(np.argsort([tmp[0] for tmp in times]))

            res = []
            if 0 not in [x[1] for x in times]:
                res.extend(chunks[0])

            for _, val in enumerate(perm_inds):
                res.extend(chunks[times[val][1]])
            self.__process_q(res)

    def __shift_downtime_windows(self, first_damage_time):
        for k, v in self.__downtime_windows.items():
            res = []
            for window in v:
                tmp = (
                    window[0] - first_damage_time,
                    window[1] - first_damage_time,
                    window[2],
                )
                res.append(tmp)
            self.__downtime_windows[k] = tuple(res)

    def shift_timelines_for_first_damage_instance(self):
        res = SnapshotAndApplicationEvents()

        if self.__fight_start_time is None:
            shift_time = self._q_snapshot_and_applications.get_first_damage_time()
            if shift_time is None:
                return self._q_snapshot_and_applications
        else:
            shift_time = self.__fight_start_time

        if shift_time is None:
            return self._q_snapshot_and_applications
        self.__shift_downtime_windows(shift_time)

        for _, val in enumerate(self.__q_button_press_timing):
            val[0] -= shift_time

        while not self._q_snapshot_and_applications.is_empty():
            [
                priority,
                event_times,
                skill,
                skill_modifier,
                snapshot_status,
                targets,
                _,
                _,
                _,
                _,
            ] = self._q_snapshot_and_applications.get_next()
            primary_time = event_times.primary
            secondary_time = event_times.secondary
            if primary_time is not None:
                primary_time -= shift_time
                priority -= Utils.transform_time_to_prio(shift_time)
            if secondary_time is not None:
                secondary_time -= shift_time
            res.add(
                priority,
                primary_time,
                secondary_time,
                skill,
                skill_modifier,
                snapshot_status,
                targets=targets,
            )
        return res

    def remove_damage_during_downtime(self):
        res = SnapshotAndApplicationEvents()
        while not self._q_snapshot_and_applications.is_empty():
            [
                priority,
                event_times,
                skill,
                skill_modifier,
                snapshot_status,
                targets,
                _,
                _,
                _,
                _,
            ] = self._q_snapshot_and_applications.get_next()
            primary_time, secondary_time = event_times.primary, event_times.secondary

            snapshot_time = primary_time

            all_valid_targets = []
            for target in targets:
                skill_damage_spec = skill.get_damage_spec(skill_modifier)
                if skill_damage_spec is not None and (
                    # only need to filter snapshot time- application time will be later
                    TimelineUtils.filter_by_downtime_range_and_damage_class(
                        self.__downtime_windows,
                        snapshot_time,
                        target,
                        skill_damage_spec.damage_class,
                    )
                ):
                    continue
                else:
                    all_valid_targets.append(target)
                continue
            if len(all_valid_targets) > 0:
                res.add(
                    priority,
                    primary_time,
                    secondary_time,
                    skill,
                    skill_modifier,
                    snapshot_status,
                    targets=tuple(all_valid_targets),
                )
        return res

    # Result: a heap encapsualted by SnapshotAndApplicationEvents. See
    # SnapshotAndApplicationEvents's documentation for what the data format is.
    def get_skill_timing(self):
        self.__status_effect_priority = self._skill_library.get_status_effect_priority(
            self.__stats.job_class
        )
        # Each downtime range is the semi-open interval [start_time, end_time). In other
        # words, boss cannot be hit at start_time, but can be hit immediately at end_time.
        # Windows are assumed to be non-overlapping. This must be called before doing
        # anything at all with downtime windows.
        self.__process_downtime_windows()

        self._q_snapshot_and_applications = SnapshotAndApplicationEvents()
        self.__q_button_press_timing.clear()
        self.__process_q_others()
        self.__process_q_self()

        last_event_time = (
            self._q_snapshot_and_applications.get_last_event_time()
            if (self.__ignore_trailing_dots)
            else None
        )
        self.__process_all_dots(last_event_time)
        if self.__enable_autos:
            self.__add_autos(last_event_time)
        self._q_snapshot_and_applications = (
            self.shift_timelines_for_first_damage_instance()
        )
        self._q_snapshot_and_applications = self.remove_damage_during_downtime()

        self.__q_button_press_timing.sort(key=lambda x: x[0])
        return SkillTimingInfo(
            self._q_snapshot_and_applications, copy.deepcopy(self.__downtime_windows)
        )

    def __assemble_speed_status_effects_timeline(self):
        # Note, this will skip num_uses since that never applies to autos
        res = []
        for event in self._q_snapshot_and_applications.get_q():
            skill = event.skill
            skill_modifier = event.skill_modifier
            offensive_buff_spec = skill.get_offensive_buff_spec(skill_modifier)
            offensive_debuff_spec = skill.get_offensive_debuff_spec(skill_modifier)

            offensive_buff_spec_has_speed = offensive_buff_spec is not None and (
                offensive_buff_spec.auto_attack_delay_reduction > 0
                or offensive_buff_spec.haste_time_reduction > 0
                or offensive_buff_spec.flat_cast_time_reduction > 0
            )
            offensive_debuff_spec_has_speed = offensive_debuff_spec is not None and (
                offensive_debuff_spec.auto_attack_delay_reduction > 0
                or offensive_debuff_spec.haste_time_reduction > 0
                or offensive_debuff_spec.flat_cast_time_reduction > 0
            )
            if (
                not offensive_buff_spec_has_speed
                and not offensive_debuff_spec_has_speed
            ):
                continue
            event_times = event.event_times
            application_time = (
                event_times.secondary
                if event_times.secondary is not None
                else event_times.primary
            )
            res.append((application_time, skill))
        res.sort(key=lambda x: x[0])
        return res

    def __get_applicable_status_effects(
        self, speed_status_effects_timeline, curr_t, skill, skill_modifier, targets
    ):
        applicable_status_effect_events = list(
            filter(lambda x: x[0] <= curr_t, speed_status_effects_timeline)
        )
        se_tracker = StatusEffectTracker(self.__status_effect_priority)
        job_resource_tracker = JobResourceTracker(
            self._skill_library.get_all_resource_settings(self.__stats.job_class)
        )

        for t, skill in applicable_status_effect_events:
            se_tracker.expire_status_effects(t)
            se_tracker.add_to_status_effects(t, skill, skill_modifier, targets)
            job_resource_tracker.add_resource(t, skill, skill_modifier)

        se_tracker.expire_status_effects(curr_t)
        curr_buffs_and_skill_modifier = se_tracker.compile_buffs(curr_t, skill)
        curr_debuffs_and_skill_modifier = se_tracker.compile_debuffs(curr_t, skill)
        return (
            curr_buffs_and_skill_modifier,
            curr_debuffs_and_skill_modifier,
        ), job_resource_tracker.compile_job_resources(curr_t, skill)

    # This is only called during a downtime window.
    def forward_to_next_non_downtime_time(self, snapshot_time, auto_target):
        for r in self.__downtime_windows.get(auto_target, tuple()):
            if r[0] <= snapshot_time < r[1] and (
                r[2] is None or r[2] == DamageClass.AUTO
            ):
                return r[1]
        return snapshot_time

    def __get_next_auto_time(self, t, no_auto_periods, auto_target):
        t = self.forward_to_next_non_downtime_time(t, auto_target)
        intersecting_no_auto_periods = list(
            filter(lambda x: (x[0] <= t) and (x[1] >= t), no_auto_periods)
        )
        return (
            t
            if len(intersecting_no_auto_periods) == 0
            else max(x[1] for x in intersecting_no_auto_periods)
        )

    # Autos, if enabled, always start at first event application time.
    def __add_autos(self, last_event_time=None):
        def shorten_sequence(seq):
            res = [seq[0]]
            curr_target = seq[0][1]
            for i in range(1, len(seq)):
                if seq[i][1] == curr_target:
                    continue
                curr_target = seq[i][1]
                res.append(seq[i])
            return res

        timestamps_and_main_target = copy.deepcopy(self.__timestamps_and_main_target)
        timestamps_and_main_target.sort(key=lambda x: x[0])
        timestamps_and_main_target = shorten_sequence(timestamps_and_main_target)

        weapon_delay = int(1000 * self.__stats.weapon_delay)  # convert to ms

        if self._skill_library.has_skill("Shot", self.__stats.job_class):
            auto_skill = self._skill_library.get_skill("Shot", self.__stats.job_class)
        else:
            auto_skill = self._skill_library.get_skill("Auto", self.__stats.job_class)

        trait_auto_delay_mult = (
            1 - self.__stats.processed_stats.trait_auto_attack_delay_reduction
        )
        if last_event_time is None:
            last_event_time = self._q_snapshot_and_applications.get_last_event_time()

        snapshot_time = (
            self._q_snapshot_and_applications.get_first_damage_time()
        )  # autos do not have cast times, so snapshot time should be immediate
        application_time = snapshot_time + auto_skill.timing_spec.application_delay

        auto_target_ind = 0

        speed_status_effects_timeline = self.__assemble_speed_status_effects_timeline()
        no_auto_periods = self.__non_auto_periods

        while application_time < last_event_time:
            while (
                auto_target_ind < len(timestamps_and_main_target)
                and timestamps_and_main_target[auto_target_ind][0] <= snapshot_time
            ):
                auto_target_ind += 1
            auto_target_ind = max(0, auto_target_ind - 1)
            auto_target = timestamps_and_main_target[auto_target_ind][1]

            self._q_snapshot_and_applications.add(
                Utils.transform_time_to_prio(snapshot_time),
                snapshot_time,
                application_time,
                auto_skill,
                SkillModifier(),
                [True, True],
                targets=(auto_target,),
            )

            (
                curr_buffs_and_skill_modifier,
                curr_debuffs_and_skill_modifier,
            ), _ = self.__get_applicable_status_effects(
                speed_status_effects_timeline,
                snapshot_time,
                auto_skill,
                SkillModifier(),
                targets=(auto_target,),
            )

            # Don't need the skill modifiers, since they're just autos
            curr_buffs = curr_buffs_and_skill_modifier[0]
            curr_debuffs = curr_debuffs_and_skill_modifier[0]

            snapshot_time += Utils.truncate_to_digit(
                weapon_delay
                * trait_auto_delay_mult
                * curr_buffs.auto_attack_delay_mult
                * curr_debuffs.auto_attack_delay_mult,
                2,
            )
            snapshot_time = self.__get_next_auto_time(
                snapshot_time, no_auto_periods, auto_target
            )
            application_time = snapshot_time + auto_skill.timing_spec.application_delay

    def get_stats(self):
        return self.__stats

    def print_button_press_timings_as_csv(self):
        if len(self.__q_button_press_timing) == 0:
            print(
                'You must call "get_skill_timing() before calling this function, in order to compute when buttons are pressed.'
            )
            return
        print("Time, skill_name, job_class, skill_conditional")
        for tmp in self.__q_button_press_timing:
            print(f"{tmp[0] / 1000}, {tmp[1]}, {tmp[2]}, {tmp[3]}")

    def get_timed_skills(self):
        res = copy.deepcopy(self._q_others)
        res.extend(copy.deepcopy(self._q_self))
        res.sort(key=lambda x: x[0])  # sort by time

        return res

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            if k == "_skill_library":
                # for efficiency, do not copy the underlying skill library
                setattr(result, k, v)
            else:
                setattr(result, k, copy.deepcopy(v, memo))

        return result
