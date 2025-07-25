from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.vpr_data import (
    all_vpr_skills,
)


class VprSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_vpr_skills)
        self._job_class = "VPR"

        # these are based off of pre-trait dread fang. IDK man, idk.
        self.__combo_base_potency_no_venom = self._skill_data.get_skill_data(
            "Combo Base", "potency_no_venom"
        )

        self.__combo_base_potency_with_venom = self._skill_data.get_skill_data(
            "Combo Base", "potency_venom"
        )

    def get_combo_breakers(self):
        # combo groups
        # 0: Hunter's coil -> twinfang bite. GCD->oGCD combo
        # 1: Swiftskin's Coil -> twinblood bite. GCD->oGCD combo
        # 2: Hunter's Den -> Twinfang Thresh. GCD->oGCD combo
        # 3: Swiftskin's Den -> Twinblood Thresh GCD->oGCD combo
        # 4: Reawaken sequence. Sequence of GCD->(oGCD) combos
        return (
            (0, (1, 2, 3, 4)),
            (1, (0, 2, 3, 4)),
            (2, (0, 1, 3, 4)),
            (3, (0, 1, 2, 4)),
            (4, (0, 1, 2, 3)),
        )

    # All Venoms that expire other venoms:
    # "Hindstung Venom", "Hindsbane Venom", "Flanksbane Venom",
    # "Flankstung Venom", "Grimskin's Venom", "Grimhunter's Venom"
    def __get_venom_follow_up(
        self,
        name,
        skill_allowlist,
        duration,
        expires_status_effects=tuple(),
        delay_after_parent_application=0,
    ):
        return FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=duration,
                    num_uses=1,
                    skill_allowlist=skill_allowlist,
                    expires_status_effects=expires_status_effects,
                ),
            ),
            delay_after_parent_application=delay_after_parent_application,
            primary_target_only=True,
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
    def steel_fangs(self):

        honed_reavers_follow_up = (
            FollowUp(
                skill=Skill(
                    name="Honed Reavers",
                    buff_spec=StatusEffectSpec(
                        add_to_skill_modifier_condition=True,
                        duration=60 * 1000,
                        num_uses=1,
                        skill_allowlist=("Reaving Fangs", "Reaving Maw"),
                        expires_status_effects=("Honed Steel",),
                    ),
                ),
                delay_after_parent_application=0,
                primary_target_only=True,
            )
            if self._version >= "7.05"
            else None
        )

        name = "Steel Fangs"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=self._skill_data.get_skill_data(name, "damage_spec"),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            follow_up_skills=(
                (honed_reavers_follow_up,) if self._version >= "7.05" else tuple()
            ),
        )

    def __get_hunters_instinct_follow_up(self):
        name = "Hunter's Instinct"
        return FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.10,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    @GenericJobClass.is_a_skill
    def hunters_sting(self):
        name = "Hunter's Sting"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
            follow_up_skills=(self.__get_hunters_instinct_follow_up(),),
        )

    def __get_noxious_gnash_follow_up(self):
        if self._version >= "7.05":
            return None
        name = "Noxious Gnash"
        return FollowUp(
            skill=Skill(
                name=name,
                debuff_spec=StatusEffectSpec(
                    damage_mult=1.10,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                    max_duration=self._skill_data.get_skill_data(name, "max_duration"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    def __get_honed_steel_follow_up(self):
        if self._version <= "7.01":
            return None
        name = "Honed Steel"
        return FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=60 * 1000,
                    num_uses=1,
                    skill_allowlist=("Steel Fangs", "Steel Maw"),
                    expires_status_effects=("Honed Reavers",),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    @GenericJobClass.is_a_skill
    def dread_fangs(self):
        if self._version >= "7.05":
            return None
        name = "Dread Fangs"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills=(self.__get_noxious_gnash_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def reaving_fangs(self):
        if self._version <= "7.01":
            return None
        name = "Reaving Fangs"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Honed Reavers": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_honed_reavers"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills=(self.__get_honed_steel_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def writhing_snap(self):
        name = "Writhing Snap"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=490
            ),
        )

    def __get_swift_scaled_follow_up(self):
        name = "Swiftscaled"
        return FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    haste_time_reduction=0.15,
                    auto_attack_delay_reduction=0.15,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    @GenericJobClass.is_a_skill
    def swiftskins_sting(self):
        name = "Swiftskin's Sting"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            follow_up_skills=(self.__get_swift_scaled_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def steel_maw(self):
        name = "Steel Maw"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1020
            ),
            damage_spec=self._skill_data.get_skill_data(name, "damage_spec"),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def flanksting_strike(self):
        venom_name = "Hindstung Venom"
        hindstung_venom_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Hindsting Strike",),
            self._skill_data.get_skill_data(venom_name, "duration"),
            (
                "Hindsbane Venom",
                "Flanksbane Venom",
                "Flankstung Venom",
                "Grimskin's Venom",
                "Grimhunter's Venom",
            ),
        )

        name = "Flanksting Strike"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "Flankstung Venom": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom"),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
                "Flankstung Venom, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_venom"
                    ),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(hindstung_venom_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def flanksbane_fang(self):
        venom_name = "Hindsbane Venom"
        hindsbane_venom_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Hindsbane Fang",),
            self._skill_data.get_skill_data(venom_name, "duration"),
            (
                "Hindstung Venom",
                "Flanksbane Venom",
                "Flankstung Venom",
                "Grimskin's Venom",
                "Grimhunter's Venom",
            ),
        )
        name = "Flanksbane Fang"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "Flanksbane Venom": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom"),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
                "Flanksbane Venom, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_venom"
                    ),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(
                hindsbane_venom_follow_up,
            ),  # application delay is a bit off due to venom timing
        )

    @GenericJobClass.is_a_skill
    def hindsting_strike(self):
        venom_name = "Flanksbane Venom"
        flanksbane_venom_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Flanksbane Fang",),
            self._skill_data.get_skill_data(venom_name, "duration"),
            (
                "Hindstung Venom",
                "Hindsbane Venom",
                "Flankstung Venom",
                "Grimskin's Venom",
                "Grimhunter's Venom",
            ),
        )

        name = "Hindsting Strike"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "Hindstung Venom": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom"),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
                "Hindstung Venom, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_venom"
                    ),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(flanksbane_venom_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def hindsbane_fang(self):
        venom_name = "Flankstung Venom"
        flankstung_venom_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Flanksting Strike",),
            self._skill_data.get_skill_data(venom_name, "duration"),
            (
                "Hindstung Venom",
                "Hindsbane Venom",
                "Flanksbane Venom",
                "Grimskin's Venom",
                "Grimhunter's Venom",
            ),
        )

        name = "Hindsbane Fang"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name),
                    use_min_potency=self.__combo_base_potency_no_venom,
                ),
                "Hindsbane Venom": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom"),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
                "Hindsbane Venom, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_venom"
                    ),
                    use_min_potency=self.__combo_base_potency_with_venom,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(flankstung_venom_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def dread_maw(self):
        if self._version >= "7.05":
            return None
        name = "Dread Maw"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(self.__get_noxious_gnash_follow_up(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def reaving_maw(self):
        if self._version <= "7.01":
            return None
        name = "Reaving Maw"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Honed Reavers": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_honed_reavers"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(self.__get_honed_steel_follow_up(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def hunters_bite(self):
        name = "Hunter's Bite"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            follow_up_skills=(self.__get_hunters_instinct_follow_up(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def swiftskins_bite(self):
        name = "Swiftskin's Bite"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1380
            ),
            follow_up_skills=(self.__get_swift_scaled_follow_up(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def jagged_maw(self):
        venom_name = "Grimskin's Venom"
        grimskins_venom_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Bloodied Maw",),
            self._skill_data.get_skill_data(venom_name, "duration"),
            (
                "Hindstung Venom",
                "Hindsbane Venom",
                "Flanksbane Venom",
                "Flankstung Venom",
                "Grimhunter's Venom",
            ),
        )

        name = "Jagged Maw"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Grimhunter's Venom": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(grimskins_venom_follow_up,),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def bloodied_maw(self):
        venom_name = "Grimhunter's Venom"
        grimhunters_venom_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Jagged Maw",),
            self._skill_data.get_skill_data(venom_name, "duration"),
            (
                "Hindstung Venom",
                "Hindsbane Venom",
                "Flanksbane Venom",
                "Flankstung Venom",
                "Grimskin's Venom",
            ),
        )

        name = "Bloodied Maw"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Grimskin's Venom": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(grimhunters_venom_follow_up,),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def death_rattle(self):
        name = "Death Rattle"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1700
            ),
        )

    @GenericJobClass.is_a_skill
    def last_lash(self):
        name = "Last Lash"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def dreadwinder(self):
        if self._version >= "7.05":
            return None
        name = "Dreadwinder"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=580,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(self.__get_noxious_gnash_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def vicewinder(self):
        if self._version <= "7.01":
            return None
        name = "Vicewinder"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=580,
                gcd_base_recast_time=3000,
            ),
        )

    def __get_hunters_venom_follow_up(self):
        name = "Hunter's Venom"
        return self.__get_venom_follow_up(
            name, ("Twinfang Bite",), self._skill_data.get_skill_data(name, "duration")
        )

    @GenericJobClass.is_a_skill
    def hunters_coil(self):
        name = "Hunter's Coil"
        hunters_coil_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=980,
        )
        hunters_coil_no_pos_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
            ),
            delay_after_parent_application=980,
        )
        hunters_instinct_follow_up = self.__get_hunters_instinct_follow_up()
        hunters_venom_follow_up = self.__get_hunters_venom_follow_up()
        return Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=0),),
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=0,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    hunters_coil_follow_up,
                    hunters_instinct_follow_up,
                    hunters_venom_follow_up,
                ),
                "No Positional": (
                    hunters_coil_no_pos_follow_up,
                    hunters_instinct_follow_up,
                    hunters_venom_follow_up,
                ),
            },
        )

    def __get_swiftskins_venom_follow_up(self):
        name = "Swiftskin's Venom"
        return self.__get_venom_follow_up(
            name, ("Twinblood Bite",), self._skill_data.get_skill_data(name, "duration")
        )

    @GenericJobClass.is_a_skill
    def swiftskins_coil(self):
        name = "Swiftskin's Coil"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_group=1),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(
                self.__get_swift_scaled_follow_up(),
                self.__get_swiftskins_venom_follow_up(),
            ),
        )

    @GenericJobClass.is_a_skill
    def pit_of_dread(self):
        if self._version >= "7.05":
            return None
        name = "Pit of Dread"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            follow_up_skills=(self.__get_noxious_gnash_follow_up(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def vicepit(self):
        if self._version <= "7.01":
            return None
        name = "Vicepit"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
        )

    def __get_fellhunters_venom_follow_up(self):
        name = "Fellhunter's Venom"
        return self.__get_venom_follow_up(
            name,
            ("Twinfang Thresh",),
            self._skill_data.get_skill_data(name, "duration"),
        )

    @GenericJobClass.is_a_skill
    def hunters_den(self):
        name = "Hunter's Den"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_group=2),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=490,
                gcd_base_recast_time=3000,
            ),
            follow_up_skills=(
                self.__get_hunters_instinct_follow_up(),
                self.__get_fellhunters_venom_follow_up(),
            ),
            has_aoe=True,
        )

    def __get_fellskins_venom_follow_up(self):
        name = "Fellskin's Venom"
        return self.__get_venom_follow_up(
            name,
            ("Twinblood Thresh",),
            self._skill_data.get_skill_data(name, "duration"),
        )

    @GenericJobClass.is_a_skill
    def swiftskins_den(self):
        name = "Swiftskin's Den"
        swiftskins_den_damage_followup = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=790,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_group=3),),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=0,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(
                swiftskins_den_damage_followup,
                self.__get_swift_scaled_follow_up(),
                self.__get_fellskins_venom_follow_up(),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def twinfang_bite(self):
        name = "Twinfang Bite"
        twinfang_bite_damage_followup = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=620,
        )
        twinfang_bite_damage_venom_followup = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom")
                ),
            ),
            delay_after_parent_application=620,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Hunter's Coil",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    twinfang_bite_damage_followup,
                    self.__get_swiftskins_venom_follow_up(),
                ),
                "Hunter's Venom": (
                    twinfang_bite_damage_venom_followup,
                    self.__get_swiftskins_venom_follow_up(),
                ),
                "Hunter's Venom, No Combo": (twinfang_bite_damage_venom_followup,),
                "No Combo": (twinfang_bite_damage_followup,),
            },
        )

    @GenericJobClass.is_a_skill
    def twinblood_bite(self):
        name = "Twinblood Bite"
        twinblood_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=670,
        )
        twinblood_damage_venom_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom")
                ),
            ),
            delay_after_parent_application=670,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Swiftskin's Coil",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    twinblood_damage_follow_up,
                    self.__get_hunters_venom_follow_up(),
                ),
                "Swiftskin's Venom": (
                    twinblood_damage_venom_follow_up,
                    self.__get_hunters_venom_follow_up(),
                ),
                "No Combo, Swiftskin's Venom": (twinblood_damage_venom_follow_up,),
                "No Combo": (twinblood_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def twinfang_thresh(self):
        name = "Twinfang Thresh"
        twinfang_thresh_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=670,
            primary_target_only=False,
        )
        twinfang_thresh_venom_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom")
                ),
            ),
            delay_after_parent_application=670,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            combo_spec=(ComboSpec(combo_group=2, combo_actions=("Hunter's Den",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    twinfang_thresh_damage_follow_up,
                    self.__get_fellskins_venom_follow_up(),
                ),
                "Fellskin's Venom": (
                    twinfang_thresh_venom_follow_up,
                    self.__get_fellskins_venom_follow_up(),
                ),
                "No Combo, Fellskin's Venom": (twinfang_thresh_venom_follow_up,),
                "No Combo": (twinfang_thresh_damage_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def twinblood_thresh(self):
        name = "Twinblood Thresh"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            combo_spec=(ComboSpec(combo_group=3, combo_actions=("Swiftskin's Den",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Fellhunter's Venom": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_venom")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    self.__get_fellhunters_venom_follow_up(),
                ),
                "No Combo": tuple(),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def uncoiled_fury(self):
        venom_name = "Poised for Twinfang"
        poised_for_twinfang_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Uncoiled Twinfang",),
            self._skill_data.get_skill_data(venom_name, "duration"),
        )

        name = "Uncoiled Fury"
        uncoiled_fury_follow_up = FollowUp(
            Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                aoe_dropoff=0.5,
            ),
            delay_after_parent_application=800,
            primary_target_only=False,
        )
        name = "Uncoiled Fury"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=0,
                gcd_base_recast_time=3500,
            ),
            follow_up_skills=(
                uncoiled_fury_follow_up,
                poised_for_twinfang_follow_up,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def reawaken(self):
        name = "Reawaken"
        return Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4),),
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=2200,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def first_generation(self):
        name = "First Generation"
        return Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Reawaken",)),),
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1700,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def second_generation(self):
        name = "Second Generation"
        return Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("First Generation",)),),
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1470,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def third_generation(self):
        name = "Third Generation"
        return Skill(
            name=name,
            combo_spec=(
                ComboSpec(combo_group=4, combo_actions=("Second Generation",)),
            ),
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1470,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def fourth_generation(self):
        name = "Fourth Generation"
        return Skill(
            name=name,
            combo_spec=(ComboSpec(combo_group=4, combo_actions=("Third Generation",)),),
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1470,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def uncoiled_twinfang(self):
        if self._level < 92:
            return None

        venom_name = "Poised for Twinblood"
        poised_for_twinblood_follow_up = self.__get_venom_follow_up(
            venom_name,
            ("Uncoiled Twinblood",),
            self._skill_data.get_skill_data(venom_name, "duration"),
        )
        name = "Uncoiled Twinfang"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Poised for Twinfang": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_poised")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,  # application delay is a bit off due to venom timing
            ),
            follow_up_skills=(poised_for_twinblood_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def uncoiled_twinblood(self):
        if self._level < 92:
            return None
        name = "Uncoiled Twinblood"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Poised for Twinblood": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_poised")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=980
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def ouroboros(self):
        if self._level < 96:
            return None
        name = "Ouroboros"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=2330,
                gcd_base_recast_time=3000,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def first_legacy(self):
        if self._level < 100:
            return None
        name = "First Legacy"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def second_legacy(self):
        if self._level < 100:
            return None
        name = "Second Legacy"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def third_legacy(self):
        if self._level < 100:
            return None
        name = "Third Legacy"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1210
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def fourth_legacy(self):
        if self._level < 100:
            return None
        name = "Fourth Legacy"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

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
    def feint(self):
        name = "Feint"
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
        )

    @GenericJobClass.is_a_skill
    def slither(self):
        name = "Slither"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def serpents_tail(self):
        name = "Serpent's Tail"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def twinfang(self):
        name = "Twinfang"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def twinblood(self):
        name = "Twinblood"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def serpents_ire(self):
        name = "Serpent's Ire"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )
