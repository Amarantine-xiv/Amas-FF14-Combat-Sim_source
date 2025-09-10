from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.damage_instance_class import (
    DamageInstanceClass,
)
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import (
    OffensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.specs.trigger_spec import TriggerSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.sam_data import (
    all_sam_skills,
)


class SamSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_sam_skills)
        self._job_class = "SAM"

    def __get_fugetsu_follow_up(self):
        name = "Fugetsu"
        return FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    damage_mult=1.13, duration=40000
                ),
            ),
            delay_after_parent_application=650,
        )

    def __get_fuka_follow_up(self):
        name = "Fuka"
        return FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    haste_time_reduction=0.13,
                    auto_attack_delay_reduction=0.13,
                    duration=40000,
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
    def hakaze(self):
        if self._level >= 92:
            return None
        name = "Hakaze"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def gyofu(self):
        if self._level < 92:
            return None
        name = "Gyofu"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=850
            ),
        )

    @GenericJobClass.is_a_skill
    def jinpu(self):
        name = "Jinpu"
        jinpu_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=620,
        )
        jinpu_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=620,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (
                    ComboSpec(
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "No Combo": (
                    ComboSpec(
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "Meikyo Shisui": (
                    ComboSpec(
                        combo_auto_succeed=True,
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        ),
                    ),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    jinpu_follow_up,
                    self.__get_fugetsu_follow_up(),
                ),
                "No Combo": (jinpu_no_combo_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def enpi(self):
        name = "Enpi"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Enhanced Enpi": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_enhanced")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=710
            ),
        )

    @GenericJobClass.is_a_skill
    def hissatsu_yaten(self):
        enhanced_enpi_follow_up = FollowUp(
            skill=Skill(
                name="Enhanced Enpi",
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=15 * 1000,
                    skill_allowlist=("Enpi",),
                ),
            ),
            delay_after_parent_application=0,
        )

        name = "Hissatsu: Yaten"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=450
            ),
            follow_up_skills=(enhanced_enpi_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def shifu(self):
        name = "Shifu"
        shifu_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=800,
        )
        shifu_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=800,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (
                    ComboSpec(
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "No Combo": (
                    ComboSpec(
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "Meikyo Shisui": (
                    ComboSpec(
                        combo_auto_succeed=True,
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        ),
                    ),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    shifu_follow_up,
                    self.__get_fuka_follow_up(),
                ),
                "No Combo": (shifu_no_combo_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def gekko(self):
        name = "Gekko"
        gekko_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=760,
        )
        gekko_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=760,
        )
        gekko_no_pos_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
            ),
            delay_after_parent_application=760,
        )
        gekko_no_pos_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_no_combo"
                    )
                ),
            ),
            delay_after_parent_application=760,
        )
        fugetsu_follow_up = self.__get_fugetsu_follow_up()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Jinpu",)),),
                "No Combo": (ComboSpec(combo_actions=("Jinpu",)),),
                "No Positional": (ComboSpec(combo_actions=("Jinpu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Jinpu",)),
                ),
                "No Positional, Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Jinpu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (gekko_follow_up,),
                "No Combo, No Positional": (gekko_no_pos_no_combo_follow_up,),
                "No Combo": (gekko_no_combo_follow_up,),
                "No Positional": (gekko_no_pos_follow_up,),
                "Meikyo Shisui": (gekko_follow_up, fugetsu_follow_up),
                "Meikyo Shisui, No Combo, No Positional": (
                    gekko_no_pos_follow_up,
                    fugetsu_follow_up,
                ),
                "Meikyo Shisui, No Combo": (gekko_follow_up, fugetsu_follow_up),
                "Meikyo Shisui, No Positional": (
                    gekko_no_pos_follow_up,
                    fugetsu_follow_up,
                ),
            },
        )

    def __get_iaijutsu_timing(self):
        return TimingSpec(
            base_cast_time=1300,
            affected_by_speed_stat=False,
            affected_by_haste_buffs=False,
            animation_lock=0,
            application_delay=620,
        )

    def __get_higanbana_follow_up(self):
        name = "Higanbana (dot)"
        return FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    damage_class=DamageClass.PHYSICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=60 * 1000,
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
        )

    @GenericJobClass.is_a_skill
    def higanbana(self):
        name = "Higanbana"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=self.__get_iaijutsu_timing(),
            follow_up_skills=(self.__get_higanbana_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def tenka_goken(self):
        name = "Tenka Goken"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=self.__get_iaijutsu_timing(),
        )

    @GenericJobClass.is_a_skill
    def midare_setsugekka(self):
        name = "Midare Setsugekka"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=self.__get_iaijutsu_timing(),
        )

    @GenericJobClass.is_a_skill
    def kaeshi_higanbana(self):
        if self._version > "6.55":
            return None
        name = "Kaeshi: Higanbana"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=self.instant_timing_spec,
            follow_up_skills=(self.__get_higanbana_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def kaeshi_goken(self):
        name = "Kaeshi: Goken"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def kaeshi_setsugekka(self):
        name = "Kaeshi: Setsugekka"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def mangetsu(self):
        name = "Mangetsu"
        magnetsu_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
            ),
            delay_after_parent_application=620,
            primary_target_only=False,
        )
        magnetsu_no_combo_follow_up = FollowUp(
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
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Fuko",)),),
                "No Combo": (ComboSpec(combo_actions=("Fuko",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Fuko",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    magnetsu_follow_up,
                    self.__get_fugetsu_follow_up(),
                ),
                "No Combo": (magnetsu_no_combo_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def kasha(self):
        name = "Kasha"
        kasha_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=620,
        )
        kasha_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=620,
        )
        kasha_no_pos_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
            ),
            delay_after_parent_application=620,
        )
        kasha_no_pos_no_combo_follow_up = FollowUp(
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
        fuka_follow_up = self.__get_fuka_follow_up()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Shifu",)),),
                "No Combo": (ComboSpec(combo_actions=("Shifu",)),),
                "No Positional": (ComboSpec(combo_actions=("Shifu",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Shifu",)),
                ),
                "No Positional, Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Shifu",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (kasha_follow_up,),
                "No Combo, No Positional": (kasha_no_pos_no_combo_follow_up,),
                "No Combo": (kasha_no_combo_follow_up,),
                "No Positional": (kasha_no_pos_follow_up,),
                "Meikyo Shisui": (kasha_follow_up, fuka_follow_up),
                "Meikyo Shisui, No Combo, No Positional": (
                    kasha_no_pos_follow_up,
                    fuka_follow_up,
                ),
                "Meikyo Shisui, No Combo": (kasha_follow_up, fuka_follow_up),
                "Meikyo Shisui, No Positional": (
                    kasha_no_pos_follow_up,
                    fuka_follow_up,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def oka(self):
        name = "Oka"
        oka_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
            ),
            delay_after_parent_application=620,
            primary_target_only=False,
        )
        oka_no_combo_follow_up = FollowUp(
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
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            ignored_conditions_for_bonus_potency=("Meikyo Shisui",),
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (ComboSpec(combo_actions=("Fuko",)),),
                "No Combo": (ComboSpec(combo_actions=("Fuko",)),),
                "Meikyo Shisui": (
                    ComboSpec(combo_auto_succeed=True, combo_actions=("Fuko",)),
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    oka_follow_up,
                    self.__get_fuka_follow_up(),
                ),
                "No Combo": (oka_no_combo_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def yukikaze(self):
        name = "Yukikaze"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec={
                SimConsts.DEFAULT_CONDITION: (
                    ComboSpec(
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
                "Meikyo Shisui": (
                    ComboSpec(
                        combo_auto_succeed=True,
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        ),
                    ),
                ),
                "No Combo": (
                    ComboSpec(
                        combo_actions=self._skill_data.get_skill_data(
                            name, "combo_actions"
                        )
                    ),
                ),
            },
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )

    @GenericJobClass.is_a_skill
    def hissatsu_shinten(self):
        name = "Hissatsu: Shinten"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def hissatsu_gyoten(self):
        name = "Hissatsu: Gyoten"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )

    @GenericJobClass.is_a_skill
    def hissatsu_kyuten(self):
        name = "Hissatsu: Kyuten"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def hissatsu_guren(self):
        name = "Hissatsu: Guren"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def hissatsu_senei(self):
        name = "Hissatsu: Senei"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )

    @GenericJobClass.is_a_skill
    def shoha(self):
        name = "Shoha"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def shoha_ii(self):
        if self._version > "6.55":
            return None
        name = "Shoha II"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )

    @GenericJobClass.is_a_skill
    def fuko(self):
        name = "Fuko"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def ogi_namikiri(self):
        name = "Ogi Namikiri"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=1300,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
                application_delay=490,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def kaeshi_namikiri(self):
        name = "Kaeshi: Namikiri"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def zanshin(self):
        if self._level < 96:
            return None
        name = "Zanshin"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1030
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def tendo_goken(self):
        if self._level < 100:
            return None
        name = "Tendo Goken"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1300, animation_lock=650, application_delay=360
            ),
        )

    @GenericJobClass.is_a_skill
    def tendo_setsugekka(self):
        if self._level < 100:
            return None
        name = "Tendo Setsugekka"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=1300,
                animation_lock=650,
                application_delay=1030,
                gcd_base_recast_time=self._skill_data.get_skill_data(
                    name, "gcd_base_recast_time"
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def tendo_kaeshi_goken(self):
        if self._level < 100:
            return None
        name = "Tendo Kaeshi Goken"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=360
            ),
        )

    @GenericJobClass.is_a_skill
    def tendo_kaeshi_setsugekka(self):
        if self._level < 100:
            return None
        name = "Tendo Kaeshi Setsugekka"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1030,
                gcd_base_recast_time=self._skill_data.get_skill_data(
                    name, "gcd_base_recast_time"
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def tengentsu_foresight(self):
        name = "Tengentsu's Foresight"

        # TODO: this actually only triggers on hit.
        # How to link back?
        return (
            Skill(
                name=f"{name}",
                is_GCD=False,
                skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
                timing_spec=self.uncontrolled_timing_spec,
                defensive_buff_spec=DefensiveStatusEffectSpec(
                    damage_reductions=0.1,
                    duration=9 * 1000,
                ),
                heal_spec=HealSpec(hot_potency=200, duration=9 * 1000),
            ),
        )

    @GenericJobClass.is_a_skill
    def tengentsu(self):
        name = "Tengentsu"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=4 * 1000,
                num_uses=1,
            ),
            trigger_spec=TriggerSpec(triggers=("Tengentsu's Foresight",)),
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
    def meikyo_shisui(self):
        name = "Meikyo Shisui"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=3,
                duration=int(self._skill_data.get_skill_data(name, "duration")),
                skill_allowlist=(
                    "Hakaze",
                    "Jinpu",
                    "Shifu",
                    "Gekko",
                    "Mangetsu",
                    "Kasha",
                    "Oka",
                    "Yukikaze",
                    "Fuko",
                ),
            ),
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
    def hagakure(self):
        name = "Hagakure"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def ikishoten(self):
        name = "Ikishoten"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
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
