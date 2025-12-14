from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.damage_instance_class import (
    DamageInstanceClass,
)
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.specs.channeling_spec import ChannelingSpec
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.shield_spec import ShieldSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import (
    OffensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.nin_data import (
    all_nin_skills,
)


class NinSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_nin_skills)
        self._job_class = "NIN"
        self.__all_bunshin_follow_ups = self.__get_all_bunshin_follow_ups()
        self.__ninjutsus = (
            "Fuma Shuriken",
            "Katon",
            "Raiton",
            "Hyoton",
            "Huton",
            "Doton",
            "Suiton",
        )
        self.__mudra_timing_spec = self.__get_mudra_timing_spec()

    def __get_mudra_timing_spec(self):
        return TimingSpec(
            base_cast_time=0,
            gcd_base_recast_time=500,
            affected_by_speed_stat=False,
            affected_by_haste_buffs=False,
            animation_lock=0,
        )

    def __get_all_bunshin_follow_ups(self):
        # TODO: this is bugged. We are setting delay_after_parent_application=88 and
        # not snapshotting with parent to mimic the 0.088s snapshot delay on anything
        # bunshin. This in return ignores when the damage actually comes out.
        BUNSHIN_MELEE_POTENCY = self._skill_data.get_skill_data(
            "Bunshin", "potency_melee"
        )
        BUNSHIN_RANGED_POTENCY = self._skill_data.get_skill_data(
            "Bunshin", "potency_ranged"
        )
        BUNSHIN_AREA_POTENCY = self._skill_data.get_skill_data(
            "Bunshin", "potency_area"
        )
        bunshin_follow_ups = [
            ("Spinning Edge", BUNSHIN_MELEE_POTENCY, True),
            ("Gust Slash", BUNSHIN_MELEE_POTENCY, True),
            ("Aeolian Edge", BUNSHIN_MELEE_POTENCY, True),
            ("Armor Crush", BUNSHIN_MELEE_POTENCY, True),
            ("Forked Raiju", BUNSHIN_MELEE_POTENCY, True),
            ("Fleeting Raiju", BUNSHIN_MELEE_POTENCY, True),
            ("Huraijin", BUNSHIN_MELEE_POTENCY, True),
            ("Throwing Dagger", BUNSHIN_RANGED_POTENCY, True),
            ("Hakke Mujinsatsu", BUNSHIN_AREA_POTENCY, False),
            ("Death Blossom", BUNSHIN_AREA_POTENCY, False),
        ]
        all_bunshin_follow_ups = {}
        for sk, bunshin_potency, primary_target_only in bunshin_follow_ups:
            all_bunshin_follow_ups[sk] = FollowUp(
                skill=Skill(
                    name=f"{sk} (pet)",
                    damage_spec=DamageSpec(
                        potency=bunshin_potency,
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                    ),
                    status_effect_denylist=("Dragon Sight",),
                ),
                delay_after_parent_application=88,
                snapshot_buffs_with_parent=False,
                snapshot_debuffs_with_parent=False,
                primary_target_only=primary_target_only,
            )
        return all_bunshin_follow_ups

    @GenericJobClass.is_a_resource
    def kazematoi(self):
        if self._version < "7.0":
            return None
        name = "Kazematoi"
        job_resource_settings = JobResourceSettings(
            max_value=5,
            skill_allowlist=("Aeolian Edge", "Armor Crush"),
            add_number_to_conditional=False,
        )
        return (name, job_resource_settings)

    def __get_hollow_nozuchi_follow_up(self):
        name = "Hollow Nozuchi"
        res = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=0,
        )
        return res

    def __get_huton_follow_up_huton(self):
        if self._version >= "7.0":
            return None
        name = "Huton (Huton)"
        return FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    haste_time_reduction=0.15,
                    auto_attack_delay_reduction=0.15,
                    duration=60 * 1000,
                    max_duration=60 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )

    def __get_huton_follow_up_hakke(self):
        if self._version >= "7.0":
            return None
        name = "Huton (Hakke)"
        return FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    haste_time_reduction=0.15,
                    auto_attack_delay_reduction=0.15,
                    duration=10 * 1000,
                    max_duration=60 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )

    def __get_huton_follow_up_armor_crush(self):
        name = "Huton (Armor Crush)"
        return FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    haste_time_reduction=0.15,
                    auto_attack_delay_reduction=0.15,
                    duration=30 * 1000,
                    max_duration=60 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )

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

    @GenericJobClass.is_a_skill
    def dream_within_a_dream(self):
        name = "Dream Within a Dream"
        _dream_follow_ups = (
            FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                ),
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=False,
                delay_after_parent_application=700,
            ),
            FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                ),
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=False,
                delay_after_parent_application=850,
            ),
            FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                ),
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=False,
                delay_after_parent_application=1000,
            ),
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            follow_up_skills=_dream_follow_ups,
        )

    @GenericJobClass.is_a_skill
    def doton(self):
        name = "Doton (dot)"
        # make follow-up so we can control snapshotting of debuffs as a ground dot
        doton_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    damage_class=DamageClass.PHYSICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=self._skill_data.get_skill_data(name, "duration"),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )
        name = "Doton"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=self._skill_data.get_skill_data("Doton (dot)", "duration"),
            ),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=1300,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=1300,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
            follow_up_skills=(doton_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def hollow_nozuchi(self):
        name = "Hollow Nozuchi"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
        )

    @GenericJobClass.is_a_skill
    def spinning_edge(self):
        name = "Spinning Edge"
        spinning_edge_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=400,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (spinning_edge_follow_up,),
                "Bunshin": (
                    self.__all_bunshin_follow_ups["Spinning Edge"],
                    spinning_edge_follow_up,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def gust_slash(self):
        name = "Gust Slash"
        gust_slash_damage_follow_up = FollowUp(
            Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=400,
        )
        gust_slash_damage_no_combo_follow_up = FollowUp(
            Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=400,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Spinning Edge",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (gust_slash_damage_follow_up,),
                "No Combo": (gust_slash_damage_no_combo_follow_up,),
                "Bunshin": (
                    self.__all_bunshin_follow_ups["Gust Slash"],
                    gust_slash_damage_follow_up,
                ),
                "Bunshin, No Combo": (
                    self.__all_bunshin_follow_ups["Gust Slash"],
                    gust_slash_damage_no_combo_follow_up,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def throwing_dagger(self):
        name = "Throwing Dagger"
        throwing_dagger_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=620,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (throwing_dagger_follow_up,),
                "Bunshin": (
                    throwing_dagger_follow_up,
                    self.__all_bunshin_follow_ups["Throwing Dagger"],
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def mug(self):
        if self._version >= "7.0":
            return None
        name = "Mug"
        mug_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=620,
        )
        mug_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                offensive_debuff_spec=OffensiveStatusEffectSpec(
                    damage_mult=1.05,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                    is_party_effect=True,
                ),
            ),
            delay_after_parent_application=0,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    mug_damage_follow_up,
                    mug_debuff_follow_up,
                ),
                "Debuff Only": (mug_debuff_follow_up,),
            },
            off_class_default_condition="Debuff Only",
        )

    @GenericJobClass.is_a_skill
    def trick_attack(self):
        if self._level >= 92:
            return None
        name = "Trick Attack"
        trick_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=800,
        )
        trick_damage_no_pos_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
            ),
            delay_after_parent_application=800,
        )
        trick_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                offensive_debuff_spec=OffensiveStatusEffectSpec(
                    damage_mult=1.10, duration=int(15.77 * 1000)
                ),
            ),
            delay_after_parent_application=0,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    trick_damage_follow_up,
                    trick_debuff_follow_up,
                ),
                "No Positional": (
                    trick_damage_no_pos_follow_up,
                    trick_debuff_follow_up,
                ),
            },
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def aeolian_edge(self):
        name = "Aeolian Edge"
        aeolian_edge_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=540,
        )
        aeolian_edge_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=540,
        )
        aeolian_edge_no_pos_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
            ),
            delay_after_parent_application=540,
        )
        aeolian_edge_no_pos_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_no_combo"
                    )
                ),
            ),
            delay_after_parent_application=540,
        )
        if self._version >= "7.0":
            potency_increment_kaz = self._skill_data.get_skill_data(
                name, "potency_increment_kaz"
            )
            # kaz. this is ugly, we can do better.
            aeolian_edge_follow_up_kaz = FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec=DamageSpec(
                        self._skill_data.get_potency(name) + potency_increment_kaz
                    ),
                ),
                delay_after_parent_application=540,
            )
            aeolian_edge_no_combo_follow_up_kaz = FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec=DamageSpec(
                        self._skill_data.get_potency_no_combo(name)
                        + potency_increment_kaz
                    ),
                ),
                delay_after_parent_application=540,
            )
            aeolian_edge_no_pos_follow_up_kaz = FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec=DamageSpec(
                        self._skill_data.get_potency_no_positional(name)
                        + potency_increment_kaz
                    ),
                ),
                delay_after_parent_application=540,
            )
            aeolian_edge_no_pos_no_combo_follow_up_kaz = FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec=DamageSpec(
                        self._skill_data.get_skill_data(name, "potency_no_pos_no_combo")
                        + potency_increment_kaz
                    ),
                ),
                delay_after_parent_application=540,
            )
        aoelian_follow_ups = {
            SimConsts.DEFAULT_CONDITION: (aeolian_edge_follow_up,),
            "No Combo": (aeolian_edge_no_combo_follow_up,),
            "No Positional": (aeolian_edge_no_pos_follow_up,),
            "No Combo, No Positional": (aeolian_edge_no_pos_no_combo_follow_up,),
            "Bunshin": (
                aeolian_edge_follow_up,
                self.__all_bunshin_follow_ups["Aeolian Edge"],
            ),
            "Bunshin, No Combo": (
                aeolian_edge_no_combo_follow_up,
                self.__all_bunshin_follow_ups["Aeolian Edge"],
            ),
            "Bunshin, No Positional": (
                aeolian_edge_no_pos_follow_up,
                self.__all_bunshin_follow_ups["Aeolian Edge"],
            ),
            "Bunshin, No Combo, No Positional": (
                aeolian_edge_no_pos_no_combo_follow_up,
                self.__all_bunshin_follow_ups["Aeolian Edge"],
            ),
        }
        if self._version >= "7.0":
            aoelian_follow_ups_100_only = {
                "Kazematoi": (aeolian_edge_follow_up_kaz,),
                "Kazematoi, No Combo": (aeolian_edge_no_combo_follow_up_kaz,),
                "Kazematoi, No Positional": (aeolian_edge_no_pos_follow_up_kaz,),
                "Kazematoi, No Combo, No Positional": (
                    aeolian_edge_no_pos_no_combo_follow_up_kaz,
                ),
                "Bunshin, Kazematoi": (
                    aeolian_edge_follow_up_kaz,
                    self.__all_bunshin_follow_ups["Aeolian Edge"],
                ),
                "Bunshin, Kazematoi, No Combo": (
                    aeolian_edge_no_combo_follow_up_kaz,
                    self.__all_bunshin_follow_ups["Aeolian Edge"],
                ),
                "Bunshin, Kazematoi, No Positional": (
                    aeolian_edge_no_pos_follow_up_kaz,
                    self.__all_bunshin_follow_ups["Aeolian Edge"],
                ),
                "Bunshin, Kazematoi, No Combo, No Positional": (
                    aeolian_edge_no_pos_no_combo_follow_up_kaz,
                    self.__all_bunshin_follow_ups["Aeolian Edge"],
                ),
            }
            aoelian_follow_ups = aoelian_follow_ups | aoelian_follow_ups_100_only
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            job_resource_spec=(
                (JobResourceSpec(name="Kazematoi", change=-1),)
                if self._version >= "7.0"
                else tuple()
            ),
            follow_up_skills=aoelian_follow_ups,
        )

    @GenericJobClass.is_a_skill
    def death_blossom(self):
        name = "Death Blossom"
        death_blossom_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
            ),
            delay_after_parent_application=710,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (death_blossom_follow_up,),
                "Bunshin": (
                    death_blossom_follow_up,
                    self.__all_bunshin_follow_ups["Death Blossom"],
                ),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def hakke_mujinsatsu(self):
        hollow_nozuchi_follow_up = self.__get_hollow_nozuchi_follow_up()
        name = "Hakke Mujinsatsu"
        hakke_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
            ),
            delay_after_parent_application=620,
            primary_target_only=False,
        )
        hakke_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
                has_aoe=True,
            ),
            delay_after_parent_application=620,
            primary_target_only=False,
        )
        huton_follow_up_hakke = self.__get_huton_follow_up_hakke()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Death Blossom",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    (hakke_follow_up,)
                    if self._version >= "7.0"
                    else (huton_follow_up_hakke, hakke_follow_up)
                ),
                "No Combo": (hakke_no_combo_follow_up,),
                "Bunshin": (
                    (
                        self.__all_bunshin_follow_ups["Hakke Mujinsatsu"],
                        hakke_follow_up,
                    )
                    if self._version >= "7.0"
                    else (
                        huton_follow_up_hakke,
                        self.__all_bunshin_follow_ups["Hakke Mujinsatsu"],
                        hakke_follow_up,
                    )
                ),
                "Bunshin, No Combo": (
                    self.__all_bunshin_follow_ups["Hakke Mujinsatsu"],
                    hakke_no_combo_follow_up,
                ),
                "Doton": (
                    (hakke_follow_up, hollow_nozuchi_follow_up)
                    if self._version >= "7.0"
                    else (
                        huton_follow_up_hakke,
                        hakke_follow_up,
                        hollow_nozuchi_follow_up,
                    )
                ),
                "Doton, No Combo": (hakke_no_combo_follow_up, hollow_nozuchi_follow_up),
                "Doton, Bunshin": (
                    (
                        self.__all_bunshin_follow_ups["Hakke Mujinsatsu"],
                        hakke_follow_up,
                        hollow_nozuchi_follow_up,
                    )
                    if self._version >= "7.0"
                    else (
                        huton_follow_up_hakke,
                        self.__all_bunshin_follow_ups["Hakke Mujinsatsu"],
                        hakke_follow_up,
                        hollow_nozuchi_follow_up,
                    )
                ),
                "Bunshin, Doton, No Combo": (
                    self.__all_bunshin_follow_ups["Hakke Mujinsatsu"],
                    hakke_no_combo_follow_up,
                    hollow_nozuchi_follow_up,
                ),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def armor_crush(self):
        name = "Armor Crush"
        armor_crush_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=620,
        )
        armor_crush_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=620,
        )
        armor_crush_no_pos_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
            ),
            delay_after_parent_application=620,
        )
        armor_crush_no_pos_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_no_combo"
                    )
                ),
            ),
            delay_after_parent_application=620,
        )
        huton_follow_up_armor_crush = self.__get_huton_follow_up_armor_crush()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Gust Slash",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            job_resource_spec=self._skill_data.get_skill_data(name, "job_resource"),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    (armor_crush_follow_up,)
                    if self._version >= "7.0"
                    else (
                        armor_crush_follow_up,
                        huton_follow_up_armor_crush,
                    )
                ),
                "No Combo": (armor_crush_no_combo_follow_up,),
                "No Positional": (
                    (armor_crush_no_pos_follow_up,)
                    if self._version >= "7.0"
                    else (
                        armor_crush_no_pos_follow_up,
                        huton_follow_up_armor_crush,
                    )
                ),
                "No Combo, No Positional": (armor_crush_no_pos_no_combo_follow_up,),
                "Bunshin": (
                    (
                        armor_crush_follow_up,
                        self.__all_bunshin_follow_ups["Armor Crush"],
                    )
                    if self._version >= "7.0"
                    else (
                        armor_crush_follow_up,
                        huton_follow_up_armor_crush,
                        self.__all_bunshin_follow_ups["Armor Crush"],
                    )
                ),
                "Bunshin, No Combo": (
                    armor_crush_no_combo_follow_up,
                    self.__all_bunshin_follow_ups["Armor Crush"],
                ),
                "Bunshin, No Positional": (
                    (
                        armor_crush_no_pos_follow_up,
                        self.__all_bunshin_follow_ups["Armor Crush"],
                    )
                    if self._version >= "7.0"
                    else (
                        armor_crush_no_pos_follow_up,
                        huton_follow_up_armor_crush,
                        self.__all_bunshin_follow_ups["Armor Crush"],
                    )
                ),
                "Bunshin, No Combo, No Positional": (
                    armor_crush_no_pos_no_combo_follow_up,
                    self.__all_bunshin_follow_ups["Armor Crush"],
                ),
            },
        )

    # for logs processing convenience
    @GenericJobClass.is_a_skill
    def dokumori_debuff(self):
        if self._version <= "6.55":
            return None

        return Skill(
            name="Dokumori (Debuff Only)",
            offensive_debuff_spec=OffensiveStatusEffectSpec(
                damage_mult=1.05,
                duration=self._skill_data.get_skill_data("Dokumori", "duration"),
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def dokumori(self):
        if self._version <= "6.55":
            return None

        name = "Dokumori"
        dokumori_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                offensive_debuff_spec=OffensiveStatusEffectSpec(
                    damage_mult=1.05,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                    is_party_effect=True,
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=False,
        )
        dokumori_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    )
                },
                has_aoe=True if self._version >= "7.1" else False,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=1070,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    dokumori_damage_follow_up,
                    dokumori_debuff_follow_up,
                ),
                "Debuff Only": (dokumori_debuff_follow_up,),
            },
            off_class_default_condition="Debuff Only",
            has_aoe=True if self._version >= "7.1" else False,
        )

    @GenericJobClass.is_a_skill
    def huraijin(self):
        if self._version > "6.55":
            return None
        huton_follow_up_huton = self.__get_huton_follow_up_huton()
        name = "Huraijin"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (huton_follow_up_huton,),
                "Bunshin": (
                    huton_follow_up_huton,
                    self.__all_bunshin_follow_ups["Huraijin"],
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def hellfrog_medium(self):
        name = "Hellfrog Medium"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def bhavacakra(self):
        name = "Bhavacakra"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Meisui": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_mesui")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def phantom_kamaitachi(self):
        name = "Phantom Kamaitachi (pet)"

        hollow_nozuchi_follow_up = self.__get_hollow_nozuchi_follow_up()
        phantom_follow_up_damage = FollowUp(
            skill=Skill(
                name=name,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                    )
                },
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=1560,
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
            primary_target_only=False,
        )
        name = "Phantom Kamaitachi"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(base_cast_time=0),
            status_effect_denylist=("Dragon Sight",),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (phantom_follow_up_damage,),
                "Doton": (phantom_follow_up_damage, hollow_nozuchi_follow_up),
            },
        )

    @GenericJobClass.is_a_skill
    def forked_raiju(self):
        name = "Forked Raiju"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (self.__all_bunshin_follow_ups["Forked Raiju"],),
            },
        )

    @GenericJobClass.is_a_skill
    def fleeting_raiju(self):
        name = "Fleeting Raiju"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Bunshin": (self.__all_bunshin_follow_ups["Fleeting Raiju"],),
            },
        )

    @GenericJobClass.is_a_skill
    def fuma_shuriken(self):
        name = "Fuma Shuriken"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=890,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=890,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def katon(self):
        name = "Katon"

        hollow_nozuchi_follow_up = self.__get_hollow_nozuchi_follow_up()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=940,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=940,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (),
                "Doton": (hollow_nozuchi_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def raiton(self):
        name = "Raiton"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=710,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=710,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def hyoton(self):
        name = "Hyoton"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=1160,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=1160,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def huton(self):
        name = "Huton"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=self._skill_data.get_skill_data(name, "damage_spec"),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    application_delay=0,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=0,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
            follow_up_skills=(
                (self.__get_huton_follow_up_huton(),)
                if self._version == "6.55"
                else tuple()
            ),
        )

    @GenericJobClass.is_a_skill
    def suiton(self):
        name = "Suiton"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1500,
                    #  application_delay=0,
                    application_delay=980,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                "Ten Chi Jin": TimingSpec(
                    base_cast_time=0,
                    gcd_base_recast_time=1000,
                    application_delay=980,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def goka_mekkyaku(self):
        name = "Goka Mekkyaku"

        hollow_nozuchi_follow_up = self.__get_hollow_nozuchi_follow_up()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=760,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (),
                "Doton": (hollow_nozuchi_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def hyosho_ranryu(self):
        name = "Hyosho Ranryu"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                application_delay=620,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )

    @GenericJobClass.is_a_skill
    def bunshin(self):
        name = "Bunshin"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=5,
                duration=int(30.7 * 1000),
                skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
            ),
        )

    @GenericJobClass.is_a_skill
    def ten_chi_jin(self):
        name = "Ten Chi Jin"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=3,
                duration=6000,
                skill_allowlist=self.__ninjutsus,
            ),
            channeling_spec=ChannelingSpec(
                duration=6000, skill_allowlist=self.__ninjutsus, num_uses=3
            ),
        )

    @GenericJobClass.is_a_skill
    def meisui(self):
        name = "Meisui"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
            ),
        )

    @GenericJobClass.is_a_skill
    def kunais_bane(self):
        if self._level < 92:
            return None
        name = "Kunai's Bane"
        kunai_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=1290,
            primary_target_only=False,
        )
        kunai_debuff_follow_up = FollowUp(
            skill=Skill(
                name=name,
                offensive_debuff_spec=OffensiveStatusEffectSpec(
                    damage_mult=1.10,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(kunai_damage_follow_up, kunai_debuff_follow_up),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def deathfrog_medium(self):
        if self._level < 96:
            return None
        name = "Deathfrog Medium"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )

    @GenericJobClass.is_a_skill
    def zesho_meppo(self):
        if self._level < 96:
            return None
        name = "Zesho Meppo"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Meisui": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_mesui")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
        )

    @GenericJobClass.is_a_skill
    def tenri_jindo(self):
        if self._level < 100:
            return None
        name = "Tenri Jindo"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1690
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def kassatsu(self):
        name = "Kassatsu"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=15 * 1000,
                damage_mult=1.3,
                skill_allowlist=(
                    "Fuma Shuriken",
                    "Raiton",
                    "Doton",
                    "Suiton",
                    "Goka Mekkyaku",
                    "Huton",
                    "Hyosho Ranryu",
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def shade_shift(self):
        name = "Shade Shift"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            shield_spec=ShieldSpec(
                shield_on_max_hp=0.2, duration=20 * 1000, is_party_effect=False
            ),
        )

    @GenericJobClass.is_a_skill
    def feint(self):
        name = "Feint"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_debuff_spec=DefensiveStatusEffectSpec(
                damage_reductions={
                    DamageInstanceClass.PHYSICAL: 0.1,
                    DamageInstanceClass.MAGICAL: 0.05,
                },
                duration=15 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def second_wind(self):
        name = "Second Wind"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=800),
        )

    @GenericJobClass.is_a_skill
    def bloodbath(self):
        name = "Bloodbath"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            # TODO: add defensive spec
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    # Ten, Chi, Jin are "gcds" or act like it, but they are technically abilities.
    @GenericJobClass.is_a_skill
    def ten(self):
        name = "Ten"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.ABILITY,  # Mudras are actually "Ability" skills
            timing_spec=self.__mudra_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def chi(self):
        name = "Chi"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.ABILITY,  # Mudras are actually "Ability" skills
            timing_spec=self.__mudra_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def jin(self):
        name = "Jin"
        return Skill(
            name=name,
            is_GCD=True,  # Mudras are actually "Ability" skills
            skill_type=SkillType.ABILITY,
            timing_spec=self.__mudra_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def true_north(self):
        name = "True North"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def hide(self):
        name = "Hide"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )
