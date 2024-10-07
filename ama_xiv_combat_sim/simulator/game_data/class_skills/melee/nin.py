from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.nin_data import (
    all_nin_skills,
)


def add_nin_skills(skill_library):
    all_nin_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_nin_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()
    mudra_timing_spec = TimingSpec(
        base_cast_time=0,
        gcd_base_recast_time=500,
        affected_by_speed_stat=False,
        affected_by_haste_buffs=False,
        animation_lock=0,
    )

    skill_library.set_current_job_class("NIN")

    if level in [100]:
        skill_library.add_resource(
            name="Kazematoi",
            job_resource_settings=JobResourceSettings(
                max_value=5,
                skill_allowlist=("Aeolian Edge", "Armor Crush"),
                add_number_to_conditional=False,
            ),
        )

    # TODO: this is bugged. We are setting delay_after_parent_application=88 and
    # not snapshotting with parent to mimic the 0.088s snapshot delay on anything
    # bunshin. This in return ignores when the damage actually comes out.
    BUNSHIN_MELEE_POTENCY = all_nin_skills.get_skill_data("Bunshin", "potency_melee")
    BUNSHIN_RANGED_POTENCY = all_nin_skills.get_skill_data("Bunshin", "potency_ranged")
    BUNSHIN_AREA_POTENCY = all_nin_skills.get_skill_data("Bunshin", "potency_area")
    bunshin_follow_ups = [
        ("Spinning Edge", BUNSHIN_MELEE_POTENCY, True),
        ("Gust Slash", BUNSHIN_MELEE_POTENCY, True),
        ("Aeolian Edge", BUNSHIN_MELEE_POTENCY, True),
        ("Armor Crush", BUNSHIN_MELEE_POTENCY, True),
        ("Forked Raiju", BUNSHIN_MELEE_POTENCY, True),
        ("Fleeting Raiju", BUNSHIN_MELEE_POTENCY, True),
        ("Huraijin", BUNSHIN_MELEE_POTENCY, True),
        ("Throwing Dagger", BUNSHIN_RANGED_POTENCY, True),
        ("Hakke Mujinsatsu", BUNSHIN_AREA_POTENCY, False),
        ("Death Blossom", BUNSHIN_AREA_POTENCY, False),
    ]
    all_bunshin_follow_ups = {}
    for sk, bunshin_potency, primary_target_only in bunshin_follow_ups:
        all_bunshin_follow_ups[sk] = FollowUp(
            skill=Skill(
                name=f"{sk} (pet)",
                is_GCD=False,
                damage_spec=DamageSpec(
                    potency=bunshin_potency,
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                ),
                status_effect_denylist=("Dragon Sight",),
            ),
            delay_after_parent_application=88,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=primary_target_only,
        )

    if level in [90]:
        name = "Huton (Huton)"
        _huton_follow_up_huton = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    haste_time_reduction=0.15,
                    auto_attack_delay_reduction=0.15,
                    duration=60 * 1000,
                    max_duration=60 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )

        name = "Huton (Hakke)"
        _huton_follow_up_hakke = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    haste_time_reduction=0.15,
                    auto_attack_delay_reduction=0.15,
                    duration=10 * 1000,
                    max_duration=60 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )

        name = "Huton (Armor Crush)"
        _huton_follow_up_armor_crush = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    haste_time_reduction=0.15,
                    auto_attack_delay_reduction=0.15,
                    duration=30 * 1000,
                    max_duration=60 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )

    name = "Dream Within a Dream"
    _dream_follow_ups = (
        FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=700,
        ),
        FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=850,
        ),
        FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=1000,
        ),
    )

    name = "Doton (dot)"
    doton_dot = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(potency=80, damage_class=DamageClass.PHYSICAL_DOT),
    )
    doton_follow_up = FollowUp(
        skill=doton_dot,
        delay_after_parent_application=0,
        dot_duration=18 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=False,
    )
    doton_dot_hollow_nozuchi = Skill(
        name="Doton hollow nozuchi (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=50, damage_class=DamageClass.PHYSICAL_DOT),
    )
    doton_hollow_nozuchi_follow_up = FollowUp(
        skill=doton_dot_hollow_nozuchi,
        delay_after_parent_application=0,
        dot_duration=18 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=False,
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

    name = "Spinning Edge"
    spinning_edge_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name))
        ),
        delay_after_parent_application=400,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (spinning_edge_follow_up,),
                "Bunshin": (
                    all_bunshin_follow_ups["Spinning Edge"],
                    spinning_edge_follow_up,
                ),
            },
        )
    )

    name = "Gust Slash"
    gust_slash_damage_follow_up = FollowUp(
        Skill(
            name=name, damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name))
        ),
        delay_after_parent_application=400,
    )
    gust_slash_damage_no_combo_follow_up = FollowUp(
        Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=400,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Spinning Edge",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (gust_slash_damage_follow_up,),
                "No Combo": (gust_slash_damage_no_combo_follow_up,),
                "Bunshin": (
                    all_bunshin_follow_ups["Gust Slash"],
                    gust_slash_damage_follow_up,
                ),
                "Bunshin, No Combo": (
                    all_bunshin_follow_ups["Gust Slash"],
                    gust_slash_damage_no_combo_follow_up,
                ),
            },
        )
    )

    name = "Throwing Dagger"
    throwing_dagger_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name))
        ),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (throwing_dagger_follow_up,),
                "Bunshin": (
                    throwing_dagger_follow_up,
                    all_bunshin_follow_ups["Throwing Dagger"],
                ),
            },
        )
    )

    if level in [90]:
        name = "Mug"
        mug_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            ),
            delay_after_parent_application=620,
        )
        mug_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                debuff_spec=StatusEffectSpec(
                    damage_mult=1.05,
                    duration=all_nin_skills.get_skill_data(name, "duration"),
                    is_party_effect=True,
                ),
            ),
            delay_after_parent_application=0,
        )
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=instant_timing_spec,
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        mug_damage_follow_up,
                        mug_debuff_follow_up,
                    ),
                    "Debuff Only": (mug_debuff_follow_up,),
                },
            )
        )

    if level in [90]:
        name = "Trick Attack"
        trick_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            ),
            delay_after_parent_application=800,
        )
        trick_damage_no_pos_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=all_nin_skills.get_potency_no_positional(name)
                ),
            ),
            delay_after_parent_application=800,
        )
        trick_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                debuff_spec=StatusEffectSpec(
                    damage_mult=1.10, duration=int(15.77 * 1000)
                ),
            ),
            delay_after_parent_application=0,
        )
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        trick_damage_follow_up,
                        trick_debuff_follow_up,
                    ),
                    "No Positional": (
                        trick_damage_no_pos_follow_up,
                        trick_debuff_follow_up,
                    ),
                },
                timing_spec=instant_timing_spec,
            )
        )

    name = "Aeolian Edge"
    aeolian_edge_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name))
        ),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_nin_skills.get_potency_no_positional(name)
            ),
        ),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_nin_skills.get_skill_data(name, "potency_no_pos_no_combo")
            ),
        ),
        delay_after_parent_application=540,
    )
    if level in [100]:
        potency_increment_kaz = all_nin_skills.get_skill_data(
            name, "potency_increment_kaz"
        )
        # kaz. this is ugly, we can do better.
        aeolian_edge_follow_up_kaz = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    all_nin_skills.get_potency(name) + potency_increment_kaz
                ),
            ),
            delay_after_parent_application=540,
        )
        aeolian_edge_no_combo_follow_up_kaz = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    all_nin_skills.get_potency_no_combo(name) + potency_increment_kaz
                ),
            ),
            delay_after_parent_application=540,
        )
        aeolian_edge_no_pos_follow_up_kaz = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    all_nin_skills.get_potency_no_positional(name)
                    + potency_increment_kaz
                ),
            ),
            delay_after_parent_application=540,
        )
        aeolian_edge_no_pos_no_combo_follow_up_kaz = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    all_nin_skills.get_skill_data(name, "potency_no_pos_no_combo")
                    + potency_increment_kaz
                ),
            ),
            delay_after_parent_application=540,
        )
    aoelian_follow_ups = {
        SimConsts.DEFAULT_CONDITION: (aeolian_edge_follow_up,),
        "No Combo": (aeolian_edge_no_combo_follow_up,),
        "No Positional": (aeolian_edge_no_pos_follow_up,),
        "No Combo, No Positional": (aeolian_edge_no_pos_no_combo_follow_up,),
        "Bunshin": (
            aeolian_edge_follow_up,
            all_bunshin_follow_ups["Aeolian Edge"],
        ),
        "Bunshin, No Combo": (
            aeolian_edge_no_combo_follow_up,
            all_bunshin_follow_ups["Aeolian Edge"],
        ),
        "Bunshin, No Positional": (
            aeolian_edge_no_pos_follow_up,
            all_bunshin_follow_ups["Aeolian Edge"],
        ),
        "Bunshin, No Combo, No Positional": (
            aeolian_edge_no_pos_no_combo_follow_up,
            all_bunshin_follow_ups["Aeolian Edge"],
        ),
    }
    if level in [100]:
        aoelian_follow_ups_100_only = {
            "Kazematoi": (aeolian_edge_follow_up_kaz,),
            "Kazematoi, No Combo": (aeolian_edge_no_combo_follow_up_kaz,),
            "Kazematoi, No Positional": (aeolian_edge_no_pos_follow_up_kaz,),
            "Kazematoi, No Combo, No Positional": (
                aeolian_edge_no_pos_no_combo_follow_up_kaz,
            ),
            "Bunshin, Kazematoi": (
                aeolian_edge_follow_up_kaz,
                all_bunshin_follow_ups["Aeolian Edge"],
            ),
            "Bunshin, Kazematoi, No Combo": (
                aeolian_edge_no_combo_follow_up_kaz,
                all_bunshin_follow_ups["Aeolian Edge"],
            ),
            "Bunshin, Kazematoi, No Positional": (
                aeolian_edge_no_pos_follow_up_kaz,
                all_bunshin_follow_ups["Aeolian Edge"],
            ),
            "Bunshin, Kazematoi, No Combo, No Positional": (
                aeolian_edge_no_pos_no_combo_follow_up_kaz,
                all_bunshin_follow_ups["Aeolian Edge"],
            ),
        }
        aoelian_follow_ups = aoelian_follow_ups | aoelian_follow_ups_100_only
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            job_resource_spec=(
                tuple()
                if level in [90]
                else (JobResourceSpec(name="Kazematoi", change=-1),)
            ),
            follow_up_skills=aoelian_follow_ups,
        )
    )

    name = "Death Blossom"
    death_blossom_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=710,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (death_blossom_follow_up,),
                "Bunshin": (
                    death_blossom_follow_up,
                    all_bunshin_follow_ups["Death Blossom"],
                ),
            },
            has_aoe=True,
        )
    )

    name = "Hakke Mujinsatsu"
    hakke_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    hakke_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency_no_combo(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Death Blossom",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    (_huton_follow_up_hakke, hakke_follow_up)
                    if level in [90]
                    else (hakke_follow_up,)
                ),
                "No Combo": (hakke_no_combo_follow_up,),
                "Bunshin": (
                    (
                        _huton_follow_up_hakke,
                        all_bunshin_follow_ups["Hakke Mujinsatsu"],
                        hakke_follow_up,
                    )
                    if level in [90]
                    else (
                        all_bunshin_follow_ups["Hakke Mujinsatsu"],
                        hakke_follow_up,
                    )
                ),
                "Bunshin, No Combo": (
                    all_bunshin_follow_ups["Hakke Mujinsatsu"],
                    hakke_no_combo_follow_up,
                ),
            },
            has_aoe=True,
        )
    )

    name = "Armor Crush"
    armor_crush_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name))
        ),
        delay_after_parent_application=620,
    )
    armor_crush_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=620,
    )
    armor_crush_no_pos_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_nin_skills.get_potency_no_positional(name)
            ),
        ),
        delay_after_parent_application=620,
    )
    armor_crush_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_nin_skills.get_skill_data(name, "potency_no_pos_no_combo")
            ),
        ),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            job_resource_spec=all_nin_skills.get_skill_data(name, "job_resource"),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    (
                        armor_crush_follow_up,
                        _huton_follow_up_armor_crush,
                    )
                    if level in [90]
                    else (armor_crush_follow_up,)
                ),
                "No Combo": (armor_crush_no_combo_follow_up,),
                "No Positional": (
                    (
                        armor_crush_no_pos_follow_up,
                        _huton_follow_up_armor_crush,
                    )
                    if level in [90]
                    else (armor_crush_no_pos_follow_up,)
                ),
                "No Combo, No Positional": (armor_crush_no_pos_no_combo_follow_up,),
                "Bunshin": (
                    (
                        armor_crush_follow_up,
                        _huton_follow_up_armor_crush,
                        all_bunshin_follow_ups["Armor Crush"],
                    )
                    if level in [90]
                    else (
                        armor_crush_follow_up,
                        all_bunshin_follow_ups["Armor Crush"],
                    )
                ),
                "Bunshin, No Combo": (
                    armor_crush_no_combo_follow_up,
                    all_bunshin_follow_ups["Armor Crush"],
                ),
                "Bunshin, No Positional": (
                    (
                        armor_crush_no_pos_follow_up,
                        _huton_follow_up_armor_crush,
                        all_bunshin_follow_ups["Armor Crush"],
                    )
                    if level in [90]
                    else (
                        armor_crush_no_pos_follow_up,
                        all_bunshin_follow_ups["Armor Crush"],
                    )
                ),
                "Bunshin, No Combo, No Positional": (
                    armor_crush_no_pos_no_combo_follow_up,
                    all_bunshin_follow_ups["Armor Crush"],
                ),
            },
        )
    )

    name = "Dream Within a Dream"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=_dream_follow_ups,
        )
    )

    if level in [100]:
        name = "Dokumori"
        dokumori_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                debuff_spec=StatusEffectSpec(
                    damage_mult=1.05,
                    duration=all_nin_skills.get_skill_data(name, "duration"),
                    is_party_effect=True,
                ),
            ),
            delay_after_parent_application=0,
        )
        dokumori_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            ),
            delay_after_parent_application=1070,
        )
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        dokumori_damage_follow_up,
                        dokumori_debuff_follow_up,
                    ),
                    "Debuff Only": (dokumori_debuff_follow_up,),
                },
            )
        )

    if level in [90]:
        name = "Huraijin"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=800
                ),
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (_huton_follow_up_huton,),
                    "Bunshin": (
                        _huton_follow_up_huton,
                        all_bunshin_follow_ups["Huraijin"],
                    ),
                },
            )
        )

    name = "Hellfrog Medium"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            has_aoe=True,
        )
    )

    name = "Bhavacakra"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_nin_skills.get_potency(name)
                ),
                "Meisui": DamageSpec(
                    potency=all_nin_skills.get_skill_data(name, "potency_mesui")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Phantom Kamaitachi (pet)"
    phantom_follow_up_damage = FollowUp(
        skill=Skill(
            name=name,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_nin_skills.get_potency(name),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        ),
        delay_after_parent_application=1560,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
        primary_target_only=False,
    )
    name = "Phantom Kamaitachi"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(base_cast_time=0),
            status_effect_denylist=("Dragon Sight",),
            follow_up_skills=(phantom_follow_up_damage,),
        )
    )

    # TODO: fix. gcds only will proc it, like bunshin. Ty An.
    name = "Hollow Nozuchi"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=270
            ),
            follow_up_skills=(doton_hollow_nozuchi_follow_up,),
        )
    )

    name = "Forked Raiju"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (all_bunshin_follow_ups["Forked Raiju"],),
            },
        )
    )

    name = "Fleeting Raiju"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (all_bunshin_follow_ups["Fleeting Raiju"],),
            },
        )
    )

    name = "Fuma Shuriken"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=890,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=890,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )

    name = "Katon"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=940,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=940,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )

    name = "Raiton"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=710,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=710,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )

    name = "Hyoton"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=1160,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=1160,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )

    name = "Huton"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=all_nin_skills.get_skill_data(name, "damage_spec"),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=0,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=0,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
            follow_up_skills=(_huton_follow_up_huton,) if level in [90] else tuple(),
        )
    )

    name = "Doton"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=1300,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=1300,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
            follow_up_skills=(doton_follow_up,),
        )
    )

    name = "Suiton"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    #  application_delay=0,
                    application_delay=980,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=980,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )
    )

    name = "Goka Mekkyaku"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=760,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )

    name = "Hyosho Ranryu"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=620,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )

    name = "Bunshin"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=5,
                duration=int(30.7 * 1000),
                skill_allowlist=all_nin_skills.get_skill_data(name, "allowlist"),
            ),
        )
    )

    name = "Ten Chi Jin"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=3,
                duration=6 * 1000,
                skill_allowlist=(
                    "Fuma Shuriken",
                    "Katon",
                    "Raiton",
                    "Hyoton",
                    "Huton",
                    "Doton",
                    "Suiton",
                ),
            ),
        )
    )

    name = "Meisui"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=all_nin_skills.get_skill_data(name, "allowlist"),
            ),
        )
    )

    if level in [100]:
        name = "Kunai's Bane"
        kunai_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
                has_aoe=True,
            ),
            delay_after_parent_application=1290,
            primary_target_only=False,
        )
        kunai_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                debuff_spec=StatusEffectSpec(
                    damage_mult=1.10,
                    duration=all_nin_skills.get_skill_data(name, "duration"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=False,
        )
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                follow_up_skills=(kunai_damage_follow_up, kunai_debuff_follow_up),
                has_aoe=True,
            )
        )

    if level in [100]:
        name = "Deathfrog Medium"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=800
                ),
            )
        )

    if level in [100]:
        name = "Zesho Meppo"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_nin_skills.get_potency(name)
                    ),
                    "Meisui": DamageSpec(
                        potency=all_nin_skills.get_skill_data(name, "potency_mesui")
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1030
                ),
            )
        )

    if level in [100]:
        name = "Tenri Jindo"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_nin_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1690
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    name = "Kassatsu"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=15 * 1000,
                damage_mult=1.3,
                skill_allowlist=(
                    "Fuma Shuriken",
                    "Raiton",
                    "Doton",
                    "Suiton",
                    "Goka Mekkyaku",
                    "Huton",
                    "Hyosho Ranryu",
                ),
            ),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Ten", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Chi", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Jin", is_GCD=True, timing_spec=mudra_timing_spec)
    )

    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Hide", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
