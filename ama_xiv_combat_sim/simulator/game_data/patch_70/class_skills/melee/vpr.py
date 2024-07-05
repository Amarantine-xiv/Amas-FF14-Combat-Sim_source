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
    COMBO_BASE_POTENCY_NO_VENOM = 120
    COMBO_BASE_POTENCY_WITH_VENOM = 220

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
            name="Steel Fangs",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    hunters_instinct_follow_up = FollowUp(
        skill=Skill(
            name="Hunter's Sting",
            buff_spec=StatusEffectSpec(damage_mult=1.10, duration=40 * 1000),
        ),
        delay_after_parent_application=0,
    )
    skill_library.add_skill(
        Skill(
            name="Hunter's Sting",
            is_GCD=True,
            damage_spec=DamageSpec(potency=260),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(hunters_instinct_follow_up,),
        )
    )
    noxious_gnash_follow_up = FollowUp(
        skill=Skill(
            name="Noxious Gnash",
            debuff_spec=StatusEffectSpec(
                damage_mult=1.10, duration=20 * 1000, max_duration=40 * 1000
            ),
        ),
        delay_after_parent_application=0,
    )
    skill_library.add_skill(
        Skill(
            name="Dread Fangs",
            is_GCD=True,
            damage_spec=DamageSpec(potency=140),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(noxious_gnash_follow_up,),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Writhing Snap",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=instant_timing_spec,
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
    )

    skill_library.add_skill(
        Skill(
            name="Swiftskin's Sting",
            is_GCD=True,
            damage_spec=DamageSpec(potency=260),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(swift_scaled_follow_up,),
        )
    )

    skill_library.add_skill(
        Skill(name="Steel Maw", is_GCD=True, damage_spec=DamageSpec(potency=100))
    )
    hindstung_venom_follow_up = get_venom_follow_up(
        "Hindstung Venom",
        ("Hindsting Strike",),
        40 * 1000,
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
                    potency=360, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=300, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Flankstung Venom": DamageSpec(
                    potency=460, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Flankstung Venom, No Positional": DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(hindstung_venom_follow_up,),
        )
    )

    hindsbane_venom_follow_up = get_venom_follow_up(
        "Hindsbane Venom",
        ("Hindsbane Fang",),
        40 * 1000,
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
                    potency=360, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=300, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Flanksbane Venom": DamageSpec(
                    potency=460, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Flanksbane Venom, No Positional": DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(hindsbane_venom_follow_up,),
        )
    )

    flanksbane_venom_follow_up = get_venom_follow_up(
        "Flanksbane Venom",
        ("Flanksbane Fang",),
        40 * 1000,
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
                    potency=360, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=300, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Hindstung Venom": DamageSpec(
                    potency=460, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Hindstung Venom, No Positional": DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(flanksbane_venom_follow_up,),
        )
    )

    flankstung_venom_follow_up = get_venom_follow_up(
        "Flankstung Venom",
        ("Flanksting Strike",),
        40 * 1000,
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
                    potency=360, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "No Positional": DamageSpec(
                    potency=300, use_min_potency=COMBO_BASE_POTENCY_NO_VENOM
                ),
                "Hindsbane Venom": DamageSpec(
                    potency=460, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
                ),
                "Hindsbane Venom, No Positional": DamageSpec(
                    potency=400, use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM
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
            name="Dread Maw",
            is_GCD=True,
            damage_spec=DamageSpec(potency=80),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(noxious_gnash_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hunter's Bite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(hunters_instinct_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Swiftskin's Bite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(swift_scaled_follow_up,),
        )
    )

    grimskins_venom_follow_up = get_venom_follow_up(
        "Grimskin's Venom",
        ("Bloodied Maw",),
        40 * 1000,
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
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(grimskins_venom_follow_up,),
        )
    )
    grimhunters_venom_follow_up = get_venom_follow_up(
        "Grimhunter's Venom",
        ("Jagged Maw",),
        40 * 1000,
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
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(grimhunters_venom_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Death Rattle",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Last Lash",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Dreadwinder",
            is_GCD=True,
            damage_spec=DamageSpec(potency=450),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(noxious_gnash_follow_up,),
        )
    )

    hunters_venom_follow_up = get_venom_follow_up(
        "Hunter's Venom", ("Twinfang Bite",), 30 * 1000
    )
    skill_library.add_skill(
        Skill(
            name="Hunter's Coil",
            combo_spec=(ComboSpec(combo_group=0),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=550),
                "No Positional": DamageSpec(potency=500),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(hunters_instinct_follow_up, hunters_venom_follow_up),
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
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=550),
                "No Positional": DamageSpec(potency=500),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(swift_scaled_follow_up, swiftskins_venom_follow_up),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Pit of Dread",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(noxious_gnash_follow_up,),
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
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(hunters_instinct_follow_up, fellhunters_venom_follow_up),
        )
    )

    fellskins_venom_follow_up = get_venom_follow_up(
        "Fellskin's Venom", ("Twinblood Thresh",), 30 * 1000
    )
    skill_library.add_skill(
        Skill(
            name="Swiftskin's Den",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=3),),
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(swift_scaled_follow_up, fellskins_venom_follow_up),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Twinfang Bite",
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Hunter's Coil",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "Hunter's Venom": DamageSpec(potency=150),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (swiftskins_venom_follow_up,),
                "No Combo": tuple(),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Twinblood Bite",
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Swiftskin's Coil",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "Swiftskin's Venom": DamageSpec(potency=150),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (hunters_venom_follow_up,),
                "No Combo": tuple(),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Twinfang Thresh",
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=2, combo_actions=("Hunter's Den",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=50),
                "Fellskin's Venom": DamageSpec(potency=80),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (fellskins_venom_follow_up,),
                "No Combo": tuple(),
            },
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
        )
    )

    poised_for_twinfang_follow_up = get_venom_follow_up(
        "Poised for Twinfang", ("Uncoiled Twinfang",), 60 * 1000
    )
    skill_library.add_skill(
        Skill(
            name="Uncoiled Fury",
            is_GCD=True,
            damage_spec=DamageSpec(potency=600),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=0,
                gcd_base_recast_time=3500,
            ),
            follow_up_skills=(poised_for_twinfang_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Reawaken",
            combo_spec=(ComboSpec(combo_group=4),),
            is_GCD=True,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=2200,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="First Generation",
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Reawaken",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "No Combo": DamageSpec(potency=400),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=2000,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Second Generation",
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("First Generation",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "No Combo": DamageSpec(potency=400),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=2000,
            ),
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
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "No Combo": DamageSpec(potency=400),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=2000,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fourth Generation",
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Third Generation",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "No Combo": DamageSpec(potency=400),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=2000,
            ),
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
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "Poised for Twinfang": DamageSpec(potency=150),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
            ),
            follow_up_skills=(poised_for_twinblood_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Uncoiled Twinblood",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "Poised for Twinblood": DamageSpec(potency=150),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ouroboros",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1050),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=3000,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="First Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Second Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Third Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fourth Legacy",
            is_GCD=False,
            damage_spec=DamageSpec(potency=250),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
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
