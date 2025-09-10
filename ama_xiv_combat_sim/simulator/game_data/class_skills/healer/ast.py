import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.channeling_spec import ChannelingSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.shield_spec import ShieldSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import (
    OffensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.ast_data import (
    all_ast_skills,
)

# TODO: model synastry


class AstSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_ast_skills)
        self._job_class = "AST"

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
    def divination(self):
        name = "Divination"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=600
            ),
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=self._skill_data.get_skill_data(name, "duration"),
                damage_mult=1.06,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def fall_malefic(self):
        name = "Fall Malefic"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1070
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def combust(self):
        name = "Combust III (dot)"
        combust_iii_dot = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Combust III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            follow_up_skills=(
                FollowUp(
                    skill=combust_iii_dot,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def astrodyne(self):
        if self._version >= "7.0":
            return None

        name = "Astrodyne"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "1 Moon, 1 Asterisk, 1 Circle": OffensiveStatusEffectSpec(
                    duration=15 * 1000, haste_time_reduction=0.10, damage_mult=1.05
                ),
                "1 Moon, 1 Asterisk": OffensiveStatusEffectSpec(
                    duration=15 * 1000, haste_time_reduction=0.10
                ),
                "1 Moon, 1 Circle": OffensiveStatusEffectSpec(
                    duration=15 * 1000, haste_time_reduction=0.10
                ),
                "1 Circle, 1 Asterisk": OffensiveStatusEffectSpec(
                    duration=15 * 1000, haste_time_reduction=0.10
                ),
            },
            job_resource_spec=(
                JobResourceSpec(name="Moon", change=-math.inf),
                JobResourceSpec(name="Asterisk", change=-math.inf),
                JobResourceSpec(name="Circle", change=-math.inf),
            ),
        )

    @GenericJobClass.is_a_skill
    def lightspeed(self):
        name = "Lightspeed"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=15 * 1000, flat_cast_time_reduction=2500
            ),
        )

    @GenericJobClass.is_a_skill
    def gravity_ii(self):
        name = "Gravity II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1160
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def macrocosmos(self):
        name = "Macrocosmos"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=100, application_delay=750
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            defensive_buff_spec=DefensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=15 * 1000,
                compiles_damage_taken=True,
            ),
            has_aoe=True,
            aoe_dropoff=0.4,
        )

    @GenericJobClass.is_a_skill
    def microcosmos(self):
        name = "Microcosmos"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                expires_status_effects=("Macrocosmos",), is_party_effect=True
            ),
            heal_spec=HealSpec(
                potency=200, heals_damage_at_fraction_taken=0.5, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def sun_sign(self):
        return Skill(
            name="Sun Sign",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=15 * 100,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def lord_of_crowns(self):
        name = "Lord of Crowns"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def lady_of_crowns(self):
        name = "Lady of Crowns"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            heal_spec=HealSpec(potency=400, is_party_effect=True, is_aoe=True),
        )

    @GenericJobClass.is_a_skill
    def card(self):
        name = "Card"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            offensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: OffensiveStatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                ),
                "Big": OffensiveStatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                ),
                "Small": OffensiveStatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.03, is_party_effect=True
                ),
            },
            off_class_default_condition="Big",
        )

    @GenericJobClass.is_a_skill
    def swiftcast(self):
        name = "Swiftcast"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=1,
                skill_allowlist=(
                    "Glare III",
                    "Holy III",
                    "Benefic",
                    "Helios",
                    "Ascend",
                    "Benefic II",
                    "Aspected Helios",
                ),
            ),
        )

    def __get_giant_dominance_followup(self):
        name = "Giant Dominance"
        return FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec={
                    SimConsts.DEFAULT_CONDITION: None,
                    "Earthly Dominance": OffensiveStatusEffectSpec(
                        duration=int(10.1 * 1000),
                        is_party_effect=False,
                        add_to_skill_modifier_condition=True,
                        num_uses=1,
                        skill_allowlist=("Stellar Explosion (pet)",),
                    ),
                },
                has_aoe=True,
            ),
            delay_after_parent_application=10 * 1000,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

    def __get_star_damage_spec(self, name):
        return {
            SimConsts.DEFAULT_CONDITION: None,
            "Earthly Dominance": DamageSpec(
                damage_class=DamageClass.PET,
                potency=self._skill_data.get_skill_data(name, "Earthly Dominance"),
                pet_job_mod_override=118,
            ),
            "Giant Dominance": DamageSpec(
                damage_class=DamageClass.PET,
                potency=self._skill_data.get_skill_data(name, "Giant Dominance"),
                pet_job_mod_override=118,
            ),
        }

    # NOTE: this implicitly relies on the offensive part of star tagging star appropriately.
    # This is not robust and introduces coupling between the offensive and defensive aspects.
    # # Maybe consider making separate offensive/defensive versions that mirror each other? But
    # doing so, would require num_uses=2 for a consumption on both offensive/defensive or some 
    # sort of specification of num_uses for defensive/offensive separately. Think about the
    # design of this carefully to deal with star. For now though, we accept the coupling.
    def __get_star_heal_spec(self, name):
        return (
            {
                SimConsts.DEFAULT_CONDITION: None,
                "Earthly Dominance": HealSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "Earthly Dominance (Heal)"
                    ),
                    is_party_effect=True,
                    is_aoe=True,
                ),
                "Giant Dominance": HealSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "Giant Dominance (Heal)"
                    ),
                    is_party_effect=True,
                    is_aoe=True,
                ),
            },
        )

    def __get_stellar_detonation_follow_up(self):
        name = "Stellar Explosion (pet)"
        return FollowUp(
            skill=Skill(
                name=name,
                status_effect_denylist=("Dragon Sight",),
                damage_spec=self.__get_star_damage_spec(name),
                heal_spec=self.__get_star_heal_spec(name),
                has_aoe=True,
            ),
            delay_after_parent_application=20 * 1000,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

    @GenericJobClass.is_a_skill
    def giant_dominance(self):
        name = "Stellar Explosion (pet)"
        stellar_detonation_follow_up2 = FollowUp(
            skill=Skill(
                name=name,
                status_effect_denylist=("Dragon Sight",),
                damage_spec=self.__get_star_damage_spec(name),
                heal_spec=self.__get_star_heal_spec(name),
                has_aoe=True,
            ),
            delay_after_parent_application=10 * 1000,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

        name = "Giant Dominance"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=int(10.1 * 1000),
                is_party_effect=False,
                add_to_skill_modifier_condition=True,
                num_uses=1,
                skill_allowlist=("Stellar Explosion (pet)",),
            ),
            follow_up_skills=(stellar_detonation_follow_up2,),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def earthly_dominance(self):
        name = "Earthly Dominance"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=int(10.1 * 1000),
                is_party_effect=False,
                add_to_skill_modifier_condition=True,
                num_uses=1,
                skill_allowlist=("Stellar Explosion (pet)", "Giant Dominance"),
            ),
            follow_up_skills=(
                self.__get_giant_dominance_followup(),
                self.__get_stellar_detonation_follow_up(),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def stellar_detonation(self):
        name = "Stellar Explosion (pet)"
        stellar_detonation_instant = FollowUp(
            skill=Skill(
                name=name,
                status_effect_denylist=("Dragon Sight",),
                damage_spec=self.__get_star_damage_spec(name),
                heal_spec=self.__get_star_heal_spec(name),
                has_aoe=True,
            ),
            delay_after_parent_application=0,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

        name = "Stellar Detonation"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            status_effect_denylist=("Dragon Sight",),
            timing_spec=TimingSpec(base_cast_time=0, application_delay=0),
            follow_up_skills=(stellar_detonation_instant,),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def earthly_star(self):
        name = "Earthly Dominance"
        earthly_dom_follow_up = FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    duration=int(10.1 * 1000),
                    is_party_effect=False,
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    skill_allowlist=("Stellar Explosion (pet)", "Giant Dominance"),
                ),
            ),
            delay_after_parent_application=0,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

        name = "Earthly Star"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            follow_up_skills=(
                earthly_dom_follow_up,
                self.__get_giant_dominance_followup(),
                self.__get_stellar_detonation_follow_up(),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def oracle(self):
        if self._level < 92:
            return None
        name = "Oracle"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1740
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def benefic(self):
        name = "Benefic"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                # TODO: figure out actual application delay
                base_cast_time=1500,
                animation_lock=650,
                application_delay=620,
            ),
            heal_spec=HealSpec(
                hot_potency=500, duration=15 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def helios(self):
        name = "Helios"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                # TODO: figure out actual application delay
                base_cast_time=1500,
                animation_lock=650,
                application_delay=620,
            ),
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Horoscope": DefensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=30 * 1000,
                    expires_status_effects=("Horoscope",),
                    is_party_effect=True,
                ),
            },
            heal_spec=HealSpec(potency=400, is_party_effect=True, is_aoe=True),
        )

    @GenericJobClass.is_a_skill
    def benefic_ii(self):
        name = "Benefic II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                # TODO: figure out actual application delay
                base_cast_time=1500,
                animation_lock=650,
                application_delay=620,
            ),
            heal_spec=HealSpec(potency=800, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def aspected_benefic(self):
        name = "Aspected Benefic"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            # TODO: figure out actual application delay
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                potency=250, hot_potency=250, duration=15 * 1000, is_party_effect=True
            ),
            shield_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Neutral Sect": ShieldSpec(
                    shield_mult_on_hp_restored=2.5, is_party_effect=True
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def aspected_helios(self):
        if self._level >= 96:
            return None
        name = "Aspected Helios"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                # TODO: figure out actual application delay
                base_cast_time=1500,
                animation_lock=650,
                application_delay=620,
            ),
            heal_spec=HealSpec(
                potency=250,
                hot_potency=150,
                duration=15 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def essential_dignity(self):
        name = "Essential Dignity"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                min_potency=400,
                min_potency_at_fraction_of_max_hp=1.0,
                max_potency=900,
                max_potency_at_fraction_of_max_hp=0.3,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def helios_conjunction(self):
        if self._level < 96:
            return None
        name = "Helios Conjunction"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=650, application_delay=620
            ),
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Horoscope": DefensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=30 * 1000,
                    expires_status_effects=("Horoscope",),
                    is_party_effect=True,
                ),
            },
            heal_spec=HealSpec(
                potency=250,
                hot_potency=175,
                duration=15 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
            shield_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Neutral Sect": ShieldSpec(
                    shield_mult_on_hp_restored=1.25, is_party_effect=True
                ),
            },
        )

    # TODO ADD HOROSCOPE HELIOS AND HOROSCOPE HELIOS CONJUNCTION AS CONVENIENCE "HEAL" CASTS?"
    @GenericJobClass.is_a_skill
    def horoscope(self):
        name = "Horoscope"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: DefensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=10 * 1000,
                    is_party_effect=True,
                ),
                "Horoscope": DefensiveStatusEffectSpec(
                    expires_status_effects=("Horoscope",)
                ),
                "Helios": DefensiveStatusEffectSpec(expires_status_effects=("Helios",)),
                "Helios Conjunction": DefensiveStatusEffectSpec(
                    expires_status_effects=("Helios Conjunction",)
                ),
                "Helios, Helios Conjunction": DefensiveStatusEffectSpec(
                    expires_status_effects=(
                        "Helios",
                        "Helios Conjunction",
                    )
                ),
            },
            heal_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Horoscope": HealSpec(potency=200, is_party_effect=True),
                "Helios": HealSpec(potency=400, is_party_effect=True),
                "Helios Conjunction": HealSpec(potency=400, is_party_effect=True),
                "Helios, Helios Conjunction": HealSpec(
                    potency=400, is_party_effect=True
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def neutral_sect(self):
        name = "Neutral Sect"
        neutral_condition_follow_up = FollowUp(
            skill=Skill(
                name=name,
                skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
                defensive_buff_spec=DefensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    duration=30 * 1000,
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
            off_class_default_condition="Buff Only",
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: DefensiveStatusEffectSpec(
                    healing_magic_potency_mult=1.2, duration=20 * 1000
                ),
                "Buff Only": None,
            },
            follow_up_skills=(neutral_condition_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def exaltation(self):
        heal_follow_up = FollowUp(
            skill=Skill(
                name="Exaltation",
                is_GCD=False,
                skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
                heal_spec=HealSpec(potency=500, is_party_effect=True),
            ),
            delay_after_parent_application=8 * 1000,
        )

        name = "Exaltation"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=8 * 1000,
                is_party_effect=True,
            ),
            follow_up_skills=(heal_follow_up,),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def ascend(self):
        name = "Ascend"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=8000, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def draw(self):
        if self._version >= "7.0":
            return None
        return Skill(
            name="Draw",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def redraw(self):
        if self._version >= "7.0":
            return None
        return Skill(
            name="Redraw",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def play(self):
        if self._version >= "7.0":
            return None
        return Skill(
            name="Play",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def minor_arcana(self):
        return Skill(
            name="Minor Arcana",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def collective_unconscious(self):
        return Skill(
            name="Collective Unconscious",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            channeling_spec=ChannelingSpec(duration=18000),
            # TODO: this should get refreshed on server tick
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=5 * 100,
                is_party_effect=True,
            ),
            heal_spec=HealSpec(
                hot_potency=100, duration=15 * 1000, is_party_effect=True, is_aoe=True
            ),
        )

    @GenericJobClass.is_a_skill
    def celestial_opposition(self):
        return Skill(
            name="Celestial Opposition",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                potency=200,
                hot_potency=100,
                duration=15 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def celestial_intersection(self):
        return Skill(
            name="Celestial Intersection",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=200, is_party_effect=True),
            shield_spec=ShieldSpec(
                shield_mult_on_hp_restored=2.0, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def astral_draw(self):
        if self._version < "7.0":
            return None
        return Skill(
            name="Astral Draw",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def umbral_draw(self):
        if self._version < "7.0":
            return None
        return Skill(
            name="Umbral Draw",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    def __get_card_skill_655(self, name, sign):
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (JobResourceSpec(name=sign, change=+1),),
                "Big": tuple(),
                "Small": tuple(),
            },
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Big": OffensiveStatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                ),
                "Small": OffensiveStatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.03, is_party_effect=True
                ),
            },
            off_class_default_condition="Big",
        )

    @GenericJobClass.is_a_skill
    def get_card_skills_655(self):
        if self._version != "6.55":
            return None
        res = []
        skill_and_resources = (
            ("the Arrow", "Moon"),
            ("The Arrow", "Moon"),
            ("the Ewer", "Moon"),
            ("The Ewer", "Moon"),
            ("the Balance", "Asterisk"),
            ("The Balance", "Asterisk"),
            ("the Bole", "Asterisk"),
            ("The Bole", "Asterisk"),
            ("the Spire", "Circle"),
            ("The Spire", "Circle"),
            ("the Spear", "Circle"),
            ("The Spear", "Circle"),
        )
        for sk, resource in skill_and_resources:
            res.append(self.__get_card_skill_655(sk, resource))

        return res

    def __get_damaging_card_skill(self, name):
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
            offensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Big": OffensiveStatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.06, is_party_effect=True
                ),
                "Small": OffensiveStatusEffectSpec(
                    duration=15 * 1000, damage_mult=1.03, is_party_effect=True
                ),
            },
            off_class_default_condition="Big",
        )

    @GenericJobClass.is_a_skill
    def the_arrow(self):
        if self._version < "7.0":
            return None
        res = []
        for name in ["the Arrow", "The Arrow"]:
            res.append(
                Skill(
                    name=name,
                    is_GCD=False,
                    skill_type=SkillType.ABILITY,
                    timing_spec=self.instant_timing_spec,
                    defensive_buff_spec=DefensiveStatusEffectSpec(
                        hp_recovery_up_via_healing_actions=0.1,
                        duration=15 * 1000,
                        is_party_effect=True,
                    ),
                )
            )
        return res

    @GenericJobClass.is_a_skill
    def the_ewer(self):
        if self._version < "7.0":
            return None
        res = []
        for name in ["the Ewer", "The Ewer"]:
            res.append(
                Skill(
                    name=name,
                    is_GCD=False,
                    skill_type=SkillType.ABILITY,
                    timing_spec=self.instant_timing_spec,
                    heal_spec=HealSpec(
                        hot_potency=200, duration=15 * 1000, is_party_effect=True
                    ),
                )
            )
        return res

    @GenericJobClass.is_a_skill
    def the_spire(self):
        if self._version < "7.0":
            return None
        res = []
        for name in ["the Spire", "The Spire"]:
            res.append(
                Skill(
                    name=name,
                    is_GCD=False,
                    skill_type=SkillType.ABILITY,
                    timing_spec=self.instant_timing_spec,
                    shield_spec=ShieldSpec(
                        potency=400, duration=30 * 1000, is_party_effect=True
                    ),
                )
            )
        return res

    @GenericJobClass.is_a_skill
    def the_bole(self):
        if self._version < "7.0":
            return None
        res = []
        for name in ["the Bole", "The Bole"]:
            res.append(
                Skill(
                    name=name,
                    is_GCD=False,
                    skill_type=SkillType.ABILITY,
                    timing_spec=self.instant_timing_spec,
                    defensive_buff_spec=DefensiveStatusEffectSpec(
                        damage_reductions=0.1,
                        duration=15 * 1000,
                        is_party_effect=True,
                    ),
                )
            )
        return res

    @GenericJobClass.is_a_skill
    def cards(self):
        if self._version < "7.0":
            return None
        res = []
        # damaging cards
        for card_name in ["the Spear", "The Spear", "the Balance", "The Balance"]:
            res.append(self.__get_damaging_card_skill(card_name))
        return res

    @GenericJobClass.is_a_resource
    def asterisk(self):
        if self._version >= "7.0":
            return None
        name = "Asterisk"
        job_resource_settings = JobResourceSettings(
            max_value=1, skill_allowlist=("Astrodyne",)
        )
        return (name, job_resource_settings)

    @GenericJobClass.is_a_resource
    def moon(self):
        if self._version >= "7.0":
            return None
        name = "Moon"
        job_resource_settings = JobResourceSettings(
            max_value=1, skill_allowlist=("Astrodyne",)
        )
        return (name, job_resource_settings)

    @GenericJobClass.is_a_resource
    def circle(self):
        if self._version >= "7.0":
            return None
        name = "Circle"
        job_resource_settings = JobResourceSettings(
            max_value=1, skill_allowlist=("Astrodyne",)
        )
        return (name, job_resource_settings)
