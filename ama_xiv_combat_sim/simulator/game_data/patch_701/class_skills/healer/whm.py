import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def add_whm_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("WHM")
    # WHM skills
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
            name="Glare III",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1290
            ),
            damage_spec=DamageSpec(potency=330),
        )
    )
    # TODO lock and delays
    skill_library.add_skill(
        Skill(
            name="Glare IV",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=100, application_delay=850
            ),
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=640)},
            has_aoe=True,
            aoe_dropoff=0.4,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Assize",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=400),
            has_aoe=True,
        )
    )
    dia_dot_whm = Skill(
        name="Dia (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=70, damage_class=DamageClass.MAGICAL_DOT),
    )
    skill_library.add_skill(
        Skill(
            name="Dia",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            damage_spec=DamageSpec(potency=70),
            follow_up_skills=(
                FollowUp(
                    skill=dia_dot_whm,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Afflatus Misery",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1320)},
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Holy III",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=2500, animation_lock=100, application_delay=2130
            ),
            damage_spec=DamageSpec(potency=150),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Presence of Mind",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
            buff_spec=StatusEffectSpec(
                duration=15000,
                haste_time_reduction=0.20,
                auto_attack_delay_reduction=0.20,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Afflatus Rapture",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Afflatus Solace",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
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
                skill_allowlist=("Glare III", "Holy III"),
            ),
        )
    )

    return skill_library
