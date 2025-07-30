import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.blm_data import (
    all_blm_skills,
)

# TODO(ama): enochian should be granted immediately, not on damage application.
# this is important to properly grant enochian timings, especially to opening damage.
# This is important for skills with long damage application times.


class BlmSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_blm_skills)
        self._job_class = "BLM"
        self.__blm_caster_tax_ms = 100
        self.__base_animation_lock = 600
        self.__blm_instant_timing_spec = TimingSpec(
            base_cast_time=0, animation_lock=self.__base_animation_lock
        )

        self.__af_skill_allowlist = self._skill_data.get_skill_data(
            "Astral Fire", "allowlist"
        )
        self.__ui_skill_allowlist = self._skill_data.get_skill_data(
            "Umbral Ice", "allowlist"
        )
        self.__clear_umbral_ice = JobResourceSpec(
            name="Umbral Ice", change=-math.inf, refreshes_duration_of_last_gained=True
        )
        self.__clear_astral_fire = JobResourceSpec(
            name="Astral Fire", change=-math.inf, refreshes_duration_of_last_gained=True
        )
        self.__enochian_buff_follow_up = self.__get_enochian_buff_follow_up()

    def __get_fire_job_resource_spec(self):
        return {
            SimConsts.DEFAULT_CONDITION: (
                JobResourceSpec(name="Astral Fire", change=+1),
            ),
            "1 Astral Fire": (
                JobResourceSpec(
                    name="Astral Fire",
                    change=+1,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            "2 Astral Fire": (
                JobResourceSpec(
                    name="Astral Fire",
                    change=+1,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            "3 Astral Fire": (
                JobResourceSpec(
                    name="Astral Fire",
                    change=+1,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            "1 Umbral Ice": (
                JobResourceSpec(
                    name="Umbral Ice",
                    change=-math.inf,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            "2 Umbral Ice": (
                JobResourceSpec(
                    name="Umbral Ice",
                    change=-math.inf,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            "3 Umbral Ice": (
                JobResourceSpec(
                    name="Umbral Ice",
                    change=-math.inf,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
        }

    def __get_enochian_buff_follow_up(self):
        name = "Enochian"
        return FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    damage_mult=self._skill_data.get_skill_data(name, "damage_mult"),
                    duration=self._skill_data.get_skill_data(name, "duration"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    @GenericJobClass.is_a_resource
    def astral_fire(self):
        name = "Astral Fire"
        job_resource_settings = JobResourceSettings(
            max_value=3,
            expiry_from_last_gain=self._skill_data.get_skill_data(name, "duration"),
            skill_allowlist=self.__af_skill_allowlist,
        )
        return (name, job_resource_settings)

    @GenericJobClass.is_a_resource
    def umbral_ice(self):
        name = "Umbral Ice"
        job_resource_settings = JobResourceSettings(
            max_value=3,
            expiry_from_last_gain=self._skill_data.get_skill_data(name, "duration"),
            skill_allowlist=self.__ui_skill_allowlist,
        )
        return (name, job_resource_settings)

    def get_status_effect_priority(self):
        return ("Swiftcast", "Triplecast")

    def __get_enochian_damage_spec_cross(self, base_potency, is_fire_spell):
        res = {}
        elem_strs = [
            "1 Astral Fire",
            "2 Astral Fire",
            "3 Astral Fire",
            "1 Umbral Ice",
            "2 Umbral Ice",
            "3 Umbral Ice",
        ]
        fire_potency_modifiers = {
            "1 Astral Fire": 1.4,
            "2 Astral Fire": 1.6,
            "3 Astral Fire": 1.8,
            "1 Umbral Ice": 0.9,
            "2 Umbral Ice": 0.8,
            "3 Umbral Ice": 0.7,
        }
        ice_potency_modifiers = {
            "1 Astral Fire": 0.9,
            "2 Astral Fire": 0.8,
            "3 Astral Fire": 0.7,
            "1 Umbral Ice": 1,
            "2 Umbral Ice": 1,
            "3 Umbral Ice": 1,
        }

        res[SimConsts.DEFAULT_CONDITION] = DamageSpec(
            potency=base_potency
        )  # no astral/umbral fire
        for elem_str in elem_strs:
            potency_modifier = (
                fire_potency_modifiers[elem_str]
                if is_fire_spell
                else ice_potency_modifiers[elem_str]
            )
            res[elem_str] = DamageSpec(
                potency=base_potency, single_damage_mult=potency_modifier
            )
        return res

    def __get_enochian_timing_spec_cross(
        self, base_cast_time, is_fire_spell, application_delay=0
    ):
        res = {}
        elem_strs = [
            "1 Astral Fire",
            "2 Astral Fire",
            "3 Astral Fire",
            "1 Umbral Ice",
            "2 Umbral Ice",
            "3 Umbral Ice",
        ]
        fire_cast_time_modifiers = {
            "1 Astral Fire": 1,
            "2 Astral Fire": 1,
            "3 Astral Fire": 1,
            "1 Umbral Ice": 1,
            "2 Umbral Ice": 1,
            "3 Umbral Ice": 0.5,
        }
        ice_cast_time_modifiers = {
            "1 Astral Fire": 1,
            "2 Astral Fire": 1,
            "3 Astral Fire": 0.5,
            "1 Umbral Ice": 1,
            "2 Umbral Ice": 1,
            "3 Umbral Ice": 1,
        }
        animation_lock_overflow = max(
            0,
            self.__base_animation_lock
            - min(base_cast_time, GameConsts.DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES),
        )
        res[SimConsts.DEFAULT_CONDITION] = TimingSpec(
            base_cast_time=base_cast_time,
            animation_lock=animation_lock_overflow,
            application_delay=application_delay,
        )
        for elem_str in elem_strs:
            cast_modifier = (
                fire_cast_time_modifiers[elem_str]
                if is_fire_spell
                else ice_cast_time_modifiers[elem_str]
            )
            animation_lock_overflow = max(
                0,
                self.__base_animation_lock
                - min(
                    int(cast_modifier * base_cast_time),
                    GameConsts.DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES,
                ),
            )
            res[elem_str] = TimingSpec(
                base_cast_time=int(cast_modifier * base_cast_time),
                animation_lock=animation_lock_overflow,
                application_delay=application_delay,
            )
        return res

    @GenericJobClass.is_a_skill
    def auto(self):
        name = "Auto"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.AUTO,
            timing_spec=self.auto_timing_spec,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )

    def __get_thunder_iii_dot_follow_up(self):
        # we set the name of the thudner dots to be the same so that they may override each other
        name = "Thunder (dot)"
        return FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency("Thunder III (dot)"),
                    damage_class=DamageClass.MAGICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=self._skill_data.get_skill_data(
                "Thunder III (dot)", "duration"
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
        )

    def __get_thunder_iv_dot_follow_up(self):
        # we set the name of the thudner dots to be the same so that they may override each other
        name = "Thunder (dot)"
        return FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency("Thunder IV (dot)"),
                    damage_class=DamageClass.MAGICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=self._skill_data.get_skill_data(
                "Thunder IV (dot)", "duration"
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
            primary_target_only=False,
        )

    @GenericJobClass.is_a_skill
    def blizzard(self):
        name = "Blizzard"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=False
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
                is_fire_spell=False,
                application_delay=840,
            ),
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Umbral Ice", change=+1),
                ),
                "1 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=-math.inf,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=-math.inf,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=-math.inf,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "1 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
            },
            follow_up_skills=(self.__enochian_buff_follow_up,),
        )

    def __get_firestart_follow_up(self):
        name = "Firestarter"
        firestarter_buff = Skill(
            name=name,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=self._skill_data.get_skill_data(name, "duration"),
                skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
            ),
        )
        return FollowUp(skill=firestarter_buff, delay_after_parent_application=10)

    @GenericJobClass.is_a_skill
    def firestarter(self):
        name = "Firestarter"
        # For automated/proc management convenience
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
            ),
        )

    def __get_thundercloud_follow_up(self):
        if self._version >= "7.0":
            return None
        name = "Thundercloud"
        thundercloud_buff = Skill(
            name=name,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=40 * 1000,
                skill_allowlist=("Thunder III", "Thunder IV"),
            ),
        )
        return FollowUp(skill=thundercloud_buff, delay_after_parent_application=10)

    @GenericJobClass.is_a_skill
    def thundercloud(self):
        if self._version >= "7.0":
            return None
        # For automated/proc management convenience
        name = "Thundercloud"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=40 * 1000,
                skill_allowlist=("Thunder III", "Thunder IV"),
            ),
        )

    @GenericJobClass.is_a_skill
    def high_fire_ii(self):
        enhanced_flare_follow_up = (
            None
            if self._version >= "7.0"
            else FollowUp(
                skill=Skill(
                    name="Enhanced",
                    buff_spec=StatusEffectSpec(
                        add_to_skill_modifier_condition=True,
                        num_uses=1,
                        # this is incorrect, since it expires with astral fire.
                        duration=math.inf,
                        skill_allowlist=("Flare",),
                    ),
                ),
                delay_after_parent_application=10,
            )
        )
        name = "High Fire II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=True
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=3000, is_fire_spell=True, application_delay=1160
            ),
            job_resource_spec=(
                self.__clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=(
                (self.__enochian_buff_follow_up,)
                if self._version >= "7.0"
                else (enhanced_flare_follow_up, self.__enochian_buff_follow_up)
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def fire(self):
        name = "Fire"
        firestarter_follow_up = self.__get_firestart_follow_up()
        fire_job_resource_spec = self.__get_fire_job_resource_spec()
        fire_damage_spec = self.__get_enochian_damage_spec_cross(
            base_potency=self._skill_data.get_potency(name), is_fire_spell=True
        )
        fire_timing_spec = self.__get_enochian_timing_spec_cross(
            base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
            is_fire_spell=True,
            application_delay=1030,
        )
        if self._version < "7.0":
            fire_keys = tuple(fire_damage_spec.keys())
            for k in fire_keys:
                assembled_str = (
                    "Sharpcast"
                    if k == SimConsts.DEFAULT_CONDITION
                    else "{k}, Sharpcast"
                )
                fire_damage_spec[assembled_str] = fire_damage_spec[k]
                fire_timing_spec[assembled_str] = fire_timing_spec[k]
                fire_job_resource_spec[assembled_str] = fire_job_resource_spec[k]
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=fire_damage_spec,
            timing_spec=fire_timing_spec,
            job_resource_spec=fire_job_resource_spec,
            follow_up_skills=(
                {
                    SimConsts.DEFAULT_CONDITION: (self.__enochian_buff_follow_up,),
                    "Sharpcast": (
                        firestarter_follow_up,
                        self.__enochian_buff_follow_up,
                    ),
                }
                if self._version < "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: (self.__enochian_buff_follow_up,),
                    "Firestarter": (
                        firestarter_follow_up,
                        self.__enochian_buff_follow_up,
                    ),
                }
            ),
        )

    @GenericJobClass.is_a_skill
    def scathe(self):
        name = "Scathe"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "2x": DamageSpec(potency=2 * self._skill_data.get_potency(name)),
                }
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "2x": DamageSpec(potency=2 * self._skill_data.get_potency(name)),
                    "Sharpcast": DamageSpec(
                        potency=2 * self._skill_data.get_potency(name)
                    ),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=670,
            ),
        )

    @GenericJobClass.is_a_skill
    def fire_iii(self):
        name = "Fire III"
        fire_iii_damage_spec = self.__get_enochian_damage_spec_cross(
            base_potency=self._skill_data.get_potency(name), is_fire_spell=True
        )
        fire_iii_timing_spec = self.__get_enochian_timing_spec_cross(
            base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
            is_fire_spell=True,
            application_delay=0,
        )
        fire_iii_keys = tuple(fire_iii_damage_spec.keys())
        for k in fire_iii_keys:
            assembled_str = (
                "Firestarter"
                if k == SimConsts.DEFAULT_CONDITION
                else f"{k}, Firestarter"
            )
            fire_iii_damage_spec[assembled_str] = fire_iii_damage_spec[k]
            fire_iii_timing_spec[assembled_str] = TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=0,
            )

        fire_iii_followups = {}
        for k, val in fire_iii_damage_spec.items():
            fire_iii_followups[k] = (
                FollowUp(
                    skill=Skill(name="Fire III", damage_spec=val),
                    delay_after_parent_application=1290,
                ),
                self.__enochian_buff_follow_up,
            )

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=fire_iii_timing_spec,
            job_resource_spec=(
                self.__clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=fire_iii_followups,
        )

    @GenericJobClass.is_a_skill
    def blizzard_iii(self):
        name = "Blizzard III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=False
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
                is_fire_spell=False,
                application_delay=840,
            ),
            buff_spec=StatusEffectSpec(expires_status_effects=("Enhanced",)),
            job_resource_spec=(
                self.__clear_astral_fire,
                JobResourceSpec(
                    name="Umbral Ice", change=+3, refreshes_duration_of_last_gained=True
                ),
            ),
            follow_up_skills=(self.__enochian_buff_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def freeze(self):
        name = "Freeze"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=False
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
                is_fire_spell=False,
                application_delay=620,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def thunder_iii(self):
        name = "Thunder III"
        thunderiii_follow_up = self.__get_thunder_iii_dot_follow_up()
        thundercloud_follow_up = (
            None if self._version >= "7.0" else self.__get_thundercloud_follow_up()
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=(
                DamageSpec(potency=self._skill_data.get_potency(name))
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Thundercloud": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_thundercloud"
                        )
                    ),
                }
            ),
            timing_spec=(
                TimingSpec(
                    base_cast_time=2500,
                    animation_lock=self.__blm_caster_tax_ms,
                    application_delay=1030,
                )
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=self._skill_data.get_skill_data(
                            name, "cast_time"
                        ),
                        animation_lock=self.__blm_caster_tax_ms,
                        application_delay=1030,
                    ),
                    "Thundercloud": TimingSpec(
                        base_cast_time=0,
                        animation_lock=self.__base_animation_lock,
                        application_delay=1030,
                    ),
                }
            ),
            follow_up_skills=(
                (thunderiii_follow_up,)
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: (thunderiii_follow_up,),
                    "Thundercloud": (thunderiii_follow_up,),
                    "Sharpcast": (thunderiii_follow_up, thundercloud_follow_up),
                    "Sharpcast, Thundercloud": (
                        (
                            thunderiii_follow_up,
                            thundercloud_follow_up,
                        )
                    ),
                }
            ),
        )

    @GenericJobClass.is_a_skill
    def flare(self):
        name = "Flare"
        flare_elem_mults = {
            "1 Astral Fire": 1.4,
            "2 Astral Fire": 1.6,
            "3 Astral Fire": 1.8,
            "1 Umbral Ice": 0.9,
            "2 Umbral Ice": 0.8,
            "3 Umbral Ice": 0.7,
        }
        flare_damage_spec = self.__get_enochian_damage_spec_cross(
            base_potency=self._skill_data.get_potency(name), is_fire_spell=True
        )
        if self._version < "7.0":
            enhanced_flare_potency = self._skill_data.get_skill_data(
                name, "potency_enhanced"
            )
            flare_damage_spec["Enhanced"] = DamageSpec(potency=enhanced_flare_potency)
            flare_damage_spec["Enhanced, Triplecast"] = DamageSpec(
                potency=enhanced_flare_potency
            )
            for k, potency_modifier in flare_elem_mults.items():
                assemebled_str = f"{k}, Enhanced"
                flare_damage_spec[assemebled_str] = DamageSpec(
                    potency=int(potency_modifier * enhanced_flare_potency)
                )
                assemebled_str = f"{k}, Enhanced, Triplecast"
                flare_damage_spec[assemebled_str] = DamageSpec(
                    potency=int(potency_modifier * enhanced_flare_potency)
                )

        flare_timing_spec = self.__get_enochian_timing_spec_cross(
            base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
            is_fire_spell=True,
            application_delay=1160,
        )
        flare_timing_keys = tuple(flare_timing_spec.keys())
        for k in flare_timing_keys:
            assembled_str = f"{k}, Enhanced"
            flare_timing_spec[assembled_str] = flare_timing_spec[k]

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=flare_damage_spec,
            timing_spec=flare_timing_spec,
            job_resource_spec=(
                self.__clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=(self.__enochian_buff_follow_up,),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def ley_lines(self):
        name = "Ley Lines"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.15,
                auto_attack_delay_reduction=0.15,
                duration=self._skill_data.get_skill_data(name, "duration"),
            ),
        )

    @GenericJobClass.is_a_skill
    def blizzard_iv(self):
        name = "Blizzard IV"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=False
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
                is_fire_spell=False,
                application_delay=1160,
            ),
        )

    @GenericJobClass.is_a_skill
    def fire_iv(self):
        name = "Fire IV"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=True
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
                is_fire_spell=True,
                application_delay=1160,
            ),
        )

    @GenericJobClass.is_a_skill
    def thunder_iv(self):
        name = "Thunder IV"
        thunderiv_follow_up = self.__get_thunder_iv_dot_follow_up()
        thundercloud_follow_up = self.__get_thundercloud_follow_up()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=(
                DamageSpec(potency=self._skill_data.get_potency(name))
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Thundercloud": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_thundercloud"
                        )
                    ),
                }
            ),
            timing_spec=(
                TimingSpec(
                    base_cast_time=2500,
                    animation_lock=self.__blm_caster_tax_ms,
                    application_delay=1160,
                )
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=self._skill_data.get_skill_data(
                            name, "cast_time"
                        ),
                        animation_lock=self.__blm_caster_tax_ms,
                        application_delay=1160,
                    ),
                    "Thundercloud": TimingSpec(
                        base_cast_time=0,
                        animation_lock=self.__blm_caster_tax_ms,
                        application_delay=1160,
                    ),
                }
            ),
            follow_up_skills=(
                (thunderiv_follow_up,)
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: (thunderiv_follow_up,),
                    "Thundercloud": (thunderiv_follow_up,),
                    "Sharpcast": (thunderiv_follow_up, thundercloud_follow_up),
                    "Sharpcast, Thundercloud": (
                        thunderiv_follow_up,
                        thundercloud_follow_up,
                    ),
                }
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def foul(self):
        name = "Foul"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1160,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def despair(self):
        name = "Despair"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=True
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
                is_fire_spell=True,
                application_delay=490,
                # may need to change the animation lock for when it's instant cast?
            ),
            job_resource_spec=(
                self.__clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=(self.__enochian_buff_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def xenoglossys(self):
        name = "Xenoglossy"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=620,
            ),
        )

    @GenericJobClass.is_a_skill
    def high_blizzard_ii(self):
        name = "High Blizzard II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=self.__get_enochian_damage_spec_cross(
                base_potency=self._skill_data.get_potency(name), is_fire_spell=False
            ),
            timing_spec=self.__get_enochian_timing_spec_cross(
                base_cast_time=3000, is_fire_spell=False, application_delay=1160
            ),
            buff_spec=StatusEffectSpec(expires_status_effects=("Enhanced",)),
            job_resource_spec=(
                self.__clear_astral_fire,
                JobResourceSpec(
                    name="Umbral Ice", change=+3, refreshes_duration_of_last_gained=True
                ),
            ),
            follow_up_skills=(self.__enochian_buff_follow_up,),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def paradox(self):
        name = "Paradox"
        paradox_base_timing_spec = (
            TimingSpec(
                base_cast_time=2500,
                animation_lock=self.__blm_caster_tax_ms,
                application_delay=670,
            )
            if self._version < "7.0"
            else None
        )

        paradox_umbral_timing_spec = (
            TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=670,
            )
            if self._version < "7.0"
            else None
        )

        firestarter_follow_up = self.__get_firestart_follow_up()

        paradox_follow_up_skills = None
        if self._version >= "7.2":
            paradox_follow_up_skills = {
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Astral Fire": (firestarter_follow_up,),
                "2 Astral Fire": (firestarter_follow_up,),
                "3 Astral Fire": (firestarter_follow_up,),
            }
        elif self._version >= "7.0":
            paradox_follow_up_skills = {
                SimConsts.DEFAULT_CONDITION: (self.__enochian_buff_follow_up,),
                "1 Astral Fire": (
                    self.__enochian_buff_follow_up,
                    firestarter_follow_up,
                ),
                "2 Astral Fire": (
                    self.__enochian_buff_follow_up,
                    firestarter_follow_up,
                ),
                "3 Astral Fire": (
                    self.__enochian_buff_follow_up,
                    firestarter_follow_up,
                ),
            }
        else:
            paradox_follow_up_skills = {
                SimConsts.DEFAULT_CONDITION: (self.__enochian_buff_follow_up,),
                "Sharpcast": (
                    firestarter_follow_up,
                    self.__enochian_buff_follow_up,
                ),
            }
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: paradox_base_timing_spec,
                    "1 Astral Fire": paradox_base_timing_spec,
                    "2 Astral Fire": paradox_base_timing_spec,
                    "3 Astral Fire": paradox_base_timing_spec,
                    "1 Umbral Ice": paradox_umbral_timing_spec,
                    "2 Umbral Ice": paradox_umbral_timing_spec,
                    "3 Umbral Ice": paradox_umbral_timing_spec,
                }
                if self._version < "7.0"
                else TimingSpec(
                    base_cast_time=0,
                    animation_lock=self.__base_animation_lock,
                    application_delay=670,
                )
            ),
            job_resource_spec=(
                tuple()
                if self._version >= "7.2"
                else {
                    SimConsts.DEFAULT_CONDITION: tuple(),
                    "1 Astral Fire": (
                        JobResourceSpec(
                            name="Astral Fire",
                            change=+1,
                            refreshes_duration_of_last_gained=True,
                        ),
                    ),
                    "2 Astral Fire": (
                        JobResourceSpec(
                            name="Astral Fire",
                            change=+1,
                            refreshes_duration_of_last_gained=True,
                        ),
                    ),
                    "3 Astral Fire": (
                        JobResourceSpec(
                            name="Astral Fire",
                            change=+1,
                            refreshes_duration_of_last_gained=True,
                        ),
                    ),
                    "1 Umbral Ice": (
                        JobResourceSpec(
                            name="Umbral Ice",
                            change=+1,
                            refreshes_duration_of_last_gained=True,
                        ),
                    ),
                    "2 Umbral Ice": (
                        JobResourceSpec(
                            name="Umbral Ice",
                            change=+1,
                            refreshes_duration_of_last_gained=True,
                        ),
                    ),
                    "3 Umbral Ice": (
                        JobResourceSpec(
                            name="Umbral Ice",
                            change=+1,
                            refreshes_duration_of_last_gained=True,
                        ),
                    ),
                }
            ),
            follow_up_skills=paradox_follow_up_skills,
        )

    @GenericJobClass.is_a_skill
    def high_thunder(self):
        if self._level < 92:
            return None
        high_thunder_follow_up = FollowUp(
            skill=Skill(
                name="Thunder (dot)",
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency("High Thunder (dot)"),
                    damage_class=DamageClass.MAGICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=self._skill_data.get_skill_data(
                "High Thunder (dot)", "duration"
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
        )

        name = "High Thunder"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2500,
                animation_lock=self.__blm_caster_tax_ms,
                application_delay=760,
            ),
            follow_up_skills=(high_thunder_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def high_thunder_ii(self):
        if self._level < 92:
            return None
        high_thunder_ii_follow_up = FollowUp(
            skill=Skill(
                name="Thunder (dot)",
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency("High Thunder II (dot)"),
                    damage_class=DamageClass.MAGICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=self._skill_data.get_skill_data(
                "High Thunder II (dot)", "duration"
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
            primary_target_only=False,
        )
        name = "High Thunder II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2500,
                animation_lock=self.__blm_caster_tax_ms,
                application_delay=760,
            ),
            follow_up_skills=(high_thunder_ii_follow_up,),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def flare_star(self):
        if self._level < 100:
            return None
        name = "Flare Star"
        flare_star_damage_spec = self.__get_enochian_damage_spec_cross(
            base_potency=self._skill_data.get_potency(name), is_fire_spell=True
        )
        flare_star_timing_spec = self.__get_enochian_timing_spec_cross(
            base_cast_time=self._skill_data.get_skill_data(name, "cast_time"),
            is_fire_spell=True,
            application_delay=620,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=flare_star_damage_spec,
            timing_spec=flare_star_timing_spec,
            has_aoe=True,
            aoe_dropoff=0.65,
        )

    @GenericJobClass.is_a_skill
    def swiftcast(self):
        name = "Swiftcast"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=1,
                skill_allowlist=(
                    (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                    if self._version >= "7.1"
                    else (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Despair",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def triplecast(self):
        name = "Triplecast"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=3,
                skill_allowlist=(
                    (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                    if self._version >= "7.1"
                    else (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Despair",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def transpose(self):
        name = "Transpose"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
            buff_spec=(
                None
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: None,
                    "1 Umbral Ice": StatusEffectSpec(
                        expires_status_effects=("Enhanced",)
                    ),
                    "2 Umbral Ice": StatusEffectSpec(
                        expires_status_effects=("Enhanced",)
                    ),
                    "3 Umbral Ice": StatusEffectSpec(
                        expires_status_effects=("Enhanced",)
                    ),
                }
            ),
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Astral Fire": (
                    self.__clear_astral_fire,
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Astral Fire": (
                    self.__clear_astral_fire,
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Astral Fire": (
                    self.__clear_astral_fire,
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "1 Umbral Ice": (
                    self.__clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Umbral Ice": (
                    self.__clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Umbral Ice": (
                    self.__clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
            },
            follow_up_skills=(self.__enochian_buff_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def sharpcast(self):
        if self._version >= "7.0":
            return None
        name = "Sharpcast"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=(
                    "Scathe",
                    "Fire",
                    "Paradox",
                    "Thunder III",
                    "Thunder IV",
                ),
            ),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def manafont(self):
        name = "Manafont"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
            job_resource_spec=(
                (
                    self.__clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+3,
                        refreshes_duration_of_last_gained=True,
                    ),
                )
                if self._version >= "7.0"
                else tuple()
            ),
        )

    @GenericJobClass.is_a_skill
    def umbral_soul(self):
        name = "Umbral Soul"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
            job_resource_spec=(
                JobResourceSpec(
                    name="Umbral Ice",
                    change=+1,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def amplifier(self):
        name = "Amplifier"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__blm_instant_timing_spec,
        )
