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


def add_rpr_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("RPR")

    _deaths_design_follow_up = FollowUp(
        skill=Skill(
            name="_Death's Design debuff",
            is_GCD=False,
            debuff_spec=StatusEffectSpec(
                damage_mult=1.10, duration=30 * 1000, max_duration=60 * 1000
            ),
        ),
        delay_after_parent_application=0,
    )

    enhanced_harp = Skill(
        name="Enhanced Harpe",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=20 * 1000,
            skill_allowlist=("Harpe",),
        ),
    )
    enhanced_harp_follow_up = FollowUp(
        skill=enhanced_harp, delay_after_parent_application=0
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
            name="Slice",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=320),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Waxing Slice",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Slice",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=400),
                "No Combo": DamageSpec(potency=160),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )

    shadow_of_death_damage = FollowUp(
        skill=Skill(name="Shadow of Death", damage_spec=DamageSpec(potency=300)),
        delay_after_parent_application=1160,
    )
    skill_library.add_skill(
        Skill(
            name="Shadow of Death",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(shadow_of_death_damage, _deaths_design_follow_up),
        )
    )

    # The handling of spee dhere is not technically correct, because if the player melded spell speed this would be a faster cast....but who's going to do that on rpr?
    skill_library.add_skill(
        Skill(
            name="Harpe",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
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
    skill_library.add_skill(
        Skill(
            name="Spinning Scythe",
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=140),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Infernal Slice",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Waxing Slice",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=500),
                "No Combo": DamageSpec(potency=180),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )

    whorl_of_death_damage = FollowUp(
        skill=Skill(name="Whorl of Death", damage_spec=DamageSpec(potency=100)),
        delay_after_parent_application=1160,
    )
    skill_library.add_skill(
        Skill(
            name="Whorl of Death",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(whorl_of_death_damage, _deaths_design_follow_up),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Nightmare Scythe",
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Spinning Scythe",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=180),
                "No Combo": DamageSpec(potency=120),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blood Stalk",
            is_GCD=False,
            damage_spec=DamageSpec(potency=340),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Grim Swathe",
            is_GCD=False,
            damage_spec=DamageSpec(potency=140),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Soul Slice",
            is_GCD=True,
            damage_spec=DamageSpec(potency=460),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1030,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Soul Scythe",
            is_GCD=True,
            damage_spec=DamageSpec(potency=180),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=670,
                affected_by_haste_buffs=False,
                affected_by_speed_stat=False,
            ),
        )
    )

    enhanced_gibbet = Skill(
        name="Enhanced Gibbet",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=60 * 1000,
            skill_allowlist=("Gibbet",),
        ),
    )
    enhanced_gibbet_follow_up = FollowUp(
        skill=enhanced_gibbet, delay_after_parent_application=0
    )
    enhanced_gallows = Skill(
        name="Enhanced Gallows",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=60 * 1000,
            skill_allowlist=("Gallows",),
        ),
    )
    enhanced_gallows_follow_up = FollowUp(
        skill=enhanced_gallows, delay_after_parent_application=0
    )
    skill_library.add_skill(
        Skill(
            name="Gibbet",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=460),
                "No Positional": DamageSpec(potency=400),
                "Enhanced Gibbet": DamageSpec(potency=520),
                "Enhanced Gibbet, No Positional": DamageSpec(potency=460),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            follow_up_skills=(enhanced_gallows_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Gallows",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=460),
                "No Positional": DamageSpec(potency=400),
                "Enhanced Gallows": DamageSpec(potency=520),
                "Enhanced Gallows, No Positional": DamageSpec(potency=460),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            follow_up_skills=(enhanced_gibbet_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Guillotine",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Unveiled Gibbet",
            is_GCD=False,
            damage_spec=DamageSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Unveiled Gallows",
            is_GCD=False,
            damage_spec=DamageSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=540
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Arcane Circle",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.03, duration=int(19.98 * 1000), is_party_effect=True
            ),
            timing_spec=instant_timing_spec,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Gluttony",
            is_GCD=False,
            damage_spec=DamageSpec(potency=520),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
        )
    )

    enhanced_void_reaping = Skill(
        name="Enhanced Void Reaping",
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
    enhanced_cross_reaping = Skill(
        name="Enhanced Cross Reaping",
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
    skill_library.add_skill(
        Skill(
            name="Void Reaping",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=460),
                "Enhanced Void Reaping": DamageSpec(potency=520),
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
    skill_library.add_skill(
        Skill(
            name="Cross Reaping",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=460),
                "Enhanced Cross Reaping": DamageSpec(potency=520),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=620
            ),
            follow_up_skills=(enhanced_void_reaping_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Grim Reaping",
            is_GCD=True,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Harvest Moon",
            is_GCD=True,
            damage_spec=DamageSpec(potency=600),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                application_delay=1160,
                affected_by_speed_stat=False,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Lemure's Slice",
            is_GCD=False,
            damage_spec=DamageSpec(potency=240),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Lemure's Scythe",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Plentiful Harvest",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1000),
                "1 stack": DamageSpec(potency=720),
                "2 stacks": DamageSpec(potency=760),
                "3 stacks": DamageSpec(potency=800),
                "4 stacks": DamageSpec(potency=840),
                "5 stacks": DamageSpec(potency=880),
                "6 stacks": DamageSpec(potency=920),
                "7 stacks": DamageSpec(potency=960),
                "8 stacks": DamageSpec(potency=1000),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Communio",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1100),
            timing_spec=TimingSpec(
                base_cast_time=1300, application_delay=620, affected_by_speed_stat=False
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hell's Ingress",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(enhanced_harp_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hell's Egress",
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
    skill_library.add_skill(
        Skill(
            name="Enshroud",
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
    skill_library.add_skill(
        Skill(
            name="Soulsow",
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
