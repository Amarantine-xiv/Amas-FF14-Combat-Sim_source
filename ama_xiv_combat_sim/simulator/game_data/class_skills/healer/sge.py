import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sge_data import (
    all_sge_skills,
)


class SgeSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_sge_skills)
        self._job_class = "SGE"

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
    def dosis_iii(self):
        name = "Dosis III"
        return Skill(
            name=name,
            is_GCD=True,
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
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=580
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_sge_skills.get_potency(name)
                )
            },
            has_aoe=True,
            aoe_dropoff=0.4,
        )

    @GenericJobClass.is_a_skill
    def eukrasia(self):
        name = "Eukrasia"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1000,
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
        if self._level not in [100]:
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
        if self._level not in [100]:
            return None
        name = "Psyche"
        return Skill(
            name=name,
            is_GCD=False,
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
