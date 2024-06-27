import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_655.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def add_sge_skills(skill_library):

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("SGE")
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
            name="Dosis III",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=670
            ),
            damage_spec=DamageSpec(potency=330),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Phlegma III",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=600),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Toxikon II",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1200
            ),
            damage_spec=DamageSpec(potency=330),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Dyskrasia II",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            damage_spec=DamageSpec(potency=170),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Pneuma",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=580
            ),
            damage_spec=DamageSpec(potency=330),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Eukrasia",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1000,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )
    dot_sge = Skill(
        name="Eukrasian Dosis III (dot)",
        damage_spec=DamageSpec(potency=75, damage_class=DamageClass.MAGICAL_DOT),
    )
    skill_library.add_skill(
        Skill(
            name="Eukrasian Dosis III",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760, gcd_base_recast_time=1500,
            ),
            follow_up_skills=(
                FollowUp(
                    skill=dot_sge,
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
                skill_allowlist=("Dosis III", "Pneuma"),
            ),
        )
    )

    return skill_library
