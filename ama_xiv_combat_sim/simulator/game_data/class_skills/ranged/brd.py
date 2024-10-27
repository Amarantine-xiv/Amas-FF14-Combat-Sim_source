import numpy as np

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_shot_timing,
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

from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.brd_data import (
    all_brd_skills,
)

def add_brd_skills(skill_library):
    all_brd_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_brd_skills.set_level(level)

    auto_timing = get_shot_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("BRD")
    skill_library.add_resource(
        name="Mage's Coda",
        job_resource_settings=JobResourceSettings(
            max_value=1,
            skill_allowlist=(
                "Mage's Ballad",
                "Radiant Finale",
            ),
        ),
    )
    skill_library.add_resource(
        name="Army's Coda",
        job_resource_settings=JobResourceSettings(
            max_value=1,
            skill_allowlist=(
                "Army's Paeon",
                "Radiant Finale",
            ),
        ),
    )
    skill_library.add_resource(
        name="Wanderer's Coda",
        job_resource_settings=JobResourceSettings(
            max_value=1,
            skill_allowlist=(
                "The Wanderer's Minuet",
                "Radiant Finale",
            ),
        ),
    )
    skill_library.add_resource(
        name="Soul Voice",
        job_resource_settings=JobResourceSettings(
            max_value=100,
            skill_allowlist=(
                "Apex Arrow",
                "Add Soul Voice",
            ),
        ),
    )
    skill_library.add_resource(
        name="Repertoire",
        job_resource_settings=JobResourceSettings(
            max_value=3,
            skill_allowlist=(
                "Pitch Perfect",
                "Add Repertoire",
            ),
        ),
    )

    name="Stormbite (dot)"
    stormbite_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=all_brd_skills.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        ),
        delay_after_parent_application=0,
        dot_duration=45 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    name = "Caustic Bite (dot)"
    caustic_bite_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=all_brd_skills.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        ),
        delay_after_parent_application=0,
        dot_duration=45 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    name="Army's Paeon"
    army_paeon_rep1 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.04,
                auto_attack_delay_reduction=0.04,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    name="Army's Paeon"
    army_paeon_rep2 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.08,
                auto_attack_delay_reduction=0.08,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    name="Army's Paeon"
    army_paeon_rep3 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.12,
                auto_attack_delay_reduction=0.12,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    name="Army's Paeon"
    army_paeon_rep4 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.16,
                auto_attack_delay_reduction=0.16,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    name="Army's Muse"
    army_muse_1_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.01,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    name="Army's Muse"
    army_muse_2_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.02,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    name="Army's Muse"
    army_muse_3_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.04,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

    name="Army's Muse"
    army_muse_4_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.12,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )    

    name="Shot"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=80, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )

    name="Raging Strikes"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.15, duration=int(19.98 * 1000)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )

    name="Bloodletter"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1600
            ),
        )
    )

    if level in [90]:
        name = "Mage's Ballad"
        mage_ballad_potency = DamageSpec(
            potency=all_brd_skills.get_potency(name), trait_damage_mult_override=1.0
        )
    
    name = "Mage's Ballad"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: mage_ballad_potency,
                    "Buff Only": None,
                }
                if level in [90]
                else None
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    damage_mult=1.01,
                    duration=45 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Army's Paeon",
                    ),
                ),
                "Buff Only": StatusEffectSpec(
                    damage_mult=1.01,
                    duration=45 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Army's Paeon",
                    ),
                ),
                "From Log, Buff Only": StatusEffectSpec(
                    damage_mult=1.01,
                    duration=5 * 1000,
                    max_duration=5 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=True,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Army's Paeon",
                    ),
                ),
                "From Log": StatusEffectSpec(
                    damage_mult=1.01,
                    duration=5 * 1000,
                    max_duration=5 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=True,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Army's Paeon",
                    ),
                ),
            },
            timing_spec=instant_timing_spec,
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Mage's Coda", change=1),
                ),
                "Buff Only": tuple(),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Army's Muse, 1 Repertoire": (army_muse_1_follow_up,),
                "Army's Muse, 2 Repertoire": (army_muse_2_follow_up,),
                "Army's Muse, 3 Repertoire": (army_muse_3_follow_up,),
                "Army's Muse, 4 Repertoire": (army_muse_4_follow_up,),
                "Buff Only": tuple(),
            },
            off_class_default_condition="Buff Only"
        )
    )

    name = "Army's Paeon"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_brd_skills.get_potency(name),
                        trait_damage_mult_override=1.0,
                    ),
                    "Buff Only": None,
                    "1 Repertoire": None,
                    "2 Repertoire": None,
                    "3 Repertoire": None,
                    "4 Repertoire": None,
                }
                if level in [90]
                else None
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    dh_rate_add=0.03,
                    duration=45 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=False,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Mage's Ballad",
                    ),
                ),
                "Buff Only": StatusEffectSpec(
                    dh_rate_add=0.03,
                    duration=45 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=True,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Mage's Ballad",
                    ),
                ),
                "From Log, Buff Only": StatusEffectSpec(
                    dh_rate_add=0.03,
                    duration=5 * 1000,
                    max_duration=5 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=True,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Mage's Ballad",
                    ),
                ),
                "From Log": StatusEffectSpec(
                    dh_rate_add=0.03,
                    duration=5 * 1000,
                    max_duration=5 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=True,
                    expires_status_effects=(
                        "The Wanderer's Minuet",
                        "Mage's Ballad",
                    ),
                ),
                "1 Repertoire": None,
                "2 Repertoire": None,
                "3 Repertoire": None,
                "4 Repertoire": None,
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: instant_timing_spec,
                "Buff Only": TimingSpec(base_cast_time=0, animation_lock=0),
                "1 Repertoire": TimingSpec(base_cast_time=0, animation_lock=0),
                "2 Repertoire": TimingSpec(base_cast_time=0, animation_lock=0),
                "3 Repertoire": TimingSpec(base_cast_time=0, animation_lock=0),
                "4 Repertoire": TimingSpec(base_cast_time=0, animation_lock=0),
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Army's Coda", change=1),
                ),
                "Buff Only": tuple(),
                "1 Repertoire": (JobResourceSpec(name="Army's Coda", change=1),),
                "2 Repertoire": (JobResourceSpec(name="Army's Coda", change=1),),
                "3 Repertoire": (JobResourceSpec(name="Army's Coda", change=1),),
                "4 Repertoire": (JobResourceSpec(name="Army's Coda", change=1),),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Buff Only": tuple(),
                "1 Repertoire": (army_paeon_rep1,),
                "2 Repertoire": (army_paeon_rep2,),
                "3 Repertoire": (army_paeon_rep3,),
                "4 Repertoire": (army_paeon_rep4,),
            },
            off_class_default_condition="Buff Only"
        )
    )

    name="Rain of Death"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1650
            ),
            has_aoe=True,
        )
    )

    name = "Battle Voice"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                dh_rate_add=0.20,
                duration=all_brd_skills.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "The Wanderer's Minuet"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_brd_skills.get_potency(name),
                        trait_damage_mult_override=1.0,
                    ),
                    "Buff Only": None,
                }
                if level in [90]
                else None
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    crit_rate_add=0.02,
                    duration=45 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Army's Paeon",
                        "Mage's Ballad",
                    ),
                ),
                "Buff Only": StatusEffectSpec(
                    crit_rate_add=0.02,
                    duration=45 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Army's Paeon",
                        "Mage's Ballad",
                    ),
                ),
                "From Log, Buff Only": StatusEffectSpec(
                    crit_rate_add=0.02,
                    duration=5 * 1000,
                    max_duration=5 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=True,
                    expires_status_effects=(
                        "Army's Paeon",
                        "Mage's Ballad",
                    ),
                ),
                "From Log": StatusEffectSpec(
                    crit_rate_add=0.02,
                    duration=5 * 1000,
                    max_duration=5 * 1000,
                    is_party_effect=True,
                    extends_existing_duration=True,
                    expires_status_effects=(
                        "Army's Paeon",
                        "Mage's Ballad",
                    ),
                ),
            },
            timing_spec=instant_timing_spec,
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Wanderer's Coda", change=1),
                ),
                "Buff Only": tuple(),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Army's Muse, 1 Repertoire": (army_muse_1_follow_up,),
                "Army's Muse, 2 Repertoire": (army_muse_2_follow_up,),
                "Army's Muse, 3 Repertoire": (army_muse_3_follow_up,),
                "Army's Muse, 4 Repertoire": (army_muse_4_follow_up,),
                "Buff Only": tuple(),
            },
            off_class_default_condition="Buff Only"
        )
    )

    name="Pitch Perfect"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_brd_skills.get_skill_data(name, "3 Repertoire")),
                "1 Repertoire": DamageSpec(potency=all_brd_skills.get_skill_data(name, "1 Repertoire")),
                "2 Repertoire": DamageSpec(potency=all_brd_skills.get_skill_data(name, "2 Repertoire")),
                "3 Repertoire": DamageSpec(potency=all_brd_skills.get_skill_data(name, "3 Repertoire")),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            job_resource_spec=(JobResourceSpec(name="Repertoire", change=-np.inf),),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name="Empyreal Arrow"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
        )
    )

    if level in [90]:
        name="Iron Jaws"
        iron_jaw_barrage2 = FollowUp(
            skill=Skill(name=name, damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name))),
            delay_after_parent_application=120,
        )
        name="Iron Jaws"
        iron_jaw_barrage3 = FollowUp(
            skill=Skill(name=name, damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name))),
            delay_after_parent_application=240,
        )
        name="Iron Jaws"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=670
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        stormbite_follow_up,
                        caustic_bite_follow_up,
                    ),
                    "Stormbite": (stormbite_follow_up,),
                    "Caustic Bite": (caustic_bite_follow_up,),
                    "No Dot": tuple(),
                    "Barrage": (
                        stormbite_follow_up,
                        caustic_bite_follow_up,
                        iron_jaw_barrage2,
                        iron_jaw_barrage3,
                    ),
                    "Barrage, Stormbite": (
                        stormbite_follow_up,
                        iron_jaw_barrage2,
                        iron_jaw_barrage3,
                    ),
                    "Barrage, Caustic Bite": (
                        caustic_bite_follow_up,
                        iron_jaw_barrage2,
                        iron_jaw_barrage3,
                    ),
                    "Barrage, No Dot": (iron_jaw_barrage2, iron_jaw_barrage3),
                },
            )
        )

    if level in [100]:
        name="Iron Jaws"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=670
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        stormbite_follow_up,
                        caustic_bite_follow_up,
                    ),
                    "Stormbite": (stormbite_follow_up,),
                    "Caustic Bite": (caustic_bite_follow_up,),
                    "No Dot": tuple(),
                },
            )
        )

    name="Sidewinder"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
        )
    )

    if level in [90]:
        name="Caustic Bite"
        caustic_bite_barrage = FollowUp(
            skill=Skill(name=name, damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name))),
            delay_after_parent_application=0,
        )
        name="Caustic Bite"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (caustic_bite_follow_up,),
                    "Barrage": (
                        caustic_bite_follow_up,
                        caustic_bite_barrage,
                        caustic_bite_barrage,
                    ),
                },
            )
        )
    if level in [100]:
        name = "Caustic Bite"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
                follow_up_skills=(caustic_bite_follow_up,),
            )
        )

    if level in [90]:
        name="Stormbite"
        stormbite_barrage2 = FollowUp(
            skill=Skill(
                name=name, is_GCD=False, damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name))
            ),
            delay_after_parent_application=120,
        )

        name="Stormbite"
        stormbite_barrage3 = FollowUp(
            skill=Skill(
                name=name, is_GCD=False, damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name))
            ),
            delay_after_parent_application=240,
        )

        name="Stormbite"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (stormbite_follow_up,),
                    "Barrage": (
                        stormbite_follow_up,
                        stormbite_barrage2,
                        stormbite_barrage3,
                    ),
                },
            )
        )
    name="Stormbite"
    if level in [100]:
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
                follow_up_skills=(stormbite_follow_up,),
            )
        )
    
    name="Refulgent Arrow"
    refulgent_arrow_barrage2 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
        ),
        delay_after_parent_application=120,
    )

    name="Refulgent Arrow"
    refulgent_arrow_barrage3 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
        ),
        delay_after_parent_application=240,
    )

    name="Refulgent Arrow"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1470
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Barrage": (refulgent_arrow_barrage2, refulgent_arrow_barrage3),
            },
        )
    )

    name="Shadowbite"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_brd_skills.get_skill_data(name, "potency")),
                "Barrage": DamageSpec(potency=all_brd_skills.get_skill_data(name, "potency_barrage")),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            has_aoe=True,
        )
    )

    if level in [90]:
        name="Burst Shot"
        burst_shot_barrage2 = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            ),
            delay_after_parent_application=120,
        )

        name="Burst Shot"
        burst_shot_barrage3 = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            ),
            delay_after_parent_application=240,
        )

        name="Burst Shot"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1470
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: tuple(),
                    "Barrage": (burst_shot_barrage2, burst_shot_barrage3),
                },
            )
        )
    if level in [100]:
        name="Burst Shot"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1470
                ),
            )
        )
        
    name="Apex Arrow"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_brd_skills.get_skill_data(name, "100 Soul Voice")),
                "20 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "20 Soul Voice")),
                "25 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "25 Soul Voice")),
                "30 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "30 Soul Voice")),
                "35 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "35 Soul Voice")),
                "40 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "40 Soul Voice")),
                "45 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "45 Soul Voice")),
                "50 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "50 Soul Voice")),
                "55 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "55 Soul Voice")),
                "60 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "60 Soul Voice")),
                "65 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "65 Soul Voice")),
                "70 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "70 Soul Voice")),
                "75 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "75 Soul Voice")),
                "80 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "80 Soul Voice")),
                "85 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "85 Soul Voice")),
                "90 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "90 Soul Voice")),
                "95 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "95 Soul Voice")),
                "100 Soul Voice": DamageSpec(potency=all_brd_skills.get_skill_data(name, "100 Soul Voice")),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            job_resource_spec=(JobResourceSpec(name="Soul Voice", change=-np.inf),),
            has_aoe=True,
        )
    )

    name="Ladonsbite"
    ladonsbite_barrage2 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
        ),
        delay_after_parent_application=120,
    )

    name="Ladonsbite"
    ladonsbite_barrage3 = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
        ),
        delay_after_parent_application=240,
    )

    name="Ladonsbite"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1110
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Barrage": (ladonsbite_barrage2, ladonsbite_barrage3),
            },
            has_aoe=True,
        )
    )

    name="Blast Arrow"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_brd_skills.get_potency(name))},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1650
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    if level in [100]:
        encore1 = FollowUp(
            skill=Skill(
                name="1 Encore",
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30 * 1000,
                    skill_allowlist=(
                        "Radiant Finale",
                        "Radiant Encore",
                    ),
                ),
            ),
            delay_after_parent_application=0,
        )
        encore2 = FollowUp(
            skill=Skill(
                name="2 Encore",
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30 * 1000,
                    skill_allowlist=(
                        "Radiant Finale",
                        "Radiant Encore",
                    ),
                ),
            ),
            delay_after_parent_application=0,
        )
        encore3 = FollowUp(
            skill=Skill(
                name="3 Encore",
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30 * 1000,
                    skill_allowlist=(
                        "Radiant Finale",
                        "Radiant Encore",
                    ),
                ),
            ),
            delay_after_parent_application=0,
        )
    name="Radiant Finale"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    damage_mult=1.06, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Mage's Coda": StatusEffectSpec(
                    damage_mult=1.02, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Army's Coda": StatusEffectSpec(
                    damage_mult=1.02, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.02, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Mage's Coda, 1 Army's Coda": StatusEffectSpec(
                    damage_mult=1.04, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Mage's Coda, 1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.04, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Army's Coda, 1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.04, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Mage's Coda, 1 Army's Coda, 1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.06, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "1 Coda": StatusEffectSpec(
                    damage_mult=1.02, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "2 Coda": StatusEffectSpec(
                    damage_mult=1.04, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
                "3 Coda": StatusEffectSpec(
                    damage_mult=1.06, duration=all_brd_skills.get_skill_data(name, "duration"), is_party_effect=True
                ),
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Mage's Coda", change=-1),
                    JobResourceSpec(name="Army's Coda", change=-1),
                    JobResourceSpec(name="Wanderer's Coda", change=-1),
                ),                
                "1 Coda": tuple(),
                "2 Coda": tuple(),
                "3 Coda": tuple(),
                #for backwards compatibility
                "1 Coda, Buff Only": tuple(),
                "2 Coda, Buff Only": tuple(),
                "3 Coda, Buff Only": tuple(),
                "Buff Only": tuple()
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (encore2,),
                "1 Mage's Coda": (encore1,),
                "1 Army's Coda": (encore1,),
                "1 Wanderer's Coda": (encore1,),
                "1 Mage's Coda, 1 Army's Coda": (encore2,),
                "1 Mage's Coda, 1 Wanderer's Coda": (encore2,),
                "1 Army's Coda, 1 Wanderer's Coda": (encore2,),
                "1 Mage's Coda, 1 Army's Coda, 1 Wanderer's Coda": (encore3,),
                "1 Coda": tuple(),
                "2 Coda": tuple(),
                "3 Coda": tuple(),
            } if level in [100] else tuple(),
            
        )
    )

    name="Barrage"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=10 * 1000,
                skill_allowlist=(
                    "Iron Jaws",
                    "Caustic Bite",
                    "Stormbite",
                    "Refulgent Arrow",
                    "Shadowbite",
                    "Burst Shot",
                    "Ladonsbite",                    
                ) if level in [90] else (
                    # for level 100
                    "Refulgent Arrow",
                    "Shadowbite",
                ),
            ),
        )
    )
    
    if level in [100]:
        name="Heartbreak Shot"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_brd_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1650
                ),
            )
        )
    
    if level in [100]:
        name="Resonant Arrow"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_brd_skills.get_potency(name))},
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1160
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )
    
    if level in [100]:
        name="Radiant Encore"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_brd_skills.get_skill_data(name, "3 Encore")),
                    "3 Encore": DamageSpec(potency=all_brd_skills.get_skill_data(name, "3 Encore")),
                    "2 Encore": DamageSpec(potency=all_brd_skills.get_skill_data(name, "2 Encore")),
                    "1 Encore": DamageSpec(potency=all_brd_skills.get_skill_data(name, "1 Encore")),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1960
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )
    
    skill_library.add_skill(
        Skill(
            name="Add Soul Voice",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Soul Voice", change=5),
                ),
                "5": (JobResourceSpec(name="Soul Voice", change=5),),
                "10": (JobResourceSpec(name="Soul Voice", change=10),),
                "15": (JobResourceSpec(name="Soul Voice", change=15),),
                "20": (JobResourceSpec(name="Soul Voice", change=20),),
                "25": (JobResourceSpec(name="Soul Voice", change=25),),
                "30": (JobResourceSpec(name="Soul Voice", change=30),),
                "35": (JobResourceSpec(name="Soul Voice", change=35),),
                "40": (JobResourceSpec(name="Soul Voice", change=40),),
                "45": (JobResourceSpec(name="Soul Voice", change=45),),
                "50": (JobResourceSpec(name="Soul Voice", change=50),),
                "55": (JobResourceSpec(name="Soul Voice", change=55),),
                "60": (JobResourceSpec(name="Soul Voice", change=60),),
                "65": (JobResourceSpec(name="Soul Voice", change=65),),
                "70": (JobResourceSpec(name="Soul Voice", change=70),),
                "75": (JobResourceSpec(name="Soul Voice", change=75),),
                "80": (JobResourceSpec(name="Soul Voice", change=80),),
                "85": (JobResourceSpec(name="Soul Voice", change=85),),
                "90": (JobResourceSpec(name="Soul Voice", change=90),),
                "95": (JobResourceSpec(name="Soul Voice", change=95),),
                "100": (JobResourceSpec(name="Soul Voice", change=100),),
            },
        )
    )

    skill_library.add_skill(
        Skill(
            name="Add Repertoire",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Repertoire", change=1),
                ),
                "1": (JobResourceSpec(name="Repertoire", change=1),),
                "2": (JobResourceSpec(name="Repertoire", change=2),),
                "3": (JobResourceSpec(name="Repertoire", change=3),),
            },
        )
    )

    return skill_library
