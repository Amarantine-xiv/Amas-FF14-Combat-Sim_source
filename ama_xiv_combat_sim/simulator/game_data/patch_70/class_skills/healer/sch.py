import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
    get_cast_gcd_timing_spec,
)
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def add_sch_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("SCH")
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
            name="Broil IV",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=800
            ),
            damage_spec=DamageSpec(potency=310),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ruin II",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=940
            ),
            damage_spec=DamageSpec(potency=270),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Energy Drain",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            damage_spec=DamageSpec(potency=100),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Art of War II",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=180),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Chain Stratagem",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            debuff_spec=StatusEffectSpec(
                duration=20 * 1000, crit_rate_add=0.10, is_party_effect=True
            ),
        )
    )
    biolysis_dot = Skill(
        name="Biolysis (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=75, damage_class=DamageClass.MAGICAL_DOT),
    )
    skill_library.add_skill(
        Skill(
            name="Biolysis",
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
    baneful_dot = Skill(
        name="Baneful Impaction (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=140, damage_class=DamageClass.MAGICAL_DOT),
    )
    skill_library.add_skill(
        Skill(
            name="Baneful Impaction",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
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
    skill_library.add_skill(
        Skill(
            name="Concitation",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=650, application_delay=670
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Manifestation",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Accession",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )
    )
    return skill_library
