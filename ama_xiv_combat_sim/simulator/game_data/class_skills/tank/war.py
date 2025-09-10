from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.shield_spec import ShieldSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import (
    OffensiveStatusEffectSpec,
)
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
                offensive_buff_spec=OffensiveStatusEffectSpec(
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
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(potency=250),
                "No Combo": None,
            },
        )

    @GenericJobClass.is_a_skill
    def storms_eye(self):
        surging_tempest_inital_follow_up = FollowUp(
            skill=Skill(
                name="Surging Tempest",
                offensive_buff_spec=OffensiveStatusEffectSpec(
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
                offensive_buff_spec=OffensiveStatusEffectSpec(
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
            offensive_buff_spec=OffensiveStatusEffectSpec(
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
                offensive_buff_spec=OffensiveStatusEffectSpec(
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
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.3,
                duration=15 * 1000,
                add_to_skill_modifier_condition=True,
            ),
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def primeval_impulse_heal(self):
        name = "Primeval Impulse"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Damnation": HealSpec(hot_potency=300, duration=15 * 1000),
            },
        )

    @GenericJobClass.is_a_skill
    def damnation(self):
        if self._level < 92:
            return None

        _primeval_impulse_heal_follow_up = FollowUp(
            skill=self.primeval_impulse_heal(), delay_after_parent_application=15 * 1000
        )

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
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.4,
                add_to_skill_modifier_condition=True,
                duration=15 * 1000,
            ),
            follow_up_skills=(_primeval_impulse_heal_follow_up,),
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
    def thrill_of_battle(self):
        return Skill(
            name="Thrill of Battle",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                # TODO: hp_recovery_up_via_healing_actions is from SELF only. Can add a new field I guess, but is there a more robust way?
                max_hp_mult=1.2,
                hp_recovery_up_via_healing_actions=0.2,
                duration=10 * 1000,
                add_to_skill_modifier_condition=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def holmgang(self):
        return Skill(
            name="Holmgang",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                is_invuln=True, duration=10 * 1000
            ),
        )

    @GenericJobClass.is_a_skill
    def equilibrium(self):
        name = "Equilibrium"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=1200, hot_potency=200, duration=15 * 1000),
        )

    @GenericJobClass.is_a_skill
    def shake(self):
        name = "Shake It Off"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            # NOTE: i know this looks really stupid and we can just enumerate the powerset
            # of [thrill, [damnation|vengeance], bloodwhetting] and programatically construct the conditions.
            # we do NOT do that because this code is also a bit of documentation on how
            # to use the sim and non-coders are going to read this. so we simply just
            # unroll everything to make it easy for non-coders to read off exactly what's going on
            # and what skill conditionals to put in and what they do.
            defensive_buff_spec={
                # 0 buffs
                SimConsts.DEFAULT_CONDITION: DefensiveStatusEffectSpec(
                    max_hp_mult=1.15,
                    duration=30 * 1000,
                    is_party_effect=True,
                ),
                # 1 buff
                "Thrill of Battle": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.02,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=("Thrill of Battle",),
                ),
                "Damnation": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.02,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=("Damnation",),
                ),
                "Vengeance": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.02,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=("Vengeance",),
                ),
                "Bloodwhetting": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.02,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=("Bloodwhetting",),
                ),
                # 2 buffs
                "Damnation, Thrill of Battle": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.04,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Damnation",
                        "Thrill of Battle",
                    ),
                ),
                "Thrill of Battle, Vengeance": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.04,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=("Thrill of Battle", "Vengeance"),
                ),
                "Bloodwhetting, Thrill of Battle": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.04,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Bloodwhetting",
                        "Thrill of Battle",
                    ),
                ),
                "Bloodwhetting, Damnation": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.04,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Bloodwhetting",
                        "Damnation",
                    ),
                ),
                "Bloodwhetting, Vengeance": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.04,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Bloodwhetting",
                        "Vengeance",
                    ),
                ),
                # 3 buffs
                "Bloodwhetting, Damnation, Thrill of Battle": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.06,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Bloodwhetting",
                        "Damnation",
                        "Thrill of Battle",
                    ),
                ),
                "Bloodwhetting, Thrill of Battle, Vengeance": DefensiveStatusEffectSpec(
                    max_hp_mult=1.15 + 0.06,
                    duration=30 * 1000,
                    is_party_effect=True,
                    expires_status_effects=(
                        "Bloodwhetting",
                        "Thrill of Battle",
                        "Vengeance",
                    ),
                ),
            },
            heal_spec=HealSpec(
                potency=300,
                hot_potency=100,
                duration=15 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
            # Kinda ugly to model here and not on the Damnation expiry itself, but this will work...
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Damnation": (
                    FollowUp(
                        skill=self.primeval_impulse_heal(),
                        delay_after_parent_application=0,
                    ),
                ),
            },
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def nascent_flash_heal(self):
        name = "Nascent Flash (Heal)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(potency=400),
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def nascent_glint_heal(self):
        name = "Nascent Glint (Heal)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(potency=400, is_party_effect=True),
        )

    # For logs parsing convenience
    def stem_the_flow(self):
        name = "Stem the Flow"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=4 * 1000,
                is_party_effect=True,
            ),
        )

    # For logs parsing convenience
    def stem_the_tide(self):
        name = "Stem the Tide"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            shield_spec=ShieldSpec(
                potency=400, duration=20 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def nascent_flash(self):
        _tide_follow_up = FollowUp(
            skill=self.stem_the_tide(), delay_after_parent_application=0
        )
        _flow_follow_up = FollowUp(
            skill=self.stem_the_flow(), delay_after_parent_application=0
        )

        return Skill(
            name="Nascent Flash",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Other": DefensiveStatusEffectSpec(
                    damage_reductions=0.1,
                    is_party_effect=True,
                    duration=8 * 1000,
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Other": (_tide_follow_up, _flow_follow_up),
            },
            off_class_default_condition="Other",
        )

    @GenericJobClass.is_a_skill
    def bloodwhetting(self):
        _tide_follow_up = FollowUp(
            skill=self.stem_the_tide(), delay_after_parent_application=0
        )
        _flow_follow_up = FollowUp(
            skill=self.stem_the_flow(), delay_after_parent_application=0
        )

        return Skill(
            name="Bloodwhetting",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1, duration=8 * 1000
            ),
            follow_up_skills=(_tide_follow_up, _flow_follow_up),
        )

    @GenericJobClass.is_a_skill
    def rampart(self):
        return Skill(
            name="Rampart",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.2,
                hp_recovery_up_via_healing_actions=0.15,
                duration=20 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def reprisal(self):
        return Skill(
            name="Reprisal",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_debuff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=15 * 1000,
            ),
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
