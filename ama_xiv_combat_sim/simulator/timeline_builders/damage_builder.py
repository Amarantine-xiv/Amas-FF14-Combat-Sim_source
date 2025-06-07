import copy
import heapq

from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)
from ama_xiv_combat_sim.simulator.utils import Utils
from ama_xiv_combat_sim.simulator.trackers.combo_tracker import ComboTracker
from ama_xiv_combat_sim.simulator.trackers.job_resource_tracker import (
    JobResourceTracker,
)
from ama_xiv_combat_sim.simulator.trackers.status_effect_tracker import (
    StatusEffectTracker,
)
from ama_xiv_combat_sim.simulator.trackers.status_effects import StatusEffects


class DamageBuilder:

    def __init__(self, stats, skill_library):
        self.__skill_library = skill_library
        self.__stats = stats
        self.__status_effect_priority = skill_library.get_status_effect_priority(
            stats.job_class
        )
        self.se = StatusEffectTracker(self.__status_effect_priority)
        self.job_resource_tracker = JobResourceTracker(
            self.__skill_library.get_all_resource_settings(stats.job_class)
        )
        self.combo_tracker = ComboTracker(
            self.__skill_library.get_all_combo_breakers(self.__stats.job_class)
        )

    @staticmethod
    def __is_application_time(event_times):
        return event_times.secondary is None

    # output is a list, sorted by timestamp of damage instance (not necessarily in stable-sort order, according to the rotation).
    # Format of the elements of the output: (time, skill, (buffs, debuffs))
    def get_damage_instances(
        self, q_snapshot_and_applications: SnapshotAndApplicationEvents
    ):
        q = []  # (current_time, skill, skill_modifier, (buffs, debuffs), job_resources)
        while not q_snapshot_and_applications.is_empty():
            [
                priority,
                event_times,
                skill,
                skill_modifier,
                snapshot_status,
                targets,
                event_id,
                job_resources_added,
                job_conditional_processed,
                combo_contional_processed,
            ] = q_snapshot_and_applications.get_next()

            curr_time = event_times.primary
            self.se.expire_status_effects(curr_time)

            is_application_time = self.__is_application_time(event_times)
            skill_modifier = copy.deepcopy(skill_modifier)
            if is_application_time:
                if not job_conditional_processed:
                    job_resource_conditional = (
                        self.job_resource_tracker.compile_job_resources(
                            curr_time, skill
                        )
                    )
                    skill_modifier.add_to_condition(job_resource_conditional)

                if not job_resources_added:
                    self.job_resource_tracker.add_resource(
                        curr_time, skill, skill_modifier
                    )

                if not combo_contional_processed:
                    combo_conditional = self.combo_tracker.compile_and_update_combo(
                        curr_time, skill, skill_modifier
                    )
                    skill_modifier.add_to_condition(combo_conditional)
                    try:
                        skill_modifier.add_to_condition(
                            Utils.get_positional_condition(skill, skill_modifier)
                        )
                    except ValueError as v:
                        print(str(v))

                if not isinstance(snapshot_status[0], StatusEffects):
                    snapshot_status[0], skill_modifier_from_buffs = (
                        self.se.compile_buffs(curr_time, skill)
                    )
                    skill_modifier.add_to_condition(skill_modifier_from_buffs)

                for i, target in enumerate(targets):
                    if len(targets) > 1:
                        skill_modifier_to_use = copy.deepcopy(skill_modifier)
                        skill_modifier_to_use.add_to_condition(f"Target {i+1}")
                        snapshot_status_use = copy.deepcopy(snapshot_status)
                        # add targetting
                        application_time = (
                            curr_time + i * GameConsts.MULTI_TARGET_DELAY_PER_TARGET
                        )  # modify app time?
                    else:
                        skill_modifier_to_use = skill_modifier
                        snapshot_status_use = snapshot_status
                        # add targetting
                        application_time = curr_time  # modify app time?

                    if not isinstance(snapshot_status_use[1], StatusEffects):
                        snapshot_status_use[1], skill_modifier_from_debuffs = (
                            self.se.compile_debuffs(curr_time, skill, target)
                        )
                        skill_modifier_to_use.add_to_condition(
                            skill_modifier_from_debuffs
                        )

                    if skill.get_damage_spec(skill_modifier_to_use) is not None:
                        heapq.heappush(
                            q,
                            (
                                application_time,
                                skill,
                                skill_modifier_to_use,
                                tuple(snapshot_status_use),
                                event_id,
                                target
                            ),
                        )
            else:
                if snapshot_status[0] is True:
                    snapshot_status[0], skill_modifier_from_buffs = (
                        self.se.compile_buffs(curr_time, skill)
                    )
                    skill_modifier.add_to_condition(skill_modifier_from_buffs)

                priority_modifier = (
                    Utils.transform_time_to_prio(event_times.primary) - priority
                )
                new_priority = (
                    Utils.transform_time_to_prio(event_times.secondary)
                    + priority_modifier
                )
                
                # make sure we process new applications before other events applied on same timestamp.
                # -10 is a hack to deal with followup skills to make sure this applies before
                # instant-skill follow ups. Superhack. Can probably get rid of with
                # bisect_right on a sorted list (which the original q is, basically)
                new_priority -= 10

                job_conditional_was_processed = False
                if not job_conditional_processed and skill.job_resources_snapshot:
                    job_resource_conditional = (
                        self.job_resource_tracker.compile_job_resources(
                            curr_time, skill
                        )
                    )
                    skill_modifier.add_to_condition(job_resource_conditional)
                    job_conditional_was_processed = True

                combo_conditional_was_processed = False
                if not combo_contional_processed:
                    combo_conditional = self.combo_tracker.compile_and_update_combo(
                        curr_time, skill, skill_modifier
                    )
                    skill_modifier.add_to_condition(combo_conditional)
                    try:
                        skill_modifier.add_to_condition(
                            Utils.get_positional_condition(skill, skill_modifier)
                        )
                    except ValueError as v:
                        print(str(v))
                    combo_conditional_was_processed = True

                if not job_resources_added:
                    self.job_resource_tracker.add_resource(
                        curr_time, skill, skill_modifier
                    )

                for i, target in enumerate(targets):
                    if len(targets) > 1:
                        skill_modifier_to_use = copy.deepcopy(skill_modifier)
                        skill_modifier_to_use.add_to_condition(f"Target {i+1}")
                        snapshot_status_use = copy.deepcopy(snapshot_status)
                        # add targetting
                        application_time = (
                            event_times.secondary
                            + i * GameConsts.MULTI_TARGET_DELAY_PER_TARGET
                        )  # modify app time?
                    else:
                        skill_modifier_to_use = skill_modifier
                        snapshot_status_use = snapshot_status
                        # add targetting
                        application_time = event_times.secondary  # modify app time?

                    if snapshot_status_use[1] is True:
                        snapshot_status_use[1], skill_modifier_from_debuffs = (
                            self.se.compile_debuffs(curr_time, skill, target)
                        )
                        skill_modifier_to_use.add_to_condition(
                            skill_modifier_from_debuffs
                        )
                    q_snapshot_and_applications.add(
                        new_priority,
                        application_time,
                        None,
                        skill,
                        skill_modifier_to_use,
                        copy.deepcopy(snapshot_status_use),
                        event_id,
                        True,
                        job_conditional_was_processed,
                        combo_conditional_was_processed,
                        targets=(target,),
                    )

            # by default, we apply buffs as the last step of any skill application
            if is_application_time:
                self.se.add_to_status_effects(curr_time, skill, skill_modifier, targets)

        q.sort(key=lambda x: x[0])
        return q
