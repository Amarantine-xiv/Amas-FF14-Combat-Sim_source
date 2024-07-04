from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_655.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def add_drk_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("DRK")
    _darkside_buff = Skill(
        name="Darkside",
        buff_spec=StatusEffectSpec(
            duration=30000, max_duration=60000, damage_mult=1.10
        ),
    )
    skill_library.add_skill(_darkside_buff)
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
            name="Hard Slash",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=170),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Syphon Strike",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Hard Slash",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=260),
                "No Combo": DamageSpec(potency=120),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Unleash",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=712
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Unmend",
            is_GCD=True,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=978
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Souleater",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Syphon Strike",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=340),
                "No Combo": DamageSpec(potency=120),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )
    )

    flood_of_shadow_damage_follow_up = FollowUp(
        skill=Skill(name="Flood of Shadow", damage_spec=DamageSpec(potency=160)),
        delay_after_parent_application=624,
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Flood of Shadow",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
            follow_up_skills=(
                flood_of_shadow_damage_follow_up,
                FollowUp(
                    skill=_darkside_buff,
                    delay_after_parent_application=0,
                    primary_target_only=True,
                ),
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Stalwart Soul",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Unleash",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=140),
                "No Combo": DamageSpec(potency=100),
            },
            # app delay needs verification
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=712
            ),
            has_aoe=True,
        )
    )

    edge_of_shadow_damage_follow_up = FollowUp(
        skill=Skill(name="Edge of Shadow", damage_spec=DamageSpec(potency=460)),
        delay_after_parent_application=624,
    )
    skill_library.add_skill(
        Skill(
            name="Edge of Shadow",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(
                edge_of_shadow_damage_follow_up,
                FollowUp(skill=_darkside_buff, delay_after_parent_application=0),
            ),
        )
    )
    salted_earth_dot_drk = Skill(
        name="Salted Earth (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=50,
            # It is believed that salted earth is a MAGICAL dot (unaspected damage)
            # but the formulas I use have Salted Earth being a very slightly
            # better fit by modelling it as a phys dot, for...some reason.
            damage_class=DamageClass.PHYSICAL_DOT,
        ),
    )
    skill_library.add_skill(salted_earth_dot_drk)
    skill_library.add_skill(
        Skill(
            name="Salted Earth",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            follow_up_skills=(
                FollowUp(
                    skill=salted_earth_dot_drk,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=False,
                ),
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Salt and Darkness",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=500)},   
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            has_aoe=True,
            aoe_dropoff= 0.5
        )
    )
    skill_library.add_skill(
        Skill(
            name="Plunge",
            is_GCD=False,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Abyssal Drain",
            is_GCD=False,
            damage_spec=DamageSpec(potency=240),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=978
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Carve and Spit",
            is_GCD=False,
            damage_spec=DamageSpec(potency=510),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1473
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bloodspiller",
            is_GCD=True,
            damage_spec=DamageSpec(potency=500),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=802
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Quietus",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shadowbringer",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=666
            ),
            has_aoe=True,
            aoe_dropoff= 0.5
        )
    )
    ls_names_and_potency = [
        ("Abyssal Drain (pet)", 350),
        ("Plunge (pet)", 350),
        ("Shadowbringer (pet)", 500),
        ("Edge of Shadow (pet)", 350),
        ("Bloodspiller (pet)", 350),
        ("Carve and Spit (pet)", 350),
    ]
    _living_shadow_follow_up_skills = []
    for skill_name, potency in ls_names_and_potency:
        sk = Skill(
            name=skill_name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=potency, damage_class=DamageClass.PET, pet_job_mod_override=100
            ),
            status_effect_denylist=("Darkside", "Dragon Sight"),
        )
        _living_shadow_follow_up_skills.append(sk)

    _living_shadow_follow_ups = tuple(
        FollowUp(
            skill=_living_shadow_follow_up_skills[i],
            delay_after_parent_application=6800 + i * 2200,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
        )
        for i in range(0, len(_living_shadow_follow_up_skills))
    )
    
    # TODO: be able to have certain parts of this skill cleave
    skill_library.add_skill(
        Skill(
            name="Living Shadow",
            is_GCD=False,
            follow_up_skills=_living_shadow_follow_ups,
            timing_spec=instant_timing_spec,
            status_effect_denylist=("Darkside", "Dragon Sight"),
        )
    )
    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Delirium", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Blood Weapon", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Rampart", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Provoke", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Reprisal", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Arm's Length", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Shirk", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
