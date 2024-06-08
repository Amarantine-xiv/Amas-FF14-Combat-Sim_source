from simulator.calcs.damage_class import DamageClass
from simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from simulator.game_data.patch_655.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from simulator.sim_consts import SimConsts
from simulator.skills.skill import Skill
from simulator.specs.combo_spec import ComboSpec
from simulator.specs.damage_spec import DamageSpec
from simulator.specs.follow_up import FollowUp
from simulator.specs.status_effect_spec import StatusEffectSpec
from simulator.specs.timing_spec import TimingSpec


def add_drg_skills(skill_library):
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
    )

    _power_surge_follow_up = FollowUp(
        skill=Skill(
            name="_Power surge buff",
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
            name="Vorpal Thrust",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=280),
                "No Combo": DamageSpec(potency=130),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1020
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

    disembowel_damage_follow_up = FollowUp(
        skill=Skill(name="Disembowel", damage_spec=DamageSpec(potency=250)),
        delay_after_parent_application=1650,
    )
    disembowel_no_combo_damage_follow_up = FollowUp(
        skill=Skill(name="Disembowel", damage_spec=DamageSpec(potency=140)),
        delay_after_parent_application=1650,
    )
    skill_library.add_skill(
        Skill(
            name="Disembowel",
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
        )
    )
    skill_library.add_skill(
        Skill(
            name="Spineshatter Dive",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Dragonfire Dive",
            is_GCD=False,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Battle Litany",
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=600),
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.10, duration=15 * 1000, is_party_effect=True
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Fang and Claw",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300),
                "No Positional": DamageSpec(potency=260),
                "Wheeling Thrust": DamageSpec(potency=400),
                "Wheeling Thrust, No Positional": DamageSpec(potency=360),
            },
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

    skill_library.add_skill(
        Skill(
            name="Wheeling Thrust",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300),
                "No Positional": DamageSpec(potency=260),
                "Fang and Claw": DamageSpec(potency=400),
                "Fang and Claw, No Positional": DamageSpec(potency=360),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=670
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
    skill_library.add_skill(
        Skill(
            name="Geirskogul",
            is_GCD=False,
            damage_spec=DamageSpec(potency=260),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=670
            ),
        )
    )

    sonic_thrust_damage_follow_up = FollowUp(
        skill=Skill(name="Sonic Thrust", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=800,
    )
    sonic_thrust_no_combo_damage_follow_up = FollowUp(
        skill=Skill(name="Sonic Thrust", damage_spec=DamageSpec(potency=100)),
        delay_after_parent_application=800,
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
        )
    )
    skill_library.add_skill(
        Skill(
            name="Dragon Sight",
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
    skill_library.add_skill(
        Skill(
            name="Left Eye",
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=0),
            buff_spec=StatusEffectSpec(
                damage_mult=1.05, duration=20 * 1000, is_party_effect=True
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
            damage_spec=DamageSpec(potency=280),
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
        )
    )
    skill_library.add_skill(
        Skill(
            name="Heavens' Thrust",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Vorpal Thrust",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=480),
                "No Combo": DamageSpec(potency=100),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=710
            ),
        )
    )
    _chaotic_spring_dot = Skill(
        name="_Chaotic Spring dot",
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
            combo_spec=(ComboSpec(combo_actions=("Disembowel",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300),
                "No Combo": DamageSpec(potency=140),
                "No Positional": DamageSpec(potency=260),
                "No Combo, No Positional": DamageSpec(potency=100),
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
            damage_spec=DamageSpec(potency=420),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1200
            ),
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
