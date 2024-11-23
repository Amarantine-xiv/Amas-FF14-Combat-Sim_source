import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.mch_data import (
    all_mch_skills,
)


class MchSkills(GenericJobClass):
    # TODO: implement queen overdrive, cutting off queen early
    # TODO: fix flamethrower dot logs-processing (maybe not here, but SOMEWHERE)

    OVERHEATED_BONUS_POTENCY = 20

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_mch_skills)
        self._job_class = "MCH"

    @GenericJobClass.is_a_resource
    def battery(self):
        name = "Battery"
        job_resource_settings = JobResourceSettings(
            max_value=100, skill_allowlist=("Automaton Queen",)
        )
        return (name, job_resource_settings)

    @GenericJobClass.is_a_resource
    def gcd(self):
        name = "GCD"
        job_resource_settings = JobResourceSettings(
            max_value=6, skill_allowlist=("Wildfire (dot)", "Detonator")
        )
        return (name, job_resource_settings)

    def __get_gcd_job_resouce_increase(self):
        return JobResourceSpec(name="GCD", change=+1)

    def __get_arm_punch_follow_ups(self):
        name = "Arm Punch (pet)"
        min_potency = self._skill_data.get_skill_data(name, "min_potency")
        max_potency = self._skill_data.get_skill_data(name, "max_potency")
        battery_range = 50
        slope = (max_potency - min_potency) / battery_range
        follow_ups = {}
        for battery in range(50, 110, 10):
            skill = Skill(
                name=name,
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

    def __get_roller_dash_follow_up(self):
        name = "Roller Dash (pet)"
        min_potency = self._skill_data.get_skill_data(name, "min_potency")
        max_potency = self._skill_data.get_skill_data(name, "max_potency")
        battery_range = 50
        slope = (max_potency - min_potency) / battery_range
        follow_up = {}
        for battery in range(50, 110, 10):
            skill = Skill(
                name=name,
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

    def __get_pile_bunker_follow_up(self):
        name = "Pile Bunker (pet)"
        min_potency = self._skill_data.get_skill_data(name, "min_potency")
        max_potency = self._skill_data.get_skill_data(name, "max_potency")
        battery_range = 50
        slope = (max_potency - min_potency) / battery_range
        follow_up = {}
        for battery in range(50, 110, 10):
            skill = Skill(
                name=name,
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

    def __get_crowned_collider_follow_up(self):
        name = "Crowned Collider (pet)"
        min_potency = self._skill_data.get_skill_data(name, "min_potency")
        max_potency = self._skill_data.get_skill_data(name, "max_potency")
        battery_range = 50
        slope = (max_potency - min_potency) / battery_range
        follow_up = {}
        for battery in range(50, 110, 10):
            skill = Skill(
                name=name,
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

    def __get_flamethrower_follow_ups(self):
        name = "Flamethrower (dot)"
        flamethrower_dot = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )
        follow_ups = {}
        for i in range(0, 11):
            follow_ups[i] = FollowUp(
                skill=flamethrower_dot,
                delay_after_parent_application=0,
                dot_duration=i * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
                primary_target_only=False,
            )
        return follow_ups

    def __get_wildfire_damage_spec(self):
        wildfire_damage_spec = {}
        for i in range(0, 7):
            wildfire_damage_spec[f"{i} GCD"] = DamageSpec(
                potency=i * 240,
                guaranteed_crit=ForcedCritOrDH.FORCE_NO,
                guaranteed_dh=ForcedCritOrDH.FORCE_NO,
            )
        wildfire_damage_spec[SimConsts.DEFAULT_CONDITION] = DamageSpec(potency=0)
        return wildfire_damage_spec

    @GenericJobClass.is_a_skill
    def auto(self):
        name = "Shot"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.shot_timing_spec,
            damage_spec=DamageSpec(
                potency=80, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )

    @GenericJobClass.is_a_skill
    def gauss_round(self):
        name = "Gauss Round"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )

    @GenericJobClass.is_a_skill
    def heat_blast(self):
        name = "Heat Blast"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=620
            ),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
        )

    @GenericJobClass.is_a_skill
    def wildfire(self):
        name = "Wildfire (dot)"
        wildfire_skill = Skill(
            name=name,
            is_GCD=False,
            job_resources_snapshot=False,
            damage_spec=self.__get_wildfire_damage_spec(),
            job_resource_spec=(JobResourceSpec(name="GCD", change=-math.inf),),
        )
        wildfire_follow_up = FollowUp(
            skill=wildfire_skill,
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
            delay_after_parent_application=10 * 1000,
        )
        name = "Wildfire"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (wildfire_follow_up,),
                "Manual": tuple(),
            },
            job_resource_spec=(JobResourceSpec(name="GCD", change=-math.inf),),
        )

    @GenericJobClass.is_a_skill
    def detonator(self):
        name = "Detonator"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=self.__get_wildfire_damage_spec(),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            job_resource_spec=(JobResourceSpec(name="GCD", change=-math.inf),),
        )

    @GenericJobClass.is_a_skill
    def ricochet(self):
        name = "Ricochet"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def auto_crossbow(self):
        name = "Auto Crossbow"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=1500, application_delay=890
            ),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def heated_split_shot(self):
        name = "Heated Split Shot"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            combo_spec=(ComboSpec(),),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
        )

    @GenericJobClass.is_a_skill
    def drill(self):
        name = "Drill"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1150
            ),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
        )

    @GenericJobClass.is_a_skill
    def heated_slug_shot(self):
        name = "Heated Slug Shot"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
                "No Combo, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo, Overheated": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "No Combo, Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            combo_spec=(ComboSpec(combo_actions=("Heated Split Shot",)),),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
        )

    @GenericJobClass.is_a_skill
    def heated_clean_shot(self):
        name = "Heated Clean Shot"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
                "No Combo, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "No Combo, Overheated": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "No Combo, Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                    + self.OVERHEATED_BONUS_POTENCY,
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
                self.__get_gcd_job_resouce_increase(),
            ),
        )

    @GenericJobClass.is_a_skill
    def blazing_shot(self):
        if self._version < "7.0":
            return None
        name = "Blazing Shot"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=850
            ),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
        )

    @GenericJobClass.is_a_skill
    def bioblaster(self):
        name = "Bioblaster (dot)"
        bioblaster_dot = Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )
        bioblaster_follow_up = FollowUp(
            skill=bioblaster_dot,
            delay_after_parent_application=0,
            dot_duration=15 * 1000,
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
            primary_target_only=False,
        )

        name = "Bioblaster"
        return Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=970
            ),
            follow_up_skills=(bioblaster_follow_up,),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
        )

    @GenericJobClass.is_a_skill
    def flamethrower(self):
        flamethrower_follow_ups = self.__get_flamethrower_follow_ups()

        flamethrower_follow_up_dict = {}
        flamethrower_timing_specs_dict = {}
        for i in range(0, 11):
            flamethrower_follow_up_dict[f"{i}s"] = (flamethrower_follow_ups[i],)
            flamethrower_timing_specs_dict[f"{i}s"] = TimingSpec(
                base_cast_time=i * 1000,
                gcd_base_recast_time=i * 1000,
                application_delay=890,
            )
        flamethrower_follow_up_dict[SimConsts.DEFAULT_CONDITION] = (
            flamethrower_follow_ups[0],
        )
        flamethrower_timing_specs_dict[SimConsts.DEFAULT_CONDITION] = TimingSpec(
            base_cast_time=0,
            gcd_base_recast_time=0,
            application_delay=890,
        )

        name = "Flamethrower"
        return Skill(
            name=name,
            timing_spec=flamethrower_timing_specs_dict,
            follow_up_skills=flamethrower_follow_up_dict,
        )

    @GenericJobClass.is_a_skill
    def air_anchor(self):
        name = "Air Anchor"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                "Overheated": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY
                ),
                "Overheated, Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name)
                    + self.OVERHEATED_BONUS_POTENCY,
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1150
            ),
            job_resource_spec=(
                JobResourceSpec(name="Battery", change=+20),
                self.__get_gcd_job_resouce_increase(),
            ),
        )

    @GenericJobClass.is_a_skill
    def automaton_queen(self):
        name = "Automaton Queen"

        arm_punch_follow_ups = self.__get_arm_punch_follow_ups()
        roller_dash_follow_up = self.__get_roller_dash_follow_up()
        pile_bunker_follow_up = self.__get_pile_bunker_follow_up()
        crowned_collider_follow_up = self.__get_crowned_collider_follow_up()

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
            queen_follow_ups[f"{battery} Battery"] = (
                roller_dash_follow_up[battery],
                arm_punch_follow_ups[battery][2],
                arm_punch_follow_ups[battery][3],
                arm_punch_follow_ups[battery][4],
                pile_bunker_follow_up[battery],
                crowned_collider_follow_up[battery],
            )
            queen_follow_ups[f"{battery} Battery, Ranged"] = (
                roller_dash_follow_up[battery],
                arm_punch_follow_ups[battery][2],
                arm_punch_follow_ups[battery][3],
                arm_punch_follow_ups[battery][4],
                pile_bunker_follow_up[battery],
                crowned_collider_follow_up[battery],
            )
            queen_follow_ups[f"{battery} Battery, Melee"] = (
                arm_punch_follow_ups[battery][0],
                arm_punch_follow_ups[battery][1],
                arm_punch_follow_ups[battery][2],
                arm_punch_follow_ups[battery][3],
                arm_punch_follow_ups[battery][4],
                pile_bunker_follow_up[battery],
                crowned_collider_follow_up[battery],
            )
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,
            follow_up_skills=queen_follow_ups,
            job_resource_spec=(JobResourceSpec(name="Battery", change=-math.inf),),
        )

    @GenericJobClass.is_a_skill
    def scattergun(self):
        name = "Scattergun"
        return Skill(
            name=name,
            is_GCD=True,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1150
            ),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
        )

    @GenericJobClass.is_a_skill
    def chain_saw(self):
        name = "Chain Saw"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
            job_resource_spec=(
                JobResourceSpec(name="Battery", change=+20),
                self.__get_gcd_job_resouce_increase(),
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )

    @GenericJobClass.is_a_skill
    def reassemble(self):
        name = "Reassemble"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,
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
                    "Blazing Shot",
                    "Excavator",
                    "Chain Saw",
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def hypercharge(self):
        name = "Overheated"
        overheated_buff = Skill(
            name=name,
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
                    "Blazing Shot",
                ),
            ),
        )

        name = "Hypercharge"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,
            follow_up_skills=(
                FollowUp(skill=overheated_buff, delay_after_parent_application=0),
            ),
        )

    @GenericJobClass.is_a_skill
    def checkmate(self):
        if self._version < "7.0" or self._level < 92:
            return None
        name = "Checkmate"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def double_check(self):
        if self._version < "7.0" or self._level < 92:
            return None
        name = "Double Check"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def excavator(self):
        if self._version < "7.0" or self._level < 96:
            return None
        name = "Excavator"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Reassemble": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            job_resource_spec=(
                JobResourceSpec(name="Battery", change=+20),
                self.__get_gcd_job_resouce_increase(),
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )

    @GenericJobClass.is_a_skill
    def full_metal_field(self):
        if self._version < "7.0" or self._level < 100:
            return None
        name = "Full Metal Field"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
            job_resource_spec=(self.__get_gcd_job_resouce_increase(),),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def tactician(self):
        return Skill(
            name="Tactician", is_GCD=False, timing_spec=self.instant_timing_spec
        )

    @GenericJobClass.is_a_skill
    def dismantle(self):
        return Skill(
            name="Dismantle", is_GCD=False, timing_spec=self.instant_timing_spec
        )

    @GenericJobClass.is_a_skill
    def barrel_stabilizer(self):
        return Skill(
            name="Barrel Stabilizer", is_GCD=False, timing_spec=self.instant_timing_spec
        )
