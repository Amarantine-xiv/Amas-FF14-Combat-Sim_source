from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
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


def add_drg_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("DRG")
    drg_weapon_skills = (
        "True Thrust",
        "Piercing Talon",
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

    _power_surge_follow_up = FollowUp(
        skill=Skill(
            name="Power Surge",
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.10, duration=int(31.6 * 1000)),
        ),
        delay_after_parent_application=0,
    )

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
            name="True Thrust",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=230),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Piercing Talon",
            is_GCD=True,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=850
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Lance Charge",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=660
            ),
            buff_spec=StatusEffectSpec(damage_mult=1.10, duration=20 * 1000),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Doom Spike",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=110),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1290
            ),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Dragonfire Dive",
            is_GCD=False,
            damage_spec=DamageSpec(potency=500),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=800
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Battle Litany",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=625
            ),
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.10, duration=20 * 1000, is_party_effect=True
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Fang and Claw",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Heavens' Thrust",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=340),
                "No Positional": DamageSpec(potency=300),
                "No Combo": DamageSpec(potency=180),
                "No Combo, No Positional": DamageSpec(potency=140),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Wheeling Thrust",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Chaotic Spring",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=340),
                "No Positional": DamageSpec(potency=300),
                "No Combo": DamageSpec(potency=180),
                "No Combo, No Positional": DamageSpec(potency=140),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
        )
    )

    life_of_the_dragon_follow_up = FollowUp(
        skill=Skill(
            name="Life of the Dragon",
            buff_spec=StatusEffectSpec(damage_mult=1.15, duration=20 * 1000),
        ),
        delay_after_parent_application=0,
    )
    geirskogul_damage_follow_up = FollowUp(
        skill=Skill(
            name="Geirskogul",
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=280)},
            has_aoe=True,  # is this needed here? What is the convention?
            aoe_dropoff=0.5,
        ),
        delay_after_parent_application=670,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Geirskogul",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=0
            ),
            follow_up_skills=(
                geirskogul_damage_follow_up,
                life_of_the_dragon_follow_up,
            ),
            has_aoe=True,
        )
    )

    sonic_thrust_damage_follow_up = FollowUp(
        skill=Skill(
            name="Sonic Thrust", damage_spec=DamageSpec(potency=120), has_aoe=True
        ),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    sonic_thrust_no_combo_damage_follow_up = FollowUp(
        skill=Skill(
            name="Sonic Thrust", damage_spec=DamageSpec(potency=100), has_aoe=True
        ),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Sonic Thrust",
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

    # This doesn't actually need a combo_spec, I think? Because the combo simply
    # allows this action to be taken.
    skill_library.add_skill(
        Skill(
            name="Drakesbane",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Wheeling Thrust", "Fang and Claw")),),
            damage_spec=DamageSpec(potency=440),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Mirage Dive",
            is_GCD=False,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Nastrond",
            is_GCD=False,
            damage_spec=DamageSpec(potency=360),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Coerthan Torment",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Sonic Thrust",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=150),
                "No Combo": DamageSpec(potency=100),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=490
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="High Jump",
            is_GCD=False,
            damage_spec=DamageSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=490
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Raiden Thrust",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=320),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Stardiver",
            is_GCD=False,
            damage_spec=DamageSpec(potency=620),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1500, application_delay=1290
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Draconian Fury",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Heavens' Thrust",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Lance Barrage",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=440),
                "No Combo": DamageSpec(potency=140),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=710
            ),
        )
    )
    _chaotic_spring_dot = Skill(
        name="Chaotic Spring (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=45, damage_class=DamageClass.PHYSICAL_DOT),
    )
    _chaotic_spring_follow_up = FollowUp(
        skill=_chaotic_spring_dot,
        delay_after_parent_application=0,
        dot_duration=24 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )
    skill_library.add_skill(
        Skill(
            name="Chaotic Spring",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Spiral Blow",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=340),
                "No Combo": DamageSpec(potency=180),
                "No Positional": DamageSpec(potency=300),
                "No Combo, No Positional": DamageSpec(potency=140),
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
    skill_library.add_skill(
        Skill(
            name="Wyrmwind Thrust",
            is_GCD=False,
            damage_spec=DamageSpec(potency=440),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1200
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Rise of the Dragon",
            is_GCD=False,
            damage_spec=DamageSpec(potency=550),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Lance Barrage",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=340),
                "No Combo": DamageSpec(potency=130),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=940
            ),
        )
    )

    spiral_blow_damage_follow_up = FollowUp(
        skill=Skill(name="Spiral Blow", damage_spec=DamageSpec(potency=300)),
        delay_after_parent_application=1380,
    )
    spiral_blow_no_combo_damage_follow_up = FollowUp(
        skill=Skill(name="Spiral Blow", damage_spec=DamageSpec(potency=140)),
        delay_after_parent_application=1380,
    )
    skill_library.add_skill(
        Skill(
            name="Spiral Blow",
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
    skill_library.add_skill(
        Skill(
            name="Starcross",
            is_GCD=False,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=980
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Life Surge",
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
    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
