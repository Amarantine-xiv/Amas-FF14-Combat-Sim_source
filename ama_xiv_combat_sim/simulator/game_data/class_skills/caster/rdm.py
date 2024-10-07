import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
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

from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.rdm_data import (
    all_rdm_skills,
)


def add_rdm_skills(skill_library):
    all_rdm_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_rdm_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("RDM")

    # lvl 100 enchanted moulinet combo stuff
    if level in [100]:
        skill_library.add_combo_breaker(1, (0,))
        skill_library.add_combo_breaker(0, (1,))

    skill_library.set_status_effect_priority(("Swiftcast", "Acceleration", "Dualcast"))

    rdm_caster_tax = 100

    dualcast_buff = Skill(
        name="Dualcast",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            flat_cast_time_reduction=math.inf,
            add_to_skill_modifier_condition=True,
            duration=15 * 1000,
            num_uses=1,
            skill_allowlist=(
                "Verthunder II",
                "Veraero II",
                "Verfire",
                "Verstone",
                "Vercure",
                "Jolt II",
                "Jolt III",
                "Verraise",
                "Impact",
                "Grand Impact",
                "Verthunder III",
                "Veraero III",
            ),
        ),
    )
    dualcast_follow_up = FollowUp(skill=dualcast_buff, delay_after_parent_application=0)

    name = "Auto"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    name = "Riposte"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            combo_spec=(ComboSpec(),),
            timing_spec=instant_timing_spec,
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    name = "Corps-a-corps"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    name = "Verthunder II"
    verthunder_2_damage_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))
        ),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verthunder_2_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (verthunder_2_damage_follow_up,),
            },
            has_aoe=True,
        )
    )

    name = "Veraero II"
    veraero_2_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    name = "Veraero II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    veraero_2_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (veraero_2_damage_follow_up,),
            },
            has_aoe=True,
        )
    )

    name = "Verfire"
    verfire_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))),
        delay_after_parent_application=800,
    )
    name = "Verfire"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verfire_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (verfire_damage_follow_up,),
            },
        )
    )

    name = "Verstone"
    verstone_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))),
        delay_after_parent_application=800,
    )
    name = "Verstone"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verstone_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (verstone_damage_follow_up,),
            },
        )
    )

    name = "Zwerchhau"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_rdm_skills.get_potency(name)),
                "No Combo": DamageSpec(potency=all_rdm_skills.get_potency_no_combo(name)),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            combo_spec=(ComboSpec(combo_actions=("Riposte", "Enchanted Riposte")),),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    name = "Displacement"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    name = "Engagement"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    name = "Fleche"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    name = "Redoublement"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Zwerchhau", "Enchanted Zwerchhau")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_rdm_skills.get_potency(name)),
                "No Combo": DamageSpec(potency=all_rdm_skills.get_potency_no_combo(name)),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    name = "Moulinet"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            status_effect_denylist=("Manafication", "Embolden"),
            has_aoe=True,
        )
    )

    name = "Contre Sixte"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            status_effect_denylist=("Manafication", "Embolden"),
            has_aoe=True,
        )
    )

    name = "Embolden"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.05,
                duration=all_rdm_skills.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=660
            ),
        )
    )
    manafication_allowlist = (
        "Verthunder II",
        "Veraero II",
        "Verfire",
        "Verstone",
        "Jolt II",
        "Jolt III",
        "Impact",
        "Grand Impact",
        "Verflare",
        "Verholy",
        "Reprise",
        "Scorch",
        "Verthunder III",
        "Veraero III",
        "Resolution",
        "Enchanted Riposte",
        "Enchanted Zwerchhau",
        "Enchanted Redoublement",
        "Enchanted Moulinet",
        "Enchanted Moulinet Deux",
        "Enchanted Moulinet Trois",
        "Enchanted Reprise",
    )
    name = "Manafication"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            combo_spec=(ComboSpec(),),
            buff_spec=StatusEffectSpec(
                damage_mult=1.05,
                duration=all_rdm_skills.get_skill_data(name, "duration"),
                num_uses=6,
                skill_allowlist=manafication_allowlist,
            ),
            timing_spec=instant_timing_spec,
        )
    )

    name = "Jolt II"
    jolt_2_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))),
        delay_after_parent_application=760,
    )
    name = "Jolt II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    jolt_2_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (jolt_2_damage_follow_up,),
            },
        )
    )

    if level in [100]:
        name="Jolt III"
        jolt_3_damage_follow_up = FollowUp(
            skill=Skill(
                name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))
            ),
            delay_after_parent_application=800,
        )
        name="Jolt III"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=2000,
                        animation_lock=rdm_caster_tax,
                        application_delay=0,
                    ),
                    "Dualcast": TimingSpec(
                        base_cast_time=0, animation_lock=650, application_delay=0
                    ),
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        jolt_3_damage_follow_up,
                        dualcast_follow_up,
                    ),
                    "Dualcast": (jolt_3_damage_follow_up,),
                },
            )
        )

    impact_acceleration_bonus_potency = 50
    name = "Impact"
    impact_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))),
        delay_after_parent_application=760,
        primary_target_only=False,
    )    
    name = "Impact"
    impact_acceleration_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name) + impact_acceleration_bonus_potency)),
        delay_after_parent_application=760,
        primary_target_only=False,
    )
    name = "Impact"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=5000,
                    animation_lock=rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration, Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    impact_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (impact_damage_follow_up,),
                "Acceleration": (impact_acceleration_damage_follow_up,),
                "Acceleration, Dualcast": (impact_acceleration_damage_follow_up,),
            },
            has_aoe=True,
        )
    )

    name = "Verflare"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Verholy"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Reprise"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=instant_timing_spec,
        )
    )

    name = "Scorch"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Verflare", "Verholy")),),
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1830
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Verthunder III"
    verthunder_3_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))),
        delay_after_parent_application=760,
    )
    name = "Verthunder III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=5000,
                    animation_lock=rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration, Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verthunder_3_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (verthunder_3_damage_follow_up,),
                "Acceleration": (verthunder_3_damage_follow_up,),
                "Acceleration, Dualcast": (verthunder_3_damage_follow_up,),
            },
        )
    )

    name = "Veraero III"
    veraero_3_damage_follow_up = FollowUp(
        skill=Skill(name=name, damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name))),
        delay_after_parent_application=760,
    )
    name = "Veraero III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=5000, animation_lock=rdm_caster_tax, application_delay=0
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration, Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    veraero_3_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (veraero_3_damage_follow_up,),
                "Acceleration": (veraero_3_damage_follow_up,),
                "Acceleration, Dualcast": (veraero_3_damage_follow_up,),
            },
        )
    )

    name = "Resolution"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Scorch",)),),
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1560
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    if level in [100]:
        name="Vice of Thorns"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=800
                ),
                status_effect_denylist=("Manafication", "Embolden"),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )

    if level in [100]:
        name="Grand Impact"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_rdm_skills.get_potency(name))},
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=5000,
                        animation_lock=rdm_caster_tax,
                        application_delay=1559,
                    ),
                    "Dualcast": TimingSpec(
                        base_cast_time=0, animation_lock=650, application_delay=1550
                    ),
                },
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (dualcast_follow_up,),
                    "Dualcast": tuple(),
                },
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )

    if level in [100]:
        name="Prefulgence"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1420
                ),
                status_effect_denylist=("Manafication",),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )

    name = "Enchanted Riposte"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=630,
            ),
        )
    )

    name = "Enchanted Zwerchhau"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Riposte", "Enchanted Riposte")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_rdm_skills.get_potency(name)),
                "No Combo": DamageSpec(potency=all_rdm_skills.get_potency_no_combo(name)),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=630,
            ),
        )
    )

    name = "Enchanted Redoublement"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Enchanted Zwerchhau",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_rdm_skills.get_potency(name)),
                "No Combo": DamageSpec(potency=all_rdm_skills.get_potency_no_combo(name)),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2200,
                animation_lock=650,
                application_delay=630,
            ),
        )
    )

    name = "Enchanted Moulinet"
    skill_library.add_skill(
        Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=1),) if level in [100] else tuple(),
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=800,
            ),
            has_aoe=True,
        )
    )
    
    if level in [100]:
        name="Enchanted Moulinet Deux"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(
                    ComboSpec(combo_group=1, combo_actions=("Enchanted Moulinet",)),
                ),
                damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    animation_lock=650,
                    application_delay=800,
                ),
                has_aoe=True,
            )
        )
    
    name="Enchanted Moulinet Trois"
    if level in [100]:
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(ComboSpec(combo_group=1, combo_actions=("Enchanted Deux",)),),
                damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    animation_lock=650,
                    application_delay=800,
                ),
                has_aoe=True,
            )
        )
    
    name = "Enchanted Reprise"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rdm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=650
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Swiftcast",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=1,
                skill_allowlist=(
                    "Verthunder II",
                    "Veraero II",
                    "Verfire",
                    "Verstone",
                    "Vercure",
                    "Jolt II",
                    "Jolt III",
                    "Verraise",
                    "Impact",
                    "Verthunder III",
                    "Veraero III",
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Acceleration",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=20 * 1000,
                num_uses=1,
                skill_allowlist=("Impact", "Verthunder III", "Veraero III"),
            ),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(
            name="Verraise",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=10 * 1000,
                gcd_base_recast_time=2500,
                animation_lock=rdm_caster_tax,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Vercure",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=2000,
                gcd_base_recast_time=2500,
                animation_lock=rdm_caster_tax,
            ),
        )
    )

    return skill_library
