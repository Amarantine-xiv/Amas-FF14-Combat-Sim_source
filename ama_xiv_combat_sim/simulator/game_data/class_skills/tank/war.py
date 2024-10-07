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

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.war_data import (
    all_war_skills,
)


def add_war_skills(skill_library):    
    version = skill_library.get_version()
    level = skill_library.get_level()
    
    all_war_skills.set_version(version)
    all_war_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("WAR")

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

    name = "Heavy Swing"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=532
            ),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
            combo_spec=(ComboSpec(),),
        )
    )

    name = "Maim"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            combo_spec=(ComboSpec(combo_actions=("Heavy Swing",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_war_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_war_skills.get_potency_no_combo(name)
                ),
            },
        )
    )

    name = "Storm's Path"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1515
            ),
            combo_spec=(ComboSpec(combo_actions=("Maim",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_war_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_war_skills.get_potency_no_combo(name)
                ),
            },
        )
    )

    surging_tempest_inital_follow_up = FollowUp(
        skill=Skill(
            name="Surging Tempest",
            buff_spec=StatusEffectSpec(
                duration=31600,
                max_duration=60000,
                damage_mult=1.10,
                add_to_skill_modifier_condition=True,
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )

    surging_tempest_follow_up = FollowUp(
        skill=Skill(
            name="Surging Tempest",
            buff_spec=StatusEffectSpec(
                duration=30000,
                max_duration=60000,
                damage_mult=1.10,
                add_to_skill_modifier_condition=True,
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )

    name = "Storm's Eye"
    storms_eye_damage_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_war_skills.get_potency(name)
            ),
        ),
        delay_after_parent_application=1649,
    )

    name = "Storm's Eye"
    storms_eye_damage_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_war_skills.get_potency_no_combo(name)
            ),
        ),
        delay_after_parent_application=1649,
    )

    name = "Storm's Eye"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=650),
            combo_spec=(ComboSpec(combo_actions=("Maim",)),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    storms_eye_damage_follow_up,
                    surging_tempest_inital_follow_up,
                ),
                "Surging Tempest": (
                    storms_eye_damage_follow_up,
                    surging_tempest_follow_up,
                ),
                "No Combo": (storms_eye_damage_no_combo_follow_up,),
            },
        )
    )

    name = "Upheaval"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
        )
    )

    name = "Onslaught"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=667
            ),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
        )
    )

    name = "Fell Cleave"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
        )
    )

    name = "Primal Rend"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1300, application_delay=1160
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_war_skills.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                )
            },
            has_aoe=True,
            aoe_dropoff=0.7,
        )
    )

    name = "Inner Chaos"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=937
            ),
            damage_spec=DamageSpec(
                potency=all_war_skills.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
        )
    )

    name = "Chaotic Cyclone"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            damage_spec=DamageSpec(
                potency=all_war_skills.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            has_aoe=True,
        )
    )

    name = "Tomahawk"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=713
            ),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
        )
    )

    name = "Overpower"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Surging Tempest"
    mythril_tempest_inital_follow_up = FollowUp(
        skill=Skill(
            name=name,
            buff_spec=StatusEffectSpec(
                duration=30470,
                max_duration=60000,
                damage_mult=1.10,
                add_to_skill_modifier_condition=True,
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )

    name = "Mythril Tempest"
    mythril_tempest_damage_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_war_skills.get_potency(name)
            ),
        ),
        delay_after_parent_application=490,
        primary_target_only=False,
    )
    mythril_tempest_damage_no_combo_follow_up = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_war_skills.get_potency_no_combo(name)
            ),
        ),
        delay_after_parent_application=490,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=650),
            combo_spec=(ComboSpec(combo_actions=("Overpower",)),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    mythril_tempest_damage_follow_up,
                    mythril_tempest_inital_follow_up,
                ),
                "Surging Tempest": (
                    mythril_tempest_damage_follow_up,
                    surging_tempest_follow_up,
                ),
                "No Combo": (mythril_tempest_damage_no_combo_follow_up,),
            },
            has_aoe=True,
        )
    )

    name = "Orogeny"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=668
            ),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Decimate"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1831
            ),
            damage_spec=DamageSpec(potency=all_war_skills.get_potency(name)),
            has_aoe=True,
        )
    )

    name = "Surging Tempest"
    ir_surging_tempest_follow_up = FollowUp(
        skill=Skill(
            name=name,
            buff_spec=StatusEffectSpec(
                duration=10000,
                max_duration=60000,
                damage_mult=1.10,
                extend_only=True,
                add_to_skill_modifier_condition=True,
            ),
        ),
        delay_after_parent_application=0,
    )

    name = "Inner Release"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                num_uses=3,
                duration=30 * 1000,
                skill_allowlist=("Fell Cleave", "Decimate"),
            ),
            follow_up_skills=(ir_surging_tempest_follow_up,),
        )
    )

    # check if this should be here in this patch/level
    if level in [70, 80, 90]:
        name = "Vengeance"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: None,
                    "Retaliation": DamageSpec(potency=all_war_skills.get_potency(name)),
                },
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: instant_timing_spec,
                    "Retaliation": TimingSpec(
                        base_cast_time=0, animation_lock=0, application_delay=534
                    ),
                },
            )
        )
    if level in [100]:
        name = "Primal Wrath"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1150
                ),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_war_skills.get_potency(name)
                    )
                },
                has_aoe=True,
                aoe_dropoff=0.7,
            )
        )
    if level in [100]:
        name = "Primal Ruination"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=1300, application_delay=1060
                ),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_war_skills.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                        guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                    )
                },
                has_aoe=True,
                aoe_dropoff=0.7,
            )
        )

    if level in [100]:
        name = "Damnation"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: None,
                    "Retaliation": DamageSpec(potency=all_war_skills.get_potency(name)),
                },
                timing_spec={
                    SimConsts.DEFAULT_CONDITION: instant_timing_spec,
                    "Retaliation": TimingSpec(
                        base_cast_time=0, animation_lock=0, application_delay=534
                    ),
                },
            )
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Infuriate", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Defiance", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Thrill of Battle", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Holmgang", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Equilibrium", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Shake It Off", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Nascent Flash", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Bloodwhetting", is_GCD=False, timing_spec=instant_timing_spec)
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
    return skill_library
