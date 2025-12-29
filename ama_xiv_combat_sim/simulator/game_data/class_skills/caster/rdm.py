import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.damage_instance_class import (
    DamageInstanceClass,
)
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import (
    OffensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.rdm_data import (
    all_rdm_skills,
)


class RdmSkills(GenericJobClass):
    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_rdm_skills)
        self._job_class = "RDM"
        self.__rdm_caster_tax = 100

    def get_status_effect_priority(self):
        return ("Swiftcast", "Acceleration", "Dualcast")

    def get_combo_breakers(self):
        if self._version >= "7.0":
            return ((1, (0,)), (0, (1,)))
        return None

    def __get_dualcast_follow_up(self):
        dualcast_buff = Skill(
            name="Dualcast",
            offensive_buff_spec=OffensiveStatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                add_to_skill_modifier_condition=True,
                duration=15 * 1000,
                num_uses=1,
                skill_allowlist=(
                    "Verthunder II",
                    "Veraero II",
                    "Verfire",
                    "Verstone",
                    "Vercure",
                    "Jolt II",
                    "Jolt III",
                    "Verraise",
                    "Impact",
                    "Grand Impact",
                    "Verthunder III",
                    "Veraero III",
                ),
            ),
        )
        return FollowUp(skill=dualcast_buff, delay_after_parent_application=0)

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
            status_effect_denylist=("Manafication", "Embolden"),
        )

    @GenericJobClass.is_a_skill
    def riposte(self):
        name = "Riposte"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(),),
            timing_spec=self.instant_timing_spec,
            status_effect_denylist=("Manafication", "Embolden"),
        )

    @GenericJobClass.is_a_skill
    def corps_a_corps(self):
        
        true_name = "Corps-a-corps"
        res = []
        for name in ["Corps-a-corps", "Corps-a-Corps"]:
            res.append(Skill(
                name=name,
                is_GCD=False,
                skill_type=SkillType.ABILITY,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(true_name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=630
                ),
                status_effect_denylist=("Manafication", "Embolden"),
            ))
        return res

    @GenericJobClass.is_a_skill
    def verthunder_ii(self):
        name = "Verthunder II"
        verthunder_2_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=800,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verthunder_2_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (verthunder_2_damage_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def veraero_ii(self):
        name = "Veraero II"
        veraero_2_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=800,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    veraero_2_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (veraero_2_damage_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def verfire(self):
        name = "Verfire"
        verfire_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=800,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verfire_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (verfire_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def verstone(self):
        name = "Verstone"
        verstone_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=800,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verstone_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (verstone_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def zwerchhau(self):
        name = "Zwerchhau"
        return Skill(
            name=name,
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
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            combo_spec=(ComboSpec(combo_actions=("Riposte", "Enchanted Riposte")),),
            status_effect_denylist=("Manafication", "Embolden"),
        )

    @GenericJobClass.is_a_skill
    def displacement(self):
        name = "Displacement"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )

    @GenericJobClass.is_a_skill
    def engagement(self):
        name = "Engagement"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=580
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )

    @GenericJobClass.is_a_skill
    def fleche(self):
        name = "Fleche"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )

    @GenericJobClass.is_a_skill
    def redoublement(self):
        name = "Redoublement"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Zwerchhau", "Enchanted Zwerchhau")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=630
            ),
            status_effect_denylist=("Manafication", "Embolden"),
        )

    @GenericJobClass.is_a_skill
    def moulinet(self):
        name = "Moulinet"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            status_effect_denylist=("Manafication", "Embolden"),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def contre_sixte(self):
        name = "Contre Sixte"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            status_effect_denylist=("Manafication", "Embolden"),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def embolden(self):
        name = "Embolden"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            offensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: OffensiveStatusEffectSpec(
                    damage_mult=self._skill_data.get_skill_data(name, "self_buff"),
                    duration=self._skill_data.get_skill_data(name, "duration"),
                ),
                "Party Buff": OffensiveStatusEffectSpec(
                    damage_mult=1.05,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                    is_party_effect=True,
                ),
                #backwards compatibility
                "Buff Only": OffensiveStatusEffectSpec(
                    damage_mult=1.05,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                    is_party_effect=True,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=660
            ),
            off_class_default_condition="Party Buff",
        )

    @GenericJobClass.is_a_skill
    def manafication(self):
        name = "Manafication"
        
        manafication_allowlist = (
            "Verthunder II",
            "Veraero II",
            "Verfire",
            "Verstone",
            "Jolt II",
            "Jolt III",
            "Impact",
            "Grand Impact",
            "Verflare",
            "Verholy",
            "Reprise",
            "Scorch",
            "Verthunder III",
            "Veraero III",
            "Resolution",
            "Enchanted Riposte",
            "Enchanted Zwerchhau",
            "Enchanted Redoublement",
            "Enchanted Moulinet",
            "Enchanted Moulinet Deux",
            "Enchanted Moulinet Trois",
            "Enchanted Reprise",
        )

        offensive_buff_spec = offensive_buff_spec=OffensiveStatusEffectSpec(
                    damage_mult=1.05,
                    duration=self._skill_data.get_skill_data(name, "duration"),
                    num_uses=6,
                    skill_allowlist=manafication_allowlist,
                ) if self._version < "7.4" else None

        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            combo_spec=(ComboSpec(),),
            offensive_buff_spec=offensive_buff_spec,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def jolt_ii(self):
        name = "Jolt II"
        jolt_2_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=760,
        )
        name = "Jolt II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    jolt_2_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (jolt_2_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def jolt_iii(self):
        if self._version < "7.0":
            return None

        name = "Jolt III"
        jolt_3_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=800,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=2000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    jolt_3_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (jolt_3_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def impact(self):
        name = "Impact"
        impact_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=760,
            primary_target_only=False,
        )
        impact_acceleration_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_acceleration"
                    )
                ),
            ),
            delay_after_parent_application=760,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=5000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration, Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    impact_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (impact_damage_follow_up,),
                "Acceleration": (impact_acceleration_damage_follow_up,),
                "Acceleration, Dualcast": (impact_acceleration_damage_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def verflare(self):
        name = "Verflare"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def verholy(self):
        name = "Verholy"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1430
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def reprise(self):
        name = "Reprise"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def scorch(self):
        name = "Scorch"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(combo_actions=("Verflare", "Verholy")),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1830
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def verthunder_iii(self):
        name = "Verthunder III"
        verthunder_3_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=760,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=5000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration, Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    verthunder_3_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (verthunder_3_damage_follow_up,),
                "Acceleration": (verthunder_3_damage_follow_up,),
                "Acceleration, Dualcast": (verthunder_3_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def veraero_iii(self):
        name = "Veraero III"
        veraero_3_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=760,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=5000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=0,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
                "Acceleration, Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=0
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    veraero_3_damage_follow_up,
                    self.__get_dualcast_follow_up(),
                ),
                "Dualcast": (veraero_3_damage_follow_up,),
                "Acceleration": (veraero_3_damage_follow_up,),
                "Acceleration, Dualcast": (veraero_3_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def resolution(self):
        name = "Resolution"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(combo_actions=("Scorch",)),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1560
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def vice_of_thorns(self):
        if self._version < "7.0" or self._level < 92:
            return None
        name = "Vice of Thorns"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),            
            status_effect_denylist=("Manafication",),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def grand_impact(self):
        if self._version < "7.0" or self._level < 96:
            return None
        name = "Grand Impact"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=5000,
                    animation_lock=self.__rdm_caster_tax,
                    application_delay=1559,
                ),
                "Dualcast": TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1550
                ),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (self.__get_dualcast_follow_up(),),
                "Dualcast": tuple(),
            },
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def prerefulgence(self):
        if self._version < "7.0" or self._level < 100:
            return None
        name = "Prefulgence"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1420
            ),
            status_effect_denylist=("Manafication",),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def enchanted_riposte(self):
        name = "Enchanted Riposte"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(),),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=630,
            ),
        )

    @GenericJobClass.is_a_skill
    def enchanted_zwerchhau(self):
        name = "Enchanted Zwerchhau"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Riposte", "Enchanted Riposte")),),
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
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=630,
            ),
        )

    @GenericJobClass.is_a_skill
    def enchanted_redoublement(self):
        name = "Enchanted Redoublement"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Enchanted Zwerchhau",)),),
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
                gcd_base_recast_time=2200,
                animation_lock=650,
                application_delay=630,
            ),
        )

    @GenericJobClass.is_a_skill
    def enchanted_moulinet(self):
        name = "Enchanted Moulinet"
        return Skill(
            name=name,
            combo_spec=(
                (ComboSpec(combo_group=1),) if self._version >= "7.0" else tuple()
            ),
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=800,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def enchanted_moulinet_deux(self):
        if self._version < "7.0":
            return None
        name = "Enchanted Moulinet Deux"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(
                ComboSpec(combo_group=1, combo_actions=("Enchanted Moulinet",)),
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=800,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def enchanted_moulinet_trois(self):
        if self._version < "7.0":
            return None
        name = "Enchanted Moulinet Trois"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Enchanted Deux",)),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=650,
                application_delay=800,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def enchanted_reprise(self):
        name = "Enchanted Reprise"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=650
            ),
        )

    @GenericJobClass.is_a_skill
    def magick_barrier(self):
        name = "Magick Barrier"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=(
                    {
                        DamageInstanceClass.MAGICAL: 0.1,
                    }
                ),
                hp_recovery_up_via_healing_actions=0.05,
                duration=10 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def addle(self):
        name = "Addle"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_debuff_spec=DefensiveStatusEffectSpec(
                damage_reductions=(
                    {
                        DamageInstanceClass.PHYSICAL: 0.05,
                        DamageInstanceClass.MAGICAL: 0.1,
                    }
                ),
                duration=15 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def vercure(self):
        name = "Vercure"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=2000,
                gcd_base_recast_time=2500,
                animation_lock=self.__rdm_caster_tax,
            ),
            heal_spec=HealSpec(potency=350, is_party_effect=True),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

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
                    "Verthunder II",
                    "Veraero II",
                    "Verfire",
                    "Verstone",
                    "Vercure",
                    "Jolt II",
                    "Jolt III",
                    "Verraise",
                    "Impact",
                    "Verthunder III",
                    "Veraero III",
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def acceleration(self):
        name = "Acceleration"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                add_to_skill_modifier_condition=True,
                duration=20 * 1000,
                num_uses=1,
                skill_allowlist=("Impact", "Verthunder III", "Veraero III"),
            ),
        )

    @GenericJobClass.is_a_skill
    def verraise(self):
        name = "Verraise"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=10 * 1000,
                gcd_base_recast_time=2500,
                animation_lock=self.__rdm_caster_tax,
            ),
        )
