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

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.rpr_data import (
    all_rpr_skills,
)


def add_rpr_skills(skill_library):
    all_rpr_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_rpr_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("RPR")

    name = "Death's Design"
    _deaths_design_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            debuff_spec=StatusEffectSpec(
                damage_mult=1.10, duration=30 * 1000, max_duration=60 * 1000
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=False,
    )

    name = "Enhanced Harpe"
    enhanced_harp = Skill(
        name=name,
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=all_rpr_skills.get_skill_data(name, "duration"),
            skill_allowlist=("Harpe",),
        ),
    )
    enhanced_harp_follow_up = FollowUp(
        skill=enhanced_harp, delay_after_parent_application=0
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

    name = "Slice"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )

    name = "Waxing Slice"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Slice",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_rpr_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_rpr_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )

    name = "Shadow of Death"
    shadow_of_death_damage = FollowUp(
        skill=Skill(
            name=name, damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name))
        ),
        delay_after_parent_application=1160,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(shadow_of_death_damage, _deaths_design_follow_up),
        )
    )

    # The handling of spee dhere is not technically correct, because if the player melded spell speed this would be a faster cast....but who's going to do that on rpr?
    name = "Harpe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=1300,
                    gcd_base_recast_time=2500,
                    application_delay=890,
                    affected_by_speed_stat=False,
                ),
                "Enhanced Harpe": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=890
                ),
            },
        )
    )

    name = "Spinning Scythe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )
    )

    name = "Infernal Slice"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Waxing Slice",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_rpr_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_rpr_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )

    name = "Whorl of Death"
    whorl_of_death_damage = FollowUp(
        skill=Skill(
            name=name,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            has_aoe=True,
        ),
        delay_after_parent_application=1160,
        primary_target_only=False,
    )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(whorl_of_death_damage, _deaths_design_follow_up),
            has_aoe=True,
        )
    )

    name = "Nightmare Scythe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Spinning Scythe",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_rpr_skills.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=all_rpr_skills.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            has_aoe=True,
        )
    )

    name = "Blood Stalk"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
        )
    )

    name = "Grim Swathe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            has_aoe=True,
        )
    )

    name = "Soul Slice"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1030,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
        )
    )

    name = "Soul Scythe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=670,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
            has_aoe=True,
        )
    )

    name = "Enhanced Gibbet"
    enhanced_gibbet = Skill(
        name=name,
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=60 * 1000,
            skill_allowlist=all_rpr_skills.get_skill_data(name, "allowlist"),
        ),
    )
    enhanced_gibbet_follow_up = FollowUp(
        skill=enhanced_gibbet, delay_after_parent_application=0
    )

    name = "Enhanced Gallows"
    enhanced_gallows = Skill(
        name=name,
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=60 * 1000,
            skill_allowlist=all_rpr_skills.get_skill_data(name, "allowlist"),
        ),
    )
    enhanced_gallows_follow_up = FollowUp(
        skill=enhanced_gallows, delay_after_parent_application=0
    )

    name = "Gibbet"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_rpr_skills.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=all_rpr_skills.get_potency_no_positional(name)
                ),
                "Enhanced Gibbet": DamageSpec(
                    potency=all_rpr_skills.get_skill_data(name, "potency_gibbet")
                ),
                "Enhanced Gibbet, No Positional": DamageSpec(
                    potency=all_rpr_skills.get_skill_data(name, "potency_no_pos_gibbet")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            follow_up_skills=(enhanced_gallows_follow_up,),
        )
    )

    name = "Gallows"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_rpr_skills.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=all_rpr_skills.get_potency_no_positional(name)
                ),
                "Enhanced Gallows": DamageSpec(
                    potency=all_rpr_skills.get_skill_data(name, "potency_gallows")
                ),
                "Enhanced Gallows, No Positional": DamageSpec(
                    potency=all_rpr_skills.get_skill_data(
                        name, "potency_no_pos_gallows"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            follow_up_skills=(enhanced_gibbet_follow_up,),
        )
    )

    name = "Guillotine"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            has_aoe=True,
        )
    )

    name = "Unveiled Gibbet"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )

    name = "Unveiled Gallows"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )

    name = "Arcane Circle"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.03,
                duration=all_rpr_skills.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )
    )

    name = "Gluttony"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            has_aoe=True,
            aoe_dropoff=0.25,
        )
    )

    name = "Enhanced Void Reaping"
    enhanced_void_reaping = Skill(
        name=name,
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=60 * 1000,
            skill_allowlist=("Void Reaping",),
        ),
    )
    enhanced_void_reaping_follow_up = FollowUp(
        skill=enhanced_void_reaping, delay_after_parent_application=0
    )

    name = "Enhanced Cross Reaping"
    enhanced_cross_reaping = Skill(
        name=name,
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=60 * 1000,
            skill_allowlist=("Cross Reaping",),
        ),
    )
    enhanced_cross_reaping_follow_up = FollowUp(
        skill=enhanced_cross_reaping, delay_after_parent_application=0
    )

    name = "Void Reaping"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_rpr_skills.get_potency(name)
                ),
                "Enhanced Void Reaping": DamageSpec(
                    potency=all_rpr_skills.get_skill_data(name, "potency_enhanced")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=540,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
            follow_up_skills=(enhanced_cross_reaping_follow_up,),
        )
    )

    name = "Cross Reaping"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_rpr_skills.get_potency(name)
                ),
                "Enhanced Cross Reaping": DamageSpec(
                    potency=all_rpr_skills.get_skill_data(name, "potency_enhanced")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=620
            ),
            follow_up_skills=(enhanced_void_reaping_follow_up,),
        )
    )

    name = "Grim Reaping"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=800
            ),
            has_aoe=True,
        )
    )

    name = "Harvest Moon"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                application_delay=1160,
                affected_by_speed_stat=False,
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    name = "Lemure's Slice"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
        )
    )

    name = "Lemure's Scythe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            has_aoe=True,
        )
    )

    name = "Plentiful Harvest"
    base_potency = all_rpr_skills.get_skill_data(name, "base_potency")
    potency_increment = all_rpr_skills.get_skill_data(name, "potency_increment")
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=base_potency + 7 * potency_increment
                ),
                "1 stack": DamageSpec(potency=base_potency),
                "2 stacks": DamageSpec(potency=base_potency + potency_increment),
                "3 stacks": DamageSpec(potency=base_potency + 2 * potency_increment),
                "4 stacks": DamageSpec(potency=base_potency + 3 * potency_increment),
                "5 stacks": DamageSpec(potency=base_potency + 4 * potency_increment),
                "6 stacks": DamageSpec(potency=base_potency + 5 * potency_increment),
                "7 stacks": DamageSpec(potency=base_potency + 6 * potency_increment),
                "8 stacks": DamageSpec(potency=base_potency + 7 * potency_increment),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Communio"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1300, application_delay=620, affected_by_speed_stat=False
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    if level in [100]:
        name = "Sacrificium"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=760
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    if level in [100]:
        name = "Executioner's Gibbet"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_rpr_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_rpr_skills.get_potency_no_positional(name)
                    ),
                    "Enhanced Gibbet": DamageSpec(
                        potency=all_rpr_skills.get_skill_data(name, "potency_enhanced")
                    ),
                    "Enhanced Gibbet, No Positional": DamageSpec(
                        potency=all_rpr_skills.get_skill_data(
                            name, "potency_no_pos_enhanced"
                        )
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=620
                ),
                follow_up_skills=(enhanced_gallows_follow_up,),
            )
        )

    if level in [100]:
        name = "Executioner's Gallows"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_rpr_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_rpr_skills.get_potency_no_positional(name)
                    ),
                    "Enhanced Gallows": DamageSpec(
                        potency=all_rpr_skills.get_skill_data(name, "potency_enhanced")
                    ),
                    "Enhanced Gallows, No Positional": DamageSpec(
                        potency=all_rpr_skills.get_skill_data(
                            name, "potency_no_pos_enhanced"
                        )
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=2140
                ),
                follow_up_skills=(enhanced_gibbet_follow_up,),
            )
        )

    if level in [100]:
        name = "Executioner's Guillotine"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_rpr_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=540
                ),
                has_aoe=True,
            )
        )

    if level in [100]:
        skill_library.add_skill(
            Skill(
                name="Perfectio",
                is_GCD=True,
                damage_spec=DamageSpec(potency=1200),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    application_delay=1290,
                    affected_by_speed_stat=False,
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )

    name = "Hell's Ingress"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(enhanced_harp_follow_up,),
        )
    )

    name = "Hell's Egress"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(enhanced_harp_follow_up,),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )

    name = "Enshroud"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                expires_status_effects=(
                    "Enhanced Void Reaping",
                    "Enhanced Cross Reaping",
                )
            ),
            timing_spec=instant_timing_spec,
        )
    )
    # Would be affected by spell speed, but I'll assume the user is not going to do that on RPR.
    name = "Soulsow"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: instant_timing_spec,
                "In Combat": TimingSpec(
                    base_cast_time=5000,
                    gcd_base_recast_time=2500,
                    affected_by_speed_stat=False,
                ),
            },
        )
    )
    return skill_library
