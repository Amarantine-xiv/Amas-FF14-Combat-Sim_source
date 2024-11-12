import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.whm_data import (
    all_whm_skills,
)

class WhmSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_whm_skills)
        self._job_class='WHM'

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
    def glare_iii(self):
        name = "Glare III"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=100, application_delay=1290
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
        )

    @GenericJobClass.is_a_skill
    def glare_iv(self):
        if self._level not in [100]:
            return None

        name = "Glare IV"
        return Skill(
                name=name,
                is_GCD=True,
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
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def dia(self):
        name = "Dia (dot)"
        dia_dot_whm = Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

        name = "Dia"
        return Skill(
            name=name,
            is_GCD=True,
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
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=530
            ),
            buff_spec=StatusEffectSpec(
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
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )

    @GenericJobClass.is_a_skill
    def afflatus_solace(self):
        name = "Afflatus Solace"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
        )

    @GenericJobClass.is_a_skill
    def medica_iii(self):
        if self._level not in [100]:
            return None
        name = "Medica III"
        return Skill(
                name=name,
                is_GCD=True,
                timing_spec=TimingSpec(
                    base_cast_time=2000, animation_lock=100, application_delay=0
                ),
            )

    @GenericJobClass.is_a_skill
    def divine_caress(self):
        if self._level not in [100]:
            return None
        name = "Divine Caress"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

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
