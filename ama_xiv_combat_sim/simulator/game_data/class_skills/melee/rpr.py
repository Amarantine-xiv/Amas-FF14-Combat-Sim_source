from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.rpr_data import (
    all_rpr_skills,
)


class RprSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_rpr_skills)
        self._job_class = "RPR"

    def __get_deaths_design_follow_up(self):
        name = "Death's Design"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                debuff_spec=StatusEffectSpec(
                    damage_mult=1.10, duration=30 * 1000, max_duration=60 * 1000
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=False,
        )

    def __get_enhanced_harp_follow_up(self):
        name = "Enhanced Harpe"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                    skill_allowlist=("Harpe",),
                ),
            ),
            delay_after_parent_application=0,
        )

    @GenericJobClass.is_a_skill
    def auto(self):
        name = "Auto"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.auto_timing_spec,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )

    @GenericJobClass.is_a_skill
    def slice(self):
        name = "Slice"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )

    @GenericJobClass.is_a_skill
    def waxing_slice(self):
        name = "Waxing Slice"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Slice",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )

    @GenericJobClass.is_a_skill
    def shadow_of_death(self):
        name = "Shadow of Death"
        shadow_of_death_damage = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=1160,
        )
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(
                shadow_of_death_damage,
                self.__get_deaths_design_follow_up(),
            ),
        )

    @GenericJobClass.is_a_skill
    def harpe(self):
        # The handling of spee dhere is not technically correct, because if the player melded spell speed this would be a faster cast....but who's going to do that on rpr?
        name = "Harpe"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=1300,
                    gcd_base_recast_time=2500,
                    application_delay=890,
                    affected_by_speed_stat=False,
                ),
                "Enhanced Harpe": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=890
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def spinning_scythe(self):
        name = "Spinning Scythe"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def infernal_slice(self):
        name = "Infernal Slice"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Waxing Slice",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )

    @GenericJobClass.is_a_skill
    def whorl_of_death(self):
        name = "Whorl of Death"
        whorl_of_death_damage = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
            ),
            delay_after_parent_application=1160,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(
                whorl_of_death_damage,
                self.__get_deaths_design_follow_up(),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def nightmare_scythe(self):
        name = "Nightmare Scythe"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Spinning Scythe",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def blood_stalk(self):
        name = "Blood Stalk"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
        )

    @GenericJobClass.is_a_skill
    def grim_swathe(self):
        name = "Grim Swathe"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def soul_slice(self):
        name = "Soul Slice"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1030,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
        )

    @GenericJobClass.is_a_skill
    def soul_scythe(self):
        name = "Soul Scythe"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=670,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
            has_aoe=True,
        )

    def __get_enhanced_gibbet_follow_up(self):
        name = "Enhanced Gibbet"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=60 * 1000,
                    skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
                ),
            ),
            delay_after_parent_application=0,
        )

    def __get_enhanced_gallows_follow_up(self):
        name = "Enhanced Gallows"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=60 * 1000,
                    skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
                ),
            ),
            delay_after_parent_application=0,
        )

    @GenericJobClass.is_a_skill
    def gibbet(self):
        name = "Gibbet"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
                "Enhanced Gibbet": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_gibbet")
                ),
                "Enhanced Gibbet, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_gibbet"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            follow_up_skills=(self.__get_enhanced_gallows_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def gallows(self):
        name = "Gallows"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
                "Enhanced Gallows": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_gallows")
                ),
                "Enhanced Gallows, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_gallows"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            follow_up_skills=(self.__get_enhanced_gibbet_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def guillotine(self):
        name = "Guillotine"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def unveiled_gibbet(self):
        name = "Unveiled Gibbet"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )

    @GenericJobClass.is_a_skill
    def unveiled_gallows(self):
        name = "Unveiled Gallows"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )

    @GenericJobClass.is_a_skill
    def arcane_circle(self):
        name = "Arcane Circle"
        return Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.03,
                duration=self._skill_data.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )

    @GenericJobClass.is_a_skill
    def gluttony(self):
        name = "Gluttony"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            has_aoe=True,
            aoe_dropoff=0.25,
        )

    def __get_enhanced_void_reaping_follow_up(self):
        name = "Enhanced Void Reaping"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=60 * 1000,
                    skill_allowlist=("Void Reaping",),
                ),
            ),
            delay_after_parent_application=0,
        )

    def __get_enhanced_cross_reaping_follow_up(self):
        name = "Enhanced Cross Reaping"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=60 * 1000,
                    skill_allowlist=("Cross Reaping",),
                ),
            ),
            delay_after_parent_application=0,
        )

    @GenericJobClass.is_a_skill
    def void_reaping(self):
        name = "Void Reaping"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Enhanced Void Reaping": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_enhanced")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=540,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
            follow_up_skills=(self.__get_enhanced_cross_reaping_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def cross_reaping(self):
        name = "Cross Reaping"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Enhanced Cross Reaping": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_enhanced")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=620
            ),
            follow_up_skills=(self.__get_enhanced_void_reaping_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def grim_reaping(self):
        name = "Grim Reaping"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=800
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def harvest_moon(self):
        name = "Harvest Moon"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                application_delay=1160,
                affected_by_speed_stat=False,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def lemures_slice(self):
        name = "Lemure's Slice"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
        )

    @GenericJobClass.is_a_skill
    def lemures_scythe(self):
        name = "Lemure's Scythe"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def plentiful_harvest(self):
        name = "Plentiful Harvest"
        base_potency = self._skill_data.get_skill_data(name, "base_potency")
        potency_increment = self._skill_data.get_skill_data(name, "potency_increment")
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=base_potency + 7 * potency_increment
                ),
                "1 stack": DamageSpec(potency=base_potency),
                "2 stacks": DamageSpec(potency=base_potency + potency_increment),
                "3 stacks": DamageSpec(potency=base_potency + 2 * potency_increment),
                "4 stacks": DamageSpec(potency=base_potency + 3 * potency_increment),
                "5 stacks": DamageSpec(potency=base_potency + 4 * potency_increment),
                "6 stacks": DamageSpec(potency=base_potency + 5 * potency_increment),
                "7 stacks": DamageSpec(potency=base_potency + 6 * potency_increment),
                "8 stacks": DamageSpec(potency=base_potency + 7 * potency_increment),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def communio(self):
        name = "Communio"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1300, application_delay=620, affected_by_speed_stat=False
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def sacrificium(self):
        if self._level < 92:
            return None
        name = "Sacrificium"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def executioners_gibbet(self):
        if self._level < 96:
            return None
        name = "Executioner's Gibbet"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
                "Enhanced Gibbet": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_enhanced")
                ),
                "Enhanced Gibbet, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_enhanced"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(self.__get_enhanced_gallows_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def executioners_gallows(self):
        if self._level < 96:
            return None
        name = "Executioner's Gallows"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
                "Enhanced Gallows": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_enhanced")
                ),
                "Enhanced Gallows, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_enhanced"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=2140
            ),
            follow_up_skills=(self.__get_enhanced_gibbet_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def executioners_guillotine(self):
        if self._level < 96:
            return None
        name = "Executioner's Guillotine"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def perfectio(self):
        if self._level < 100:
            return None
        name = "Perfectio"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                application_delay=1290,
                affected_by_speed_stat=False,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def hells_ingress(self):
        name = "Hell's Ingress"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,
            follow_up_skills=(self.__get_enhanced_harp_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def hells_egress(self):
        name = "Hell's Egress"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,
            follow_up_skills=(self.__get_enhanced_harp_follow_up(),),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def true_north(self):
        name = "True North"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def enshroud(self):
        name = "Enshroud"
        return Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                expires_status_effects=(
                    "Enhanced Void Reaping",
                    "Enhanced Cross Reaping",
                )
            ),
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def soulsow(self):
        # Would be affected by spell speed, but I'll assume the user is not going to do that on RPR.
        name = "Soulsow"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: self.instant_timing_spec,
                "In Combat": TimingSpec(
                    base_cast_time=5000,
                    gcd_base_recast_time=2500,
                    affected_by_speed_stat=False,
                ),
            },
        )
