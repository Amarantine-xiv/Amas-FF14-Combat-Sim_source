from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.dnc_data import (
    all_dnc_skills,
)


class DncSkills(GenericJobClass):
    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_dnc_skills)
        self._job_class = "DNC"

    def __get_standard_finish2_follow_up(self):
        name = "Standard Finish"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.05, duration=60000, is_party_effect=True
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    # Unlike the other phys ranged, DNC's auto potency is 90.
    @GenericJobClass.is_a_skill
    def auto(self):
        name = "Auto"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.shot_timing_spec,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )

    @GenericJobClass.is_a_skill
    def cascade(self):
        name = "Cascade"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )

    @GenericJobClass.is_a_skill
    def fountain(self):
        name = "Fountain"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Cascade",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=980
            ),
        )

    @GenericJobClass.is_a_skill
    def windmill(self):
        name = "Windmill"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def standard_finish(self):
        name = "Standard Finish"
        res = []

        _standard_finish2_follow_up = self.__get_standard_finish2_follow_up()

        _standard_finish1_follow_up = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.02, duration=60000, is_party_effect=True
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

        name = "Standard Finish Remove Buff"
        _standard_remove_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    expires_status_effects=("Standard Finish",), is_party_effect=True
                ),
            ),
            delay_after_parent_application=0,
        )

        name = "Double Standard Finish"
        standard_finish_follow_up_damage_2 = FollowUp(
            skill=Skill(
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Standard Finish", "aoe_dropoff"),
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data("Standard Finish", "Double")
                ),
            ),
            delay_after_parent_application=530,
            primary_target_only=False,
        )
        name = "Single Standard Finish"
        standard_finish_follow_up_damage_1 = FollowUp(
            skill=Skill(
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Standard Finish", "aoe_dropoff"),
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data("Standard Finish", "Single")
                ),
            ),
            delay_after_parent_application=530,
            primary_target_only=False,
        )
        name = "Standard Finish"
        standard_finish_follow_up_damage_0 = FollowUp(
            skill=Skill(
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Standard Finish", "aoe_dropoff"),
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data("Standard Finish", "Zero")
                ),
            ),
            delay_after_parent_application=530,
            primary_target_only=False,
        )

        name = "Double Standard Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Standard Finish", "aoe_dropoff"),
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=0,
                        gcd_base_recast_time=1500,
                        affected_by_speed_stat=False,
                    ),
                    "Buff Only": TimingSpec(base_cast_time=0, gcd_base_recast_time=0),
                    "Remove Buff": TimingSpec(base_cast_time=0, gcd_base_recast_time=0),
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        standard_finish_follow_up_damage_2,
                        _standard_finish2_follow_up,
                    ),
                    "Buff Only": (_standard_finish2_follow_up,),
                    "Remove Buff": (_standard_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )

        name = "Single Standard Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Standard Finish", "aoe_dropoff"),
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=0,
                        gcd_base_recast_time=1500,
                        affected_by_speed_stat=False,
                    ),
                    "Buff Only": TimingSpec(base_cast_time=0, gcd_base_recast_time=0),
                    "Remove Buff": TimingSpec(base_cast_time=0, gcd_base_recast_time=0),
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        standard_finish_follow_up_damage_1,
                        _standard_finish1_follow_up,
                    ),
                    "Buff Only": (_standard_finish1_follow_up,),
                    "Remove Buff": (_standard_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )

        name = "Standard Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Standard Finish", "aoe_dropoff"),
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=0,
                        gcd_base_recast_time=1500,
                        affected_by_speed_stat=False,
                    ),
                    "Buff Only": TimingSpec(base_cast_time=0, gcd_base_recast_time=0),
                    "Remove Buff": TimingSpec(base_cast_time=0, gcd_base_recast_time=0),
                },
                follow_up_skills={
                    # by default, we will ASSUME the user actually means Double Standard Finish, unless otherwise specified.
                    SimConsts.DEFAULT_CONDITION: (
                        standard_finish_follow_up_damage_2,
                        _standard_finish2_follow_up,
                    ),
                    "Buff Only": (_standard_finish2_follow_up,),
                    "Remove Buff": (_standard_remove_followup,),
                    # if it's specifically from a log, then we will use the real names.
                    "Log": (standard_finish_follow_up_damage_0,),
                    "Buff Only, Log": tuple(),
                    "Remove Buff, Log": (_standard_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )
        return res

    @GenericJobClass.is_a_skill
    def reverse_cascade(self):
        name = "Reverse Cascade"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def bladeshower(self):
        name = "Bladeshower"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Windmill",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def fan_dance(self):
        name = "Fan Dance"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def rising_windmill(self):
        name = "Rising Windmill"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def fountainfaill(self):
        name = "Fountainfall"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1210
            ),
        )

    @GenericJobClass.is_a_skill
    def bloodshower(self):
        name = "Bloodshower"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def fan_dance_ii(self):
        name = "Fan Dance II"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def devilment(self):
        name = "Devilment"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: self.instant_timing_spec,
                "Dance Partner": TimingSpec(base_cast_time=0, animation_lock=0),
            },
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.20,
                dh_rate_add=0.20,
                duration=self._skill_data.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def fan_dance_iii(self):
        name = "Fan Dance III"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def technical_finish(self):
        res = []

        name = "Technical Finish"
        tech4_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.05, duration=int(20.45 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        tech3_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.03, duration=int(20.45 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        tech2_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.02, duration=int(20.45 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        tech1_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.01, duration=int(20.45 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        tech4_longest_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.05, duration=int(20.95 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        tech3_longest_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.03, duration=int(20.95 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        tech2_longest_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.02, duration=int(20.95 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        tech1_longest_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.01, duration=int(20.95 * 1000), is_party_effect=True
                ),
            ),
            delay_after_parent_application=125,
            primary_target_only=True,
        )

        name = "Technical Finish Remove buff"
        tech_remove_followup = FollowUp(
            Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    expires_status_effects=("Technical Finish",),
                    is_party_effect=True,
                ),
            ),
            delay_after_parent_application=0,
        )
        tech_finish_timing = TimingSpec(
            base_cast_time=0,
            gcd_base_recast_time=1500,
            affected_by_speed_stat=False,
            application_delay=535,
        )
        tech_finish_status_effect_only_timing = TimingSpec(
            base_cast_time=0, gcd_base_recast_time=0, application_delay=0
        )

        name = "Quadruple Technical Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Technical Finish", "aoe_dropoff"),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            "Technical Finish", "Quadruple"
                        )
                    ),
                    "Buff Only": None,
                    "Remove Buff": None,
                },
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                    "Buff Only": tech_finish_status_effect_only_timing,
                    "Remove Buff": tech_finish_status_effect_only_timing,
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (tech4_followup,),
                    "Longest": (tech4_longest_followup,),
                    "Remove Buff": (tech_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )

        name = "Triple Technical Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Technical Finish", "aoe_dropoff"),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            "Technical Finish", "Triple"
                        )
                    ),
                    "Buff Only": None,
                    "Remove Buff": None,
                },
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                    "Buff Only": tech_finish_status_effect_only_timing,
                    "Remove Buff": tech_finish_status_effect_only_timing,
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (tech3_followup,),
                    "Longest": (tech3_longest_followup,),
                    "Remove Buff": (tech_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )

        name = "Double Technical Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Technical Finish", "aoe_dropoff"),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            "Technical Finish", "Double"
                        )
                    ),
                    "Buff Only": None,
                    "Remove Buff": None,
                },
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                    "Buff Only": tech_finish_status_effect_only_timing,
                    "Remove Buff": tech_finish_status_effect_only_timing,
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (tech2_followup,),
                    "Longest": (tech2_longest_followup,),
                    "Remove Buff": (tech_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )

        name = "Single Technical Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Technical Finish", "aoe_dropoff"),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            "Technical Finish", "Single"
                        )
                    ),
                    "Buff Only": None,
                    "Remove Buff": None,
                },
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                    "Buff Only": tech_finish_status_effect_only_timing,
                    "Remove Buff": tech_finish_status_effect_only_timing,
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (tech1_followup,),
                    "Longest": (tech1_longest_followup,),
                    "Remove Buff": (tech_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )

        name = "Technical Finish"
        res.append(
            Skill(
                name=name,
                is_GCD=True,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data("Technical Finish", "aoe_dropoff"),
                damage_spec={
                    # Default to QUADRUPLE technical finish, unless the user specifies otherwise
                    # by passing in "Log" as the skill conditional.
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1200),
                    "Log": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            "Technical Finish", "Zero"
                        )
                    ),
                    "Buff Only": None,
                    "Remove Buff": None,
                },
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                    "Buff Only": tech_finish_status_effect_only_timing,
                    "Remove Buff": tech_finish_status_effect_only_timing,
                },
                follow_up_skills={
                    # assume QUADRUPLE technical finish, unless the user specifies otherwise
                    # by passing in "Log" as the skill conditional.
                    SimConsts.DEFAULT_CONDITION: (tech4_followup,),
                    "Longest": (tech4_longest_followup,),
                    "Log": tuple(),
                    "Log, Longest": tuple(),
                    "Remove Buff": (tech_remove_followup,),
                    "Log, Remove Buff": (tech_remove_followup,),
                },
                off_class_default_condition="Buff Only",
            )
        )
        return res

    @GenericJobClass.is_a_skill
    def saber_dance(self):
        name = "Saber Dance"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=440
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def tillana(self):
        name = "Tillana"
        return Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            aoe_dropoff=0.5,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                affected_by_speed_stat=False,
                application_delay=840
            ),
        )

    @GenericJobClass.is_a_skill
    def finishing_move(self):
        if self._level < 96:
            return None

        name = "Finishing Move"
        finishing_move_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
                aoe_dropoff=0.75
            ),
            delay_after_parent_application=2050,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                affected_by_speed_stat=False,
            ),
            follow_up_skills=(
                finishing_move_damage_follow_up,
                self.__get_standard_finish2_follow_up(),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def fan_dance_iv(self):
        name = "Fan Dance IV"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=320
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def starfall_dance(self):
        name = "Starfall Dance"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
            has_aoe=True,
            aoe_dropoff=0.75,
        )

    @GenericJobClass.is_a_skill
    def last_dance(self):
        if self._level < 92:
            return None
        name = "Last Dance"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1250
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def dance_of_the_dawn(self):
        if self._level < 100:
            return None
        name = "Dance of the Dawn"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=2360
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def standard_step(self):
        name = "Standard Step"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                affected_by_speed_stat=False,
            ),
        )

    @GenericJobClass.is_a_skill
    def technical_step(self):
        name = "Technical Step"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                affected_by_speed_stat=False,
            ),
        )

    @GenericJobClass.is_a_skill
    def flourish(self):
        return Skill(
            name="Flourish", is_GCD=False, timing_spec=self.instant_timing_spec
        )

    @GenericJobClass.is_a_skill
    def step_actions(self):
        res = []
        step_timing = TimingSpec(
            base_cast_time=0, gcd_base_recast_time=1000, affected_by_speed_stat=False
        )
        for step_name in ["Emboite", "Entrechat", "Jete", "Pirouette", "Step Action"]:
            res.append(Skill(name=step_name, is_GCD=True, timing_spec=step_timing))
        return res
