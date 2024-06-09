from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.testing.test_add_lbs_to_skill_library import add_lbs_to_skill_library
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.skills.skill_library import SkillLibrary
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def create_test_skill_library():
    skill_library = SkillLibrary(version="test")

    # TimingSpecs
    gcd_2500 = TimingSpec(base_cast_time=2500, animation_lock=5)
    gcd_1500_lock = TimingSpec(base_cast_time=1500, animation_lock=50)
    gcd_instant = TimingSpec(base_cast_time=0, animation_lock=5)
    gcd_instant_no_lock = TimingSpec(base_cast_time=0, animation_lock=0)
    gcd_2500_app_delay = TimingSpec(base_cast_time=2500, application_delay=100)
    ogcd_instant = TimingSpec(base_cast_time=0, animation_lock=0)
    ogcd_instant_animation_lock = TimingSpec(base_cast_time=0, animation_lock=35)
    gcd_1500_const_cast = TimingSpec(
        base_cast_time=1500,
        animation_lock=5,
        affected_by_speed_stat=False,
        affected_by_haste_buffs=False,
    )
    gcd_1500_no_haste = TimingSpec(
        base_cast_time=1500, animation_lock=5, affected_by_haste_buffs=False
    )
    auto_timing = TimingSpec(base_cast_time=0, animation_lock=0, application_delay=500)

    # DamageSpecs
    simple_damage = DamageSpec(potency=660)
    simple_tank_damage = DamageSpec(potency=200)
    simple_magical_dot_damage = DamageSpec(
        potency=70, damage_class=DamageClass.MAGICAL_DOT
    )
    simple_physical_dot_damage = DamageSpec(
        potency=90, damage_class=DamageClass.PHYSICAL_DOT
    )
    simple_tank_dot_damage = DamageSpec(
        potency=50, damage_class=DamageClass.MAGICAL_DOT
    )
    guaranteed_dh_damage = DamageSpec(
        potency=660, guaranteed_dh=ForcedCritOrDH.FORCE_YES
    )
    guaranteed_crit_damage = DamageSpec(
        potency=660, guaranteed_crit=ForcedCritOrDH.FORCE_YES
    )
    guaranteed_crit_dh_damage = DamageSpec(
        potency=660,
        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
        guaranteed_dh=ForcedCritOrDH.FORCE_YES,
    )
    guaranteed_no_crit_dh_damage = DamageSpec(
        potency=660,
        guaranteed_crit=ForcedCritOrDH.FORCE_NO,
        guaranteed_dh=ForcedCritOrDH.FORCE_NO,
    )
    auto_damage = DamageSpec(
        potency=110, damage_class=DamageClass.AUTO, trait_damage_mult_override=1.0
    )
    healer_auto_damage = DamageSpec(
        potency=80, damage_class=DamageClass.AUTO, trait_damage_mult_override=1.0
    )
    simple_damage_trait_override = DamageSpec(
        potency=660, trait_damage_mult_override=1.0
    )
    guaranteed_dh_dot_damage = DamageSpec(
        potency=50,
        guaranteed_dh=ForcedCritOrDH.FORCE_YES,
        damage_class=DamageClass.MAGICAL_DOT,
    )
    guaranteed_crit_dot_damage = DamageSpec(
        potency=50,
        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
        damage_class=DamageClass.MAGICAL_DOT,
    )
    guaranteed_crit_dh_dot_damage = DamageSpec(
        potency=50,
        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
        guaranteed_dh=ForcedCritOrDH.FORCE_YES,
        damage_class=DamageClass.MAGICAL_DOT,
    )
    pet_damage = DamageSpec(
        potency=350,
        pet_job_mod_override=100,
        trait_damage_mult_override=1,
        damage_class=DamageClass.PET,
    )

    # StatusEffectSpecs (buff/debuff)
    simple_buff = StatusEffectSpec(
        duration=30000, max_duration=60000, crit_rate_add=0.05, is_party_effect=True
    )
    simple_buff_2 = StatusEffectSpec(
        duration=10000, crit_rate_add=0.06, dh_rate_add=0.2
    )
    simple_debuff = StatusEffectSpec(
        duration=30000, max_duration=60000, damage_mult=1.2, is_party_effect=True
    )
    simple_debuff_2 = StatusEffectSpec(duration=10000, damage_mult=1.3)
    auto_attack_buff = StatusEffectSpec(
        duration=10000, auto_attack_delay_reduction=0.25
    )
    haste_buff1 = StatusEffectSpec(duration=15000, haste_time_reduction=0.25)
    haste_buff2 = StatusEffectSpec(duration=15000, haste_time_reduction=0.10)
    flat_cast_time_reduction_buff = StatusEffectSpec(
        duration=15000, flat_cast_time_reduction=2500
    )
    simple_buff_with_allowlist = StatusEffectSpec(
        duration=30000,
        max_duration=60000,
        crit_rate_add=0.05,
        skill_allowlist=("test_gcd",),
    )
    num_uses_buff_with_cast_reduction = StatusEffectSpec(
        duration=30000, max_duration=60000, flat_cast_time_reduction=3000, num_uses=2
    )
    guaranteed_crit_buff = StatusEffectSpec(
        duration=30000,
        max_duration=60000,
        num_uses=1,
        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
    )
    guaranteed_dh_buff = StatusEffectSpec(
        duration=30000,
        max_duration=60000,
        num_uses=1,
        guaranteed_dh=ForcedCritOrDH.FORCE_YES,
    )
    guaranteed_crit_dh_buff = StatusEffectSpec(
        duration=30000,
        max_duration=60000,
        num_uses=1,
        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
        guaranteed_dh=ForcedCritOrDH.FORCE_YES,
    )
    num_uses_buff_with_priority1 = StatusEffectSpec(
        duration=30000,
        max_duration=60000,
        crit_rate_add=0.1,
        num_uses=1,
        skill_allowlist=("test_instant_gcd",),
    )
    num_uses_buff_with_priority2 = StatusEffectSpec(
        duration=30000,
        max_duration=60000,
        dh_rate_add=0.1,
        num_uses=1,
        skill_allowlist=("test_instant_gcd",),
    )

    # Skill creation
    test_gcd = Skill(
        name="test_gcd", is_GCD=True, timing_spec=gcd_2500, damage_spec=simple_damage
    )
    test_gcd_1500_lock = Skill(
        name="test_gcd_1500_lock",
        is_GCD=True,
        timing_spec=gcd_1500_lock,
        damage_spec=simple_damage,
    )
    test_instant_gcd = Skill(
        name="test_instant_gcd",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=simple_damage,
    )
    test_instant_gcd_no_lock = Skill(
        name="test_instant_gcd_no_lock",
        is_GCD=True,
        timing_spec=gcd_instant_no_lock,
        damage_spec=simple_damage,
    )
    test_tank_gcd = Skill(
        name="test_tank_gcd",
        is_GCD=True,
        timing_spec=gcd_2500,
        damage_spec=simple_tank_damage,
    )
    test_gcd_with_app_delay = Skill(
        name="test_gcd_with_app_delay", is_GCD=True, timing_spec=gcd_2500_app_delay
    )
    test_ogcd = Skill(name="test_ogcd", is_GCD=False, timing_spec=ogcd_instant)
    test_ogcd_animation_lock = Skill(
        name="test_ogcd_animation_lock",
        is_GCD=False,
        timing_spec=ogcd_instant_animation_lock,
    )
    test_non_dot_follow_up = Skill(name="test_non_dot_follow_up", is_GCD=False)
    test_follow_up = Skill(
        name="test_follow_up",
        is_GCD=False,
        timing_spec=gcd_2500,
        follow_up_skills=(
            FollowUp(
                skill=test_non_dot_follow_up,
                delay_after_parent_application=0,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            ),
            FollowUp(
                skill=test_non_dot_follow_up,
                delay_after_parent_application=3000,
                snapshot_buffs_with_parent=False,
                snapshot_debuffs_with_parent=True,
            ),
            FollowUp(
                skill=test_non_dot_follow_up,
                delay_after_parent_application=7000,
                snapshot_buffs_with_parent=False,
                snapshot_debuffs_with_parent=False,
            ),
        ),
    )
    test_magical_dot_tick = Skill(
        name="test_magical_dot_tick",
        is_GCD=False,
        damage_spec=simple_magical_dot_damage,
    )
    test_physical_dot_tick = Skill(
        name="test_physical_dot_tick",
        is_GCD=False,
        damage_spec=simple_physical_dot_damage,
    )
    test_tank_dot_tick = Skill(
        name="test_tank_dot_tick", is_GCD=False, damage_spec=simple_tank_dot_damage
    )
    test_magical_dot_gcd = Skill(
        name="test_magical_dot_gcd",
        is_GCD=True,
        timing_spec=gcd_2500,
        follow_up_skills=(
            FollowUp(
                skill=test_magical_dot_tick,
                delay_after_parent_application=0,
                dot_duration=15 * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            ),
        ),
    )
    test_physical_dot_gcd = Skill(
        name="test_physical_dot_gcd",
        is_GCD=True,
        timing_spec=gcd_2500,
        follow_up_skills=(
            FollowUp(
                skill=test_physical_dot_tick,
                delay_after_parent_application=0,
                dot_duration=15 * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            ),
        ),
    )

    test_magical_dot_instant_gcd = Skill(
        name="test_magical_dot_instant_gcd",
        is_GCD=True,
        timing_spec=gcd_instant,
        follow_up_skills=(
            FollowUp(
                skill=test_magical_dot_tick,
                delay_after_parent_application=0,
                dot_duration=15 * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            ),
        ),
    )
    test_magical_dot_gcd_with_other_follow_up = Skill(
        name="test_magical_dot_gcd_with_other_follow_up",
        is_GCD=True,
        timing_spec=gcd_2500,
        follow_up_skills=(
            FollowUp(
                skill=test_non_dot_follow_up,
                delay_after_parent_application=0,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            ),
            FollowUp(
                skill=test_magical_dot_tick,
                delay_after_parent_application=0,
                dot_duration=15 * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            ),
        ),
    )
    test_ground_dot_gcd = Skill(
        name="test_ground_dot_gcd",
        is_GCD=True,
        timing_spec=gcd_2500,
        follow_up_skills=(
            FollowUp(
                skill=test_magical_dot_tick,
                delay_after_parent_application=0,
                dot_duration=15 * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=False,
            ),
        ),
    )
    test_simple_buff_gcd = Skill(
        "test_simple_buff_gcd",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=simple_buff,
    )
    test_party_buff = Skill(
        "test_party_buff", is_GCD=True, timing_spec=gcd_instant, buff_spec=simple_buff
    )
    test_simple_buff_gcd_2 = Skill(
        "test_simple_buff_gcd_2",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=simple_buff_2,
    )
    test_simple_buff_gcd_3 = Skill(
        "test_simple_buff_gcd_3",
        is_GCD=True,
        timing_spec=gcd_2500,
        buff_spec=simple_buff,
    )  # NOT instant cast
    test_simple_debuff_gcd = Skill(
        "test_simple_debuff_gcd",
        is_GCD=True,
        timing_spec=gcd_instant,
        debuff_spec=simple_debuff,
    )
    test_simple_debuff_gcd_2 = Skill(
        "test_simple_debuff_gcd_2",
        is_GCD=True,
        timing_spec=gcd_instant,
        debuff_spec=simple_debuff_2,
    )
    test_guaranteed_dh = Skill(
        "test_guaranteed_dh",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=guaranteed_dh_damage,
    )
    test_guaranteed_crit = Skill(
        "test_guaranteed_crit",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=guaranteed_crit_damage,
    )
    test_guaranteed_crit_dh = Skill(
        "test_guaranteed_crit_dh",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=guaranteed_crit_dh_damage,
    )
    test_guaranteed_no_crit_dh = Skill(
        "test_guaranteed_no_crit_dh",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=guaranteed_no_crit_dh_damage,
    )
    test_guaranteed_dh_dot = Skill(
        "test_guaranteed_dh_dot",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=guaranteed_dh_dot_damage,
    )
    test_guaranteed_crit_dot = Skill(
        "test_guaranteed_crit_dot",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=guaranteed_crit_dot_damage,
    )
    test_guaranteed_crit_dh_dot = Skill(
        "test_guaranteed_crit_dh_dot",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec=guaranteed_crit_dh_dot_damage,
    )
    test_auto = Skill(
        "Auto", is_GCD=False, timing_spec=auto_timing, damage_spec=auto_damage
    )
    test_healer_auto = Skill(
        "Auto", is_GCD=False, timing_spec=auto_timing, damage_spec=healer_auto_damage
    )
    test_gcd_trait_override = Skill(
        name="test_gcd_trait_override",
        is_GCD=True,
        timing_spec=gcd_2500,
        damage_spec=simple_damage_trait_override,
    )
    test_auto_attack_buff = Skill(
        name="test_auto_attack_buff",
        is_GCD=True,
        timing_spec=gcd_2500,
        buff_spec=auto_attack_buff,
    )
    test_auto_attack_buff_instant = Skill(
        name="test_auto_attack_buff_instant",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=auto_attack_buff,
    )
    test_auto_attack_buff_instant_follow_up = Skill(
        name="test_auto_attack_buff_instant_follow_up",
        is_GCD=False,
        buff_spec=auto_attack_buff,
    )
    test_auto_attack_buff_on_follow_up = Skill(
        name="test_auto_attack_buff_on_follow_up",
        is_GCD=True,
        timing_spec=gcd_2500,
        follow_up_skills=(
            FollowUp(
                skill=test_auto_attack_buff_instant_follow_up,
                delay_after_parent_application=0,
            ),
        ),
    )
    test_auto_attack_buff2 = Skill(
        name="test_auto_attack_buff2",
        is_GCD=True,
        timing_spec=gcd_2500,
        buff_spec=auto_attack_buff,
    )
    test_haste_buff1 = Skill(
        name="test_haste_buff1",
        is_GCD=False,
        timing_spec=ogcd_instant,
        buff_spec=haste_buff1,
    )
    test_haste_buff2 = Skill(
        name="test_haste_buff2",
        is_GCD=False,
        timing_spec=ogcd_instant,
        buff_spec=haste_buff2,
    )
    _test_haste_follow_up = Skill(
        name="_test_haste_follow_up", is_GCD=False, buff_spec=haste_buff1
    )
    test_haste_follow_up = Skill(
        name="test_haste_follow_up",
        is_GCD=False,
        timing_spec=ogcd_instant,
        follow_up_skills=(
            FollowUp(skill=_test_haste_follow_up, delay_after_parent_application=0),
        ),
    )
    test_gcd_1500_const_cast = Skill(
        name="test_gcd_1500_const_cast",
        is_GCD=True,
        timing_spec=gcd_1500_const_cast,
        damage_spec=simple_damage,
    )
    test_gcd_1500_no_haste = Skill(
        name="test_gcd_1500_no_haste",
        is_GCD=True,
        timing_spec=gcd_1500_no_haste,
        damage_spec=simple_damage,
    )
    test_pet_gcd = Skill(
        name="test_pet_gcd",
        is_GCD=True,
        timing_spec=gcd_1500_lock,
        damage_spec=pet_damage,
    )
    test_gcd_with_denylist = Skill(
        name="test_gcd_with_denylist",
        is_GCD=True,
        timing_spec=gcd_2500,
        damage_spec=simple_damage,
        status_effect_denylist=("test_simple_buff_gcd_2", "test_simple_debuff_gcd"),
    )
    test_flat_cast_time_reduction = Skill(
        name="test_flat_cast_time_reduction",
        is_GCD=False,
        timing_spec=ogcd_instant,
        buff_spec=flat_cast_time_reduction_buff,
    )
    _test_buff_then_damage = Skill(
        "_test_buff_then_damage", is_GCD=False, damage_spec=simple_damage
    )
    test_buff_then_damage = Skill(
        name="test_buff_then_damage",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=simple_buff,
        follow_up_skills=(
            FollowUp(skill=_test_buff_then_damage, delay_after_parent_application=0),
        ),
    )
    test_default_buff_damage_order = Skill(
        name="test_default_buff_damage_order",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=simple_buff,
        damage_spec=simple_damage,
    )
    test_damage_spec_with_cond = Skill(
        name="test_damage_spec_with_cond",
        is_GCD=True,
        timing_spec=gcd_instant,
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(potency=1000),
            "cond1": DamageSpec(potency=200),
            "cond2": DamageSpec(potency=400),
            "cond3": None,
        },
    )
    test_timing_spec_with_cond = Skill(
        name="test_timing_spec_with_cond",
        is_GCD=True,
        timing_spec={"instant": gcd_instant, "cast": gcd_2500},
        damage_spec=DamageSpec(potency=1000),
    )
    test_buff_with_cond = Skill(
        name="test_buff_with_cond",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec={
            "crit": StatusEffectSpec(
                duration=30000, crit_rate_add=0.1, is_party_effect=True
            ),
            "dh": StatusEffectSpec(
                duration=30000, dh_rate_add=0.2, is_party_effect=True
            ),
        },
    )
    test_debuff_with_cond = Skill(
        name="test_debuff_with_cond",
        is_GCD=True,
        timing_spec=gcd_instant,
        debuff_spec={
            "crit": StatusEffectSpec(duration=30000, crit_rate_add=0.15),
            "dh": StatusEffectSpec(duration=30000, dh_rate_add=0.25),
        },
    )
    test_follow_up_with_cond = Skill(
        name="test_follow_up_with_cond",
        is_GCD=True,
        timing_spec=gcd_2500,
        follow_up_skills={
            "1": (
                FollowUp(
                    skill=test_non_dot_follow_up,
                    delay_after_parent_application=0,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            "2": (
                FollowUp(
                    skill=test_non_dot_follow_up,
                    delay_after_parent_application=0,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
                FollowUp(
                    skill=test_non_dot_follow_up,
                    delay_after_parent_application=3000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        },
    )
    _follow_up_buff = Skill(
        name="follow_up_buff",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            duration=30000, max_duration=60000, crit_rate_add=0.15, is_party_effect=True
        ),
    )
    _follow_up_buff_override = Skill(
        name="follow_up_buff",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            duration=30000, max_duration=60000, crit_rate_add=0.50
        ),
    )
    _follow_up_buff_other_duration = Skill(
        name="follow_up_buff",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            duration=10000, max_duration=60000, crit_rate_add=0.15
        ),
    )
    _follow_up_debuff = Skill(
        name="follow_up_debuff",
        is_GCD=False,
        debuff_spec=StatusEffectSpec(
            duration=30000, max_duration=60000, crit_rate_add=0.25
        ),
    )
    test_skill_with_follow_up_buff1 = Skill(
        name="test_skill_with_follow_up_buff1",
        is_GCD=True,
        timing_spec=gcd_instant,
        follow_up_skills=(
            FollowUp(skill=_follow_up_buff, delay_after_parent_application=0),
        ),
    )
    test_skill_with_follow_up_buff2 = Skill(
        name="test_skill_with_follow_up_buff2",
        is_GCD=True,
        timing_spec=gcd_instant,
        follow_up_skills=(
            FollowUp(skill=_follow_up_buff, delay_after_parent_application=0),
        ),
    )
    test_skill_with_follow_up_buff_other_duration = Skill(
        name="test_skill_with_follow_up_buff_other_duration",
        is_GCD=True,
        timing_spec=gcd_instant,
        follow_up_skills=(
            FollowUp(
                skill=_follow_up_buff_other_duration, delay_after_parent_application=0
            ),
        ),
    )
    test_skill_with_follow_up_buff_override = Skill(
        name="test_skill_with_follow_up_buff_override",
        is_GCD=True,
        timing_spec=gcd_instant,
        follow_up_skills=(
            FollowUp(skill=_follow_up_buff_override, delay_after_parent_application=0),
        ),
    )
    test_simple_buff_with_allowlist = Skill(
        "simple_buff_with_allowlist",
        is_GCD=False,
        timing_spec=ogcd_instant,
        buff_spec=simple_buff_with_allowlist,
    )
    test_num_uses_buff_with_cast_reduction = Skill(
        "test_num_uses_buff_with_cast_reduction",
        is_GCD=False,
        timing_spec=ogcd_instant_animation_lock,
        buff_spec=num_uses_buff_with_cast_reduction,
    )
    test_guaranteed_crit_buff = Skill(
        "test_guaranteed_crit_buff",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=guaranteed_crit_buff,
    )
    test_guaranteed_dh_buff = Skill(
        "test_guaranteed_dh_buff",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=guaranteed_dh_buff,
    )
    test_guaranteed_crit_dh_buff = Skill(
        "guaranteed_crit_dh_buff",
        is_GCD=True,
        timing_spec=gcd_instant,
        buff_spec=guaranteed_crit_dh_buff,
    )
    test_num_uses_buff_with_priority1 = Skill(
        "test_num_uses_buff_with_priority1",
        is_GCD=False,
        timing_spec=ogcd_instant_animation_lock,
        buff_spec=num_uses_buff_with_priority1,
    )
    test_num_uses_buff_with_priority2 = Skill(
        "test_num_uses_buff_with_priority2",
        is_GCD=False,
        timing_spec=ogcd_instant_animation_lock,
        buff_spec=num_uses_buff_with_priority2,
    )
    test_skill_with_conditional = Skill(
        "test_skill_with_conditional",
        is_GCD=False,
        timing_spec=ogcd_instant_animation_lock,
        buff_spec=StatusEffectSpec(
            duration=30000,
            max_duration=60000,
            add_to_skill_modifier_condition=True,
            num_uses=1,
        ),
    )
    test_skill_add_gauge = Skill(
        name="test_skill_add_gauge",
        is_GCD=False,
        timing_spec=ogcd_instant_animation_lock,
        job_resource_spec=(JobResourceSpec(name="Gauge", change=10),),
    )
    test_skill_use_gauge = Skill(
        name="test_skill_use_gauge",
        is_GCD=False,
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
            "10 Gauge": DamageSpec(potency=600),
        },
        timing_spec=ogcd_instant_animation_lock,
        job_resource_spec=(JobResourceSpec(name="Gauge", change=-10),),
    )
    test_combo0 = Skill(
        name="test_combo0",
        is_GCD=True,
        damage_spec=DamageSpec(potency=100),
        timing_spec=gcd_instant_no_lock,
        combo_spec=(ComboSpec(),),
    )
    test_combo1 = Skill(
        name="test_combo1",
        is_GCD=True,
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
            SimConsts.COMBO_FAIL: DamageSpec(potency=100),
        },
        timing_spec=gcd_instant_no_lock,
        combo_spec=(ComboSpec(combo_actions=("test_combo0",)),),
    )
    test_damage_with_debuff_follow_up = Skill(
        name="test_damage_with_debuff_follow_up",
        is_GCD=False,
        damage_spec=simple_damage,
        timing_spec=ogcd_instant,
        follow_up_skills=(
            FollowUp(skill=_follow_up_debuff, delay_after_parent_application=0),
        ),
    )
    test_combo_pos = Skill(
        name="test_combo_pos",
        is_GCD=True,
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(potency=380),
            "No Combo, No Positional": DamageSpec(potency=120),
            "No Combo": DamageSpec(potency=170),
            "No Positional": DamageSpec(potency=330),
            "To Ignore": DamageSpec(potency=380),
            "No Positional, To Ignore": DamageSpec(potency=330),
        },
        timing_spec=gcd_instant,
        ignored_conditions_for_bonus_potency=("To Ignore",),
    )

    skill_library.set_current_job_class("test_job")
    skill_library.add_resource(
        "Gauge",
        JobResourceSettings(
            max_value=100,
            skill_allowlist=(("test_instant_gcd", "test_skill_use_gauge")),
        ),
    )

    skill_library.add_skill(test_gcd)
    skill_library.add_skill(test_ogcd)
    skill_library.add_skill(test_gcd_with_app_delay)
    skill_library.add_skill(test_non_dot_follow_up)
    skill_library.add_skill(test_follow_up)
    skill_library.add_skill(test_magical_dot_gcd)
    skill_library.add_skill(test_physical_dot_gcd)
    skill_library.add_skill(test_ground_dot_gcd)
    skill_library.add_skill(test_magical_dot_tick)
    skill_library.add_skill(test_physical_dot_tick)
    skill_library.add_skill(test_magical_dot_gcd_with_other_follow_up)
    skill_library.add_skill(test_magical_dot_instant_gcd)
    skill_library.add_skill(test_simple_buff_gcd)
    skill_library.add_skill(test_simple_buff_gcd_2)
    skill_library.add_skill(test_simple_buff_gcd_3)
    skill_library.add_skill(test_simple_debuff_gcd)
    skill_library.add_skill(test_simple_debuff_gcd_2)
    skill_library.add_skill(test_guaranteed_dh)
    skill_library.add_skill(test_guaranteed_crit)
    skill_library.add_skill(test_guaranteed_crit_dh)
    skill_library.add_skill(test_guaranteed_no_crit_dh)
    skill_library.add_skill(test_guaranteed_dh_dot)
    skill_library.add_skill(test_guaranteed_crit_dot)
    skill_library.add_skill(test_guaranteed_crit_dh_dot)
    skill_library.add_skill(test_auto_attack_buff)
    skill_library.add_skill(test_auto_attack_buff2)
    skill_library.add_skill(test_auto)
    skill_library.add_skill(test_instant_gcd)
    skill_library.add_skill(test_instant_gcd_no_lock)
    skill_library.add_skill(test_auto_attack_buff_instant)
    skill_library.add_skill(test_auto_attack_buff_on_follow_up)
    skill_library.add_skill(test_auto_attack_buff_instant_follow_up)
    skill_library.add_skill(test_ogcd_animation_lock)
    skill_library.add_skill(test_gcd_1500_lock)
    skill_library.add_skill(test_haste_buff1)
    skill_library.add_skill(test_haste_buff2)
    skill_library.add_skill(_test_haste_follow_up)
    skill_library.add_skill(test_haste_follow_up)
    skill_library.add_skill(test_pet_gcd)
    skill_library.add_skill(test_gcd_with_denylist)
    skill_library.add_skill(test_gcd_1500_const_cast)
    skill_library.add_skill(test_gcd_1500_no_haste)
    skill_library.add_skill(test_flat_cast_time_reduction)
    skill_library.add_skill(test_buff_then_damage)
    skill_library.add_skill(_test_buff_then_damage)
    skill_library.add_skill(test_default_buff_damage_order)
    skill_library.add_skill(test_damage_spec_with_cond)
    skill_library.add_skill(test_timing_spec_with_cond)
    skill_library.add_skill(test_buff_with_cond)
    skill_library.add_skill(test_debuff_with_cond)
    skill_library.add_skill(test_follow_up_with_cond)
    skill_library.add_skill(_follow_up_buff)
    skill_library.add_skill(test_skill_with_follow_up_buff1)
    skill_library.add_skill(test_skill_with_follow_up_buff2)
    skill_library.add_skill(test_skill_with_follow_up_buff_other_duration)
    skill_library.add_skill(test_skill_with_follow_up_buff_override)
    skill_library.add_skill(test_simple_buff_with_allowlist)
    skill_library.add_skill(test_num_uses_buff_with_cast_reduction)
    skill_library.add_skill(test_guaranteed_crit_buff)
    skill_library.add_skill(test_guaranteed_dh_buff)
    skill_library.add_skill(test_guaranteed_crit_dh_buff)
    skill_library.add_skill(test_num_uses_buff_with_priority1)
    skill_library.add_skill(test_num_uses_buff_with_priority2)
    skill_library.add_skill(test_skill_with_conditional)
    skill_library.add_skill(test_skill_add_gauge)
    skill_library.add_skill(test_skill_use_gauge)
    skill_library.add_skill(test_combo0)
    skill_library.add_skill(test_combo1)
    skill_library.add_skill(_follow_up_debuff)
    skill_library.add_skill(test_damage_with_debuff_follow_up)
    skill_library.add_skill(test_combo_pos)

    skill_library.set_status_effect_priority(
        ("test_num_uses_buff_with_priority1", "test_num_uses_buff_with_priority2")
    )

    skill_library.set_current_job_class("test_job2")
    skill_library.add_skill(test_auto)
    skill_library.add_skill(test_gcd)
    skill_library.add_skill(test_gcd_trait_override)
    skill_library.add_skill(test_party_buff)

    skill_library.set_current_job_class("test_tank_job")
    skill_library.add_skill(test_auto)
    skill_library.add_skill(test_tank_gcd)
    skill_library.add_skill(test_tank_dot_tick)
    skill_library.add_skill(test_pet_gcd)

    skill_library.set_current_job_class("test_healer_job")
    skill_library.add_skill(test_healer_auto)

    skill_library.set_current_job_class("test_job_haste")
    skill_library.add_skill(test_auto)
    skill_library.add_skill(test_instant_gcd)
    skill_library.add_skill(test_gcd)

    skill_library = add_lbs_to_skill_library(skill_library)

    return skill_library
