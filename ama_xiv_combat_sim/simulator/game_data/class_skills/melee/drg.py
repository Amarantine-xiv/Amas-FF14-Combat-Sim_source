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

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.drg_data import (
    all_drg_skills,
)


def add_drg_skills(skill_library):
    all_drg_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_drg_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("DRG")
    drg_weapon_skills = (
        "True Thrust",
        "Vorpal Thrust",
        "Piercing Talon",
        "Disembowel",
        "Doom Spike",
        "Fang and Claw",
        "Wheeling Thrust",
        "Sonic Thrust",
        "Coerthan Torment",
        "Raiden Thrust",
        "Draconian Fury",
        "Heavens' Thrust",
        "Chaotic Spring",
        "Drakesbane",
        "Lance Barrage",
        "Spiral Blow",
    )

    name = "Power Surge"
    _power_surge_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.10, duration=int(31.6 * 1000)),
        ),
        delay_after_parent_application=0,
    )

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

    name = "True Thrust"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
        )
    )

    if level in [90]:
        name = "Vorpal Thrust"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_drg_skills.get_potency(name)
                    ),
                    "No Combo": DamageSpec(
                        potency=all_drg_skills.get_potency_no_combo(name)
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=1020
                ),
            )
        )

    name = "Piercing Talon"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=850
            ),
        )
    )

    if level in [90]:
        name = "Disembowel"
        disembowel_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            ),
            delay_after_parent_application=1650,
        )
        name = "Disembowel"
        disembowel_no_combo_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=all_drg_skills.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=1650,
        )
        name = "Disembowel"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=0
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        disembowel_damage_follow_up,
                        _power_surge_follow_up,
                    ),
                    "No Combo": (disembowel_no_combo_damage_follow_up,),
                },
            )
        )

    name = "Lance Charge"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=660
            ),
            buff_spec=StatusEffectSpec(
                damage_mult=all_drg_skills.get_skill_data(name, "damage_mult"),
                duration=20 * 1000,
            ),
        )
    )

    name = "Doom Spike"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1290
            ),
            has_aoe=True,
        )
    )

    if level in [90]:
        name = "Spineshatter Dive"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=800, application_delay=800
                ),
            )
        )

    name = "Dragonfire Dive"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=800
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Battle Litany"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.10,
                duration=all_drg_skills.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
        )
    )

    name = "Fang and Claw"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                tuple()
                if level in [90]
                else (ComboSpec(combo_actions=("Heavens' Thrust",)),)
            ),
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_drg_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_drg_skills.get_potency_no_positional(name)
                    ),
                    "Wheeling Thrust": DamageSpec(
                        potency=all_drg_skills.get_skill_data(name, "potency_wheeling")
                    ),
                    "Wheeling Thrust, No Positional": DamageSpec(
                        potency=all_drg_skills.get_skill_data(
                            name, "potency_wheeling_no_pos"
                        )
                    ),
                }
                if level in [90]
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_drg_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_drg_skills.get_potency_no_positional(name)
                    ),
                    "No Combo": DamageSpec(
                        potency=all_drg_skills.get_potency_no_combo(name)
                    ),
                    "No Combo, No Positional": DamageSpec(
                        potency=all_drg_skills.get_skill_data(
                            name, "potency_no_pos_no_combo"
                        )
                    ),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30
                    * 1000,  # is this actually 31.6? or 30+application delay or whatever?
                    # have this buff be consumed (and maybe wasted) on next weaponskill
                    skill_allowlist=drg_weapon_skills,
                ),
                "Wheeling Thrust": None,
            },
        )
    )

    name = "Wheeling Thrust"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                tuple()
                if level in [90]
                else (ComboSpec(combo_actions=("Chaotic Spring",)),)
            ),
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_drg_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_drg_skills.get_potency_no_positional(name)
                    ),
                    "Fang and Claw": DamageSpec(
                        potency=all_drg_skills.get_skill_data(name, "potency_fc")
                    ),
                    "Fang and Claw, No Positional": DamageSpec(
                        potency=all_drg_skills.get_skill_data(name, "potency_fc_no_pos")
                    ),
                }
                if level in [90]
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_drg_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_drg_skills.get_potency_no_positional(name)
                    ),
                    "No Combo": DamageSpec(
                        potency=all_drg_skills.get_potency_no_combo(name)
                    ),
                    "No Combo, No Positional": DamageSpec(
                        potency=all_drg_skills.get_skill_data(
                            name, "potency_no_pos_no_combo"
                        )
                    ),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30
                    * 1000,  # is this actually 31.6? or 30+application delay or whatever?
                    skill_allowlist=drg_weapon_skills,
                ),
                "Fang and Claw": None,
            },
        )
    )

    if level in [100]:
        life_of_the_dragon_follow_up = FollowUp(
            skill=Skill(
                name="Life of the Dragon",
                buff_spec=StatusEffectSpec(damage_mult=1.15, duration=20 * 1000),
            ),
            delay_after_parent_application=0,
        )
    if level in [100]:
        name = "Geirskogul"
        geirskogul_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=280)},
                has_aoe=True,  # is this needed here? What is the convention?
                aoe_dropoff=all_drg_skills.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=670,
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
            primary_target_only=False,
        )

    name = "Geirskogul"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=(
                DamageSpec(potency=all_drg_skills.get_potency(name))
                if level in [90]
                else None
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=0
            ),
            has_aoe=True,  # is this needed here? What is the convention?
            aoe_dropoff=(
                all_drg_skills.get_skill_data(name, "aoe_dropoff")
                if level in [90]
                else None
            ),
            follow_up_skills=(
                tuple()
                if level in [90]
                else (
                    geirskogul_damage_follow_up,
                    life_of_the_dragon_follow_up,
                )
            ),
        )
    )

    name = "Sonic Thrust"
    sonic_thrust_damage_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    sonic_thrust_no_combo_damage_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency_no_combo(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Doom Spike",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    sonic_thrust_damage_follow_up,
                    _power_surge_follow_up,
                ),
                "No Combo": (sonic_thrust_no_combo_damage_follow_up,),
            },
            has_aoe=True,
        )
    )

    if level in [100]:
        name = "Drakesbane"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(
                    ComboSpec(combo_actions=("Wheeling Thrust", "Fang and Claw")),
                ),
                damage_spec=DamageSpec(potency=440),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=620
                ),
            )
        )

    if level in [90]:
        name = "Dragon Sight"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=0, animation_lock=600, application_delay=660
                    ),
                    "Left Eye": TimingSpec(base_cast_time=0, animation_lock=0),
                },
                buff_spec={
                    SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                        damage_mult=1.1, duration=20 * 1000
                    ),
                    "Left Eye": StatusEffectSpec(
                        damage_mult=1.05, duration=20 * 1000, is_party_effect=True
                    ),
                },
            )
        )
    # add this is a potential buff for convenience
    if level in [90]:
        name = "Left Eye"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(base_cast_time=0, animation_lock=0),
                buff_spec=StatusEffectSpec(
                    damage_mult=1.05, duration=20 * 1000, is_party_effect=True
                ),
            )
        )

    name = "Mirage Dive"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=800
            ),
        )
    )

    name = "Nastrond"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Coerthan Torment"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Sonic Thrust",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drg_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_drg_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=490
            ),
            has_aoe=True,
        )
    )

    name = "High Jump"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=490
            ),
        )
    )

    name = "Raiden Thrust"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
        )
    )

    name = "Stardiver"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1500, application_delay=1290
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Draconian Fury"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
            has_aoe=True,
        )
    )

    name = "Heavens' Thrust"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                ComboSpec(
                    combo_actions=all_drg_skills.get_skill_data(name, "combo_action")
                ),
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drg_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_drg_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=710
            ),
        )
    )

    name = "Chaotic Spring (dot)"
    _chaotic_spring_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=all_drg_skills.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        ),
        delay_after_parent_application=0,
        dot_duration=24 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    name = "Chaotic Spring"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                ComboSpec(
                    combo_actions=all_drg_skills.get_skill_data(name, "combo_action")
                ),
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_drg_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_drg_skills.get_potency_no_combo(name)
                ),
                "No Positional": DamageSpec(
                    potency=all_drg_skills.get_potency_no_positional(name)
                ),
                "No Combo, No Positional": DamageSpec(
                    potency=all_drg_skills.get_skill_data(name, "potency_no_pos_no_combo")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=450
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (_chaotic_spring_follow_up,),
                "No Combo": tuple(),
                "No Positional": (_chaotic_spring_follow_up,),
                "No Combo, No Positional": tuple(),
            },
        )
    )

    name = "Wyrmwind Thrust"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1200
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    if level in [100]:
        name = "Rise of the Dragon"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_drg_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=1160
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    if level in [100]:
        name = "Lance Barrage"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_drg_skills.get_potency(name)
                    ),
                    "No Combo": DamageSpec(
                        potency=all_drg_skills.get_potency_no_combo(name)
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=940
                ),
            )
        )

    if level in [100]:
        name = "Spiral Blow"
        spiral_blow_damage_follow_up = FollowUp(
            skill=Skill(name=name, damage_spec=DamageSpec(potency=300)),
            delay_after_parent_application=1380,
        )
        name = "Spiral Blow"
        spiral_blow_no_combo_damage_follow_up = FollowUp(
            skill=Skill(name=name, damage_spec=DamageSpec(potency=140)),
            delay_after_parent_application=1380,
        )
        name = "Spiral Blow"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=0
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        spiral_blow_damage_follow_up,
                        _power_surge_follow_up,
                    ),
                    "No Combo": (spiral_blow_no_combo_damage_follow_up,),
                },
            )
        )

    if level in [100]:
        name = "Starcross"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=700),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=980
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    name = "Life Surge"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=600),
            buff_spec=StatusEffectSpec(
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                duration=5 * 1000,
                num_uses=1,
                skill_allowlist=drg_weapon_skills,
            ),
        )
    )
    # # These skills do not damage, but grants resources/affects future skills.
    # # Since we do not model resources YET, we just record their usage/timings but
    # # not their effect.
    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
