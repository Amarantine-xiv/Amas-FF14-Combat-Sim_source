from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
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


def add_nin_skills(skill_library):
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
    BUNSHIN_MELEE_POTENCY = 160
    BUNSHIN_RANGED_POTENCY = 160
    BUNSHIN_AREA_POTENCY = 80
    bunshin_follow_ups = [
        ("Spinning Edge", BUNSHIN_MELEE_POTENCY, True),
        ("Gust Slash", BUNSHIN_MELEE_POTENCY, True),
        ("Aeolian Edge", BUNSHIN_MELEE_POTENCY, True),
        ("Armor Crush", BUNSHIN_MELEE_POTENCY, True),
        ("Forked Raiju", BUNSHIN_MELEE_POTENCY, True),
        ("Fleeting Raiju", BUNSHIN_MELEE_POTENCY, True),
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
            ),
            delay_after_parent_application=88,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=primary_target_only,
        )

    _dream_follow_ups = (
        FollowUp(
            skill=Skill(
                name="Dream Within a Dream",
                is_GCD=False,
                damage_spec=DamageSpec(150),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=700,
        ),
        FollowUp(
            skill=Skill(
                name="Dream Within a Dream",
                is_GCD=False,
                damage_spec=DamageSpec(150),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=850,
        ),
        FollowUp(
            skill=Skill(
                name="Dream Within a Dream",
                is_GCD=False,
                damage_spec=DamageSpec(150),
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=1000,
        ),
    )

    doton_dot = Skill(
        name="Doton (dot)",
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

    spinning_edge_damage = Skill(
        name="Spinning Edge", damage_spec=DamageSpec(potency=300)
    )
    spinning_edge_follow_up = FollowUp(
        skill=spinning_edge_damage, delay_after_parent_application=400
    )
    skill_library.add_skill(
        Skill(
            name="Spinning Edge",
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

    gust_slash_damage_follow_up = FollowUp(
        Skill(name="Gust Slash", damage_spec=DamageSpec(potency=400)),
        delay_after_parent_application=400,
    )
    gust_slash_damage_no_combo_follow_up = FollowUp(
        Skill(name="Gust Slash", damage_spec=DamageSpec(potency=240)),
        delay_after_parent_application=400,
    )
    skill_library.add_skill(
        Skill(
            name="Gust Slash",
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

    throwing_dagger_follow_up = FollowUp(
        skill=Skill(name="Throwing Dagger", damage_spec=DamageSpec(potency=120)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Throwing Dagger",
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

    aeolian_edge_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(440)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_combo_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(260)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(380)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(200)),
        delay_after_parent_application=540,
    )
    # kaz. this is ugly, we can do better.
    aeolian_edge_follow_up_kaz = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(440 + 100)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_combo_follow_up_kaz = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(260 + 100)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_follow_up_kaz = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(380 + 100)),
        delay_after_parent_application=540,
    )
    aeolian_edge_no_pos_no_combo_follow_up_kaz = FollowUp(
        skill=Skill(name="Aeolian Edge", damage_spec=DamageSpec(200 + 100)),
        delay_after_parent_application=540,
    )

    skill_library.add_skill(
        Skill(
            name="Aeolian Edge",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            job_resource_spec=(JobResourceSpec(name="Kazematoi", change=-1),),
            follow_up_skills={
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
                #
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
            },
        )
    )

    skill_library.add_skill(
        Skill(name="Ten", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Chi", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Jin", is_GCD=True, timing_spec=mudra_timing_spec)
    )
    death_blossom_follow_up = FollowUp(
        skill=Skill(name="Death Blossom", damage_spec=DamageSpec(100), has_aoe=True),
        delay_after_parent_application=710,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Death Blossom",
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

    hakke_follow_up = FollowUp(
        skill=Skill(name="Hakke Mujinsatsu", damage_spec=DamageSpec(130), has_aoe=True),
        delay_after_parent_application=620,
        primary_target_only=False,
    )
    hakke_no_combo_follow_up = FollowUp(
        skill=Skill(name="Hakke Mujinsatsu", damage_spec=DamageSpec(100), has_aoe=True),
        delay_after_parent_application=620,
        primary_target_only=False,
    )

    skill_library.add_skill(
        Skill(
            name="Hakke Mujinsatsu",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Death Blossom",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (hakke_follow_up,),
                "No Combo": (hakke_no_combo_follow_up,),
                "Bunshin": (
                    all_bunshin_follow_ups["Hakke Mujinsatsu"],
                    hakke_follow_up,
                ),
                "Bunshin, No Combo": (
                    all_bunshin_follow_ups["Hakke Mujinsatsu"],
                    hakke_no_combo_follow_up,
                ),
            },
            has_aoe=True,
        )
    )

    armor_crush_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(480)),
        delay_after_parent_application=620,
    )
    armor_crush_no_combo_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(280)),
        delay_after_parent_application=620,
    )
    armor_crush_no_pos_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(420)),
        delay_after_parent_application=620,
    )
    armor_crush_no_pos_no_combo_follow_up = FollowUp(
        skill=Skill(name="Armor Crush", damage_spec=DamageSpec(220)),
        delay_after_parent_application=620,
    )
    skill_library.add_skill(
        Skill(
            name="Armor Crush",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            job_resource_spec=(JobResourceSpec(name="Kazematoi", change=2),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (armor_crush_follow_up,),
                "No Combo": (armor_crush_no_combo_follow_up,),
                "No Positional": (armor_crush_no_pos_follow_up,),
                "No Combo, No Positional": (armor_crush_no_pos_no_combo_follow_up,),
                "Bunshin": (
                    armor_crush_follow_up,
                    all_bunshin_follow_ups["Armor Crush"],
                ),
                "Bunshin, No Combo": (
                    armor_crush_no_combo_follow_up,
                    all_bunshin_follow_ups["Armor Crush"],
                ),
                "Bunshin, No Positional": (
                    armor_crush_no_pos_follow_up,
                    all_bunshin_follow_ups["Armor Crush"],
                ),
                "Bunshin, No Combo, No Positional": (
                    armor_crush_no_pos_no_combo_follow_up,
                    all_bunshin_follow_ups["Armor Crush"],
                ),
            },
        )
    )

    skill_library.add_skill(
        Skill(
            name="Dream Within a Dream",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=_dream_follow_ups,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Hellfrog Medium",
            is_GCD=False,
            damage_spec=DamageSpec(potency=160),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            has_aoe=True,
        )
    )

    dokumori_debuff_follow_up = FollowUp(
        skill=Skill(
            name="Dokumori",
            debuff_spec=StatusEffectSpec(
                damage_mult=1.05, duration=int(21.02 * 1000), is_party_effect=True
            ),
        ),
        delay_after_parent_application=0,
    )
    dokumori_damage_follow_up = FollowUp(
        skill=Skill("Dokumori", damage_spec=DamageSpec(potency=300)),
        delay_after_parent_application=1070,
    )
    skill_library.add_skill(
        Skill(
            name="Dokumori",
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

    skill_library.add_skill(
        Skill(
            name="Bhavacakra",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=380),
                "Meisui": DamageSpec(potency=530),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    phantom_follow_up_damage = FollowUp(
        skill=Skill(
            name="Phantom Kamaitachi (pet)",
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=600, damage_class=DamageClass.PET, pet_job_mod_override=100
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
    skill_library.add_skill(
        Skill(
            name="Phantom Kamaitachi",
            is_GCD=True,
            timing_spec=TimingSpec(base_cast_time=0, application_delay=1560),
            follow_up_skills=(phantom_follow_up_damage,),
            has_aoe=True,
        )
    )

    # TODO: fix. gcds only will proc it, like bunshin. Ty An.
    skill_library.add_skill(
        Skill(
            name="Hollow Nozuchi",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=270
            ),
            follow_up_skills=(doton_hollow_nozuchi_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Forked Raiju",
            is_GCD=True,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (all_bunshin_follow_ups["Forked Raiju"],),
            },
        )
    )

    skill_library.add_skill(
        Skill(
            name="Fleeting Raiju",
            is_GCD=True,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (all_bunshin_follow_ups["Fleeting Raiju"],),
            },
        )
    )

    # ninjitsus
    skill_library.add_skill(
        Skill(
            name="Fuma Shuriken",
            is_GCD=True,
            damage_spec=DamageSpec(potency=500),
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
    skill_library.add_skill(
        Skill(
            name="Katon",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=350),
                "Ten Chi Jin": DamageSpec(potency=350),
            },
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
    skill_library.add_skill(
        Skill(
            name="Raiton",
            is_GCD=True,
            damage_spec=DamageSpec(potency=740),
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
    skill_library.add_skill(
        Skill(
            name="Hyoton",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=350),
                "Ten Chi Jin": DamageSpec(potency=350),
            },
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
    skill_library.add_skill(
        Skill(
            name="Huton",
            is_GCD=True,
            damage_spec=DamageSpec(potency=240),
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
        )
    )

    skill_library.add_skill(
        Skill(
            name="Doton",
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

    skill_library.add_skill(
        Skill(
            name="Suiton",
            is_GCD=True,
            damage_spec=DamageSpec(potency=580),
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
    skill_library.add_skill(
        Skill(
            name="Goka Mekkyaku",
            is_GCD=True,
            damage_spec=DamageSpec(potency=600),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=760,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hyosho Ranryu",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1300),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=620,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bunshin",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=5,
                duration=int(30.7 * 1000),
                skill_allowlist=(
                    "Spinning Edge",
                    "Gust Slash",
                    "Throwing Dagger",
                    "Aeolian Edge",
                    "Death Blossom",
                    "Hakke Mujinsatsu",
                    "Armor Crush",
                    "Forked Raiju",
                    "Fleeting Raiju",
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ten Chi Jin",
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
    skill_library.add_skill(
        Skill(
            name="Meisui",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=("Bhavacakra", "Zesho Meppo"),
            ),
        )
    )

    kunai_damage_follow_up = FollowUp(
        skill=Skill("Kunai's Bane", damage_spec=DamageSpec(potency=600), has_aoe=True),
        delay_after_parent_application=1290,
        primary_target_only=False,
    )
    kunai_debuff_follow_up = FollowUp(
        skill=Skill(
            name="Kunai's Bane",
            debuff_spec=StatusEffectSpec(damage_mult=1.10, duration=int(16.26 * 1000)),
        ),
        delay_after_parent_application=0,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name="Kunai's Bane",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(kunai_damage_follow_up, kunai_debuff_follow_up),
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Deathfrog Medium",
            is_GCD=False,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Zesho Meppo",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=700),
                "Meisui": DamageSpec(potency=850),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Tenri Jindo",
            is_GCD=False,
            damage_spec=DamageSpec(potency=1100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1690
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Kassatsu",
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
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Hide", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
