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


def add_ast_skills(skill_library):

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("AST")
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
            name="Divination",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=600
            ),
            buff_spec=StatusEffectSpec(
                duration=20 * 1000, damage_mult=1.06, is_party_effect=True
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fall Malefic",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1070
            ),
            damage_spec=DamageSpec(potency=270),
        )
    )
    combust_iii_dot = Skill(
        name="Combust III (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=70, damage_class=DamageClass.MAGICAL_DOT),
    )
    skill_library.add_skill(
        Skill(
            name="Combust III",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(
                FollowUp(
                    skill=combust_iii_dot,
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
            name="Lightspeed",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                duration=15 * 1000, flat_cast_time_reduction=2500
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Gravity II",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1160
            ),
            damage_spec=DamageSpec(potency=130),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Macrocosmos",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=100, application_delay=750
            ),
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=250)},
            has_aoe=True,
            aoe_dropoff=0.4,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Lord of Crowns",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            damage_spec=DamageSpec(potency=400),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Card",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                ),
                "Small": StatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.03, is_party_effect=True
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Card Small",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            buff_spec=StatusEffectSpec(
                duration=15 * 1000, damage_mult=1.03, is_party_effect=True
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
                skill_allowlist=("Fall Malefic", "Gravity II"),
            ),
        )
    )

    stellar_detonation_follow_up = FollowUp(
        skill=Skill(
            name="Stellar Explosion (pet)",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": DamageSpec(
                    damage_class=DamageClass.PET, potency=205, pet_job_mod_override=118
                ),
                "Giant Dominance": DamageSpec(
                    damage_class=DamageClass.PET, potency=310, pet_job_mod_override=118
                ),
            },
        ),
        delay_after_parent_application=20 * 1000,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )
    stellar_detonation_follow_up2 = FollowUp(
        skill=Skill(
            name="Stellar Explosion (pet)",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": DamageSpec(
                    damage_class=DamageClass.PET, potency=205, pet_job_mod_override=118
                ),
                "Giant Dominance": DamageSpec(
                    damage_class=DamageClass.PET, potency=310, pet_job_mod_override=118
                ),
            },
        ),
        delay_after_parent_application=10 * 1000,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )

    stellar_detonation_instant = FollowUp(
        skill=Skill(
            name="Stellar Explosion (pet)",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": DamageSpec(
                    damage_class=DamageClass.PET, potency=205, pet_job_mod_override=118
                ),
                "Giant Dominance": DamageSpec(
                    damage_class=DamageClass.PET, potency=310, pet_job_mod_override=118
                ),
            },
        ),
        delay_after_parent_application=0,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )

    giant_dom_follow_up = FollowUp(
        skill=Skill(
            name="Giant Dominance",
            is_GCD=False,
            buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": StatusEffectSpec(
                    duration=int(10.1 * 1000),
                    is_party_effect=False,
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    skill_allowlist=("Stellar Explosion (pet)",),
                ),
            },
        ),
        delay_after_parent_application=10 * 1000,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )

    earthly_dom_follow_up = FollowUp(
        skill=Skill(
            name="Earthly Dominance",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                duration=int(10.1 * 1000),
                is_party_effect=False,
                add_to_skill_modifier_condition=True,
                num_uses=1,
                skill_allowlist=("Stellar Explosion (pet)", "Giant Dominance"),
            ),
        ),
        delay_after_parent_application=0,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )

    skill_library.add_skill(
        Skill(
            name="Giant Dominance",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                duration=int(10.1 * 1000),
                is_party_effect=False,
                add_to_skill_modifier_condition=True,
                num_uses=1,
                skill_allowlist=("Stellar Explosion (pet)",),
            ),
            follow_up_skills=(stellar_detonation_follow_up2,),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Earthly Dominance",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                duration=int(10.1 * 1000),
                is_party_effect=False,
                add_to_skill_modifier_condition=True,
                num_uses=1,
                skill_allowlist=("Stellar Explosion (pet)", "Giant Dominance"),
            ),
            follow_up_skills=(giant_dom_follow_up, stellar_detonation_follow_up),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Stellar Detonation",
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, application_delay=0),
            follow_up_skills=(stellar_detonation_instant,),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Earthly Star",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(
                earthly_dom_follow_up,
                giant_dom_follow_up,
                stellar_detonation_follow_up,
            ),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Oracle",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1740
            ),
            damage_spec=DamageSpec(potency=860),
            has_aoe=True,
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(
            name="Helios Conjunction",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=650, application_delay=620
            ),
        )
    )

    skill_library.add_skill(
        Skill(name="Astral Draw", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Umbral Draw", is_GCD=False, timing_spec=instant_timing_spec)
    )

    for name in [
        "the Arrow",
        "The Arrow",
        "the Ewer",
        "The Ewer",
        "the Spire",
        "The Spire",
        "the Bole",
        "The Bole",
    ]:
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=620
                ),
            )
        )
    for name in ["the Spear", "The Spear", "the Balance", "The Balance"]:
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=620
                ),
                buff_spec={
                    SimConsts.DEFAULT_CONDITION: None,
                    "Big": StatusEffectSpec(
                        duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                    ),
                    "Small": StatusEffectSpec(
                        duration=15 * 1000, damage_mult=1.03, is_party_effect=True
                    ),
                },
            )
        )
    skill_library.add_skill(
        Skill(
            name="Minor Arcana",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    return skill_library
