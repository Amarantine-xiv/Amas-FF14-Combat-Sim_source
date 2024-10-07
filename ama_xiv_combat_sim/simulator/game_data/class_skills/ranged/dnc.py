from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
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


def add_dnc_skills(skill_library):
    all_dnc_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_dnc_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("DNC")
    # Unlike the other phys ranged, DNC's auto potency is 90.

    name = "Auto"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )

    name = "Cascade"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )

    name = "Fountain"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Cascade",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_dnc_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=980
            ),
        )
    )

    name = "Windmill"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Standard Finish"
    _standard_finish_follow_up2 = FollowUp(
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

    name = "Standard Finish"
    _standard_finish_follow_up1 = FollowUp(
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
            name=name,
            damage_spec=DamageSpec(
                potency=all_dnc_skills.get_skill_data("Standard Finish", "Double")
            ),
        ),
        delay_after_parent_application=530,
        primary_target_only=False,
    )
    name = "Single Standard Finish"
    standard_finish_follow_up_damage_1 = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_dnc_skills.get_skill_data("Standard Finish", "Single")
            ),
        ),
        delay_after_parent_application=530,
        primary_target_only=False,
    )
    name = "Standard Finish"
    standard_finish_follow_up_damage_0 = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_dnc_skills.get_skill_data("Standard Finish", "Zero")
            ),
        ),
        delay_after_parent_application=530,
        primary_target_only=False,
    )

    name = "Double Standard Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
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
                    _standard_finish_follow_up2,
                ),
                "Buff Only": (_standard_finish_follow_up2,),
                "Remove Buff": (_standard_remove_followup,),
            },
        )
    )

    name = "Single Standard Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
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
                    _standard_finish_follow_up1,
                ),
                "Buff Only": (_standard_finish_follow_up1,),
                "Remove Buff": (_standard_remove_followup,),
            },
        )
    )

    name = "Standard Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
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
                    _standard_finish_follow_up2,
                ),
                "Buff Only": (_standard_finish_follow_up2,),
                "Remove Buff": (_standard_remove_followup,),
                # if it's specifically from a log, then we will use the real names.
                "Log": (standard_finish_follow_up_damage_0,),
                "Buff Only, Log": tuple(),
                "Remove Buff, Log": (_standard_remove_followup,),
            },
        )
    )

    name = "Reverse Cascade"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Bladeshower"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Windmill",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_dnc_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )

    name = "Fan Dance"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Rising Windmill"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )

    name = "Fountainfall"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1210
            ),
        )
    )

    name = "Bloodshower"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )

    name = "Fan Dance II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
            has_aoe=True,
        )
    )

    name = "Devilment"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: instant_timing_spec,
                "Dance Partner": TimingSpec(base_cast_time=0, animation_lock=0),
            },
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.20,
                dh_rate_add=0.20,
                duration=20 * 1000,
                is_party_effect=True,
            ),
        )
    )

    name = "Fan Dance III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

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

    name = "Technical Finish"
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

    name = "Technical Finish"
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

    name = "Technical Finish"
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

    name = "Technical Finish"
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

    name = "Technical Finish"
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

    name = "Technical Finish"
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

    name = "Technical Finish"
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
    tech_finish_status_effect_only = TimingSpec(
        base_cast_time=0, gcd_base_recast_time=0, application_delay=0
    )

    name = "Quadruple Technical Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_skill_data(
                        "Technical Finish", "Quadruple"
                    )
                ),
                "Buff Only": None,
                "Remove Buff": None,
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                "Buff Only": tech_finish_status_effect_only,
                "Remove Buff": tech_finish_status_effect_only,
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (tech4_followup,),
                "Longest": (tech4_longest_followup,),
                "Remove Buff": (tech_remove_followup,),
            },
        )
    )

    name = "Triple Technical Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_skill_data("Technical Finish", "Triple")
                ),
                "Buff Only": None,
                "Remove Buff": None,
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                "Buff Only": tech_finish_status_effect_only,
                "Remove Buff": tech_finish_status_effect_only,
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (tech3_followup,),
                "Longest": (tech3_longest_followup,),
                "Remove Buff": (tech_remove_followup,),
            },
        )
    )

    name = "Double Technical Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_skill_data("Technical Finish", "Double")
                ),
                "Buff Only": None,
                "Remove Buff": None,
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                "Buff Only": tech_finish_status_effect_only,
                "Remove Buff": tech_finish_status_effect_only,
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (tech2_followup,),
                "Longest": (tech2_longest_followup,),
                "Remove Buff": (tech_remove_followup,),
            },
        )
    )

    name = "Single Technical Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_skill_data("Technical Finish", "Single")
                ),
                "Buff Only": None,
                "Remove Buff": None,
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                "Buff Only": tech_finish_status_effect_only,
                "Remove Buff": tech_finish_status_effect_only,
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (tech1_followup,),
                "Longest": (tech1_longest_followup,),
                "Remove Buff": (tech_remove_followup,),
            },
        )
    )

    name = "Technical Finish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                # Default to QUADRUPLE technical finish, unless the user specifies otherwise
                # by passing in "Log" as the skill conditional.
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1200),
                "Log": DamageSpec(potency=350),
                "Buff Only": None,
                "Remove Buff": None,
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: tech_finish_timing,
                "Buff Only": tech_finish_status_effect_only,
                "Remove Buff": tech_finish_status_effect_only,
            },
            follow_up_skills={
                # assume QUADRUPLE technical finish, unless the user specifies otherwise
                # by passing in "Log" as the skill conditional.
                SimConsts.DEFAULT_CONDITION: (tech4_followup,),
                "Longest": (tech4_longest_followup,),
                "Log": tuple(),
                "Log, Longest": tuple(),
                "Remove Buff": (tech_remove_followup,),
                "Remove Buff, Log": (tech_remove_followup,),
            },
        )
    )

    name = "Saber Dance"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=440
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Tillana"
    tillana_damage_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name))
        ),
        delay_after_parent_application=840,
        primary_target_only=False,
    )

    name = "Tillana"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                affected_by_speed_stat=False,
            ),
            follow_up_skills=(tillana_damage_follow_up,),
        )
    )

    if level in [100]:
        name = "Finishing Move"
        finishing_move_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=all_dnc_skills.get_potency(name)),
            ),
            delay_after_parent_application=2050,
            primary_target_only=False,
        )

        name = "Finishing Move"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    affected_by_speed_stat=False,
                ),
                follow_up_skills=(
                    finishing_move_damage_follow_up,
                    _standard_finish_follow_up2,
                ),
                has_aoe=True,
            )
        )

    name = "Fan Dance IV"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=320
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Starfall Dance"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_dnc_skills.get_potency(name),
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
    )

    if level in [100]:
        name = "Last Dance"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_dnc_skills.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1250
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    if level in [100]:
        name = "Dance of the Dawn"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_dnc_skills.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=2360
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    name = "Standard Step"
    skill_library.add_skill(
        Skill(
            name="Standard Step",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                affected_by_speed_stat=False,
            ),
        )
    )

    name = "Technical Step"
    skill_library.add_skill(
        Skill(
            name="Technical Step",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                affected_by_speed_stat=False,
            ),
        )
    )
    skill_library.add_skill(
        Skill(name="Flourish", is_GCD=False, timing_spec=instant_timing_spec)
    )

    # Step Actions
    step_timing = TimingSpec(
        base_cast_time=0, gcd_base_recast_time=1000, affected_by_speed_stat=False
    )
    skill_library.add_skill(Skill(name="Emboite", is_GCD=True, timing_spec=step_timing))
    skill_library.add_skill(
        Skill(name="Entrechat", is_GCD=True, timing_spec=step_timing)
    )
    skill_library.add_skill(Skill(name="Jete", is_GCD=True, timing_spec=step_timing))
    skill_library.add_skill(
        Skill(name="Pirouette", is_GCD=True, timing_spec=step_timing)
    )
    skill_library.add_skill(
        Skill(name="Step Action", is_GCD=True, timing_spec=step_timing)
    )
    return skill_library
