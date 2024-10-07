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

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.sam_data import (
    all_sam_skills,
)


def add_sam_skills(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()

    all_sam_skills.set_version(version)
    all_sam_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("SAM")

    name = "Fugetsu"
    _fugetsu_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.13, duration=40000),
        ),
        delay_after_parent_application=650,
    )

    name = "Fuka"
    _fuka_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.13,
                auto_attack_delay_reduction=0.13,
                duration=40000,
            ),
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

    if level in [90]:
        name = "Hakaze"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(ComboSpec(),),
                damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=620
                ),
            )
        )
    if level in [100]:
        name = "Gyofu"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                combo_spec=(ComboSpec(),),
                damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=850
                ),
            )
        )

    name = "Jinpu"
    jinpu_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name))
        ),
        delay_after_parent_application=620,
    )
    jinpu_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (
                    ComboSpec(
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "No Combo": (
                    ComboSpec(
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "Meikyo Shisui": (
                    ComboSpec(
                        combo_auto_succeed=True,
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        ),
                    ),
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

    name = "Enhanced Enpi"
    enhanced_enpi_buff = Skill(
        name=name,
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
    name = "Enpi"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sam_skills.get_potency(name)
                ),
                "Enhanced Enpi": DamageSpec(
                    potency=all_sam_skills.get_skill_data(name, "potency_enhanced")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
        )
    )
    name = "Shifu"
    shifu_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name))
        ),
        delay_after_parent_application=800,
    )
    shifu_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=800,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (
                    ComboSpec(
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "No Combo": (
                    ComboSpec(
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "Meikyo Shisui": (
                    ComboSpec(
                        combo_auto_succeed=True,
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        ),
                    ),
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
    name = "Gekko"
    gekko_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name))
        ),
        delay_after_parent_application=760,
    )
    gekko_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=760,
    )
    gekko_no_pos_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_potency_no_positional(name)
            ),
        ),
        delay_after_parent_application=760,
    )
    gekko_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_skill_data(name, "potency_no_pos_no_combo")
            ),
        ),
        delay_after_parent_application=760,
    )
    name = "Gekko"
    skill_library.add_skill(
        Skill(
            name=name,
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

    iaijutsu_timing = TimingSpec(
        base_cast_time=1300,
        affected_by_speed_stat=False,
        affected_by_haste_buffs=False,
        animation_lock=0,
        application_delay=620,
    )

    name = "Higanbana (dot)"
    higanbana_dot = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_sam_skills.get_potency(name),
            damage_class=DamageClass.PHYSICAL_DOT,
        ),
    )
    higanbana_follow_up = FollowUp(
        skill=higanbana_dot,
        delay_after_parent_application=0,
        dot_duration=60 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    name = "Higanbana"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=iaijutsu_timing,
            follow_up_skills=(higanbana_follow_up,),
        )
    )

    name = "Tenka Goken"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=iaijutsu_timing,
        )
    )

    name = "Midare Setsugekka"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=iaijutsu_timing,
        )
    )

    if version in ["6.55"]:
        name = "Kaeshi: Higanbana"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
                timing_spec=instant_timing_spec,
                follow_up_skills=(higanbana_follow_up,),
            )
        )

    name = "Kaeshi: Goken"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Kaeshi: Setsugekka"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Mangetsu"
    magnetsu_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    magnetsu_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency_no_combo(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Kasha"
    kasha_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name))
        ),
        delay_after_parent_application=620,
    )
    kasha_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=620,
    )
    kasha_no_pos_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_potency_no_positional(name)
            ),
        ),
        delay_after_parent_application=620,
    )
    kasha_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_skill_data(name, "potency_no_pos_no_combo")
            ),
        ),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Oka"
    oka_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    oka_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency_no_combo(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Yukikaze"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (
                    ComboSpec(
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "Meikyo Shisui": (
                    ComboSpec(
                        combo_auto_succeed=True,
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        ),
                    ),
                ),
                "No Combo": (
                    ComboSpec(
                        combo_actions=all_sam_skills.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
            },
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sam_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_sam_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )

    name = "Hissatsu: Shinten"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Hissatsu: Gyoten"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )

    name = "Hissatsu: Yaten"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=450
            ),
            follow_up_skills=(enhanced_enpi_follow_up,),
        )
    )

    name = "Hissatsu: Kyuten"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )

    name = "Hissatsu: Guren"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
            aoe_dropoff=0.25,
        )
    )

    name = "Hissatsu: Senei"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )
    )

    name = "Shoha"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )

    if level in [90]:
        name = "Shoha II"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=580
                ),
            )
        )

    name = "Fuko"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
        )
    )

    name = "Ogi Namikiri"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
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

    name = "Kaeshi: Namikiri"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=all_sam_skills.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            has_aoe=True,
            aoe_dropoff=0.75,
        )
    )

    if level in [100]:
        name = "Zanshin"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1030
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )

    if level in [100]:
        name = "Tendo Goken"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=1300, animation_lock=650, application_delay=360
                ),
            )
        )

    if level in [100]:
        name = "Tendo Setsugekka"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(
                    potency=all_sam_skills.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                timing_spec=TimingSpec(
                    base_cast_time=1300,
                    animation_lock=650,
                    application_delay=1030,
                    gcd_base_recast_time=all_sam_skills.get_skill_data(
                        name, "gcd_base_recast_time"
                    ),
                ),
            )
        )

    if level in [100]:
        name = "Tendo Kaeshi Goken"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_sam_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=360
                ),
            )
        )

    if level in [100]:
        name = "Tendo Kaeshi Setsugekka"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(
                    potency=all_sam_skills.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=1030,
                    gcd_base_recast_time=all_sam_skills.get_skill_data(
                        name, "gcd_base_recast_time"
                    ),
                ),
            )
        )

    name = "Meikyo Shisui"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=3,
                duration=int(15.1 * 1000),
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
