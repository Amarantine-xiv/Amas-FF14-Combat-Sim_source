from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
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

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.drk_data import (
    all_drk_skills,
)


def add_drk_skills(skill_library):
    all_drk_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_drk_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("DRK")

    name = "Darkside"
    _darkside_buff = Skill(
        name=name,
        buff_spec=StatusEffectSpec(
            duration=30000, max_duration=60000, damage_mult=1.10
        ),
    )
    skill_library.add_skill(_darkside_buff)

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

    name = "Hard Slash"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
        )
    )

    name = "Syphon Strike"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Hard Slash",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drk_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_drk_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )
    )

    name = "Unleash"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=712
            ),
            has_aoe=True,
        )
    )

    name = "Unmend"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=978
            ),
        )
    )

    name = "Souleater"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Syphon Strike",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drk_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_drk_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )
    )

    name = "Flood of Shadow"
    flood_of_shadow_damage_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name))
        ),
        delay_after_parent_application=624,
        primary_target_only=False,
    )

    name = "Flood of Shadow"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Stalwart Soul"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Unleash",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drk_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_drk_skills.get_potency_no_combo(name)
                ),
            },
            # app delay needs verification
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=712
            ),
            has_aoe=True,
        )
    )

    name = "Edge of Shadow"
    edge_of_shadow_damage_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name))
        ),
        delay_after_parent_application=624,
    )

    name = "Edge of Shadow"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Salted Earth (dot)"
    salted_earth_dot_drk = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_drk_skills.get_potency(name),
            # It is believed that salted earth is a MAGICAL dot (unaspected damage)
            # but the formulas I use have Salted Earth being a very slightly
            # better fit by modelling it as a phys dot, for...some reason.
            damage_class=DamageClass.PHYSICAL_DOT,
        ),
    )
    skill_library.add_skill(salted_earth_dot_drk)

    name = "Salted Earth"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Salt and Darkness"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drk_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Plunge"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=(
                DamageSpec(potency=all_drk_skills.get_potency(name))
                if level in [90]
                else None
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )
    )

    name = "Abyssal Drain"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=978
            ),
            has_aoe=True,
        )
    )

    name = "Carve and Spit"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1473
            ),
        )
    )

    name = "Bloodspiller"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=802
            ),
        )
    )

    name = "Quietus"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            has_aoe=True,
        )
    )

    name = "Shadowbringer"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drk_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=666
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    if level in [90]:
        ls_names_and_potency_and_delays = [
            (
                "Abyssal Drain (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800,
                True,
            ),
            (
                "Plunge (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800 + 2200,
                True,
            ),
            (
                "Shadowbringer (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_shadowbringer"),
                6800 + 2 * 2200,
                False,
            ),
            (
                "Edge of Shadow (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800 + 3 * 2200,
                True,
            ),
            (
                "Bloodspiller (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800 + 4 * 2200,
                True,
            ),
            (
                "Carve and Spit (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800 + 5 * 2200,
                True,
            ),
        ]
    else:
        ls_names_and_potency_and_delays = [
            (
                "Abyssal Drain (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800,
                True,
            ),
            (
                "Shadowbringer (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_shadowbringer"),
                6800 + 2 * 2200,
                False,
            ),
            (
                "Edge of Shadow (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800 + 3 * 2200,
                True,
            ),
            (
                "Bloodspiller (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_base"),
                6800 + 4 * 2200,
                True,
            ),
            (
                "Disesteem (pet)",
                all_drk_skills.get_skill_data("Living Shadow", "potency_disesteem"),
                6800 + 5 * 2200,
                False,
            ),
        ]

    _living_shadow_follow_ups = []
    for (
        skill_name,
        potency,
        delay,
        primary_target_only,
    ) in ls_names_and_potency_and_delays:
        fu = FollowUp(
            skill=Skill(
                name=skill_name,
                is_GCD=False,
                damage_spec=DamageSpec(
                    potency=potency,
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                ),
                status_effect_denylist=("Darkside", "Dragon Sight"),
            ),
            delay_after_parent_application=delay,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=primary_target_only,
        )
        _living_shadow_follow_ups.append(fu)
    _living_shadow_follow_ups = tuple(_living_shadow_follow_ups)

    name = "Living Shadow"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            follow_up_skills=_living_shadow_follow_ups,
            timing_spec=instant_timing_spec,
            status_effect_denylist=("Darkside", "Dragon Sight"),
        )
    )

    if level in [100]:
        name = "Scarlet Delirium"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=581
                ),
            )
        )

    if level in [100]:
        name = "Comeuppance"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=670
                ),
            )
        )

    if level in [100]:
        name = "Torcleaver"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=620
                ),
            )
        )

    if level in [100]:
        name = "Impalement"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_drk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=980
                ),
                has_aoe=True,
            )
        )

    if level in [100]:
        name = "Disesteem"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_drk_skills.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1650
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
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
