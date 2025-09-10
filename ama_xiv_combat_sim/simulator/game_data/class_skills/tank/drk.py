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

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.drk_data import (
    all_drk_skills,
)


class DrkSkills(GenericJobClass):
    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_drk_skills)
        self._job_class = "DRK"

    def __get_darkside_buff(self):
        name = "Darkside"
        return Skill(
            name=name,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=30000, max_duration=60000, damage_mult=1.10
            ),
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
    def hard_slash(self):
        name = "Hard Slash"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
        )

    @GenericJobClass.is_a_skill
    def syphon_strike(self):
        name = "Syphon Strike"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Hard Slash",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )

    @GenericJobClass.is_a_skill
    def unleash(self):
        name = "Unleash"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=712
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def unmend(self):
        name = "Unmend"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=978
            ),
        )

    @GenericJobClass.is_a_skill
    def souleater(self):
        name = "Souleater"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Syphon Strike",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )

    @GenericJobClass.is_a_skill
    def flood_of_shadow(self):
        name = "Flood of Shadow"
        flood_of_shadow_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=624,
            primary_target_only=False,
        )

        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
            follow_up_skills=(
                flood_of_shadow_damage_follow_up,
                FollowUp(
                    skill=self.__get_darkside_buff(),
                    delay_after_parent_application=0,
                    primary_target_only=True,
                ),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def stalwart_soul(self):
        name = "Stalwart Soul"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(combo_actions=("Unleash",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            # app delay needs verification
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=712
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def edge_of_shadow(self):
        name = "Edge of Shadow"
        edge_of_shadow_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=624,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(
                edge_of_shadow_damage_follow_up,
                FollowUp(
                    skill=self.__get_darkside_buff(), delay_after_parent_application=0
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def salted_earth(self):
        name = "Salted Earth (dot)"
        salted_earth_dot_drk = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                # It is believed that salted earth is a MAGICAL dot (unaspected damage)
                # but the formulas I use have Salted Earth being a very slightly
                # better fit by modelling it as a phys dot, for...some reason.
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )
        name = "Salted Earth"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            follow_up_skills=(
                FollowUp(
                    skill=salted_earth_dot_drk,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=False,
                    primary_target_only=False,
                ),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def salt_and_darkness(self):
        name = "Salt and Darkness"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def plunge(self):
        if self._version >= "7.0":
            return None
        name = "Plunge"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=624
            ),
        )

    @GenericJobClass.is_a_skill
    def abyssal_drain(self):
        name = "Abyssal Drain"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=978
            ),
            # TODO: need to make this not multi-heal on multi-targets. Currently, it will.
            heal_spec=HealSpec(potency=500),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def carve_and_spit(self):
        name = "Carve and Spit"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1473
            ),
            heal_spec=HealSpec(potency=500),
        )

    @GenericJobClass.is_a_skill
    def bloodspiller(self):
        name = "Bloodspiller"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=802
            ),
        )

    @GenericJobClass.is_a_skill
    def quietus(self):
        name = "Quietus"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def shadowbringer(self):
        name = "Shadowbringer"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=666
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def living_shadow(self):
        name = "Living Shadow"
        if self._level >= 100:
            ls_names_and_potency_and_delays = [
                (
                    "Abyssal Drain (pet)",
                    self._skill_data.get_skill_data("Living Shadow", "potency_base"),
                    6800,
                    False,
                    None,
                ),
                (
                    "Shadowbringer (pet)",
                    self._skill_data.get_skill_data(
                        "Living Shadow", "potency_shadowbringer"
                    ),
                    6800 + 2 * 2200,
                    True,
                    self._skill_data.get_skill_data("Shadowbringer", "aoe_dropoff"),
                ),
                (
                    "Edge of Shadow (pet)",
                    self._skill_data.get_skill_data("Living Shadow", "potency_base"),
                    6800 + 3 * 2200,
                    False,
                    None,
                ),
                (
                    "Bloodspiller (pet)",
                    self._skill_data.get_skill_data("Living Shadow", "potency_base"),
                    6800 + 4 * 2200,
                    False,
                    None,
                ),
                (
                    "Disesteem (pet)",
                    self._skill_data.get_skill_data(
                        "Living Shadow", "potency_disesteem"
                    ),
                    6800 + 5 * 2200,
                    True,
                    self._skill_data.get_skill_data("Disesteem", "aoe_dropoff"),
                ),
            ]
        else:
            if self._version >= "7.0":
                ls_names_and_potency_and_delays = [
                    (
                        "Abyssal Drain (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800,
                        False,
                        None,
                    ),
                    (
                        "Shadowbringer (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_shadowbringer"
                        ),
                        6800 + 2 * 2200,
                        True,
                        self._skill_data.get_skill_data("Shadowbringer", "aoe_dropoff"),
                    ),
                    (
                        "Edge of Shadow (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800 + 3 * 2200,
                        False,
                        None,
                    ),
                    (
                        "Bloodspiller (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800 + 4 * 2200,
                        False,
                        None,
                    ),
                    (
                        "Carve and Spit (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800 + 5 * 2200,
                        False,
                        None,
                    ),
                ]
            else:
                ls_names_and_potency_and_delays = [
                    (
                        "Abyssal Drain (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800,
                        False,
                        None,
                    ),
                    (
                        "Plunge (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800 + 2200,
                        False,
                        None,
                    ),
                    (
                        "Shadowbringer (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_shadowbringer"
                        ),
                        6800 + 2 * 2200,
                        True,
                        self._skill_data.get_skill_data("Shadowbringer", "aoe_dropoff"),
                    ),
                    (
                        "Edge of Shadow (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800 + 3 * 2200,
                        False,
                        None,
                    ),
                    (
                        "Bloodspiller (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800 + 4 * 2200,
                        False,
                        None,
                    ),
                    (
                        "Carve and Spit (pet)",
                        self._skill_data.get_skill_data(
                            "Living Shadow", "potency_base"
                        ),
                        6800 + 5 * 2200,
                        False,
                        None,
                    ),
                ]

        _living_shadow_follow_ups = []
        for (
            skill_name,
            potency,
            delay,
            has_aoe,
            aoe_dropoff,
        ) in ls_names_and_potency_and_delays:
            fu = FollowUp(
                skill=Skill(
                    name=skill_name,
                    damage_spec=DamageSpec(
                        potency=potency,
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                    ),
                    status_effect_denylist=("Darkside", "Dragon Sight"),
                    has_aoe=has_aoe,
                    aoe_dropoff=aoe_dropoff,
                ),
                delay_after_parent_application=delay,
                snapshot_buffs_with_parent=False,
                snapshot_debuffs_with_parent=False,
                primary_target_only=not has_aoe,
            )
            _living_shadow_follow_ups.append(fu)
        _living_shadow_follow_ups = tuple(_living_shadow_follow_ups)

        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            follow_up_skills=_living_shadow_follow_ups,
            timing_spec=self.instant_timing_spec,
            status_effect_denylist=("Darkside", "Dragon Sight"),
        )

    @GenericJobClass.is_a_skill
    def scarlet_delirium(self):
        if self._level < 96:
            return None

        name = "Scarlet Delirium"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
        )

    @GenericJobClass.is_a_skill
    def comeuppance(self):
        if self._level < 96:
            return None

        name = "Comeuppance"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=670
            ),
        )

    @GenericJobClass.is_a_skill
    def torcleaver(self):
        if self._level < 96:
            return None

        name = "Torcleaver"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def impalement(self):
        if self._level < 96:
            return None

        name = "Impalement"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=980
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def disesteem(self):
        if self._level < 100:
            return None

        name = "Disesteem"
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
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def shadow_wall(self):
        if self._level >= 92:
            return None
        return Skill(
            name="Shadow Wall",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.3,
                duration=15 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def shadow_vigil_expire(self):
        if self._level < 92:
            return None
        return Skill(
            name="Shadow Vigil (Expire)",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Shadow Vigil": HealSpec(potency=1200),
            },
            # This isn't necessary, but let's be just a bit defensive here.
            defensive_buff_spec=DefensiveStatusEffectSpec(
                expires_status_effects=("Shadow Vigil",)
            ),
        )

    @GenericJobClass.is_a_skill
    def shadow_vigil_heal(self):
        if self._level < 92:
            return None
        return Skill(
            name="Shadow Vigil (Heal)",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(potency=1200),
        )

    @GenericJobClass.is_a_skill
    def shadow_vigil(self):
        if self._level < 92:
            return None
        return Skill(
            name="Shadow Vigil",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.4,
                duration=15 * 1000,
                add_to_skill_modifier_condition=True,
            ),
            follow_up_skills=(
                FollowUp(
                    skill=self.shadow_vigil_expire(),
                    delay_after_parent_application=15 * 1000,
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def dark_mind(self):
        return Skill(
            name="Dark Mind",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions={
                    DamageInstanceClass.PHYSICAL: 0.1,
                    DamageInstanceClass.MAGICAL: 0.2,
                },
                duration=10 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def dark_missionary(self):
        return Skill(
            name="Dark Missionary",
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

    @GenericJobClass.is_a_skill
    def walking_dead(self):
        return Skill(
            name="Walking Dead",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                is_invuln=True,
                duration=10 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def living_dead_heal(self):
        return Skill(
            name="Living Dead (Heal)",
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(potency=1500),
        )

    @GenericJobClass.is_a_skill
    def living_dead(self):
        return Skill(
            name="Living Dead",
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

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

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
    def delirium(self):
        return Skill(
            name="Delirium",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def blood_weapon(self):
        return Skill(
            name="Blood Weapon",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def shadowstride(self):
        return Skill(
            name="Shadowstride",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def the_blackest_night(self):
        return Skill(
            name="The Blackest Night",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            shield_spec=ShieldSpec(
                shield_on_max_hp=0.25, duration=7 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def oblation(self):
        return Skill(
            name="Oblation",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=10 * 1000,
                is_party_effect=True,
            ),
        )
