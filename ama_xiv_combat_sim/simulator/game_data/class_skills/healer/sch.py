import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sch_data import (
    all_sch_skills,
)


class SchSkills(GenericJobClass):
    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_sch_skills)
        self._job_class = "SCH"

    @GenericJobClass.is_a_skill
    def auto(self):
        name = "Auto"
        return Skill(
            name=name,
            is_GCD=False,
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
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def art_of_war_ii(self):
        name = "Art of War II"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def add_chain_stratagem(self):
        name = "Chain Stratagem"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            debuff_spec=StatusEffectSpec(
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
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Biolysis"
        return Skill(
            name=name,
            is_GCD=True,
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
        if self._level not in [100]:
            return None

        name = "Baneful Impaction (dot)"
        baneful_dot = Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Baneful Impaction"
        return Skill(
            name=name,
            is_GCD=True,
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
            timing_spec=self.instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=1,
                skill_allowlist=("Glare III", "Holy III"),
            ),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def dissipation(self):
        return Skill(
            name="Dissipation", is_GCD=False, timing_spec=self.instant_timing_spec
        )

    @GenericJobClass.is_a_skill
    def aetherflow(self):
        return Skill(
            name="Aetherflow", is_GCD=False, timing_spec=self.instant_timing_spec
        )

    @GenericJobClass.is_a_skill
    def concitation(self):
        if self._level not in [100]:
            return None
        name = "Concitation"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=650, application_delay=670
            ),
        )

    @GenericJobClass.is_a_skill
    def manifestation(self):
        if self._level not in [100]:
            return None
        name = "Manifestation"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )

    @GenericJobClass.is_a_skill
    def accession(self):
        if self._level not in [100]:
            return None
        name = "Accession"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )
