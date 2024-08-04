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


def add_sam_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("SAM")
    _fugetsu_follow_up = FollowUp(
        skill=Skill(
            name="Fugetsu",
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.13, duration=40000),
        ),
        delay_after_parent_application=650,
    )
    _fuka_follow_up = FollowUp(
        skill=Skill(
            name="Fuka",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.13,
                auto_attack_delay_reduction=0.13,
                duration=40000,
            ),
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
            name="Gyofu",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=230),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=850
            ),
        )
    )

    jinpu_follow_up = FollowUp(
        skill=Skill(name="Jinpu", damage_spec=DamageSpec(potency=300)),
        delay_after_parent_application=620,
    )
    jinpu_no_combo_follow_up = FollowUp(
        skill=Skill(name="Jinpu", damage_spec=DamageSpec(potency=140)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Jinpu",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Gyofu",)),),
                "No Combo": (ComboSpec(combo_actions=("Gyofu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Gyofu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    jinpu_follow_up,
                    _fugetsu_follow_up,
                ),
                "No Combo": (jinpu_no_combo_follow_up,),
            },
        )
    )

    enhanced_enpi_buff = Skill(
        name="Enhanced Enpi",
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=15 * 1000,
            skill_allowlist=("Enpi",),
        ),
    )
    enhanced_enpi_follow_up = FollowUp(
        skill=enhanced_enpi_buff, delay_after_parent_application=0
    )

    skill_library.add_skill(
        Skill(
            name="Enpi",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "Enhanced Enpi": DamageSpec(potency=260),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
        )
    )

    shifu_follow_up = FollowUp(
        skill=Skill(name="Shifu", damage_spec=DamageSpec(potency=300)),
        delay_after_parent_application=800,
    )
    shifu_no_combo_follow_up = FollowUp(
        skill=Skill(name="Shifu", damage_spec=DamageSpec(potency=140)),
        delay_after_parent_application=800,
    )
    skill_library.add_skill(
        Skill(
            name="Shifu",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Gyofu",)),),
                "No Combo": (ComboSpec(combo_actions=("Gyofu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Gyofu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    shifu_follow_up,
                    _fuka_follow_up,
                ),
                "No Combo": (shifu_no_combo_follow_up,),
            },
        )
    )

    gekko_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=420)),
        delay_after_parent_application=760,
    )
    gekko_no_combo_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=210)),
        delay_after_parent_application=760,
    )
    gekko_no_pos_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=370)),
        delay_after_parent_application=760,
    )
    gekko_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Gekko", damage_spec=DamageSpec(potency=160)),
        delay_after_parent_application=760,
    )
    skill_library.add_skill(
        Skill(
            name="Gekko",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Jinpu",)),),
                "No Combo": (ComboSpec(combo_actions=("Jinpu",)),),
                "No Positional": (ComboSpec(combo_actions=("Jinpu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Jinpu",)),
                ),
                "No Positional, Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Jinpu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (gekko_follow_up,),
                "No Combo, No Positional": (gekko_no_pos_no_combo_follow_up,),
                "No Combo": (gekko_no_combo_follow_up,),
                "No Positional": (gekko_no_pos_follow_up,),
                "Meikyo Shisui": (gekko_follow_up, _fugetsu_follow_up),
                "Meikyo Shisui, No Combo, No Positional": (
                    gekko_no_pos_follow_up,
                    _fugetsu_follow_up,
                ),
                "Meikyo Shisui, No Combo": (gekko_follow_up, _fugetsu_follow_up),
                "Meikyo Shisui, No Positional": (
                    gekko_no_pos_follow_up,
                    _fugetsu_follow_up,
                ),
            },
        )
    )
    higanbana_dot = Skill(
        name="Higanbana (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=50, damage_class=DamageClass.PHYSICAL_DOT),
    )
    higanbana_follow_up = FollowUp(
        skill=higanbana_dot,
        delay_after_parent_application=0,
        dot_duration=60 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )
    kaeshi_higanbana_dot = Skill(
        name="Higanbana (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=45, damage_class=DamageClass.PHYSICAL_DOT),
    )
    kaeshi_higanbana_follow_up = FollowUp(
        skill=kaeshi_higanbana_dot,
        delay_after_parent_application=0,
        dot_duration=60 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    iaijutsu_timing = TimingSpec(
        base_cast_time=1300,
        affected_by_speed_stat=False,
        affected_by_haste_buffs=False,
        animation_lock=0,
        application_delay=620,
    )

    skill_library.add_skill(
        Skill(
            name="Higanbana",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=iaijutsu_timing,
            follow_up_skills=(higanbana_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tenka Goken",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=iaijutsu_timing,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Midare Setsugekka",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=640, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=iaijutsu_timing,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Higanbana",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=instant_timing_spec,
            follow_up_skills=(kaeshi_higanbana_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Goken",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Setsugekka",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=640, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    magnetsu_follow_up = FollowUp(
        skill=Skill(name="Mangetsu", damage_spec=DamageSpec(potency=120), has_aoe=True),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    magnetsu_no_combo_follow_up = FollowUp(
        skill=Skill(name="Mangetsu", damage_spec=DamageSpec(potency=100), has_aoe=True),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Mangetsu",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Fuko",)),),
                "No Combo": (ComboSpec(combo_actions=("Fuko",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Fuko",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (magnetsu_follow_up, _fugetsu_follow_up),
                "No Combo": (magnetsu_no_combo_follow_up,),
            },
            has_aoe=True,
        )
    )

    kasha_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=420)),
        delay_after_parent_application=620,
    )
    kasha_no_combo_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=210)),
        delay_after_parent_application=620,
    )
    kasha_no_pos_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=370)),
        delay_after_parent_application=620,
    )
    kasha_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Kasha", damage_spec=DamageSpec(potency=160)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Kasha",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Shifu",)),),
                "No Combo": (ComboSpec(combo_actions=("Shifu",)),),
                "No Positional": (ComboSpec(combo_actions=("Shifu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Shifu",)),
                ),
                "No Positional, Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Shifu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (kasha_follow_up,),
                "No Combo, No Positional": (kasha_no_pos_no_combo_follow_up,),
                "No Combo": (kasha_no_combo_follow_up,),
                "No Positional": (kasha_no_pos_follow_up,),
                "Meikyo Shisui": (kasha_follow_up, _fuka_follow_up),
                "Meikyo Shisui, No Combo, No Positional": (
                    kasha_no_pos_follow_up,
                    _fuka_follow_up,
                ),
                "Meikyo Shisui, No Combo": (kasha_follow_up, _fuka_follow_up),
                "Meikyo Shisui, No Positional": (
                    kasha_no_pos_follow_up,
                    _fuka_follow_up,
                ),
            },
        )
    )
    oka_follow_up = FollowUp(
        skill=Skill(name="Oka", damage_spec=DamageSpec(potency=120), has_aoe=True),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    oka_no_combo_follow_up = FollowUp(
        skill=Skill(name="Oka", damage_spec=DamageSpec(potency=100), has_aoe=True),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Oka",
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Fuko",)),),
                "No Combo": (ComboSpec(combo_actions=("Fuko",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Fuko",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (oka_follow_up, _fuka_follow_up),
                "No Combo": (oka_no_combo_follow_up,),
            },
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Yukikaze",
            is_GCD=True,
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Gyofu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Gyofu",)),
                ),
                "No Combo": (ComboSpec(combo_actions=("Gyofu",)),),
            },
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=340),
                "No Combo": DamageSpec(potency=160),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Shinten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Gyoten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Yaten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=450
            ),
            follow_up_skills=(enhanced_enpi_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Kyuten",
            is_GCD=False,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Guren",
            is_GCD=False,
            damage_spec=DamageSpec(potency=500),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
            aoe_dropoff=0.25,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hissatsu: Senei",
            is_GCD=False,
            damage_spec=DamageSpec(potency=800),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shoha",
            is_GCD=False,
            damage_spec=DamageSpec(potency=640),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fuko",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ogi Namikiri",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=900, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=1300,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
                application_delay=490,
            ),
            has_aoe=True,
            aoe_dropoff=0.75,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Kaeshi: Namikiri",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=900, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            has_aoe=True,
            aoe_dropoff=0.75,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Zanshin",
            is_GCD=False,
            damage_spec=DamageSpec(potency=820),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tendo Goken",
            is_GCD=True,
            damage_spec=DamageSpec(potency=410),
            timing_spec=TimingSpec(
                base_cast_time=1300, animation_lock=650, application_delay=360
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tendo Setsugekka",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=1020, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=1300,
                animation_lock=650,
                application_delay=1030,
                gcd_base_recast_time=2500,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tendo Kaeshi Goken",
            is_GCD=True,
            damage_spec=DamageSpec(potency=410),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=360
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tendo Kaeshi Setsugekka",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=1020, guaranteed_crit=ForcedCritOrDH.FORCE_YES
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1030,
                gcd_base_recast_time=2500,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Meikyo Shisui",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=3,
                duration=int(20.1 * 1000),
                skill_allowlist=(
                    "Hakaze",
                    "Jinpu",
                    "Shifu",
                    "Gekko",
                    "Mangetsu",
                    "Kasha",
                    "Oka",
                    "Yukikaze",
                    "Fuko",
                ),
            ),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Ikishoten", is_GCD=False, timing_spec=instant_timing_spec)
    )

    return skill_library
