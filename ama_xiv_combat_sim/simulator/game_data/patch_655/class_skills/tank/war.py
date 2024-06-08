from simulator.calcs.damage_class import DamageClass
from simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from simulator.game_data.patch_655.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from simulator.sim_consts import SimConsts
from simulator.skills.skill import Skill
from simulator.specs.combo_spec import ComboSpec
from simulator.specs.damage_spec import DamageSpec
from simulator.specs.follow_up import FollowUp
from simulator.specs.status_effect_spec import StatusEffectSpec
from simulator.specs.timing_spec import TimingSpec


def add_war_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("WAR")
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
            name="Heavy Swing",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=532
            ),
            damage_spec=DamageSpec(potency=200),
            combo_spec=(ComboSpec(),),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Maim",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            combo_spec=(ComboSpec(combo_actions=("Heavy Swing",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300),
                "No Combo": DamageSpec(150),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Storm's Path",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1515
            ),
            combo_spec=(ComboSpec(combo_actions=("Maim",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=440),
                "No Combo": DamageSpec(potency=160),
            },
        )
    )

    surging_tempest_skill_inital = Skill(
        name="Surging Tempest",
        buff_spec=StatusEffectSpec(
            duration=31600,
            max_duration=60000,
            damage_mult=1.10,
            add_to_skill_modifier_condition=True,
        ),
    )
    surging_tempest_inital_follow_up = FollowUp(
        skill=surging_tempest_skill_inital, delay_after_parent_application=0
    )
    surging_tempest_skill = Skill(
        name="Surging Tempest",
        buff_spec=StatusEffectSpec(
            duration=30000,
            max_duration=60000,
            damage_mult=1.10,
            add_to_skill_modifier_condition=True,
        ),
    )
    surging_tempest_follow_up = FollowUp(
        skill=surging_tempest_skill, delay_after_parent_application=0
    )

    storms_eye_damage_follow_up = FollowUp(
        skill=Skill(name="Storm's Eye", damage_spec=DamageSpec(potency=440)),
        delay_after_parent_application=1649,
    )
    storms_eye_damage_no_combo_follow_up = FollowUp(
        skill=Skill(name="Storm's Eye", damage_spec=DamageSpec(potency=160)),
        delay_after_parent_application=1649,
    )
    skill_library.add_skill(
        Skill(
            name="Storm's Eye",
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
    skill_library.add_skill(
        Skill(
            name="Upheaval",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            damage_spec=DamageSpec(potency=400),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Onslaught",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=667
            ),
            damage_spec=DamageSpec(potency=150),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fell Cleave",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            damage_spec=DamageSpec(potency=520),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Primal Rend",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1300, application_delay=1160
            ),
            damage_spec=DamageSpec(
                potency=700,
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Inner Chaos",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=937
            ),
            damage_spec=DamageSpec(
                potency=660,
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Chaotic Cyclone",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=668
            ),
            damage_spec=DamageSpec(
                potency=320,
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Tomahawk",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=713
            ),
            damage_spec=DamageSpec(potency=150),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Overpower",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=110),
        )
    )

    mythril_tempest_skill_inital = Skill(
        name="Surging Tempest",
        buff_spec=StatusEffectSpec(
            duration=30470,
            max_duration=60000,
            damage_mult=1.10,
            add_to_skill_modifier_condition=True,
        ),
    )
    mythril_tempest_inital_follow_up = FollowUp(
        skill=mythril_tempest_skill_inital, delay_after_parent_application=0
    )

    mythril_tempest_damage_follow_up = FollowUp(
        skill=Skill(name="_Mythril Tempest", damage_spec=DamageSpec(potency=150)),
        delay_after_parent_application=490,
    )
    mythril_tempest_damage_no_combo_follow_up = FollowUp(
        skill=Skill(name="_Storm's Eye", damage_spec=DamageSpec(potency=100)),
        delay_after_parent_application=490,
    )
    skill_library.add_skill(
        Skill(
            name="Mythril Tempest",
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
        )
    )

    skill_library.add_skill(
        Skill(
            name="Orogeny",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=668
            ),
            damage_spec=DamageSpec(potency=150),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Decimate",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1831
            ),
            damage_spec=DamageSpec(potency=200),
        )
    )

    ir_surging_tempest_skill = Skill(
        name="Surging Tempest",
        buff_spec=StatusEffectSpec(
            duration=10000,
            max_duration=60000,
            damage_mult=1.10,
            extend_only=True,
            add_to_skill_modifier_condition=True,
        ),
    )
    ir_surging_tempest_follow_up = FollowUp(
        skill=ir_surging_tempest_skill, delay_after_parent_application=0
    )
    skill_library.add_skill(
        Skill(
            name="Inner Release",
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
        Skill(
            name="Vengeance",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Retaliation": DamageSpec(potency=55),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: instant_timing_spec,
                "Retaliation": TimingSpec(
                    base_cast_time=0, animation_lock=0, application_delay=534
                ),
            },
        )
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
