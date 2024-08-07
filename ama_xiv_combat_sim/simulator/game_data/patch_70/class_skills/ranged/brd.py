import numpy as np

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
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


def add_brd_skills(skill_library):
    auto_timing = get_shot_timing()
    instant_timing_spec = get_instant_timing_spec()

    stormbite_dot = Skill(
        name="Stormbite (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=25, damage_class=DamageClass.PHYSICAL_DOT),
    )
    stormbite_follow_up = FollowUp(
        skill=stormbite_dot,
        delay_after_parent_application=0,
        dot_duration=45 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )
    caustic_bite_dot = Skill(
        name="Caustic Bite (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=20, damage_class=DamageClass.PHYSICAL_DOT),
    )
    caustic_bite_follow_up = FollowUp(
        skill=caustic_bite_dot,
        delay_after_parent_application=0,
        dot_duration=45 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    army_paeon_rep1 = FollowUp(
        skill=Skill(
            name="Army's Paeon",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.04,
                auto_attack_delay_reduction=0.04,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    army_paeon_rep2 = FollowUp(
        skill=Skill(
            name="Army's Paeon",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.08,
                auto_attack_delay_reduction=0.08,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    army_paeon_rep3 = FollowUp(
        skill=Skill(
            name="Army's Paeon",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.12,
                auto_attack_delay_reduction=0.12,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    army_paeon_rep4 = FollowUp(
        skill=Skill(
            name="Army's Paeon",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.16,
                auto_attack_delay_reduction=0.16,
                duration=45 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    army_muse_1_follow_up = FollowUp(
        skill=Skill(
            name="Army's Muse",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.01,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    army_muse_2_follow_up = FollowUp(
        skill=Skill(
            name="Army's Muse",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.02,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    army_muse_3_follow_up = FollowUp(
        skill=Skill(
            name="Army's Muse",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.04,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )
    army_muse_4_follow_up = FollowUp(
        skill=Skill(
            name="Army's Muse",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.12,
                auto_attack_delay_reduction=0.01,
                duration=10 * 1000,
            ),
        ),
        delay_after_parent_application=0,
    )

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

    skill_library.add_skill(
        Skill(
            name="Shot",
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=80, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Raging Strikes",
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.15, duration=int(19.98 * 1000)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bloodletter",
            is_GCD=False,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1600
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Mage's Ballad",
            is_GCD=False,
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
        )
    )

    skill_library.add_skill(
        Skill(
            name="Army's Paeon",
            is_GCD=False,
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
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rain of Death",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1650
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Battle Voice",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                dh_rate_add=0.20, duration=20 * 1000, is_party_effect=True
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="The Wanderer's Minuet",
            is_GCD=False,
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
        )
    )
    skill_library.add_skill(
        Skill(
            name="Pitch Perfect",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=360),
                "1 Repertoire": DamageSpec(potency=100),
                "2 Repertoire": DamageSpec(potency=220),
                "3 Repertoire": DamageSpec(potency=360),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            job_resource_spec=(JobResourceSpec(name="Repertoire", change=-np.inf),),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Empyreal Arrow",
            is_GCD=False,
            damage_spec=DamageSpec(potency=260),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Iron Jaws",
            is_GCD=True,
            damage_spec=DamageSpec(potency=100),
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
    skill_library.add_skill(
        Skill(
            name="Sidewinder",
            is_GCD=False,
            damage_spec=DamageSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Caustic Bite",
            is_GCD=False,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills=(caustic_bite_follow_up,),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Stormbite",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills=(stormbite_follow_up,),
        )
    )

    refulgent_arrow_barrage2 = FollowUp(
        skill=Skill(
            name="Refulgent Arrow",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
        ),
        delay_after_parent_application=120,
    )
    refulgent_arrow_barrage3 = FollowUp(
        skill=Skill(
            name="Refulgent Arrow",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
        ),
        delay_after_parent_application=240,
    )
    skill_library.add_skill(
        Skill(
            name="Refulgent Arrow",
            is_GCD=True,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1470
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Barrage": (refulgent_arrow_barrage2, refulgent_arrow_barrage3),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shadowbite",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=170),
                "Barrage": DamageSpec(potency=270),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Burst Shot",
            is_GCD=True,
            damage_spec=DamageSpec(potency=220),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1470
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Apex Arrow",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "20 Soul Voice": DamageSpec(potency=120),
                "25 Soul Voice": DamageSpec(potency=150),
                "30 Soul Voice": DamageSpec(potency=180),
                "35 Soul Voice": DamageSpec(potency=210),
                "40 Soul Voice": DamageSpec(potency=240),
                "45 Soul Voice": DamageSpec(potency=270),
                "50 Soul Voice": DamageSpec(potency=300),
                "55 Soul Voice": DamageSpec(potency=330),
                "60 Soul Voice": DamageSpec(potency=360),
                "65 Soul Voice": DamageSpec(potency=390),
                "70 Soul Voice": DamageSpec(potency=420),
                "75 Soul Voice": DamageSpec(potency=450),
                "80 Soul Voice": DamageSpec(potency=480),
                "85 Soul Voice": DamageSpec(potency=510),
                "90 Soul Voice": DamageSpec(potency=540),
                "95 Soul Voice": DamageSpec(potency=570),
                "100 Soul Voice": DamageSpec(potency=600),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            job_resource_spec=(JobResourceSpec(name="Soul Voice", change=-np.inf),),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Ladonsbite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1110
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blast Arrow",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1650
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

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

    skill_library.add_skill(
        Skill(
            name="Radiant Finale",
            is_GCD=False,
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    damage_mult=1.06, duration=20 * 1000, is_party_effect=True
                ),
                "1 Mage's Coda": StatusEffectSpec(
                    damage_mult=1.02, duration=20 * 1000, is_party_effect=True
                ),
                "1 Army's Coda": StatusEffectSpec(
                    damage_mult=1.02, duration=20 * 1000, is_party_effect=True
                ),
                "1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.02, duration=20 * 1000, is_party_effect=True
                ),
                "1 Mage's Coda, 1 Army's Coda": StatusEffectSpec(
                    damage_mult=1.04, duration=20 * 1000, is_party_effect=True
                ),
                "1 Mage's Coda, 1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.04, duration=20 * 1000, is_party_effect=True
                ),
                "1 Army's Coda, 1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.04, duration=20 * 1000, is_party_effect=True
                ),
                "1 Mage's Coda, 1 Army's Coda, 1 Wanderer's Coda": StatusEffectSpec(
                    damage_mult=1.06, duration=20 * 1000, is_party_effect=True
                ),
                "1 Coda, Buff Only": StatusEffectSpec(
                    damage_mult=1.02, duration=20 * 1000, is_party_effect=True
                ),
                "2 Coda, Buff Only": StatusEffectSpec(
                    damage_mult=1.04, duration=20 * 1000, is_party_effect=True
                ),
                "3 Coda, Buff Only": StatusEffectSpec(
                    damage_mult=1.06, duration=20 * 1000, is_party_effect=True
                ),
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Mage's Coda", change=-1),
                    JobResourceSpec(name="Army's Coda", change=-1),
                    JobResourceSpec(name="Wanderer's Coda", change=-1),
                ),
                "Buff Only": tuple(),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
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
                "1 Coda, Buff Only": (encore1,),
                "2 Coda, Buff Only": (encore2,),
                "3 Coda, Buff Only": (encore3,),
            },
        )
    )

    skill_library.add_skill(
        Skill(
            name="Barrage",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=10 * 1000,
                skill_allowlist=(
                    "Refulgent Arrow",
                    "Shadowbite",
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Heartbreak Shot",
            is_GCD=False,
            damage_spec=DamageSpec(potency=180),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1650
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Resonant Arrow",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Radiant Encore",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=900),
                "3 Encore": DamageSpec(potency=900),
                "2 Encore": DamageSpec(potency=600),
                "1 Encore": DamageSpec(potency=500),
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
