from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
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


def add_pld_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    divine_might_buff = Skill(
        name="Divine Might",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=30 * 1000,
            skill_allowlist=("Holy Spirit", "Holy Circle"),
        ),
    )
    divine_might_follow_up = FollowUp(
        skill=divine_might_buff, delay_after_parent_application=0,
        primary_target_only=True
    )

    skill_library.set_current_job_class("PLD")
    skill_library.set_status_effect_priority(("Divine Might", "Requiescat"))
    # combo group 0: 1-2-3, with fast blade and AOE
    # combo 1: Confiteor + blade of X combos
    skill_library.add_combo_breaker(1, (0,))

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
            name="Fast Blade",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=220),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fight or Flight",
            is_GCD=False,
            buff_spec=StatusEffectSpec(duration=20000, damage_mult=1.25),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Riot Blade",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=330),
                "No Combo": DamageSpec(potency=170),
            },
            combo_spec=(ComboSpec(combo_actions=("Fast Blade",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Total Eclipse",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shield Bash",
            is_GCD=True,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=446
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shield Lob",
            is_GCD=True,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=889
            ),
        )
    )

    promimence_follow_up = FollowUp(
        skill=Skill(name="Prominence", damage_spec=DamageSpec(potency=170)),
        delay_after_parent_application=623,
        primary_target_only=False
    )
    promimence_no_combo_follow_up = FollowUp(
        skill=Skill(name="Prominence", damage_spec=DamageSpec(potency=100)),
        delay_after_parent_application=623,
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Prominence",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Total Eclipse",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    promimence_follow_up,
                    divine_might_follow_up,
                ),
                "No Combo": (promimence_no_combo_follow_up,),
            },
            has_aoe=True
        )
    )
    circle_of_scorn_dot_pld = Skill(
        name="Circle of Scorn (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=30, damage_class=DamageClass.PHYSICAL_DOT),
    )
    skill_library.add_skill(circle_of_scorn_dot_pld)
    skill_library.add_skill(
        Skill(
            name="Circle of Scorn",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1023
            ),
            damage_spec=DamageSpec(potency=140),
            follow_up_skills=(
                FollowUp(
                    skill=circle_of_scorn_dot_pld,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Goring Blade",
            is_GCD=True,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=534
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Royal Authority",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=440),
                "No Combo": DamageSpec(potency=180),
            },
            combo_spec=(ComboSpec(combo_actions=("Riot Blade",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=578
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (divine_might_follow_up,),
                "No Combo": tuple(),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Holy Spirit",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=370),
                "Divine Might": DamageSpec(potency=470),
                "Requiescat": DamageSpec(potency=670),
                "Divine Might, Requiescat": DamageSpec(potency=470),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=1500,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
                "Divine Might": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
                "Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
                "Divine Might, Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
            },
        )
    )
    req_charges_follow_up = FollowUp(
        skill=Skill(
            name="Requiescat",
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=4,
                duration=30 * 1000,
                skill_allowlist=(
                    "Holy Spirit",
                    "Holy Circle",
                    "Confiteor",
                    "Blade of Faith",
                    "Blade of Truth",
                    "Blade of Valor",
                ),
            ),
        ),
        delay_after_parent_application=0,
    )
    skill_library.add_skill(
        Skill(
            name="Requiescat",
            is_GCD=False,
            damage_spec=DamageSpec(potency=320),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            follow_up_skills=(req_charges_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Imperator",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=580)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills=(req_charges_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.5
        )
    )
    skill_library.add_skill(
        Skill(
            name="Holy Circle",
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "Divine Might": DamageSpec(potency=200),
                "Requiescat": DamageSpec(potency=300),
                "Divine Might, Requiescat": DamageSpec(potency=200),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=1500,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
                "Divine Might": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
                "Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
                "Divine Might, Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Intervene",
            is_GCD=False,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=578
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Atonement",
            is_GCD=True,
            damage_spec=DamageSpec(potency=440),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1293
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Supplication",
            is_GCD=True,
            damage_spec=DamageSpec(potency=460),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Sepulchre",
            is_GCD=True,
            damage_spec=DamageSpec(potency=480),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Confiteor",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=440),
                "Requiescat": DamageSpec(potency=940),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            has_aoe=True,
            aoe_dropoff=0.5
        )
    )
    skill_library.add_skill(
        Skill(
            name="Expiacion",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=450)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=357
            ),
            has_aoe=True,
            aoe_dropoff=0.6
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blade of Faith",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Confiteor",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=240),
                "Requiescat": DamageSpec(potency=740),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=666
            ),
            has_aoe=True,
            aoe_dropoff=0.5
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blade of Truth",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Blade of Faith",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=340),
                "Requiescat": DamageSpec(potency=840),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=891
            ),
            has_aoe=True,
            aoe_dropoff=0.5
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blade of Valor",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Blade of Truth",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=440),
                "Requiescat": DamageSpec(potency=940),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=891
            ),
            has_aoe=True,
            aoe_dropoff=0.5
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blade of Honor",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1000)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=0.5
        )
    )
    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Rampart", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Provoke", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Reprisal", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Arm's Length", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Shirk", is_GCD=False, timing_spec=instant_timing_spec)
    )

    return skill_library
