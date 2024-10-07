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

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.gnb_data import (
    all_gnb_skills,
)


def add_gnb_skills(skill_library):
    all_gnb_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_gnb_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("GNB")

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

    name = "Keen Edge"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=0),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=893
            ),
        )
    )

    name = "No Mercy"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(duration=int(19.96 * 1000), damage_mult=1.20),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )

    name = "Brutal Shell"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_gnb_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_gnb_skills.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Keen Edge",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1074
            ),
        )
    )

    name = "Demon Slice"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=0),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
            has_aoe=True,
        )
    )

    name = "Lightning Shot"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
        )
    )

    name = "Solid Barrel"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_gnb_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_gnb_skills.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Brutal Shell",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1653
            ),
        )
    )

    name = "Burst Strike"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=714
            ),
        )
    )

    name = "Demon Slaughter"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_gnb_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_gnb_skills.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Demon Slice",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
            has_aoe=True,
        )
    )

    name = "Sonic Break (dot)"
    sonic_break_dot_gnb = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_gnb_skills.get_potency(name),
            damage_class=DamageClass.PHYSICAL_DOT,
        ),
    )
    skill_library.add_skill(sonic_break_dot_gnb)

    name = "Sonic Break"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=sonic_break_dot_gnb,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )
    )

    if level in [90]:
        name = "Rough Divide"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=491
                ),
            )
        )

    name = "Gnashing Fang"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
        )
    )

    name = "Savage Claw"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Gnashing Fang",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )
    )

    name = "Wicked Talon"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Savage Claw",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1162
            ),
        )
    )

    name = "Bow Shock (dot)"
    bow_shock_dot_gnb = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_gnb_skills.get_potency(name),
            damage_class=DamageClass.PHYSICAL_DOT,
        ),
    )
    skill_library.add_skill(bow_shock_dot_gnb)

    name = "Bow Shock"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=627
            ),
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=bow_shock_dot_gnb,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True,
        )
    )

    name = "Jugular Rip"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=802
            ),
        )
    )

    name = "Abdomen Tear"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
        )
    )

    name = "Eye Gouge"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=981
            ),
        )
    )

    name = "Fated Circle"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=537
            ),
            has_aoe=True,
        )
    )

    name = "Blasting Zone"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )
    )

    name = "Hypervelocity"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
        )
    )

    name = "Double Down"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_gnb_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
            has_aoe=True,
            aoe_dropoff=0.15,
        )
    )

    if level in [100]:
        name = "Fated Brand"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_gnb_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1160
                ),
                has_aoe=True,
            )
        )
    if level in [100]:
        name = "Reign of Beasts"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_gnb_skills.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1160
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )

    if level in [100]:
        name = "Noble Blood"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_gnb_skills.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1650
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )
    if level in [100]:
        name = "Lion Heart"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_gnb_skills.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1790
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Bloodfest", is_GCD=False, timing_spec=instant_timing_spec)
    )
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
    skill_library.add_skill(
        Skill(name="Camouflage", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Royal Guard", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Release Royal Guard", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Nebula", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Aurora", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Superbolide", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Heart of Light", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Heart of Stone", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Hear of Corundrum", is_GCD=False, timing_spec=instant_timing_spec)
    )

    return skill_library
