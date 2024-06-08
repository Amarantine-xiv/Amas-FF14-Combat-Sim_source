import math

from simulator.calcs.damage_class import DamageClass
from simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from simulator.game_data.patch_655.convenience_timings import (
    get_shot_timing,
    get_instant_timing_spec,
)
from simulator.sim_consts import SimConsts
from simulator.skills.skill import Skill
from simulator.specs.combo_spec import ComboSpec
from simulator.specs.damage_spec import DamageSpec
from simulator.specs.follow_up import FollowUp
from simulator.specs.job_resource_settings import JobResourceSettings
from simulator.specs.job_resource_spec import JobResourceSpec
from simulator.specs.status_effect_spec import StatusEffectSpec
from simulator.specs.timing_spec import TimingSpec


def add_mch_skills(skill_library):
    auto_timing = get_shot_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("MCH")
    skill_library.add_resource(
        name="Battery",
        job_resource_settings=JobResourceSettings(
            max_value=100, skill_allowlist=("Automaton Queen",)
        ),
    )
    skill_library.add_resource(
        name="GCD",
        job_resource_settings=JobResourceSettings(
            max_value=6, skill_allowlist=("_Wildfire", "Detonator")
        ),
    )

    job_resource_spec_gcd = JobResourceSpec(name="GCD", change=+1)
    # TODO: implement queen overdrive, cutting off queen early

    def get_arm_punch_follow_ups():
        min_potency = 120
        max_potency = 240
        battery_range = 50
        slope = (max_potency - min_potency) / battery_range
        follow_ups = {}
        for battery in range(50, 110, 10):
            skill = Skill(
                name="Arm Punch",
                status_effect_denylist=("Dragon Sight",),
                damage_spec=DamageSpec(
                    potency=int((battery - 50) * slope + min_potency),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                ),
            )
            follow_ups[battery] = {}
            for hit in range(0, 5):
                delay = int((5.5 + 1.6 * hit) * 1000)
                follow_ups[battery][hit] = FollowUp(
                    skill=skill,
                    delay_after_parent_application=delay,
                    snapshot_buffs_with_parent=False,
                    snapshot_debuffs_with_parent=False,
                )
        return follow_ups

    def get_roller_dash_follow_up():
        min_potency = 240
        max_potency = 480
        battery_range = 50
        slope = (max_potency - min_potency) / battery_range
        follow_up = {}
        for battery in range(50, 110, 10):
            skill = Skill(
                name="Roller Dash",
                status_effect_denylist=("Dragon Sight",),
                damage_spec=DamageSpec(
                    potency=int((battery - 50) * slope + min_potency),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                ),
            )
            follow_up[battery] = FollowUp(
                skill=skill,
                delay_after_parent_application=int(5.5 * 1000),
                snapshot_buffs_with_parent=False,
                snapshot_debuffs_with_parent=False,
            )
        return follow_up

    def get_pile_bunker_follow_up():
        min_potency = 340
        max_potency = 680
        battery_range = 50
        slope = (max_potency - min_potency) / battery_range
        follow_up = {}
        for battery in range(50, 110, 10):
            skill = Skill(
                name="Pile Bunker",
                status_effect_denylist=("Dragon Sight",),
                damage_spec=DamageSpec(
                    potency=int((battery - 50) * slope + min_potency),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                ),
            )
            follow_up[battery] = FollowUp(
                skill=skill,
                delay_after_parent_application=int((5.5 + 5 * 1.6) * 1000),
                snapshot_buffs_with_parent=False,
                snapshot_debuffs_with_parent=False,
            )
        return follow_up

    def get_crowned_collider_follow_up():
        follow_up = {}
        for battery in range(50, 110, 10):
            min_potency = 390
            max_potency = 780
            battery_range = 50
            slope = (max_potency - min_potency) / battery_range
            skill = Skill(
                name="Crowned Collider",
                status_effect_denylist=("Dragon Sight",),
                damage_spec=DamageSpec(
                    potency=int((battery - 50) * slope + min_potency),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                ),
            )
            follow_up[battery] = FollowUp(
                skill=skill,
                delay_after_parent_application=int((5.5 + 5 * 1.6 + 2) * 1000),
                snapshot_buffs_with_parent=False,
                snapshot_debuffs_with_parent=False,
            )
        return follow_up

    def get_flamethrower_follow_ups():
        flamethrower_dot = Skill(
            name="_Flamethrower dot",
            damage_spec=DamageSpec(potency=80, damage_class=DamageClass.PHYSICAL_DOT),
        )
        follow_ups = {}
        for i in range(0, 11):
            follow_ups[i] = FollowUp(
                skill=flamethrower_dot,
                delay_after_parent_application=0,
                dot_duration=i * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            )
        return follow_ups

    arm_punch_follow_ups = get_arm_punch_follow_ups()
    roller_dash_follow_up = get_roller_dash_follow_up()
    pile_bunker_follow_up = get_pile_bunker_follow_up()
    crowned_collider_follow_up = get_crowned_collider_follow_up()
    flamethrower_follow_ups = get_flamethrower_follow_ups()

    overheated_bonus_potency = 20

    skill_library.add_skill(
        Skill(
            name="Shot",
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=80, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Gauss Round",
            is_GCD=False,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Heat Blast",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200),
                "Reassemble": DamageSpec(
                    potency=200,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=200 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=200 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=620
            ),
            job_resource_spec=(job_resource_spec_gcd,),
        )
    )

    wildfire_damage_spec = {}
    for i in range(0, 7):
        wildfire_damage_spec["{} GCD".format(i)] = DamageSpec(
            potency=i * 240,
            guaranteed_crit=ForcedCritOrDH.FORCE_NO,
            guaranteed_dh=ForcedCritOrDH.FORCE_NO,
        )
    wildfire_damage_spec[SimConsts.DEFAULT_CONDITION] = DamageSpec(potency=0)
    wildfire_skill = Skill(
        name="_Wildfire",
        is_GCD=False,
        job_resources_snapshot=False,
        damage_spec=wildfire_damage_spec,
        job_resource_spec=(JobResourceSpec(name="GCD", change=-math.inf),),
    )
    wildfire_follow_up = FollowUp(
        skill=wildfire_skill,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
        delay_after_parent_application=10 * 1000,
    )
    detonator_follow_up = FollowUp(
        skill=wildfire_skill,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
        delay_after_parent_application=0,
    )

    skill_library.add_skill(
        Skill(
            name="Wildfire",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (wildfire_follow_up,),
                "Manual": tuple(),
            },
            job_resource_spec=(JobResourceSpec(name="GCD", change=-math.inf),),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Detonator",
            is_GCD=False,
            damage_spec=wildfire_damage_spec,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            job_resource_spec=(JobResourceSpec(name="GCD", change=-math.inf),),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ricochet",
            is_GCD=False,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Auto Crossbow",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=140),
                "Reassemble": DamageSpec(
                    potency=140,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=140 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=140 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=890
            ),
            job_resource_spec=(job_resource_spec_gcd,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Heated Split Shot",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200),
                "Reassemble": DamageSpec(
                    potency=200,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=200 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=200 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            combo_spec=(ComboSpec(),),
            job_resource_spec=(job_resource_spec_gcd,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Drill",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "Reassemble": DamageSpec(
                    potency=600,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=600 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=600 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1150
            ),
            job_resource_spec=(job_resource_spec_gcd,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Heated Slug Shot",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=300),
                "Reassemble": DamageSpec(
                    potency=300,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo": DamageSpec(potency=120),
                "No Combo, Reassemble": DamageSpec(
                    potency=120,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=300 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=300 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo, Overheated": DamageSpec(
                    potency=120 + overheated_bonus_potency
                ),
                "No Combo, Overheated, Reassemble": DamageSpec(
                    potency=120 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            combo_spec=(ComboSpec(combo_actions=("Heated Split Shot",)),),
            job_resource_spec=(job_resource_spec_gcd,),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Heated Clean Shot",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=380),
                "Reassemble": DamageSpec(
                    potency=380,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo": DamageSpec(potency=120),
                "No Combo, Reassemble": DamageSpec(
                    potency=120,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=380 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=380 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo, Overheated": DamageSpec(
                    potency=120 + overheated_bonus_potency
                ),
                "No Combo, Overheated, Reassemble": DamageSpec(
                    potency=120 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            combo_spec=(ComboSpec(combo_actions=("Heated Slug Shot",)),),
            job_resource_spec=(
                JobResourceSpec(name="Battery", change=+10),
                job_resource_spec_gcd,
            ),
        )
    )
    bioblaster_dot = Skill(
        name="_Bioblaster dot",
        is_GCD=False,
        damage_spec=DamageSpec(potency=50, damage_class=DamageClass.PHYSICAL_DOT),
    )
    bioblaster_follow_up = FollowUp(
        skill=bioblaster_dot,
        delay_after_parent_application=0,
        dot_duration=15 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )
    skill_library.add_skill(
        Skill(
            name="Bioblaster",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=50),
                "Reassemble": DamageSpec(
                    potency=50,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=50 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=50 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=970
            ),
            follow_up_skills=(bioblaster_follow_up,),
            job_resource_spec=(job_resource_spec_gcd,),
        )
    )

    flamethrower_follow_up_dict = {}
    flamethrower_timing_specs_dict = {}
    for i in range(0, 11):
        flamethrower_follow_up_dict["{}s".format(i)] = (flamethrower_follow_ups[i],)
        flamethrower_timing_specs_dict["{}s".format(i)] = TimingSpec(
            base_cast_time=i * 1000,
            gcd_base_recast_time=i * 1000,
            application_delay=890,
        )
    skill_library.add_skill(
        Skill(
            name="Flamethrower",
            timing_spec=flamethrower_timing_specs_dict,
            follow_up_skills=flamethrower_follow_up_dict,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Air Anchor",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "Reassemble": DamageSpec(
                    potency=600,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(potency=600 + overheated_bonus_potency),
                "Overheated, Reassemble": DamageSpec(
                    potency=600 + overheated_bonus_potency,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1150
            ),
            job_resource_spec=(
                JobResourceSpec(name="Battery", change=+20),
                job_resource_spec_gcd,
            ),
        )
    )

    queen_follow_ups = {}
    queen_follow_ups["Ranged"] = (
        roller_dash_follow_up[100],
        arm_punch_follow_ups[100][2],
        arm_punch_follow_ups[100][3],
        arm_punch_follow_ups[100][4],
        pile_bunker_follow_up[100],
        crowned_collider_follow_up[100],
    )
    queen_follow_ups["Melee"] = (
        arm_punch_follow_ups[100][0],
        arm_punch_follow_ups[100][1],
        arm_punch_follow_ups[100][2],
        arm_punch_follow_ups[100][3],
        arm_punch_follow_ups[100][4],
        pile_bunker_follow_up[100],
        crowned_collider_follow_up[100],
    )
    for battery in range(50, 110, 10):
        queen_follow_ups["{} Battery".format(battery)] = (
            roller_dash_follow_up[battery],
            arm_punch_follow_ups[battery][2],
            arm_punch_follow_ups[battery][3],
            arm_punch_follow_ups[battery][4],
            pile_bunker_follow_up[battery],
            crowned_collider_follow_up[battery],
        )
        queen_follow_ups["{} Battery, Ranged".format(battery)] = (
            roller_dash_follow_up[battery],
            arm_punch_follow_ups[battery][2],
            arm_punch_follow_ups[battery][3],
            arm_punch_follow_ups[battery][4],
            pile_bunker_follow_up[battery],
            crowned_collider_follow_up[battery],
        )
        queen_follow_ups["{} Battery, Melee".format(battery)] = (
            arm_punch_follow_ups[battery][0],
            arm_punch_follow_ups[battery][1],
            arm_punch_follow_ups[battery][2],
            arm_punch_follow_ups[battery][3],
            arm_punch_follow_ups[battery][4],
            pile_bunker_follow_up[battery],
            crowned_collider_follow_up[battery],
        )
    skill_library.add_skill(
        Skill(
            name="Automaton Queen",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=queen_follow_ups,
            job_resource_spec=(JobResourceSpec(name="Battery", change=-math.inf),),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Scattergun",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=150),
                "Reassemble": DamageSpec(
                    potency=150,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1150
            ),
            job_resource_spec=(job_resource_spec_gcd,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Chain Saw",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=600),
                "Reassemble": DamageSpec(
                    potency=600,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
            job_resource_spec=(
                JobResourceSpec(name="Battery", change=+20),
                job_resource_spec_gcd,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Reassemble",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=5 * 1000,
                skill_allowlist=(
                    "Heat Blast",
                    "Auto Crossbow",
                    "Heated Split Shot",
                    "Drill",
                    "Heated Slug Shot",
                    "Heated Clean Shot",
                    "Bioblaster",
                    "Air Anchor",
                    "Scattergun",
                    "Chain Saw",
                ),
            ),
        )
    )
    overheated_buff = Skill(
        name="Overheated",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=5,
            duration=10 * 1000,
            skill_allowlist=(
                "Heat Blast",
                "Auto Crossbow",
                "Heated Split Shot",
                "Drill",
                "Heated Slug Shot",
                "Heated Clean Shot",
                "Bioblaster",
                "Air Anchor",
            ),
        ),
    )
    overheated_follow_up = FollowUp(
        skill=overheated_buff, delay_after_parent_application=0
    )

    skill_library.add_skill(
        Skill(
            name="Hypercharge",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(overheated_follow_up,),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    skill_library.add_skill(
        Skill(name="Tactician", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Dismantle", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Barrel Stabilizer", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
