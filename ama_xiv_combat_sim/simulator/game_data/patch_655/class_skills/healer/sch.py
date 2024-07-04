import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_655.convenience_timings import (
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
    cast_gcd_timing_spec = get_cast_gcd_timing_spec()
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
            damage_spec=DamageSpec(potency=295),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ruin II",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=940
            ),
            damage_spec=DamageSpec(potency=220),
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
            has_aoe=True,
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
                duration=15000, crit_rate_add=0.10, is_party_effect=True
            ),
        )
    )
    biolysis_dot_sch = Skill(
        name="Biolysis (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=70, damage_class=DamageClass.MAGICAL_DOT),
    )
    skill_library.add_skill(biolysis_dot_sch)
    skill_library.add_skill(
        Skill(
            name="Biolysis",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            follow_up_skills=(
                FollowUp(
                    skill=biolysis_dot_sch,
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
    return skill_library
