from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.war_data import (
    all_war_skills,
)


class WarSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_war_skills)
        self._job_class = "WAR"

    def __surging_tempest_followup(self):
        return FollowUp(
            skill=Skill(
                name="Surging Tempest",
                buff_spec=StatusEffectSpec(
                    duration=30000,
                    max_duration=60000,
                    damage_mult=1.10,
                    add_to_skill_modifier_condition=True,
                ),
            ),
            delay_after_parent_application=0,
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
    def heavy_swing(self):
        name = "Heavy Swing"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=532
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(),),
        )

    @GenericJobClass.is_a_skill
    def maim(self):
        name = "Maim"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            combo_spec=(ComboSpec(combo_actions=("Heavy Swing",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def storms_path(self):
        name = "Storm's Path"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1515
            ),
            combo_spec=(ComboSpec(combo_actions=("Maim",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def storms_eye(self):
        surging_tempest_inital_follow_up = FollowUp(
            skill=Skill(
                name="Surging Tempest",
                buff_spec=StatusEffectSpec(
                    duration=31600,
                    max_duration=60000,
                    damage_mult=1.10,
                    add_to_skill_modifier_condition=True,
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

        name = "Storm's Eye"
        storms_eye_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=1649,
        )
        storms_eye_damage_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=1649,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=650),
            combo_spec=(ComboSpec(combo_actions=("Maim",)),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    storms_eye_damage_follow_up,
                    surging_tempest_inital_follow_up,
                ),
                "Surging Tempest": (
                    storms_eye_damage_follow_up,
                    self.__surging_tempest_followup(),
                ),
                "No Combo": (storms_eye_damage_no_combo_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def inner_release(self):
        name = "Surging Tempest"
        ir_surging_tempest_follow_up = FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    duration=10000,
                    max_duration=60000,
                    damage_mult=1.10,
                    extend_only=True,
                    add_to_skill_modifier_condition=True,
                ),
            ),
            delay_after_parent_application=0,
        )

        name = "Inner Release"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
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

    @GenericJobClass.is_a_skill
    def upheaval(self):
        name = "Upheaval"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def onslaught(self):
        name = "Onslaught"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=667
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def fell_cleave(self):
        name = "Fell Cleave"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def primal_rend(self):
        name = "Primal Rend"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1300, application_delay=1160
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                )
            },
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def inner_chaos(self):
        name = "Inner Chaos"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=937
            ),
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
        )

    @GenericJobClass.is_a_skill
    def chaotic_cyclone(self):
        name = "Chaotic Cyclone"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def tomahawk(self):
        name = "Tomahawk"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=713
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def overpower(self):
        name = "Overpower"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def mythril_tempest(self):
        name = "Surging Tempest"
        mythril_tempest_inital_follow_up = FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    duration=30470,
                    max_duration=60000,
                    damage_mult=1.10,
                    add_to_skill_modifier_condition=True,
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

        name = "Mythril Tempest"
        mythril_tempest_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=490,
            primary_target_only=False,
        )
        mythril_tempest_damage_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=490,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=650),
            combo_spec=(ComboSpec(combo_actions=("Overpower",)),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    mythril_tempest_damage_follow_up,
                    mythril_tempest_inital_follow_up,
                ),
                "Surging Tempest": (
                    mythril_tempest_damage_follow_up,
                    self.__surging_tempest_followup(),
                ),
                "No Combo": (mythril_tempest_damage_no_combo_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def orogeny(self):
        name = "Orogeny"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=668
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def decimate(self):
        name = "Decimate"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1831
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def vengeance(self):
        if self._level >= 92:
            return None

        name = "Vengeance"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Retaliation": DamageSpec(potency=self._skill_data.get_potency(name)),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: self.instant_timing_spec,
                "Retaliation": TimingSpec(
                    base_cast_time=0, animation_lock=0, application_delay=534
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def damnation(self):
        if self._level < 92:
            return None

        name = "Damnation"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Retaliation": DamageSpec(potency=self._skill_data.get_potency(name)),
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: self.instant_timing_spec,
                "Retaliation": TimingSpec(
                    base_cast_time=0, animation_lock=0, application_delay=534
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def primal_wrath(self):
        if self._level < 96:
            return None
        name = "Primal Wrath"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1150
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def primal_ruination(self):
        if self._level < 100:
            return None
        name = "Primal Ruination"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1300, application_delay=1060
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                )
            },
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    @GenericJobClass.is_a_skill
    def infuriate(self):
        return Skill(
            name="Infuriate",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def defiance(self):
        return Skill(
            name="Defiance",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def thrill(self):
        return Skill(
            name="Thrill of Battle",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def holmgang(self):
        return Skill(
            name="Holmgang",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def equilibrium(self):
        return Skill(
            name="Equilibrium",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def shake(self):
        return Skill(
            name="Shake It Off",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def nascent(self):
        return Skill(
            name="Nascent Flash",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def bloodwhetting(self):
        return Skill(
            name="Bloodwhetting",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def rampart(self):
        return Skill(
            name="Rampart",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def provoke(self):
        return Skill(
            name="Provoke",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def reprisal(self):
        return Skill(
            name="Reprisal",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def arms_length(self):
        return Skill(
            name="Arm's Length",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def shirk(self):
        return Skill(
            name="Shirk",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )
