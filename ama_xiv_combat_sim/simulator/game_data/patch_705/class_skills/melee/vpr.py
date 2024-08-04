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


def add_vpr_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    # these are based off of pre-trait dread fang. IDK man, idk.
    # COMBO_BASE_POTENCY_NO_VENOM = 180
    # COMBO_BASE_POTENCY_WITH_VENOM = 280
    COMBO_BASE_POTENCY_NO_VENOM = 160
    COMBO_BASE_POTENCY_WITH_VENOM = 260

    skill_library.set_current_job_class("VPR")
    # combo groups
    # 0: Hunter's coil -> twinfang bite. GCD->oGCD combo
    # 1: Swiftskin's Coil -> twinblood bite. GCD->oGCD combo
    # 2: Hunter's Den -> Twinfang Thresh. GCD->oGCD combo
    # 3: Swiftskin's Den -> Twinblood Thresh GCD->oGCD combo
    # 4: Reawaken sequence. Sequence of GCD->(oGCD) combos

    skill_library.add_combo_breaker(
        0,
        (
            1,
            2,
            3,
            4,
        ),
    )
    skill_library.add_combo_breaker(
        1,
        (
            0,
            2,
            3,
            4,
        ),
    )
    skill_library.add_combo_breaker(
        2,
        (
            0,
            1,
            3,
            4,
        ),
    )
    skill_library.add_combo_breaker(
        3,
        (
            0,
            1,
            2,
            4,
        ),
    )
    skill_library.add_combo_breaker(
        4,
        (
            0,
            1,
            2,
            3,
        ),
    )

    # All Venoms that expire other venoms:
    # "Hindstung Venom", "Hindsbane Venom", "Flanksbane Venom",
    # "Flankstung Venom", "Grimskin's Venom", "Grimhunter's Venom"
    def get_venom_follow_up(
        name,
        skill_allowlist,
        duration,
        expires_status_effects=tuple(),
        delay_after_parent_application=0,
    ):
        return FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=duration,
                    num_uses=1,
                    skill_allowlist=skill_allowlist,
                    expires_status_effects=expires_status_effects,
                ),
            ),
            delay_after_parent_application=delay_after_parent_application,
            primary_target_only=True,
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

    honed_reavers_follow_up = FollowUp(
        skill=Skill(
            name="Honed Reavers",
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=60*1000,
                num_uses=1,
                skill_allowlist=("Reaving Fangs", "Reaving Maw"),
                expires_status_effects=("Honed Steel",),
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True
    )

    skill_library.add_skill(
        Skill(
            name="Steel Fangs",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200),
                "Honed Steel": DamageSpec(potency=300),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            follow_up_skills=(honed_reavers_follow_up,),
        )
    )

    hunters_instinct_follow_up = FollowUp(
        skill=Skill(
            name="Hunter's Instinct",
            buff_spec=StatusEffectSpec(damage_mult=1.10, duration=40 * 1000),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )
    skill_library.add_skill(
        Skill(
            name="Hunter's Sting",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
            follow_up_skills=(hunters_instinct_follow_up,),
        )
    )

    honed_steel_follow_up = FollowUp(
        skill=Skill(
            name="Honed Steel",
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=60*1000,
                num_uses=1,
                skill_allowlist=("Steel Fangs", "Steel Maw"),
                expires_status_effects=("Honed Reavers",),
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True
    )
    skill_library.add_skill(
        Skill(
            name="Reaving Fangs",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200),
                         "Honed Reavers": DamageSpec(potency=300)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills=(honed_steel_follow_up,)
        )
    )

    skill_library.add_skill(
        Skill(
            name="Writhing Snap",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )
    swift_scaled_follow_up = FollowUp(
        skill=Skill(
            name="Swiftscaled",
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.15,
                auto_attack_delay_reduction=0.15,
                duration=40 * 1000,
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )

    skill_library.add_skill(
        Skill(
            name="Swiftskin's Sting",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            follow_up_skills=(swift_scaled_follow_up,),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Steel Maw",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1020
            ),
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                         "Honed Steel": DamageSpec(potency=120)},
            follow_up_skills=(honed_reavers_follow_up,),
            has_aoe=True,
        )
    )
    hindstung_venom_follow_up = get_venom_follow_up(
        "Hindstung Venom",
        ("Hindsting Strike",),
        60 * 1000,
        (
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Flanksting Strike",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=340, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Flankstung Venom": DamageSpec(
                    potency=500, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Flankstung Venom, No Positional": DamageSpec(
                    potency=440, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(hindstung_venom_follow_up,),
        )
    )

    hindsbane_venom_follow_up = get_venom_follow_up(
        "Hindsbane Venom",
        ("Hindsbane Fang",),
        60 * 1000,
        (
            "Hindstung Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Flanksbane Fang",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=340, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Flanksbane Venom": DamageSpec(
                    potency=500, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Flanksbane Venom, No Positional": DamageSpec(
                    potency=440, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(
                hindsbane_venom_follow_up,
            ),  # application delay is a bit off due to venom timing
        )
    )

    flanksbane_venom_follow_up = get_venom_follow_up(
        "Flanksbane Venom",
        ("Flanksbane Fang",),
        60 * 1000,
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Hindsting Strike",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=340, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Hindstung Venom": DamageSpec(
                    potency=500, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Hindstung Venom, No Positional": DamageSpec(
                    potency=440, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(flanksbane_venom_follow_up,),
        )
    )

    flankstung_venom_follow_up = get_venom_follow_up(
        "Flankstung Venom",
        ("Flanksting Strike",),
        60 * 1000,
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Hindsbane Fang",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=340, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Hindsbane Venom": DamageSpec(
                    potency=500, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Hindsbane Venom, No Positional": DamageSpec(
                    potency=440, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(flankstung_venom_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Reaving Maw",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                         "Honed Reavers": DamageSpec(potency=120)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(honed_steel_follow_up,),
            has_aoe=True,            
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hunter's Bite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            follow_up_skills=(hunters_instinct_follow_up,),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Swiftskin's Bite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1380
            ),
            follow_up_skills=(swift_scaled_follow_up,),
            has_aoe=True,
        )
    )

    grimskins_venom_follow_up = get_venom_follow_up(
        "Grimskin's Venom",
        ("Bloodied Maw",),
        60 * 1000,
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimhunter's Venom",
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Jagged Maw",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=140),
                "Grimhunter's Venom": DamageSpec(potency=160),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(grimskins_venom_follow_up,),
            has_aoe=True,
        )
    )
    grimhunters_venom_follow_up = get_venom_follow_up(
        "Grimhunter's Venom",
        ("Jagged Maw",),
        60 * 1000,
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Bloodied Maw",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=140),
                "Grimskin's Venom": DamageSpec(potency=160),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(grimhunters_venom_follow_up,),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Death Rattle",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1700
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Last Lash",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Vicewinder",
            is_GCD=True,
            damage_spec=DamageSpec(potency=500),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=580,
                gcd_base_recast_time=3000,
            ),
        )
    )

    hunters_venom_follow_up = get_venom_follow_up(
        "Hunter's Venom", ("Twinfang Bite",), 30 * 1000
    )
    hunters_coil_follow_up = FollowUp(
        skill=Skill(name="Hunter's Coil", damage_spec=DamageSpec(potency=620)),
        delay_after_parent_application=980,
    )
    hunters_coil_no_pos_follow_up = FollowUp(
        skill=Skill(name="Hunter's Coil", damage_spec=DamageSpec(potency=570)),
        delay_after_parent_application=980,
    )
    skill_library.add_skill(
        Skill(
            name="Hunter's Coil",
            combo_spec=(ComboSpec(combo_group=0),),
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=0,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    hunters_coil_follow_up,
                    hunters_instinct_follow_up,
                    hunters_venom_follow_up,
                ),
                "No Positional": (
                    hunters_coil_no_pos_follow_up,
                    hunters_instinct_follow_up,
                    hunters_venom_follow_up,
                ),
            },
        )
    )

    swiftskins_venom_follow_up = get_venom_follow_up(
        "Swiftskin's Venom", ("Twinblood Bite",), 30 * 1000
    )
    skill_library.add_skill(
        Skill(
            name="Swiftskin's Coil",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=620),
                "No Positional": DamageSpec(potency=570),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(swift_scaled_follow_up, swiftskins_venom_follow_up),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Vicepit",
            is_GCD=True,
            damage_spec=DamageSpec(potency=220),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
        )
    )

    fellhunters_venom_follow_up = get_venom_follow_up(
        "Fellhunter's Venom", ("Twinfang Thresh",), 30 * 1000
    )
    skill_library.add_skill(
        Skill(
            name="Hunter's Den",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=2),),
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=490,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(hunters_instinct_follow_up, fellhunters_venom_follow_up),
            has_aoe=True,
        )
    )

    fellskins_venom_follow_up = get_venom_follow_up(
        "Fellskin's Venom", ("Twinblood Thresh",), 30 * 1000
    )
    fellskin_damage_followup = FollowUp(
        skill=Skill(name="Swiftskin's Den", damage_spec=DamageSpec(potency=280)),
        delay_after_parent_application=790,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Swiftskin's Den",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=3),),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=0,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(
                fellskin_damage_followup,
                swift_scaled_follow_up,
                fellskins_venom_follow_up,
            ),
            has_aoe=True,
        )
    )

    twinfang_bite_damage_followup = FollowUp(
        skill=Skill(name="Twinfang Bite", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=620,
    )
    twinfang_bite_damage_venom_followup = FollowUp(
        skill=Skill(name="Twinfang Bite", damage_spec=DamageSpec(potency=170)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Twinfang Bite",
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Hunter's Coil",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    twinfang_bite_damage_followup,
                    swiftskins_venom_follow_up,
                ),
                "Hunter's Venom": (
                    twinfang_bite_damage_venom_followup,
                    swiftskins_venom_follow_up,
                ),
                "Hunter's Venom, No Combo": (twinfang_bite_damage_venom_followup,),
                "No Combo": (twinfang_bite_damage_followup,),
            },
        )
    )

    twinblood_damage_follow_up = FollowUp(
        skill=Skill(name="Twinblood Bite", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=670,
    )
    twinblood_damage_venom_follow_up = FollowUp(
        skill=Skill(name="Twinblood Bite", damage_spec=DamageSpec(potency=170)),
        delay_after_parent_application=670,
    )
    skill_library.add_skill(
        Skill(
            name="Twinblood Bite",
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Swiftskin's Coil",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    twinblood_damage_follow_up,
                    hunters_venom_follow_up,
                ),
                "Swiftskin's Venom": (
                    twinblood_damage_venom_follow_up,
                    hunters_venom_follow_up,
                ),
                "No Combo, Swiftskin's Venom": (twinblood_damage_venom_follow_up,),
                "No Combo": (twinblood_damage_follow_up,),
            },
        )
    )

    twinfang_thresh_damage_follow_up = FollowUp(
        skill=Skill(name="Twinfang Thresh", damage_spec=DamageSpec(potency=50)),
        delay_after_parent_application=670,
        primary_target_only=False,
    )
    twinfang_thresh_venom_follow_up = FollowUp(
        skill=Skill(name="Twinfang Thresh", damage_spec=DamageSpec(potency=80)),
        delay_after_parent_application=670,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Twinfang Thresh",
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=2, combo_actions=("Hunter's Den",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    twinfang_thresh_damage_follow_up,
                    fellskins_venom_follow_up,
                ),
                "Fellskin's Venom": (
                    twinfang_thresh_venom_follow_up,
                    fellskins_venom_follow_up,
                ),
                "No Combo, Fellskin's Venom": (twinfang_thresh_venom_follow_up,),
                "No Combo": (twinfang_thresh_damage_follow_up,),
            },
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Twinblood Thresh",
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=3, combo_actions=("Swiftskin's Den",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=50),
                "Fellhunter's Venom": DamageSpec(potency=80),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (fellhunters_venom_follow_up,),
                "No Combo": tuple(),
            },
            has_aoe=True,
        )
    )

    poised_for_twinfang_follow_up = get_venom_follow_up(
        "Poised for Twinfang", ("Uncoiled Twinfang",), 60 * 1000
    )
    uncoiled_fury_follow_up = FollowUp(
        Skill(
            name="Uncoiled Fury", damage_spec=DamageSpec(potency=680), aoe_dropoff=0.5
        ),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Uncoiled Fury",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=0,
                gcd_base_recast_time=3500,
            ),
            follow_up_skills=(
                uncoiled_fury_follow_up,
                poised_for_twinfang_follow_up,
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Reawaken",
            combo_spec=(ComboSpec(combo_group=4),),
            is_GCD=True,
            damage_spec=DamageSpec(potency=750),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=2200,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="First Generation",
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Reawaken",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=680),
                "No Combo": DamageSpec(potency=480),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1700,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Second Generation",
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("First Generation",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=680),
                "No Combo": DamageSpec(potency=480),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1470,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Third Generation",
            combo_spec=(
                ComboSpec(combo_group=4, combo_actions=("Second Generation",)),
            ),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=680),
                "No Combo": DamageSpec(potency=480),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1470,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fourth Generation",
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Third Generation",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=680),
                "No Combo": DamageSpec(potency=480),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1470,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    poised_for_twinblood_follow_up = get_venom_follow_up(
        "Poised for Twinblood", ("Uncoiled Twinblood",), 60 * 1000
    )
    skill_library.add_skill(
        Skill(
            name="Uncoiled Twinfang",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=120),
                "Poised for Twinfang": DamageSpec(potency=170),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(poised_for_twinblood_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Uncoiled Twinblood",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=120),
                "Poised for Twinblood": DamageSpec(potency=170),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=980
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ouroboros",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1150),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=2330,
                gcd_base_recast_time=3000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    skill_library.add_skill(
        Skill(
            name="First Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Second Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Third Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1210
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fourth Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Feint", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Bloodbath", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Slither", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Serpent's Tail", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Twinfang", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Twinblood", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Serpent's Ire", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
