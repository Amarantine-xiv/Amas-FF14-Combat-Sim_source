from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
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

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.vpr_data import (
    all_vpr_skills,
)


def add_vpr_skills(skill_library):
    level = skill_library.get_level()
    version = skill_library.get_version()
    if level not in [100]:
        return skill_library

    all_vpr_skills.set_level(level)
    all_vpr_skills.set_version(version)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    # these are based off of pre-trait dread fang. IDK man, idk.
    COMBO_BASE_POTENCY_NO_VENOM = all_vpr_skills.get_skill_data(
        "Combo Base", "potency_no_venom"
    )
    COMBO_BASE_POTENCY_WITH_VENOM = all_vpr_skills.get_skill_data(
        "Combo Base", "potency_venom"
    )

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

    if version not in ["7.0", "7.01"]:
        name = "Honed Reavers"
        honed_reavers_follow_up = FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=60 * 1000,
                    num_uses=1,
                    skill_allowlist=("Reaving Fangs", "Reaving Maw"),
                    expires_status_effects=("Honed Steel",),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    name = "Steel Fangs"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=all_vpr_skills.get_skill_data(name, "damage_spec"),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            follow_up_skills=(
                tuple() if version in ["7.0", "7.01"] else (honed_reavers_follow_up,)
            ),
        )
    )

    name = "Hunter's Instinct"
    hunters_instinct_follow_up = FollowUp(
        skill=Skill(
            name=name,
            buff_spec=StatusEffectSpec(
                damage_mult=1.10,
                duration=all_vpr_skills.get_skill_data(name, "duration"),
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )

    name = "Hunter's Sting"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
            follow_up_skills=(hunters_instinct_follow_up,),
        )
    )

    if version in ["7.0", "7.01"]:
        name = "Noxious Gnash"
        noxious_gnash_follow_up = FollowUp(
            skill=Skill(
                name=name,
                debuff_spec=StatusEffectSpec(
                    damage_mult=1.10,
                    duration=all_vpr_skills.get_skill_data(name, "duration"),
                    max_duration=all_vpr_skills.get_skill_data(name, "max_duration"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    if version not in ["7.0", "7.01"]:
        name = "Honed Steel"
        honed_steel_follow_up = FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=60 * 1000,
                    num_uses=1,
                    skill_allowlist=("Steel Fangs", "Steel Maw"),
                    expires_status_effects=("Honed Reavers",),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    if version in ["7.0", "7.01"]:
        name = "Dread Fangs"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
                follow_up_skills=(noxious_gnash_follow_up,),
            )
        )

    if version not in ["7.0", "7.01"]:
        name = "Reaving Fangs"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_vpr_skills.get_potency(name)
                    ),
                    "Honed Reavers": DamageSpec(
                        potency=all_vpr_skills.get_skill_data(
                            name, "potency_honed_reavers"
                        )
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
                follow_up_skills=(honed_steel_follow_up,),
            )
        )

    name = "Writhing Snap"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )

    name = "Swiftscaled"
    swift_scaled_follow_up = FollowUp(
        skill=Skill(
            name=name,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.15,
                auto_attack_delay_reduction=0.15,
                duration=all_vpr_skills.get_skill_data(name, "duration"),
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )

    name = "Swiftskin's Sting"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            follow_up_skills=(swift_scaled_follow_up,),
        )
    )

    name = "Steel Maw"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1020
            ),
            damage_spec=all_vpr_skills.get_skill_data(name, "damage_spec"),
            has_aoe=True,
        )
    )

    name = "Hindstung Venom"
    hindstung_venom_follow_up = get_venom_follow_up(
        name,
        ("Hindsting Strike",),
        all_vpr_skills.get_skill_data(name, "duration"),
        (
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )

    name = "Flanksting Strike"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "No Positional": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_positional(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "Flankstung Venom": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
                ),
                "Flankstung Venom, No Positional": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_no_pos_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
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

    name = "Hindsbane Venom"
    hindsbane_venom_follow_up = get_venom_follow_up(
        name,
        ("Hindsbane Fang",),
        all_vpr_skills.get_skill_data(name, "duration"),
        (
            "Hindstung Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )
    name = "Flanksbane Fang"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "No Positional": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_positional(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "Flanksbane Venom": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
                ),
                "Flanksbane Venom, No Positional": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_no_pos_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
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

    name = "Flanksbane Venom"
    flanksbane_venom_follow_up = get_venom_follow_up(
        name,
        ("Flanksbane Fang",),
        all_vpr_skills.get_skill_data(name, "duration"),
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )

    name = "Hindsting Strike"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "No Positional": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_positional(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "Hindstung Venom": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
                ),
                "Hindstung Venom, No Positional": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_no_pos_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
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

    name = "Flankstung Venom"
    flankstung_venom_follow_up = get_venom_follow_up(
        name,
        ("Flanksting Strike",),
        all_vpr_skills.get_skill_data(name, "duration"),
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Grimskin's Venom",
            "Grimhunter's Venom",
        ),
    )

    name = "Hindsbane Fang"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "No Positional": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_positional(name),
                    use_min_potency=COMBO_BASE_POTENCY_NO_VENOM,
                ),
                "Hindsbane Venom": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
                ),
                "Hindsbane Venom, No Positional": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_no_pos_venom"),
                    use_min_potency=COMBO_BASE_POTENCY_WITH_VENOM,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(flankstung_venom_follow_up,),
        )
    )

    if version in ["7.0", "7.01"]:
        name = "Dread Maw"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=620
                ),
                follow_up_skills=(noxious_gnash_follow_up,),
                has_aoe=True,
            )
        )
    if version not in ["7.0", "7.01"]:
        name = "Reaving Maw"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_vpr_skills.get_potency(name)
                    ),
                    "Honed Reavers": DamageSpec(
                        potency=all_vpr_skills.get_skill_data(
                            name, "potency_honed_reavers"
                        )
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=620
                ),
                follow_up_skills=(honed_steel_follow_up,),
                has_aoe=True,
            )
        )

    name = "Hunter's Bite"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            follow_up_skills=(hunters_instinct_follow_up,),
            has_aoe=True,
        )
    )

    name = "Swiftskin's Bite"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1380
            ),
            follow_up_skills=(swift_scaled_follow_up,),
            has_aoe=True,
        )
    )

    name = "Grimskin's Venom"
    grimskins_venom_follow_up = get_venom_follow_up(
        name,
        ("Bloodied Maw",),
        all_vpr_skills.get_skill_data(name, "duration"),
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimhunter's Venom",
        ),
    )

    name = "Jagged Maw"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "Grimhunter's Venom": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_venom")
                ),
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

    name = "Grimhunter's Venom"
    grimhunters_venom_follow_up = get_venom_follow_up(
        name,
        ("Jagged Maw",),
        all_vpr_skills.get_skill_data(name, "duration"),
        (
            "Hindstung Venom",
            "Hindsbane Venom",
            "Flanksbane Venom",
            "Flankstung Venom",
            "Grimskin's Venom",
        ),
    )

    name = "Bloodied Maw"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "Grimskin's Venom": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_venom")
                ),
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

    name = "Death Rattle"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1700
            ),
        )
    )

    name = "Last Lash"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
        )
    )

    if version in ["7.0", "7.01"]:
        name = "Dreadwinder"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=580,
                    gcd_base_recast_time=3000,
                ),
                follow_up_skills=(noxious_gnash_follow_up,),
            )
        )
    if version not in ["7.0", "7.01"]:
        name = "Vicewinder"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=580,
                    gcd_base_recast_time=3000,
                ),
            )
        )

    name = "Hunter's Venom"
    hunters_venom_follow_up = get_venom_follow_up(
        name, ("Twinfang Bite",), all_vpr_skills.get_skill_data(name, "duration")
    )

    name = "Hunter's Coil"
    hunters_coil_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name))
        ),
        delay_after_parent_application=980,
    )
    name = "Hunter's Coil"
    hunters_coil_no_pos_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_vpr_skills.get_potency_no_positional(name)
            ),
        ),
        delay_after_parent_application=980,
    )
    name = "Hunter's Coil"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Swiftskin's Venom"
    swiftskins_venom_follow_up = get_venom_follow_up(
        name, ("Twinblood Bite",), all_vpr_skills.get_skill_data(name, "duration")
    )

    name = "Swiftskin's Coil"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_positional(name)
                ),
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

    if version in ["7.0", "7.01"]:
        name = "Pit of Dread"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=760
                ),
                follow_up_skills=(noxious_gnash_follow_up,),
                has_aoe=True,
            )
        )

    if version not in ["7.0", "7.01"]:
        skill_library.add_skill(
            Skill(
                name="Vicepit",
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=760
                ),
                has_aoe=True,
            )
        )

    name = "Fellhunter's Venom"
    fellhunters_venom_follow_up = get_venom_follow_up(
        name, ("Twinfang Thresh",), all_vpr_skills.get_skill_data(name, "duration")
    )

    name = "Hunter's Den"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=2),),
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
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

    name = "Fellskin's Venom"
    fellskins_venom_follow_up = get_venom_follow_up(
        name, ("Twinblood Thresh",), all_vpr_skills.get_skill_data(name, "duration")
    )

    name = "Swiftskin's Den"
    fellskin_damage_followup = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name))
        ),
        delay_after_parent_application=790,
        primary_target_only=False,
    )
    name = "Swiftskin's Den"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Twinfang Bite"
    twinfang_bite_damage_followup = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name))
        ),
        delay_after_parent_application=620,
    )
    name = "Twinfang Bite"
    twinfang_bite_damage_venom_followup = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_vpr_skills.get_skill_data(name, "potency_venom")
            ),
        ),
        delay_after_parent_application=620,
    )
    name = "Twinfang Bite"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Twinblood Bite"
    twinblood_damage_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name))
        ),
        delay_after_parent_application=670,
    )
    name = "Twinblood Bite"
    twinblood_damage_venom_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_vpr_skills.get_skill_data(name, "potency_venom")
            ),
        ),
        delay_after_parent_application=670,
    )
    name = "Twinblood Bite"
    skill_library.add_skill(
        Skill(
            name=name,
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

    name = "Twinfang Thresh"
    twinfang_thresh_damage_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name))
        ),
        delay_after_parent_application=670,
        primary_target_only=False,
    )
    name = "Twinfang Thresh"
    twinfang_thresh_venom_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_vpr_skills.get_skill_data(name, "potency_venom")
            ),
        ),
        delay_after_parent_application=670,
        primary_target_only=False,
    )
    name = "Twinfang Thresh"
    skill_library.add_skill(
        Skill(
            name=name,
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
    name = "Twinblood Thresh"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            combo_spec=(ComboSpec(combo_group=3, combo_actions=("Swiftskin's Den",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "Fellhunter's Venom": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_venom")
                ),
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

    name = "Poised for Twinfang"
    poised_for_twinfang_follow_up = get_venom_follow_up(
        name, ("Uncoiled Twinfang",), all_vpr_skills.get_skill_data(name, "duration")
    )

    name = "Uncoiled Fury"
    uncoiled_fury_follow_up = FollowUp(
        Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            aoe_dropoff=0.5,
        ),
        delay_after_parent_application=800,
        primary_target_only=False,
    )
    name = "Uncoiled Fury"
    skill_library.add_skill(
        Skill(
            name=name,
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
    name = "Reawaken"
    skill_library.add_skill(
        Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4),),
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
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

    name = "First Generation"
    skill_library.add_skill(
        Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Reawaken",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_combo(name)
                ),
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

    name = "Second Generation"
    skill_library.add_skill(
        Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("First Generation",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_combo(name)
                ),
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

    name = "Third Generation"
    skill_library.add_skill(
        Skill(
            name=name,
            combo_spec=(
                ComboSpec(combo_group=4, combo_actions=("Second Generation",)),
            ),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_combo(name)
                ),
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

    name = "Fourth Generation"
    skill_library.add_skill(
        Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Third Generation",)),),
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_vpr_skills.get_potency_no_combo(name)
                ),
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

    name = "Poised for Twinblood"
    poised_for_twinblood_follow_up = get_venom_follow_up(
        name, ("Uncoiled Twinblood",), all_vpr_skills.get_skill_data(name, "duration")
    )

    name = "Uncoiled Twinfang"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "Poised for Twinfang": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_poised")
                ),
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

    name = "Uncoiled Twinblood"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_vpr_skills.get_potency(name)
                ),
                "Poised for Twinblood": DamageSpec(
                    potency=all_vpr_skills.get_skill_data(name, "potency_poised")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=980
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Ouroboros"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
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

    name = "First Legacy"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Second Legacy"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Third Legacy"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1210
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Fourth Legacy"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_vpr_skills.get_potency(name)),
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
