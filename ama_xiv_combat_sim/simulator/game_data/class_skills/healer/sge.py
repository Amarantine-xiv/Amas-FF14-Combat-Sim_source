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

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sge_data import (
    all_sge_skills,
)


def add_sge_skills(skill_library):

    all_sge_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_sge_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("SGE")

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

    name = "Dosis III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=670
            ),
            damage_spec=DamageSpec(potency=all_sge_skills.get_potency(name)),
        )
    )

    name = "Phlegma III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Toxikon II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1200
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Dyskrasia II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            damage_spec=DamageSpec(potency=all_sge_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Pneuma"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=580
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.4,
        )
    )

    name = "Eukrasia"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1000,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )

    name = "Eukrasian Dosis III (dot)"
    e_dosis_iii = Skill(
        name=name,
        damage_spec=DamageSpec(
            potency=all_sge_skills.get_potency(name),
            damage_class=DamageClass.MAGICAL_DOT,
        ),
    )

    name = "Eukrasian Dosis III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=760,
                gcd_base_recast_time=1500,
            ),
            follow_up_skills=(
                FollowUp(
                    skill=e_dosis_iii,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )
    )

    if level in [100]:
        name = "Eukrasian Dosis III (dot)" #for now, put same name to overwrite, even though it's E. dysk....
        e_dysk = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_sge_skills.get_skill_data(name, "potency_dysk"),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Eukrasian Dyskrasia"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=1030,
                    gcd_base_recast_time=1500,
                ),
                follow_up_skills=(
                    FollowUp(
                        skill=e_dysk,
                        delay_after_parent_application=0,
                        dot_duration=30 * 1000,
                        snapshot_buffs_with_parent=True,
                        snapshot_debuffs_with_parent=True,
                    ),
                ),
                has_aoe=True,
            )
        )
    
    if level in [100]:
        name="Psyche"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=100, application_delay=1100
                ),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_sge_skills.get_potency(name)
                    )
                },
                has_aoe=True,
                aoe_dropoff=0.5,
            )
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
                skill_allowlist=("Dosis III", "Pneuma"),
            ),
        )
    )

    return skill_library
