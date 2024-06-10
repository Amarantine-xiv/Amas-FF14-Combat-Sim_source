from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_655.convenience_timings import (
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


def add_gnb_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("GNB")
    # combo group 0: 1-2-3, with keen edge and AOE
    # combo 1: gnashing fang combo
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
            name="Keen Edge",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            combo_spec=(ComboSpec(combo_group=0),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=893
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="No Mercy",
            is_GCD=False,
            buff_spec=StatusEffectSpec(duration=int(19.96 * 1000), damage_mult=1.20),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Brutal Shell",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300),
                "No Combo": DamageSpec(potency=160),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Keen Edge",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1074
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Demon Slice",
            is_GCD=True,
            damage_spec=DamageSpec(potency=100),
            combo_spec=(ComboSpec(combo_group=0),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Lightning Shot",
            is_GCD=True,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Solid Barrel",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=360),
                "No Combo": DamageSpec(potency=140),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Brutal Shell",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1653
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Burst Strike",
            is_GCD=True,
            damage_spec=DamageSpec(potency=380),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=714
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Demon Slaughter",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=160),
                "No Combo": DamageSpec(potency=100),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Demon Slice",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
        )
    )
    sonic_break_dot_gnb = Skill(
        name="_Sonic Break dot",
        is_GCD=False,
        damage_spec=DamageSpec(potency=60, damage_class=DamageClass.PHYSICAL_DOT),
    )
    skill_library.add_skill(sonic_break_dot_gnb)
    skill_library.add_skill(
        Skill(
            name="Sonic Break",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
            damage_spec=DamageSpec(potency=300),
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
    skill_library.add_skill(
        Skill(
            name="Rough Divide",
            is_GCD=False,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=491
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Gnashing Fang",
            is_GCD=True,
            damage_spec=DamageSpec(potency=380),
            combo_spec=(ComboSpec(combo_group=1),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Savage Claw",
            is_GCD=True,
            damage_spec=DamageSpec(potency=460),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Gnashing Fang",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Wicked Talon",
            is_GCD=True,
            damage_spec=DamageSpec(potency=540),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Savage Claw",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1162
            ),
        )
    )
    sonick_break_dot_gnb = Skill(
        name="_Bow Shock dot",
        is_GCD=False,
        damage_spec=DamageSpec(potency=60, damage_class=DamageClass.PHYSICAL_DOT),
    )
    skill_library.add_skill(sonick_break_dot_gnb)
    skill_library.add_skill(
        Skill(
            name="Bow Shock",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=627
            ),
            damage_spec=DamageSpec(potency=150),
            follow_up_skills=(
                FollowUp(
                    skill=sonick_break_dot_gnb,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Jugular Rip",
            is_GCD=False,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=802
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Abdomen Tear",
            is_GCD=False,
            damage_spec=DamageSpec(potency=240),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Eye Gouge",
            is_GCD=False,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=981
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fated Circle",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=537
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blasting Zone",
            is_GCD=False,
            damage_spec=DamageSpec(potency=720),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hypervelocity",
            is_GCD=False,
            damage_spec=DamageSpec(potency=180),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Double Down",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
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
