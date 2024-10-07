import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.whm_data import (
    all_whm_skills,
)


def add_whm_skills(skill_library):
    all_whm_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_whm_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("WHM")

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

    name = "Glare III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1290
            ),
            damage_spec=DamageSpec(potency=all_whm_skills.get_potency(name)),
        )
    )

    if level in [100]:
        name = "Glare IV"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=100, application_delay=850
                ),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_whm_skills.get_potency(name)
                    )
                },
                has_aoe=True,
                aoe_dropoff=0.4,
            )
        )

    name = "Assize"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=all_whm_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Dia (dot)"
    dia_dot_whm = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_whm_skills.get_potency(name),
            damage_class=DamageClass.MAGICAL_DOT,
        ),
    )

    name = "Dia"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            damage_spec=DamageSpec(potency=all_whm_skills.get_potency(name)),
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

    name = "Afflatus Misery"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_whm_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Holy III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=2500, animation_lock=100, application_delay=2130
            ),
            damage_spec=DamageSpec(potency=all_whm_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Presence of Mind"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
            buff_spec=StatusEffectSpec(
                duration=15 * 1000,
                haste_time_reduction=0.20,
                auto_attack_delay_reduction=0.20,
            ),
        )
    )

    name = "Afflatus Rapture"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )

    name = "Afflatus Solace"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )

    if level in [100]:
        name = "Medica III"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=2000, animation_lock=100, application_delay=0
                ),
            )
        )

    if level in [100]:
        name = "Divine Caress"
        skill_library.add_skill(
            Skill(name=name, is_GCD=False, timing_spec=instant_timing_spec)
        )

    name = "Swiftcast"
    skill_library.add_skill(
        Skill(
            name=name,
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
