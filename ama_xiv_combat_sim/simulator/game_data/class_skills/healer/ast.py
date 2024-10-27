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
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.ast_data import (
    all_ast_skills,
)


def add_ast_skills(skill_library):
    all_ast_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_ast_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("AST")

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

    name = "Divination"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=600
            ),
            buff_spec=StatusEffectSpec(
                duration=all_ast_skills.get_skill_data(name, "duration"),
                damage_mult=1.06,
                is_party_effect=True,
            ),
        )
    )

    name = "Fall Malefic"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1070
            ),
            damage_spec=DamageSpec(potency=all_ast_skills.get_potency(name)),
        )
    )

    name = "Combust III (dot)"
    combust_iii_dot = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_ast_skills.get_potency(name),
            damage_class=DamageClass.MAGICAL_DOT,
        ),
    )

    name = "Combust III"
    skill_library.add_skill(
        Skill(
            name=name,
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

    if level in [90]:
        name = "Astrodyne"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=instant_timing_spec,
                buff_spec={
                    SimConsts.DEFAULT_CONDITION: None,
                    "1 Moon, 1 Asterisk, 1 Circle": StatusEffectSpec(
                        duration=15 * 1000, haste_time_reduction=0.10, damage_mult=1.05
                    ),
                    "1 Moon, 1 Asterisk": StatusEffectSpec(
                        duration=15 * 1000, haste_time_reduction=0.10
                    ),
                    "1 Moon, 1 Circle": StatusEffectSpec(
                        duration=15 * 1000, haste_time_reduction=0.10
                    ),
                    "1 Circle, 1 Asterisk": StatusEffectSpec(
                        duration=15 * 1000, haste_time_reduction=0.10
                    ),
                },
                job_resource_spec=(
                    JobResourceSpec(name="Moon", change=-math.inf),
                    JobResourceSpec(name="Asterisk", change=-math.inf),
                    JobResourceSpec(name="Circle", change=-math.inf),
                ),
            )
        )

    name = "Lightspeed"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                duration=15 * 1000, flat_cast_time_reduction=2500
            ),
        )
    )

    name = "Gravity II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1160
            ),
            damage_spec=DamageSpec(potency=all_ast_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Macrocosmos"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=100, application_delay=750
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_ast_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.4,
        )
    )

    name = "Lord of Crowns"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            damage_spec=DamageSpec(potency=all_ast_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Card"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                ),
                "Big": StatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                ),
                "Small": StatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.03, is_party_effect=True
                ),
            },
            off_class_default_condition="Big"
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
                skill_allowlist=("Fall Malefic", "Gravity II"),
            ),
        )
    )

    name = "Stellar Explosion (pet)"
    stellar_detonation_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            status_effect_denylist=("Dragon Sight",),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": DamageSpec(
                    damage_class=DamageClass.PET,
                    potency=all_ast_skills.get_skill_data(name, "Earthly Dominance"),
                    pet_job_mod_override=118,
                ),
                "Giant Dominance": DamageSpec(
                    damage_class=DamageClass.PET,
                    potency=all_ast_skills.get_skill_data(name, "Giant Dominance"),
                    pet_job_mod_override=118,
                ),
            },
        ),
        delay_after_parent_application=20 * 1000,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )

    name = "Stellar Explosion (pet)"
    stellar_detonation_follow_up2 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            status_effect_denylist=("Dragon Sight",),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": DamageSpec(
                    damage_class=DamageClass.PET,
                    potency=all_ast_skills.get_skill_data(name, "Earthly Dominance"),
                    pet_job_mod_override=118,
                ),
                "Giant Dominance": DamageSpec(
                    damage_class=DamageClass.PET,
                    potency=all_ast_skills.get_skill_data(name, "Giant Dominance"),
                    pet_job_mod_override=118,
                ),
            },
        ),
        delay_after_parent_application=10 * 1000,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
    )

    name = "Stellar Explosion (pet)"
    stellar_detonation_instant = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            status_effect_denylist=("Dragon Sight",),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": DamageSpec(
                    damage_class=DamageClass.PET,
                    potency=all_ast_skills.get_skill_data(name, "Earthly Dominance"),
                    pet_job_mod_override=118,
                ),
                "Giant Dominance": DamageSpec(
                    damage_class=DamageClass.PET,
                    potency=all_ast_skills.get_skill_data(name, "Giant Dominance"),
                    pet_job_mod_override=118,
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

    name = "Earthly Dominance"
    earthly_dom_follow_up = FollowUp(
        skill=Skill(
            name=name,
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

    name = "Giant Dominance"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Earthly Dominance"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Stellar Detonation"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            status_effect_denylist=("Dragon Sight",),
            timing_spec=TimingSpec(base_cast_time=0, application_delay=0),
            follow_up_skills=(stellar_detonation_instant,),
            has_aoe=True,
        )
    )

    name = "Earthly Star"
    skill_library.add_skill(
        Skill(
            name=name,
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

    if level in [100]:
        name="Oracle"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1740
                ),
                damage_spec=DamageSpec(potency=all_ast_skills.get_potency(name)),
                has_aoe=True,
            )
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    if level in [100]:
        name="Helios Conjunction"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=1500, animation_lock=650, application_delay=620
                ),
            )
        )        
    
    if level in [90]:
        skill_library.add_skill(
            Skill(name="Draw", is_GCD=False, timing_spec=instant_timing_spec)
        )
    if level in [90]:
        skill_library.add_skill(
            Skill(name="Redraw", is_GCD=False, timing_spec=instant_timing_spec)
        )
    if level in [90]:
        skill_library.add_skill(
            Skill(name="Play", is_GCD=False, timing_spec=instant_timing_spec)
        )

    if level in [90]:
        skill_library.add_resource(
            name="Asterisk",
            job_resource_settings=JobResourceSettings(
                max_value=1, skill_allowlist=("Astrodyne",)
            ),
        )
        skill_library.add_resource(
            name="Moon",
            job_resource_settings=JobResourceSettings(
                max_value=1, skill_allowlist=("Astrodyne",)
            ),
        )
        skill_library.add_resource(
            name="Circle",
            job_resource_settings=JobResourceSettings(
                max_value=1, skill_allowlist=("Astrodyne",)
            ),
        )

    if level in [90]:
        for name, sign in [
            ("the Arrow", "Moon"),
            ("The Arrow", "Moon"),
            ("the Ewer", "Moon"),
            ("The Ewer", "Moon"),
            ("the Balance", "Asterisk"),
            ("The Balance", "Asterisk"),
            ("the Bole", "Asterisk"),
            ("The Bole", "Asterisk"),
            ("the Spire", "Circle"),
            ("The Spire", "Circle"),
            ("the Spear", "Circle"),
            ("The Spear", "Circle"),
        ]:
            skill_library.add_skill(
                Skill(
                    name=name,
                    is_GCD=False,
                    job_resource_spec={
                        SimConsts.DEFAULT_CONDITION: (
                            JobResourceSpec(name=sign, change=+1),
                        ),
                        "Big": tuple(),
                        "Small": tuple(),
                    },
                    timing_spec=instant_timing_spec,
                    buff_spec={
                        SimConsts.DEFAULT_CONDITION: None,
                        "Big": StatusEffectSpec(
                            duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                        ),
                        "Small": StatusEffectSpec(
                            duration=15 * 1000, damage_mult=1.03, is_party_effect=True
                        ),
                    },
                    off_class_default_condition="Big"
                )
            )

    if level in [100]:
        skill_library.add_skill(
            Skill(name="Astral Draw", is_GCD=False, timing_spec=instant_timing_spec)
        )
    if level in [100]:
        skill_library.add_skill(
            Skill(name="Umbral Draw", is_GCD=False, timing_spec=instant_timing_spec)
        )
            
    if level in [100]:
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
                    off_class_default_condition="Big"
                )
            )
                
    name = "Minor Arcana"
    skill_library.add_skill(
        Skill(name=name, is_GCD=False, timing_spec=instant_timing_spec)
    )

    return skill_library
