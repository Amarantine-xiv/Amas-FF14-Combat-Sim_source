from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
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


def add_dnc_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("DNC")

    # Unlike the other phys ranged, DNC's auto potency is 90.
    skill_library.add_skill(
        Skill(
            name="Auto",
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Cascade",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=220),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fountain",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Cascade",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=280),
                "No Combo": DamageSpec(potency=120),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=980
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Windmill",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    _standard_finish_follow_up2 = FollowUp(
        skill=Skill(
            name="Standard Finish",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.05,
                duration=60000,
                is_party_effect=True,
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )
    _standard_finish_follow_up1 = FollowUp(
        skill=Skill(
            name="Standard Finish",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.02, duration=60000, is_party_effect=True
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )
    _standard_remove_followup = FollowUp(
        Skill(
            name="Standard Finish Remove Buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                expires_status_effects=("Standard Finish",), is_party_effect=True
            ),
        ),
        delay_after_parent_application=0,
    )

    standard_finish_follow_up_damage_2 = FollowUp(
        skill=Skill(name="Double Standard Finish", damage_spec=DamageSpec(potency=850)),
        delay_after_parent_application=530,
        primary_target_only=False,
    )
    standard_finish_follow_up_damage_1 = FollowUp(
        skill=Skill(name="Single Standard Finish", damage_spec=DamageSpec(potency=540)),
        delay_after_parent_application=530,
        primary_target_only=False,
    )
    standard_finish_follow_up_damage_0 = FollowUp(
        skill=Skill(name="Standard Finish", damage_spec=DamageSpec(potency=360)),
        delay_after_parent_application=530,
        primary_target_only=False,
    )

    skill_library.add_skill(
        Skill(
            name="Double Standard Finish",
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
    skill_library.add_skill(
        Skill(
            name="Single Standard Finish",
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
    skill_library.add_skill(
        Skill(
            name="Standard Finish",
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

    skill_library.add_skill(
        Skill(
            name="Reverse Cascade",
            is_GCD=True,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bladeshower",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Windmill",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=140),
                "No Combo": DamageSpec(potency=100),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fan Dance",
            is_GCD=False,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rising Windmill",
            is_GCD=True,
            damage_spec=DamageSpec(potency=140),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fountainfall",
            is_GCD=True,
            damage_spec=DamageSpec(potency=340),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1210
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bloodshower",
            is_GCD=True,
            damage_spec=DamageSpec(potency=180),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fan Dance II",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Devilment",
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
    skill_library.add_skill(
        Skill(
            name="Fan Dance III",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    tech4_followup = FollowUp(
        Skill(
            name="Technical Finish",
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
            name="Technical Finish",
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
            name="Technical Finish",
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
            name="Technical Finish",
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
            name="Technical Finish",
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
            name="Technical Finish",
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
            name="Technical Finish",
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
            name="Technical Finish",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.01, duration=int(20.95 * 1000), is_party_effect=True
            ),
        ),
        delay_after_parent_application=125,
        primary_target_only=True,
    )

    tech_remove_followup = FollowUp(
        Skill(
            name="Technical Finish Remove buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                expires_status_effects=("Technical Finish",), is_party_effect=True
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

    skill_library.add_skill(
        Skill(
            name="Quadruple Technical Finish",
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1300),
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

    skill_library.add_skill(
        Skill(
            name="Triple Technical Finish",
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=900),
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

    skill_library.add_skill(
        Skill(
            name="Double Technical Finish",
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=720),
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

    skill_library.add_skill(
        Skill(
            name="Single Technical Finish",
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=540),
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

    skill_library.add_skill(
        Skill(
            name="Technical Finish",
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

    skill_library.add_skill(
        Skill(
            name="Saber Dance",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=520)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=440
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    tillana_damage_follow_up = FollowUp(
        skill=Skill(name="Tillana", damage_spec=DamageSpec(potency=600)),
        delay_after_parent_application=840,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Tillana",
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
    finishing_move_damage_follow_up = FollowUp(
        skill=Skill(name="Finishing Move", damage_spec=DamageSpec(potency=850)),
        delay_after_parent_application=2200,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Finishing Move",
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
    skill_library.add_skill(
        Skill(
            name="Fan Dance IV",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=320
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Starfall Dance",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=600,
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
    skill_library.add_skill(
        Skill(
            name="Last Dance",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=520)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1250
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Dance of the Dawn",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1000)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=2300
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
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
