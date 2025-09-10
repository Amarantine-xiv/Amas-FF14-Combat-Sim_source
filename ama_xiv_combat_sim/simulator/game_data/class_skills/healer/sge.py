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

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sge_data import (
    all_sge_skills,
)


class SgeSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_sge_skills)
        self._job_class = "SGE"

    @staticmethod
    def _get_non_stacking_shield_set():
        # TODO: there's a difference between galvanize and catalyze
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

    @GenericJobClass.is_a_resource
    def panhaimatinon_resource(self):
        name = "Panhaimatinon"
        job_resource_settings = JobResourceSettings(
            max_value=5,
            skill_allowlist=(
                "Panhaima (Absorb)",
                "Panhaima (Expire)",
                "Panhaima",
            ),
        )
        return (name, job_resource_settings)

    @GenericJobClass.is_a_resource
    def haimatinon_resource(self):
        name = "Haimatinon"
        job_resource_settings = JobResourceSettings(
            max_value=5,
            skill_allowlist=(
                "Haima (Absorb)",
                "Haima (Expire)",
                "Haima",
            ),
        )
        return (name, job_resource_settings)

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
    def dosis_iii(self):
        name = "Dosis III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=670
            ),
            damage_spec=DamageSpec(potency=all_sge_skills.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def phlegma_iii(self):
        name = "Phlegma III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def toxikon_ii(self):
        name = "Toxikon II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1200
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def dyskrasia_ii(self):
        name = "Dyskrasia II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            damage_spec=DamageSpec(potency=all_sge_skills.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def pneuma(self):
        name = "Pneuma"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=580
            ),
            heal_spec=HealSpec(potency=600, is_aoe=True, is_party_effect=True),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.4,
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def philosophia_heal(self):
        return Skill(
            name="Philosophia (Heal)",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(potency=150),
        )

    @GenericJobClass.is_a_skill
    def philosophia(self):
        return Skill(
            name="Philosophia",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                healing_magic_potency_mult=1.2,
                duration=20 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def eukrasia(self):
        name = "Eukrasia"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1000,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )

    @GenericJobClass.is_a_skill
    def eukrasia_dosis_iii(self):
        name = "Eukrasian Dosis III (dot)"
        e_dosis_iii = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_sge_skills.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Eukrasian Dosis III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=760,
                gcd_base_recast_time=1500,
            ),
            follow_up_skills=(
                FollowUp(
                    skill=e_dosis_iii,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def eukrasian_dyskrasia(self):
        if self._version < "7.0":
            return None
        name = "Eukrasian Dosis III (dot)"  # for now, put same name to overwrite, even though it's E. dysk....
        e_dysk = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=all_sge_skills.get_skill_data(name, "potency_dysk"),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Eukrasian Dyskrasia"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1030,
                gcd_base_recast_time=1500,
            ),
            follow_up_skills=(
                FollowUp(
                    skill=e_dysk,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def psyche(self):
        if self._version < "7.0" or self._level < 92:
            return None
        name = "Psyche"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=100, application_delay=1100
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def diagnosis(self):
        name = "Diagnosis"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            # TODO: Fix made up application delay
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=670
            ),
            heal_spec=HealSpec(potency=450, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def prognosis(self):
        name = "Prognosis"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            # TODO: Fix made up application delay
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=100, application_delay=670
            ),
            heal_spec=HealSpec(potency=300, is_party_effect=True, is_aoe=True),
        )

    @GenericJobClass.is_a_skill
    def physis_ii(self):
        name = "Physis II"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                hot_potency=130,
                duration=15 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
            defensive_buff_spec=DefensiveStatusEffectSpec(
                hp_recovery_up_via_healing_actions=0.1,
                duration=all_sge_skills.get_skill_data(name, "healing_action_duration"),
            ),
        )

    @GenericJobClass.is_a_skill
    def eukrasian_diagnosis(self):
        name = "Eukrasian Diagnosis"
        non_stacking_shield_set = self._get_non_stacking_shield_set()
        non_stacking_shield_set.remove(name)

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(base_cast_time=0, gcd_base_recast_time=1500),
            heal_spec=HealSpec(potency=300, is_party_effect=True),
            shield_spec={
                SimConsts.DEFAULT_CONDITION: ShieldSpec(
                    shield_mult_on_hp_restored=1.8,
                    duration=30 * 1000,
                    is_party_effect=True,
                    does_not_stack_with=frozenset(non_stacking_shield_set),
                ),
                "Critical": ShieldSpec(
                    shield_mult_on_hp_restored=3.6,
                    duration=30 * 1000,
                    is_party_effect=True,
                    does_not_stack_with=frozenset(non_stacking_shield_set),
                ),
            },
            defensive_buff_spec=DefensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True, duration=30 * 1000
            ),
        )

    @GenericJobClass.is_a_skill
    def eukrasian_prognosis_ii(self):
        if self._level < 96:
            return None
        name = "Eukrasian Prognosis II"
        non_stacking_shield_set = self._get_non_stacking_shield_set()
        non_stacking_shield_set.remove(name)

        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(base_cast_time=0, gcd_base_recast_time=1500),
            heal_spec=HealSpec(potency=100, is_party_effect=True, is_aoe=True),
            shield_spec=ShieldSpec(
                shield_mult_on_hp_restored=3.6,
                duration=30 * 1000,
                is_party_effect=True,
                is_aoe=True,
                does_not_stack_with=frozenset(non_stacking_shield_set),
            ),
            defensive_buff_spec=DefensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True, duration=30 * 1000
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
                    "Dosis III",
                    "Pneuma",
                    "Diagnosis",
                    "Prognosis",
                    "Egeiro",
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def kerachole(self):
        return Skill(
            name="Kerachole",
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
    def druochole(self):
        name = "Druochole"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=600, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def ixochole(self):
        name = "Ixochole"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=400, is_party_effect=True, is_aoe=True),
        )

    @GenericJobClass.is_a_skill
    def zoe(self):
        name = "Zoe"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                healing_magic_potency_mult=1.5,
                num_uses=1,
                skill_allowlist=(
                    "Diagnosis",
                    "Prognosis",
                    "Eukrasian Diagnosis",
                    "Eukrasian Prognosis II",
                    "Pneuma",
                ),
                duration=30 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def pepsis(self):
        return Skill(
            name="Pepsis",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Eukrasian Diagnosis": HealSpec(
                    potency=450, is_party_effect=True, is_aoe=True
                ),
                "Eukrasian Prognosis II": HealSpec(
                    potency=350, is_party_effect=True, is_aoe=True
                ),
            },
            defensive_buff_spec=DefensiveStatusEffectSpec(
                expires_status_effects=(
                    ("Eukrasian Prognosis II", "Eukrasian Diagnosis")
                )
            ),
        )

    @GenericJobClass.is_a_skill
    def taurochole(self):
        name = "Taurochole"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=700, is_party_effect=True),
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=15 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def holos(self):
        name = "Holos"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(potency=300, is_party_effect=True, is_aoe=True),
            shield_spec=ShieldSpec(
                shield_mult_on_hp_restored=1.0,
                duration=30 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=20 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def haima_expire(self):
        # TODO: this should probably be named something different
        # depending on what logs actually call it
        name = "Haima (Expire)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            off_class_default_condition="Heal Only",
            heal_spec={
                "5 Haimatinon": HealSpec(potency=int(150 * 5), is_party_effect=True),
                "4 Haimatinon": HealSpec(potency=int(150 * 4), is_party_effect=True),
                "3 Haimatinon": HealSpec(potency=int(150 * 3), is_party_effect=True),
                "2 Haimatinon": HealSpec(potency=int(150 * 2), is_party_effect=True),
                "1 Haimatinon": HealSpec(potency=int(150 * 1), is_party_effect=True),
                SimConsts.DEFAULT_CONDITION: None,
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Haimatinon", change=-math.inf),
                ),
                "Heal Only": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def haima_absorb(self):
        # TODO: this should probably be named something different
        # depending on what logs actually call it
        name = "Haima (Absorb)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            off_class_default_condition="Shield Only",
            shield_spec={
                # TODO: these durations are NOT right- they should be
                # 15s - (time it's lasted so far). But we get around this
                # by forcing the Haimatinon expiration.
                "5 Haimatinon": ShieldSpec(
                    potency=300, duration=15 * 1000, is_party_effect=True
                ),
                "4 Haimatinon": ShieldSpec(
                    potency=300, duration=15 * 1000, is_party_effect=True
                ),
                "3 Haimatinon": ShieldSpec(
                    potency=300, duration=15 * 1000, is_party_effect=True
                ),
                "2 Haimatinon": ShieldSpec(
                    potency=300, duration=15 * 1000, is_party_effect=True
                ),
                "1 Haimatinon": ShieldSpec(
                    potency=300, duration=15 * 1000, is_party_effect=True
                ),
                SimConsts.DEFAULT_CONDITION: None,
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Haimatinon", change=-1),
                ),
                "Shield Only": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def haima(self):
        name = "Haima"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            off_class_default_condition="Shield Only",
            shield_spec=ShieldSpec(
                potency=300, duration=15 * 1000, is_party_effect=True
            ),
            job_resource_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: (
                        JobResourceSpec(
                            name="Haimatinon", change=5, duration=15 * 1000
                        ),
                    ),
                    "Shield Only": tuple(),
                }
            ),
            # TODO: this can trigger earlier
            follow_up_skills=(
                FollowUp(
                    skill=self.haima_expire(),
                    delay_after_parent_application=15 * 1000,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def panhaima_expire(self):
        # TODO: this should probably be named something different
        # depending on what logs actually call it
        name = "Panhaima (Expire)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            off_class_default_condition="Heal Only",
            heal_spec={
                "5 Panhaimatinon": HealSpec(potency=int(100 * 5), is_party_effect=True),
                "4 Panhaimatinon": HealSpec(potency=int(100 * 4), is_party_effect=True),
                "3 Panhaimatinon": HealSpec(potency=int(100 * 3), is_party_effect=True),
                "2 Panhaimatinon": HealSpec(potency=int(100 * 2), is_party_effect=True),
                "1 Panhaimatinon": HealSpec(potency=int(100 * 1), is_party_effect=True),
                SimConsts.DEFAULT_CONDITION: None,
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Panhaimatinon", change=-math.inf),
                ),
                "Heal Only": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def panhaima_absorb(self):
        # TODO: this should probably be named something different
        # depending on what logs actually call it
        name = "Panhaima (Absorb)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            off_class_default_condition="Shield Only",
            shield_spec={
                # TODO: these durations are NOT right- they should be
                # 15s - (time it's lasted so far). But we get around this
                # by forcing the Panhaimatinon expiration.
                "5 Panhaimatinon": ShieldSpec(
                    potency=200, duration=15 * 1000, is_party_effect=True
                ),
                "4 Panhaimatinon": ShieldSpec(
                    potency=200, duration=15 * 1000, is_party_effect=True
                ),
                "3 Panhaimatinon": ShieldSpec(
                    potency=200, duration=15 * 1000, is_party_effect=True
                ),
                "2 Panhaimatinon": ShieldSpec(
                    potency=200, duration=15 * 1000, is_party_effect=True
                ),
                "1 Panhaimatinon": ShieldSpec(
                    potency=200, duration=15 * 1000, is_party_effect=True
                ),
                SimConsts.DEFAULT_CONDITION: None,
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Panhaimatinon", change=-1),
                ),
                "Shield Only": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def panhaima(self):
        name = "Panhaima"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            off_class_default_condition="Shield Only",
            # TODO: this should trigger multiple shields, up to 5 uses.
            shield_spec=ShieldSpec(
                potency=200, duration=15 * 1000, is_party_effect=True
            ),
            job_resource_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: (
                        JobResourceSpec(
                            name="Panhaimatinon", change=5, duration=15 * 1000
                        ),
                    ),
                    "Shield Only": tuple(),
                }
            ),
            follow_up_skills=(
                FollowUp(
                    skill=self.panhaima_expire(),
                    delay_after_parent_application=15 * 1000,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def krasis(self):
        return Skill(
            name="Krasis",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                hp_recovery_up_via_healing_actions=0.2,
                duration=10 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def kardia_heal(self):
        return Skill(
            name="Kardia (Heal)",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(potency=170, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def kardion_heal(self):
        return Skill(
            name="Kardion (Heal)",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(potency=170, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def kardia(self):
        return Skill(
            name="Kardia",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def soteria(self):
        return Skill(
            name="Soteria",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def rhizomata(self):
        return Skill(
            name="Rhizomata",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def icarus(self):
        return Skill(
            name="Icarus",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def egeiro(self):
        name = "Egeiro"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=8000, animation_lock=650, application_delay=620
            ),
        )
