import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
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


def add_rdm_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("RDM")
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

    skill_library.add_skill(
        Skill(
            name="Auto",
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Riposte",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            combo_spec=(ComboSpec(),),
            timing_spec=instant_timing_spec,
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Corps-a-corps",
            is_GCD=False,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    verthunder_2_damage_follow_up = FollowUp(
        skill=Skill(name="Verthunder II", damage_spec=DamageSpec(potency=140)),
        delay_after_parent_application=800,
    )
    skill_library.add_skill(
        Skill(
            name="Verthunder II",
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
        )
    )

    veraero_2_damage_follow_up = FollowUp(
        skill=Skill(name="Veraero II", damage_spec=DamageSpec(potency=140)),
        delay_after_parent_application=800,
    )
    skill_library.add_skill(
        Skill(
            name="Veraero II",
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
        )
    )

    verfire_damage_follow_up = FollowUp(
        skill=Skill(name="Verfire", damage_spec=DamageSpec(potency=380)),
        delay_after_parent_application=800,
    )
    skill_library.add_skill(
        Skill(
            name="Verfire",
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

    verstone_damage_follow_up = FollowUp(
        skill=Skill(name="Verstone", damage_spec=DamageSpec(potency=380)),
        delay_after_parent_application=800,
    )
    skill_library.add_skill(
        Skill(
            name="Verstone",
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
    skill_library.add_skill(
        Skill(
            name="Zwerchhau",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=150),
                "No Combo": DamageSpec(potency=100),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            combo_spec=(ComboSpec(combo_actions=("Riposte", "Enchanted Riposte")),),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Displacement",
            is_GCD=False,
            damage_spec=DamageSpec(potency=180),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Engagement",
            is_GCD=False,
            damage_spec=DamageSpec(potency=180),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fleche",
            is_GCD=False,
            damage_spec=DamageSpec(potency=460),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Redoublement",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Zwerchhau", "Enchanted Zwerchhau")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=230),
                "No Combo": DamageSpec(potency=100),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Moulinet",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Contre Sixte",
            is_GCD=False,
            damage_spec=DamageSpec(potency=380),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Embolden",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.05, duration=int(19.95 * 1000), is_party_effect=True
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=610
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
    skill_library.add_skill(
        Skill(
            name="Manafication",
            is_GCD=False,
            combo_spec=(ComboSpec(),),
            buff_spec=StatusEffectSpec(
                damage_mult=1.05,
                duration=15 * 1000,
                num_uses=6,
                skill_allowlist=manafication_allowlist,
            ),
            timing_spec=instant_timing_spec,
        )
    )

    jolt_2_damage_follow_up = FollowUp(
        skill=Skill(name="Jolt II", damage_spec=DamageSpec(potency=280)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Jolt II",
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

    jolt_3_damage_follow_up = FollowUp(
        skill=Skill(name="Jolt III", damage_spec=DamageSpec(potency=360)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Jolt III",
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

    impact_damage_follow_up = FollowUp(
        skill=Skill(name="Impact", damage_spec=DamageSpec(potency=210)),
        delay_after_parent_application=760,
    )
    impact_acceleration_damage_follow_up = FollowUp(
        skill=Skill(name="Impact", damage_spec=DamageSpec(potency=260)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Impact",
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
        )
    )
    skill_library.add_skill(
        Skill(
            name="Verflare",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=620),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Verholy",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=620),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Reprise",
            is_GCD=True,
            damage_spec=DamageSpec(potency=100),
            timing_spec=instant_timing_spec,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Scorch",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Verflare", "Verholy")),),
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1830
            ),
        )
    )

    verthunder_3_damage_follow_up = FollowUp(
        skill=Skill(name="Verthunder III", damage_spec=DamageSpec(potency=420)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Verthunder III",
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

    veraero_3_damage_follow_up = FollowUp(
        skill=Skill(name="Veraero III", damage_spec=DamageSpec(potency=420)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Veraero III",
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
                    veraero_3_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (veraero_3_damage_follow_up,),
                "Acceleration": (veraero_3_damage_follow_up,),
                "Acceleration, Dualcast": (veraero_3_damage_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Resolution",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Scorch",)),),
            damage_spec=DamageSpec(potency=800),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1560
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Vice of Thorns",
            is_GCD=False,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    grand_impact_damage_follow_up = FollowUp(
        skill=Skill(name="Grand Impact", damage_spec=DamageSpec(potency=600)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Grand Impact",
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
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    grand_impact_damage_follow_up,
                    dualcast_follow_up,
                ),
                "Dualcast": (grand_impact_damage_follow_up,),
            },
        )
    )

    skill_library.add_skill(
        Skill(
            name="Prefulgence",
            is_GCD=False,
            damage_spec=DamageSpec(potency=900),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Enchanted Riposte",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=630,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enchanted Zwerchhau",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Riposte", "Enchanted Riposte")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=360),
                "No Combo": DamageSpec(potency=170),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=630,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enchanted Redoublement",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Enchanted Zwerchhau",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=540),
                "No Combo": DamageSpec(potency=170),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2200,
                animation_lock=650,
                application_delay=630,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enchanted Moulinet",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1),),
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=800,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enchanted Moulinet Deux",
            is_GCD=True,
            combo_spec=(
                ComboSpec(combo_group=1, combo_actions=("Enchanted Moulinet",)),
            ),
            damage_spec=DamageSpec(potency=140),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=800,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enchanted Moulinet Trois",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Enchanted Deux",)),),
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=800,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enchanted Reprise",
            is_GCD=True,
            damage_spec=DamageSpec(potency=380),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=650,
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
            timing_spec=TimingSpec(base_cast_time=10 * 1000, gcd_base_recast_time=2500, animation_lock=rdm_caster_tax),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Vercure",
            is_GCD=True,
            timing_spec=TimingSpec(base_cast_time=2000, gcd_base_recast_time=2500, animation_lock=rdm_caster_tax),
        )
    )

    return skill_library
