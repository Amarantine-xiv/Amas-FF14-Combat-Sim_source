import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sch_data import (
    all_sch_skills,
)


def add_sch_skills(skill_library):
    all_sch_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_sch_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("SCH")

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

    name = "Broil IV"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=800
            ),
            damage_spec=DamageSpec(potency=all_sch_skills.get_potency(name)),
        )
    )

    name = "Ruin II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=940
            ),
            damage_spec=DamageSpec(potency=all_sch_skills.get_potency(name)),
        )
    )

    name = "Energy Drain"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            damage_spec=DamageSpec(potency=all_sch_skills.get_potency(name)),
        )
    )

    name = "Art of War II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=all_sch_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Chain Stratagem"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            debuff_spec=StatusEffectSpec(
                duration=all_sch_skills.get_skill_data(name, "duration"),
                crit_rate_add=0.10,
                is_party_effect=True,
            ),
        )
    )

    name = "Biolysis (dot)"
    biolysis_dot = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_sch_skills.get_potency(name),
            damage_class=DamageClass.MAGICAL_DOT,
        ),
    )
    skill_library.add_skill(biolysis_dot)

    name = "Biolysis"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            follow_up_skills=(
                FollowUp(
                    skill=biolysis_dot,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )
    )

    if level in [100]:
        name="Baneful Impaction (dot)"
        baneful_dot = Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sch_skills.get_potency(name), damage_class=DamageClass.MAGICAL_DOT),
        )
    
    if level in [100]:
        name="Baneful Impaction"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
                follow_up_skills=(
                    FollowUp(
                        skill=baneful_dot,
                        delay_after_parent_application=0,
                        dot_duration=15 * 1000,
                        snapshot_buffs_with_parent=True,
                        snapshot_debuffs_with_parent=True,
                    ),
                ),
                has_aoe=True,
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
                skill_allowlist=("Broil IV",),
            ),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Dissipation", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Aetherflow", is_GCD=False, timing_spec=instant_timing_spec)
    )
    
    if level in [100]:
        name="Concitation"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=2000, animation_lock=650, application_delay=670
                ),
            )
        )
        
    if level in [100]:
        name="Manifestation"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=670
                ),
            )
        )
        
    if level in [100]:
        name="Accession"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=670
                ),
            )
        )
    return skill_library
