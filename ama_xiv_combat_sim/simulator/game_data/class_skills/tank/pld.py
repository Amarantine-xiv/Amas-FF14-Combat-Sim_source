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

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.pld_data import (
    all_pld_skills,
)


def add_pld_skills(skill_library):
    all_pld_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_pld_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    divine_might_follow_up = FollowUp(
        skill=Skill(
            name="Divine Might",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=("Holy Spirit", "Holy Circle"),
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
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
    name = "Fast Blade"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
        )
    )

    name = "Fight or Flight"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(duration=20000, damage_mult=1.25),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Riot Blade"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_pld_skills.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_actions=("Fast Blade",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
        )
    )

    name = "Total Eclipse"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
            has_aoe=True,
        )
    )

    name = "Shield Bash"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=446
            ),
        )
    )

    name = "Shield Lob"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=889
            ),
        )
    )

    name = "Prominence"
    promimence_follow_up = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name))
        ),
        delay_after_parent_application=623,
        primary_target_only=False,
    )

    name = "Prominence"
    promimence_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency_no_combo(name)),
        ),
        delay_after_parent_application=623,
        primary_target_only=False,
    )

    name = "Prominence"
    skill_library.add_skill(
        Skill(
            name=name,
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
            has_aoe=True,
        )
    )

    name = "Circle of Scorn (dot)"
    circle_of_scorn_dot_pld = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_pld_skills.get_potency(name),
            damage_class=DamageClass.PHYSICAL_DOT,
        ),
    )
    skill_library.add_skill(circle_of_scorn_dot_pld)

    name = "Circle of Scorn"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1023
            ),
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=circle_of_scorn_dot_pld,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True,
        )
    )

    name = "Goring Blade"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=534
            ),
        )
    )

    name = "Royal Authority"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_pld_skills.get_potency_no_combo(name)
                ),
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

    name = "Holy Spirit"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency")
                ),
                "Divine Might": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_divine_might")
                ),
                "Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_req")
                ),
                "Divine Might, Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(
                        name, "potency_divine_might_req"
                    )
                ),
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

    name = "Requiescat"
    req_charges_follow_up = FollowUp(
        skill=Skill(
            name=name,
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

    name = "Requiescat"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            follow_up_skills=(req_charges_follow_up,),
        )
    )

    if level in [100]:
        name = "Imperator"
        imperator_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_pld_skills.get_potency(name))},
                has_aoe=True,
                aoe_dropoff=0.5,
            ),
            delay_after_parent_application=1290,
            primary_target_only=False,
        )
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                follow_up_skills=(imperator_damage_follow_up, req_charges_follow_up,),
            )
        )

    name = "Holy Circle"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency")
                ),
                "Divine Might": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_divine_might")
                ),
                "Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_req")
                ),
                "Divine Might, Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(
                        name, "potency_divine_might_req"
                    )
                ),
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

    name = "Intervene"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=578
            ),
        )
    )

    name = "Atonement"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1293
            ),
        )
    )

    if level in [100]:
        name = "Supplication"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1160
                ),
            )
        )

    if level in [100]:
        name = "Sepulchre"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_pld_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1290
                ),
            )
        )

    name = "Confiteor"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_req")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Expiacion"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=357
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Blade of Faith"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Confiteor",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_req")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=666
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Blade of Truth"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Blade of Faith",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_req")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=891
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Blade of Valor"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Blade of Truth",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=all_pld_skills.get_skill_data(name, "potency_req")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=891
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    if level in [100]:
        name = "Blade of Honor"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_pld_skills.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1160
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
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
