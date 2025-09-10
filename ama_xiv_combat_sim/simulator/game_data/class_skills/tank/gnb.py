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

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.gnb_data import (
    all_gnb_skills,
)


class GnbSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_gnb_skills)
        self._job_class = "GNB"

    def get_combo_breakers(self):
        # 0: 1-2-3 combo with keen edge
        # 1: savage claw/gnashing fang
        # 2: aoe combo
        return (
            (0, (2,)),
            (1, (0, 1)),
            (2, (0,)),
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
    def keen_edge(self):
        name = "Keen Edge"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=0),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=893
            ),
        )

    @GenericJobClass.is_a_skill
    def no_mercy(self):
        name = "No Mercy"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=int(19.96 * 1000), damage_mult=1.20
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def brutal_shell(self):
        name = "Brutal Shell"
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
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Keen Edge",)),),
            heal_spec={
                SimConsts.DEFAULT_CONDITION: HealSpec(potency=200),
                "No Combo": None,
            },
            shield_spec={
                SimConsts.DEFAULT_CONDITION: ShieldSpec(shield_mult_on_hp_restored=1.0),
                "No Combo": None,
            },
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: DefensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    skill_allowlist=("Heart of Corundum",),
                    duration=30 * 1000,
                ),
                "No Combo": None,
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1074
            ),
        )

    @GenericJobClass.is_a_skill
    def demon_slice(self):
        name = "Demon Slice"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=2),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def lightning_shot(self):
        name = "Lightning Shot"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
        )

    @GenericJobClass.is_a_skill
    def solid_barrel(self):
        name = "Solid Barrel"
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
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Brutal Shell",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1653
            ),
        )

    @GenericJobClass.is_a_skill
    def burst_strike(self):
        name = "Burst Strike"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=714
            ),
        )

    @GenericJobClass.is_a_skill
    def demon_slaughter(self):
        name = "Demon Slaughter"
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
            combo_spec=(ComboSpec(combo_group=2, combo_actions=("Demon Slice",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def sonic_break(self):
        name = "Sonic Break (dot)"
        sonic_break_dot_gnb = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )

        name = "Sonic Break"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=sonic_break_dot_gnb,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def rough_divide(self):
        if self._version >= "7.0":
            return None

        name = "Rough Divide"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=491
            ),
        )

    @GenericJobClass.is_a_skill
    def gnashing_fang(self):
        name = "Gnashing Fang"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
        )

    @GenericJobClass.is_a_skill
    def savage_claw(self):
        name = "Savage Claw"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Gnashing Fang",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )

    @GenericJobClass.is_a_skill
    def wicked_talon(self):
        name = "Wicked Talon"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Savage Claw",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1162
            ),
        )

    @GenericJobClass.is_a_skill
    def bow_shock(self):
        name = "Bow Shock (dot)"
        bow_shock_dot_gnb = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )

        name = "Bow Shock"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=627
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=bow_shock_dot_gnb,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def jugular_rip(self):
        name = "Jugular Rip"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=802
            ),
        )

    @GenericJobClass.is_a_skill
    def abdomen_tear(self):
        name = "Abdomen Tear"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
        )

    @GenericJobClass.is_a_skill
    def eye_gouge(self):
        name = "Eye Gouge"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=981
            ),
        )

    @GenericJobClass.is_a_skill
    def fated_circle(self):
        name = "Fated Circle"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=537
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def blasting_zone(self):
        name = "Blasting Zone"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )

    @GenericJobClass.is_a_skill
    def hypervelocity(self):
        name = "Hypervelocity"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
        )

    @GenericJobClass.is_a_skill
    def double_down(self):
        name = "Double Down"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
            has_aoe=True,
            aoe_dropoff=0.15,
        )

    @GenericJobClass.is_a_skill
    def fated_brand(self):
        if self._level < 96:
            return None

        name = "Fated Brand"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def reign_of_beasts(self):
        if self._level < 100:
            return None

        name = "Reign of Beasts"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def noble_blood(self):
        if self._level < 100:
            return None

        name = "Noble Blood"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1650
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def lion_heart(self):
        if self._level < 100:
            return None
        name = "Lion Heart"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1790
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def bloodfest(self):
        return Skill(
            name="Bloodfest",
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

    @GenericJobClass.is_a_skill
    def camouflage(self):
        return Skill(
            name="Camouflage",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                increase_parry_rate=0.5,
                duration=20 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def royal_guard(self):
        return Skill(
            name="Royal Guard",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def release_royal_guard(self):
        return Skill(
            name="Release Royal Guard",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def nebula(self):
        if self._level >= 92:
            return None
        return Skill(
            name="Nebula",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.3, duration=15 * 1000
            ),
        )

    @GenericJobClass.is_a_skill
    def great_nebula(self):
        if self._level < 92:
            return None
        return Skill(
            name="Great Nebula",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.4,
                max_hp_mult=1.2,
                duration=15 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def aurora(self):
        return Skill(
            name="Aurora",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec=HealSpec(
                hot_potency=300, duration=18 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def superbolide(self):
        return Skill(
            name="Superbolide",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            # TODO: model the 50% hp cut
            defensive_buff_spec=DefensiveStatusEffectSpec(
                is_invuln=True,
                duration=10 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def trajectory(self):
        if self._version < "7.0":
            return None
        return Skill(
            name="Trajectory",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def heart_of_light(self):
        return Skill(
            name="Heart of Light",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions={
                    DamageInstanceClass.PHYSICAL: 0.05,
                    DamageInstanceClass.MAGICAL: 0.1,
                },
                duration=15 * 1000,
                is_party_effect=True,
            ),
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def catharsis_of_corundum_heal(self):
        name = "Catharsis of Corundum (Heal)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Catharsis of Corundum": HealSpec(potency=900),
            },
            defensive_buff_spec=DefensiveStatusEffectSpec(
                expires_status_effects=("Catharsis of Corundum",), is_party_effect=True
            ),
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def clarity_of_corundum(self):
        name = "Clarity of Corundum"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.15,
                duration=4 * 1000,
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def heart_of_corundum(self):
        clarity_follow_up = FollowUp(
            skill=self.clarity_of_corundum(), delay_after_parent_application=0
        )
        catharsis_follow_up_heal = FollowUp(
            skill=self.catharsis_of_corundum_heal(),
            delay_after_parent_application=int(20.1 * 1000),
        )
        catharsis_follow_up_status = FollowUp(
            skill=Skill(
                name="Catharsis of Corundum",
                is_GCD=False,
                skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
                timing_spec=self.uncontrolled_timing_spec,
                # Defensively set duration, just in case a trigger is missed.
                defensive_buff_spec=DefensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    is_party_effect=True,
                    duration=20 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )

        return Skill(
            name="Heart of Corundum",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.15,
                duration=8 * 1000,
                is_party_effect=True,
                expires_status_effects=("Brutal Shell",),
            ),
            heal_spec={
                "Brutal Shell": HealSpec(potency=200),
                SimConsts.DEFAULT_CONDITION: None,
            },
            shield_spec={
                "Brutal Shell": ShieldSpec(shield_mult_on_hp_restored=1.0),
                SimConsts.DEFAULT_CONDITION: None,
            },
            follow_up_skills=(
                clarity_follow_up,
                catharsis_follow_up_status,
                catharsis_follow_up_heal,
            ),
        )
