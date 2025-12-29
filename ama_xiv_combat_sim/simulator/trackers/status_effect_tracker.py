from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.trackers.offensive_status_effects import OffensiveStatusEffects
from ama_xiv_combat_sim.simulator.trackers.offensive_status_effect_info import OffensiveStatusEffectInfo

class StatusEffectTracker:
    def __init__(self, status_effects_priority=tuple()):
        self.offensive_buffs = {}
        self.offensive_debuffs = {}  # double map to the given target
        self.__status_effects_priority = status_effects_priority

    def __get_debuffs(self, target):
        if target not in self.offensive_debuffs:
            self.offensive_debuffs[target] = {}
        return self.offensive_debuffs[target]

    @staticmethod
    def __expire_status_effects(t, status_effects):
        se_skill_names = list(status_effects.keys())
        for se_skill_name in se_skill_names:
            (_, end_time, num_uses, _) = status_effects[se_skill_name]
            if (t >= end_time) or num_uses == 0:
                del status_effects[se_skill_name]

    def expire_status_effects(self, t):
        self.__expire_status_effects(t, self.offensive_buffs)
        for target in self.offensive_debuffs:
            self.__expire_status_effects(t, self.__get_debuffs(target))

    @staticmethod
    def __add_to_status_effects(
        status_effects, start_time, skill_name, status_effect_spec
    ):
        if skill_name not in status_effects:
            # check if the status effect needs to exist before it's extended
            if status_effect_spec.extend_only:
                return

            prev_start_time = start_time
            end_time = start_time + status_effect_spec.duration
            status_effects[skill_name] = (
                start_time,
                end_time,
                status_effect_spec.num_uses,
                status_effect_spec,
            )
        else:
            prev_start_time, prev_end_time, prev_num_uses, prev_status_effect_spec = (
                status_effects[skill_name]
            )
            time_left = max(prev_end_time - start_time, 0)
            if status_effect_spec.extends_existing_duration:
                new_duration = min(
                    status_effect_spec.max_duration,
                    time_left + status_effect_spec.duration,
                )
            else:
                new_duration = time_left
            new_num_uses = min(
                prev_num_uses + status_effect_spec.num_uses,
                status_effect_spec.max_num_uses,
            )
            # Note that this overrides the existing status_effect_spec. This is on purpose,
            # as that seems generally how the game works.
            status_effects[skill_name] = (
                prev_start_time,
                start_time + new_duration,
                new_num_uses,
                status_effect_spec,
            )

            if status_effect_spec != prev_status_effect_spec:
                prev_status_effect_spec_has_speed = (
                    prev_status_effect_spec.auto_attack_delay_reduction > 0
                    or prev_status_effect_spec.haste_time_reduction > 0
                    or prev_status_effect_spec.flat_cast_time_reduction > 0
                )
                if prev_status_effect_spec_has_speed:
                    print(
                        "---Warning: overwrote previous status effect spec. Rotation timings may be off."
                    )

    def __expire_named_effect(
        self, expired_effect_name, t, target=SimConsts.DEFAULT_TARGET
    ):
        if expired_effect_name in self.offensive_buffs.keys():
            start_time, _, prev_num_uses, prev_status_effect_spec = self.offensive_buffs[
                expired_effect_name
            ]
            self.offensive_buffs[expired_effect_name] = (
                start_time,
                t,
                prev_num_uses,
                prev_status_effect_spec,
            )
        if expired_effect_name in self.__get_debuffs(target):
            start_time, _, prev_num_uses, prev_status_effect_spec = self.__get_debuffs(
                target
            )[expired_effect_name]
            self.__get_debuffs(target)[expired_effect_name] = (
                start_time,
                t,
                prev_num_uses,
                prev_status_effect_spec,
            )

    def add_to_status_effects(
        self, t, skill, skill_modifier, targets=(SimConsts.DEFAULT_TARGET,)
    ):
        offensive_buff_spec = skill.get_offensive_buff_spec(skill_modifier)
        offensive_debuff_spec = skill.get_offensive_debuff_spec(skill_modifier)

        if offensive_buff_spec is not None:
            if offensive_buff_spec.clear_all_status_effects:
                self.offensive_buffs = {}
            self.__add_to_status_effects(self.offensive_buffs, t, skill.name, offensive_buff_spec)
            for expired_effect_name in offensive_buff_spec.expires_status_effects:
                self.__expire_named_effect(expired_effect_name, t)

        if offensive_debuff_spec is not None:
            for target in targets:
                self.__add_to_status_effects(
                    self.__get_debuffs(target), t, skill.name, offensive_debuff_spec
                )
                for expired_effect_name in offensive_debuff_spec.expires_status_effects:
                    self.__expire_named_effect(expired_effect_name, t, target)

    @staticmethod
    def __get_valid_status_effects(
        curr_t, status_effects, status_effect_denylist, skill_name
    ):
        res = []
        for status_effect_skill_name in status_effects.keys():
            (start_time, end_time, num_uses, spec) = status_effects[
                status_effect_skill_name
            ]
            # this is needed because some times the start time of a buff is recorded,
            # but we have not reached its start time yet when processing
            # the timeline.
            if curr_t < start_time:
                continue
            if status_effect_skill_name in status_effect_denylist:
                continue
            if (
                spec.skill_allowlist is not None
                and skill_name not in spec.skill_allowlist
            ):
                continue
            res.append(status_effect_skill_name)
        return tuple(res)

    def __delete_lower_priority_status_effects(self, valid_status_effects):
        valid_status_effects = list(valid_status_effects)

        for i, _ in enumerate(range(len(self.__status_effects_priority))):
            status_effect = self.__status_effects_priority[i]
            if status_effect in valid_status_effects:
                for j in range(i + 1, len(self.__status_effects_priority)):
                    status_effect_to_delete = self.__status_effects_priority[j]
                    try:
                        idx = valid_status_effects.index(status_effect_to_delete)
                        del valid_status_effects[idx]
                    except ValueError:
                        pass
                break
        return tuple(valid_status_effects)

    def __compile_status_effects(
        self, curr_t, status_effects, status_effect_denylist, skill_name
    ):
        crit_rate_add = 0.0
        dh_rate_add = 0.0
        damage_mult = 1.0
        main_stat_add = 0.0
        main_stat_mult = 1.0
        auto_attack_delay_mult = 1.0
        haste_time_mult = 1.0
        flat_cast_time_reduction = 0
        flat_gcd_recast_time_reduction = 0

        guaranteed_crit = ForcedCritOrDH.DEFAULT
        guaranteed_dh = ForcedCritOrDH.DEFAULT
        skill_modifier_conditions = []

        valid_status_effects = self.__get_valid_status_effects(
            curr_t, status_effects, status_effect_denylist, skill_name
        )
        valid_and_prioritized_status_effects = (
            self.__delete_lower_priority_status_effects(valid_status_effects)
        )

        all_status_effects_info = []
        for status_effect_skill_name in valid_and_prioritized_status_effects:
            (start_time, end_time, num_uses, spec) = status_effects[
                status_effect_skill_name
            ]
            status_effects[status_effect_skill_name] = (
                start_time,
                end_time,
                num_uses - 1,
                spec,
            )
            crit_rate_add += spec.crit_rate_add
            dh_rate_add += spec.dh_rate_add
            damage_mult *= spec.damage_mult
            main_stat_mult *= spec.main_stat_mult
            main_stat_add += spec.main_stat_add
            auto_attack_delay_mult *= 1 - spec.auto_attack_delay_reduction
            haste_time_mult *= 1 - spec.haste_time_reduction
            flat_cast_time_reduction += spec.flat_cast_time_reduction
            flat_gcd_recast_time_reduction += spec.flat_gcd_recast_time_reduction

            all_status_effects_info.append(OffensiveStatusEffectInfo(status_effect_skill_name, spec))
            if spec.guaranteed_crit is not ForcedCritOrDH.DEFAULT:
                assert (
                    guaranteed_crit is ForcedCritOrDH.DEFAULT
                ), "Cannot force 2 different crit statuses on a skill. Be sure to only have 1 forced crit status on all buffs/debuffs."
                guaranteed_crit = spec.guaranteed_crit

            if spec.guaranteed_dh is not ForcedCritOrDH.DEFAULT:
                assert (
                    guaranteed_dh is ForcedCritOrDH.DEFAULT
                ), "Cannot force 2 different direct hit statuses on a skill. Be sure to only have 1 forced direct hit status on all buffs/debuffs."
                guaranteed_dh = spec.guaranteed_dh

            if spec.add_to_skill_modifier_condition:
                skill_modifier_conditions.append(status_effect_skill_name)

        status_effects = OffensiveStatusEffects(
            crit_rate_add=crit_rate_add,
            dh_rate_add=dh_rate_add,
            damage_mult=damage_mult,
            main_stat_add=main_stat_add,
            main_stat_mult=main_stat_mult,
            auto_attack_delay_mult=auto_attack_delay_mult,
            haste_time_mult=haste_time_mult,
            flat_cast_time_reduction=flat_cast_time_reduction,
            flat_gcd_recast_time_reduction=flat_gcd_recast_time_reduction,
            guaranteed_crit=guaranteed_crit,
            guaranteed_dh=guaranteed_dh,
            status_effects=tuple(valid_and_prioritized_status_effects),
            all_status_effects_info = tuple(all_status_effects_info)
        )
        return (status_effects, ", ".join(skill_modifier_conditions))

    def compile_buffs(self, t, skill=Skill(name="")):
        status_effect_denylist = skill.status_effect_denylist
        return self.__compile_status_effects(
            t, self.offensive_buffs, status_effect_denylist, skill.name
        )

    def compile_debuffs(self, t, skill=Skill(name=""), target=SimConsts.DEFAULT_TARGET):
        status_effect_denylist = skill.status_effect_denylist
        return self.__compile_status_effects(
            t, self.__get_debuffs(target), status_effect_denylist, skill.name
        )
