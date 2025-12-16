import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.shield_spec import ShieldSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import (
    OffensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.whm_data import (
    all_whm_skills,
)


class WhmSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_whm_skills)
        self._job_class = "WHM"

    @GenericJobClass.is_a_resource
    def liturgy_of_the_bell_resource(self):
        name = "Liturgy of the Bell"
        job_resource_settings = JobResourceSettings(
            max_value=5,
            skill_allowlist=(
                "Liturgy of the Bell (Heal)",
                "Liturgy of the Bell (Expire)",
                "Liturgy of the Bell",
            ),
        )
        return (name, job_resource_settings)

    # For logs parsing convenience, and construction convenience
    @GenericJobClass.is_a_skill
    def plenary_indulgence_heal(self):
        return Skill(
            name="Plenary Indulgence (Heal)",
            heal_spec=HealSpec(potency=200, is_party_effect=True, is_aoe=True),
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
    def glare_iii(self):
        name = "Glare III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1290
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def glare_iv(self):
        if self._level < 92:
            return None

        name = "Glare IV"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=100, application_delay=850
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.4,
        )

    @GenericJobClass.is_a_skill
    def assize(self):
        name = "Assize"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            heal_spec=HealSpec(potency=400, is_aoe=True, is_party_effect=True),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def dia(self):
        name = "Dia (dot)"
        dia_dot_whm = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Dia"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=dia_dot_whm,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def afflatus_misery(self):
        name = "Afflatus Misery"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def holy_iii(self):
        name = "Holy III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=self._skill_data.get_skill_data(name, "cast time"),
                animation_lock=100,
                application_delay=2130,
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def presence_of_mind(self):
        name = "Presence of Mind"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=15 * 1000,
                haste_time_reduction=0.20,
                auto_attack_delay_reduction=0.20,
            ),
        )

    @GenericJobClass.is_a_skill
    def afflatus_rapture(self):
        name = "Afflatus Rapture"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=400, is_aoe=True, is_party_effect=True),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Plenary Indulgence": (
                    FollowUp(
                        skill=self.plenary_indulgence_heal(),
                        delay_after_parent_application=100,
                    ),
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def medica_iii(self):
        if self._level < 96:
            return None
        name = "Medica III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=100, application_delay=0
            ),
            heal_spec=HealSpec(
                potency=250,
                hot_potency=175,
                duration=15 * 1000,
                is_aoe=True,
                is_party_effect=True,
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Plenary Indulgence": (
                    FollowUp(
                        skill=self.plenary_indulgence_heal(),
                        delay_after_parent_application=100,
                    ),
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def aquaveil(self):
        name = "Aquaveil"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.15,
                duration=8 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def temperance(self):
        name = "Temperance"
        healing_potency_up = Skill(
            name=name,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                healing_magic_potency_mult=1.2, duration=20 * 1000
            ),
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            off_class_default_condition="Damage Reduction Only",
            # This should refresh based on proximity to the WHM, and the game does
            # check on occassion so this is not perfectly accurate.
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=20 * 1000,
                is_party_effect=True,
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    FollowUp(
                        skill=healing_potency_up, delay_after_parent_application=0
                    ),
                ),
                "Damage Reduction Only": tuple(),
            },
        )

    # For logs parsing convenience.
    @GenericJobClass.is_a_skill
    def divine_aura(self):
        if self._level < 100:
            return None
        name = "Divine Aura"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(
                hot_potency=200, duration=15 * 1000, is_party_effect=True, is_aoe=True
            ),
        )

    @GenericJobClass.is_a_skill
    def divine_caress(self):
        if self._level < 100:
            return None
        name = "Divine Caress"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            shield_spec=ShieldSpec(
                potency=400, duration=10 * 1000, is_party_effect=True
            ),
            # The barrier can expire earlier, so this is not exactly right.
            follow_up_skills=(
                FollowUp(
                    skill=self.divine_aura(), delay_after_parent_application=10 * 1000
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def cure(self):
        name = "Cure"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=0, application_delay=0
            ),
            heal_spec=HealSpec(potency=500, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def medica(self):
        name = "Medica"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=0, application_delay=0
            ),
            heal_spec=HealSpec(potency=400, is_party_effect=True, is_aoe=True),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Plenary Indulgence": (
                    FollowUp(
                        skill=self.plenary_indulgence_heal(),
                        delay_after_parent_application=100,
                    ),
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def cure_ii(self):
        name = "Cure II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=0, application_delay=0
            ),
            heal_spec=HealSpec(potency=800, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def regen(self):
        name = "Regen"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                hot_potency=250, duration=18 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def cure_iii(self):
        name = "Cure III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=0, application_delay=0
            ),
            heal_spec=HealSpec(potency=600, is_party_effect=True),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Plenary Indulgence": (
                    FollowUp(
                        skill=self.plenary_indulgence_heal(),
                        delay_after_parent_application=100,
                    ),
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def medica_ii(self):
        if self._level >= 96:
            return None
        name = "Medica II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=0, application_delay=0
            ),
            # TODO: does this stack with regen? I actually don't know.
            heal_spec=HealSpec(
                potency=250,
                hot_potency=150,
                duration=15 * 1000,
                is_aoe=True,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def benediction(self):
        name = "Benediction"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=math.inf, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def afflatus_solace(self):
        name = "Afflatus Solace"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=800, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def asylum(self):
        name = "Asylum"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                hot_potency=100, duration=24 * 1000, is_aoe=True, is_party_effect=True
            ),
            defensive_buff_spec=DefensiveStatusEffectSpec(
                hp_recovery_up_via_healing_actions=0.1,
                duration=24 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def tetragrammaton(self):
        name = "Tetragrammaton"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=700, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def plenary_indulgence(self):
        name = "Plenary Indulgence"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=10 * 1000,
                damage_reductions=self._skill_data.get_skill_data(
                    name, "damage_reduction"
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def divine_benison(self):
        name = "Divine Benison"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            shield_spec=ShieldSpec(
                potency=500, duration=15 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def bell_expire(self):
        # TODO: this should probably be named something different
        # depending on what logs actually call it
        name = "Liturgy of the Bell (Expire)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            off_class_default_condition="Heal Only",
            heal_spec={
                "5 Liturgy of the Bell": HealSpec(
                    potency=int(200 * 5), is_party_effect=True
                ),
                "4 Liturgy of the Bell": HealSpec(
                    potency=int(200 * 4), is_party_effect=True
                ),
                "3 Liturgy of the Bell": HealSpec(
                    potency=int(200 * 3), is_party_effect=True
                ),
                "2 Liturgy of the Bell": HealSpec(
                    potency=int(200 * 2), is_party_effect=True
                ),
                "1 Liturgy of the Bell": HealSpec(
                    potency=int(200 * 1), is_party_effect=True
                ),
                SimConsts.DEFAULT_CONDITION: None,
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Liturgy of the Bell", change=-math.inf),
                ),
                "Heal Only": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def bell_heal(self):
        # TODO: this should probably be named something different
        # depending on what logs actually call it
        name = "Liturgy of the Bell (Heal)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            off_class_default_condition="Heal Only",
            heal_spec={
                "5 Liturgy of the Bell": HealSpec(potency=400, is_party_effect=True),
                "4 Liturgy of the Bell": HealSpec(potency=400, is_party_effect=True),
                "3 Liturgy of the Bell": HealSpec(potency=400, is_party_effect=True),
                "2 Liturgy of the Bell": HealSpec(potency=400, is_party_effect=True),
                "1 Liturgy of the Bell": HealSpec(potency=400, is_party_effect=True),
                "Heal Only": HealSpec(potency=400, is_party_effect=True),
                SimConsts.DEFAULT_CONDITION: None,
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Liturgy of the Bell", change=-1),
                ),
                "Heal Only": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def bell(self):
        name = "Liturgy of the Bell"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            off_class_default_condition="Heal Only",
            job_resource_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: (
                        JobResourceSpec(
                            name="Liturgy of the Bell", change=5, duration=20 * 1000
                        ),
                    ),
                    "Heal Only": tuple(),
                }
            ),
            follow_up_skills=(
                FollowUp(
                    skill=self.bell_expire(),
                    delay_after_parent_application=20 * 1000,
                ),
            ),
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
                    "Raise",
                    "Medica III",
                    "Cure",
                    "Medica",
                    "Cure II",
                    "Cure III",
                    "Medica II",
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def raise_skill(self):
        name = "Raise"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=8000, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def aetherial_shift(self):
        return Skill(
            name="Aetherial Shift",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def thin_air(self):
        return Skill(
            name="Thin Air",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )
