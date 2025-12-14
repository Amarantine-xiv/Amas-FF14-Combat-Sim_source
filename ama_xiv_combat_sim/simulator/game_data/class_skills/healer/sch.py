import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.damage_instance_class import (
    DamageInstanceClass,
)
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
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

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sch_data import (
    all_sch_skills,
)


class SchSkills(GenericJobClass):
    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_sch_skills)
        self._job_class = "SCH"

    @staticmethod
    def _get_non_stacking_shield_set():
        return set(
            (
                "Eukrasian Diagnosis",
                "Eukrasian Prognosis II",
                "Adloquium",
                "Succor",
                "Concitation",
                "Accession",
                "Manifestation",
            )
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
    def broil_iv(self):
        name = "Broil IV"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=800
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def ruin_ii(self):
        name = "Ruin II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=940
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def energy_drain(self):
        name = "Energy Drain"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            # This technically heals, too
        )

    @GenericJobClass.is_a_skill
    def art_of_war_ii(self):
        name = "Art of War II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def chain_stratagem(self):
        name = "Chain Stratagem"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            offensive_debuff_spec=OffensiveStatusEffectSpec(
                duration=self._skill_data.get_skill_data(name, "duration"),
                crit_rate_add=0.10,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def biolysis(self):
        name = "Biolysis (dot)"
        biolysis_dot = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Biolysis"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            follow_up_skills=(
                FollowUp(
                    skill=biolysis_dot,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def baneful_impaction(self):
        if self._level < 92:
            return None

        name = "Baneful Impaction (dot)"
        baneful_dot = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
            has_aoe=True,
        )

        name = "Baneful Impaction"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills=(
                FollowUp(
                    skill=baneful_dot,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True,
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
                    "Physick",
                    "Resurrection",
                    "Adloquium",
                    "Succor",
                    "Concitation",
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def whispering_dawn(self):
        res = []
        for name in ["Whispering Dawn", "Angel's Whisper"]:
            res.append(
                Skill(
                    name=name,
                    is_GCD=False,
                    skill_type=SkillType.ABILITY,
                    timing_spec=self.instant_timing_spec,
                    heal_spec=HealSpec(
                        hot_potency=80,
                        duration=21 * 1000,
                        is_party_effect=True,
                        is_aoe=True,
                    ),
                )
            )
        return res

    @GenericJobClass.is_a_skill
    def fey_illumination(self):

        res = []
        for name in ["Fey Illumination", "Seraphic Illumination"]:
            healing_potency_up = Skill(
                name=name,
                defensive_buff_spec=DefensiveStatusEffectSpec(
                    healing_magic_potency_mult=1.1, duration=20 * 1000
                ),
            )

            res.append(
                Skill(
                    name=name,
                    is_GCD=False,
                    skill_type=SkillType.ABILITY,
                    timing_spec=self.instant_timing_spec,
                    off_class_default_condition="Reduction Only",
                    defensive_buff_spec=DefensiveStatusEffectSpec(
                        damage_reductions={DamageInstanceClass.MAGICAL: 0.05},
                        duration=20 * 1000,
                        is_party_effect=True,
                    ),
                    follow_up_skills={
                        SimConsts.DEFAULT_CONDITION: (
                            FollowUp(
                                skill=healing_potency_up,
                                delay_after_parent_application=0,
                            ),
                        ),
                        "Reduction Only": tuple(),
                    },
                )
            )
        return res

    @GenericJobClass.is_a_skill
    def adloquium(self):
        name = "Adloquium"
        non_stacking_shield_set = self._get_non_stacking_shield_set()
        non_stacking_shield_set.remove(name)

        galvanize_follow_up = self._get_galvanize_followup(
            shield_mult_on_hp_restored=1.8,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=False,
        )
        catalyze_follow_up = self._get_catalyze_followup(
            shield_mult_on_hp_restored=1.8,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=False,
        )

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=100, application_delay=800
            ),
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(
                    potency=300, is_party_effect=True
                ),
                "Recitation": HealSpec(
                    potency=300, is_party_effect=True, guaranteed_crit=True
                ),
                "Emergency Tactics": HealSpec(potency=840, is_party_effect=True),
                "Critical, Emergency Tactics": HealSpec(
                    potency=int(4.6 * 300), is_party_effect=True
                ),
                "Emergency Tactics, Recitation": HealSpec(
                    potency=(2.8 * 300), is_party_effect=True, guaranteed_crit=True
                ),
                "Critical, Emergency Tactics, Recitation": HealSpec(
                    potency=int(4.6 * 300), is_party_effect=True, guaranteed_crit=True
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (galvanize_follow_up,),
                "Critical": (galvanize_follow_up, catalyze_follow_up),
                "Recitation": (galvanize_follow_up, catalyze_follow_up),
                "Critical, Recitation": (galvanize_follow_up, catalyze_follow_up),
                "Emergency Tactics": tuple(),
                "Emergency Tactics, Critical": tuple(),
                "Emergency Tactics, Recitation": tuple(),
                "Critical, Emergency Tactics, Recitation": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def manifestation(self):
        name = "Manifestation"
        non_stacking_shield_set = self._get_non_stacking_shield_set()
        non_stacking_shield_set.remove(name)

        galvanize_follow_up = self._get_galvanize_followup(
            shield_mult_on_hp_restored=1.8,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=False,
        )
        catalyze_follow_up = self._get_catalyze_followup(
            shield_mult_on_hp_restored=1.8,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=False,
        )

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.instant_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(
                    potency=360, is_party_effect=True
                ),
                "Emergency Tactics": HealSpec(
                    potency=int(2.8 * 360), is_party_effect=True
                ),
                "Critical, Emergency Tactics": HealSpec(
                    potency=int(4.6 * 360), is_party_effect=True
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (galvanize_follow_up,),
                "Critical": (galvanize_follow_up, catalyze_follow_up),
                "Emergency Tactics": tuple(),
                "Emergency Tactics, Critical": tuple(),
            },
        )

    @staticmethod
    def _get_shield_followup(
        name, shield_mult_on_hp_restored, non_stacking_shield_set, is_aoe
    ):
        return FollowUp(
            skill=Skill(
                name=name,
                shield_spec=ShieldSpec(
                    shield_mult_on_hp_restored=shield_mult_on_hp_restored,
                    duration=30 * 1000,
                    is_party_effect=True,
                    is_aoe=is_aoe,
                    does_not_stack_with=frozenset(non_stacking_shield_set),
                ),
            ),
            delay_after_parent_application=0,
        )

    @staticmethod
    def _get_galvanize_followup(
        shield_mult_on_hp_restored, non_stacking_shield_set, is_aoe
    ):
        return SchSkills._get_shield_followup(
            name="Galvanize",
            shield_mult_on_hp_restored=shield_mult_on_hp_restored,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=is_aoe,
        )

    @staticmethod
    def _get_catalyze_followup(
        shield_mult_on_hp_restored, non_stacking_shield_set, is_aoe
    ):
        return SchSkills._get_shield_followup(
            name="Catalyze",
            shield_mult_on_hp_restored=shield_mult_on_hp_restored,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=is_aoe,
        )

    @GenericJobClass.is_a_skill
    # for logs processing convenience for now.
    # TODO: deprecate when cast association is complete.
    def galvanize(self):
        return Skill(
            name="Galvanize",
            shield_spec=ShieldSpec(
                duration=30 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    # for logs processing convenience for now.
    # TODO: deprecate when cast association is complete.
    def catalize(self):
        return Skill(
            name="Catalyze",
            shield_spec=ShieldSpec(
                duration=30 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def concitation(self):
        if self._level < 96:
            return None
        name = "Concitation"
        non_stacking_shield_set = self._get_non_stacking_shield_set()
        non_stacking_shield_set.remove(name)

        galvanize_follow_up = self._get_galvanize_followup(
            shield_mult_on_hp_restored=1.8,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=True,
        )

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=100, application_delay=800
            ),
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(
                    potency=200, is_party_effect=True, is_aoe=True
                ),
                "Recitation": HealSpec(
                    potency=200, is_party_effect=True, is_aoe=True, guaranteed_crit=True
                ),
                "Emergency Tactics": HealSpec(
                    potency=int(2.8 * 200), is_party_effect=True, is_aoe=True
                ),
                "Emergency Tactics, Recitation": HealSpec(
                    potency=int(2.8 * 200),
                    is_party_effect=True,
                    is_aoe=True,
                    guaranteed_crit=True,
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (galvanize_follow_up,),
                "Emergency Tactics": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def accession(self):
        if self._level < 100:
            return None
        name = "Accession"
        non_stacking_shield_set = self._get_non_stacking_shield_set()
        non_stacking_shield_set.remove(name)

        galvanize_follow_up = self._get_galvanize_followup(
            shield_mult_on_hp_restored=1.8,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=True,
        )

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.instant_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(
                    potency=240, is_party_effect=True, is_aoe=True
                ),
                "Emergency Tactics": HealSpec(
                    potency=int(2.8 * 240), is_party_effect=True, is_aoe=True
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (galvanize_follow_up,),
                "Emergency Tactics": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def succor(self):
        if self._level >= 96:
            return None
        name = "Succor"
        non_stacking_shield_set = self._get_non_stacking_shield_set()
        non_stacking_shield_set.remove(name)

        galvanize_follow_up = self._get_galvanize_followup(
            shield_mult_on_hp_restored=1.6,
            non_stacking_shield_set=non_stacking_shield_set,
            is_aoe=True,
        )

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=100, application_delay=800
            ),
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(
                    potency=200, is_party_effect=True, is_aoe=True
                ),
                "Emergency Tactics": HealSpec(
                    potency=int(2.6 * 200), is_party_effect=True, is_aoe=True
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (galvanize_follow_up,),
                "Emergency Tactics": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def physick(self):
        name = "Physick"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=650, application_delay=620
            ),
            heal_spec=HealSpec(potency=450, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def lustrate(self):
        name = "Lustrate"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=600, is_party_effect=True),
        )

    # For logs processing convenience
    @GenericJobClass.is_a_skill
    def sacred_soil_heal(self):
        return Skill(
            name="Sacred Soil (Heal)",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            # TODO: just 1 tick of heal
            heal_spec=HealSpec(potency=100, is_party_effect=True, is_aoe=True),
        )

    @GenericJobClass.is_a_skill
    def sacred_soil(self):
        return Skill(
            name="Sacred Soil",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            # TODO: this should get refreshed on server tick
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=15 * 100,
                is_party_effect=True,
            ),
            heal_spec=HealSpec(
                hot_potency=100, duration=15 * 1000, is_party_effect=True, is_aoe=True
            ),
        )

    @GenericJobClass.is_a_skill
    def indomitability(self):
        name = "Indomitability"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(
                    potency=400, is_party_effect=True, is_aoe=True
                ),
                "Recitation": HealSpec(
                    potency=400, is_party_effect=True, is_aoe=True, guaranteed_crit=True
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def emergency_tactics(self):
        return Skill(
            name="Emergency Tactics",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True, duration=15 * 1000
            ),
        )

    @GenericJobClass.is_a_skill
    def dissipation(self):
        return Skill(
            name="Dissipation",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                healing_magic_potency_mult=1.2, duration=30 * 1000
            ),
        )

    @GenericJobClass.is_a_skill
    def excogitation(self):
        res = []
        for name in ["Excogitation", "Excogitation (Heal)"]:
            res.append(
                Skill(
                    name=name,
                    is_GCD=False,
                    skill_type=SkillType.ABILITY,
                    timing_spec=self.instant_timing_spec,
                    heal_spec={
                        SimConsts.DEFAULT_CONDITION: HealSpec(
                            potency=800, is_party_effect=True
                        ),
                        "Recitation": HealSpec(
                            potency=800, is_party_effect=True, guaranteed_crit=True
                        ),
                    },
                    # TODO: has a trigger condition
                )
            )
        return res

    @GenericJobClass.is_a_skill
    def seraphism(self):
        name = "Seraphism"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                hot_potency=100,
                duration=20 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def fey_union(self):
        name = "Fey Union"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=TimingSpec(
                base_cast_time=0, application_delay=0, animation_lock=0
            ),
            # TODO: has a trigger condition. for now, use this as the manual heal tick...
            heal_spec=HealSpec(potency=300, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def fey_blessing(self):
        name = "Fey Blessing"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=320, is_party_effect=True, is_aoe=True),
        )

    @GenericJobClass.is_a_skill
    def consolation(self):
        name = "Consolation"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=250, is_party_effect=True, is_aoe=True),
            shield_spec=ShieldSpec(
                shield_mult_on_hp_restored=1.0,
                is_party_effect=True,
                is_aoe=True,
                duration=30 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def embrace(self):
        name = "Embrace"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=TimingSpec(
                base_cast_time=0, application_delay=0, animation_lock=0
            ),
            heal_spec=HealSpec(potency=180, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def seraphic_veil(self):
        name = "Seraphic Veil"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=TimingSpec(
                base_cast_time=0, application_delay=0, animation_lock=0
            ),
            heal_spec=HealSpec(potency=180, is_party_effect=True),
            shield_spec=ShieldSpec(
                shield_mult_on_hp_restored=1.0, duration=30 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def protraction(self):
        name = "Protraction"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                max_hp_mult=1.1,
                hp_recovery_up_via_healing_actions=0.1,
                duration=10 * 1000,
            ),
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def desperate_measures(self):
        name = "Desperate Measures"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=TimingSpec(
                base_cast_time=0, gcd_base_recast_time=0, animation_lock=0
            ),
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=20 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def expedient(self):
        name = "Expedient"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            follow_up_skills=(
                FollowUp(
                    skill=self.desperate_measures(), delay_after_parent_application=0
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def recitation(self):
        name = "Recitation"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=15 * 1000,
                num_uses=1,
                skill_allowlist=(
                    "Excogitation",
                    "Indomitability",
                    "Adloquium",
                    "Concitation",
                ),
            ),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def aetherpact(self):
        name = "Aetherpact"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def resurrection(self):
        name = "Resurrection"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=8000, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def aetherflow(self):
        return Skill(
            name="Aetherflow",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def deployment_tactics(self):
        return Skill(
            name="Deployment Tactics",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def summon_seraph(self):
        return Skill(
            name="Summon Seraph",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )
