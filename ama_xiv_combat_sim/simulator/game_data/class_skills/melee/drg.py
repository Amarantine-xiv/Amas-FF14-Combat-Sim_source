from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.drg_data import (
    all_drg_skills,
)


class DrgSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_drg_skills)
        self._job_class = "DRG"
        self.__drg_weapon_skills = (
            "True Thrust",
            "Vorpal Thrust",
            "Piercing Talon",
            "Disembowel",
            "Doom Spike",
            "Fang and Claw",
            "Wheeling Thrust",
            "Sonic Thrust",
            "Coerthan Torment",
            "Raiden Thrust",
            "Draconian Fury",
            "Heavens' Thrust",
            "Chaotic Spring",
            "Drakesbane",
            "Lance Barrage",
            "Spiral Blow",
        )

    def __get_power_surge_follow_up(self):
        name = "Power Surge"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(damage_mult=1.10, duration=int(31.6 * 1000)),
            ),
            delay_after_parent_application=0,
        )

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
    def true_thrust(self):
        name = "True Thrust"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
        )

    @GenericJobClass.is_a_skill
    def vorpal_thrust(self):
        if self._level >= 96:
            return None
        name = "Vorpal Thrust"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1020
            ),
        )

    @GenericJobClass.is_a_skill
    def piercing_talon(self):
        name = "Piercing Talon"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Enhanced Piercing Talon": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "enhanced potency"
                        )
                    ),
                }
                if self._version >= "7.1"
                else DamageSpec(potency=self._skill_data.get_potency(name))
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=850
            ),
        )

    @GenericJobClass.is_a_skill
    def disembowel(self):
        if self._level >= 96:
            return None
        name = "Disembowel"
        disembowel_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=1650,
        )
        disembowel_no_combo_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=1650,
        )
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    disembowel_damage_follow_up,
                    self.__get_power_surge_follow_up(),
                ),
                "No Combo": (disembowel_no_combo_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def lance_charge(self):
        name = "Lance Charge"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=660
            ),
            buff_spec=StatusEffectSpec(
                damage_mult=self._skill_data.get_skill_data(name, "damage_mult"),
                duration=self._skill_data.get_skill_data(name, "duration"),
            ),
        )

    @GenericJobClass.is_a_skill
    def doom_spike(self):
        name = "Doom Spike"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1290
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def spineshatter_dive(self):
        if self._version >= "7.0":
            return None
        name = "Spineshatter Dive"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=800
            ),
        )

    @GenericJobClass.is_a_skill
    def dragonfire_dive(self):
        name = "Dragonfire Dive"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=800
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def battle_litany(self):
        name = "Battle Litany"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
            buff_spec=StatusEffectSpec(
                crit_rate_add=self._skill_data.get_skill_data(name, "crit_rate_add"),
                duration=self._skill_data.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def fang_and_claw(self):
        name = "Fang and Claw"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                (ComboSpec(combo_actions=("Heavens' Thrust",)),)
                if self._version >= "7.0"
                else tuple()
            ),
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                    "No Combo": DamageSpec(
                        potency=self._skill_data.get_potency_no_combo(name)
                    ),
                    "No Combo, No Positional": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_no_pos_no_combo"
                        )
                    ),
                }
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                    "Wheeling Thrust": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_wheeling"
                        )
                    ),
                    "Wheeling Thrust, No Positional": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_wheeling_no_pos"
                        )
                    ),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30
                    * 1000,  # is this actually 31.6? or 30+application delay or whatever?
                    # have this buff be consumed (and maybe wasted) on next weaponskill
                    skill_allowlist=self.__drg_weapon_skills,
                ),
                "Wheeling Thrust": None,
            },
        )

    @GenericJobClass.is_a_skill
    def wheeling_thrust(self):
        name = "Wheeling Thrust"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                (ComboSpec(combo_actions=("Chaotic Spring",)),)
                if self._version >= "7.0"
                else tuple()
            ),
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                    "No Combo": DamageSpec(
                        potency=self._skill_data.get_potency_no_combo(name)
                    ),
                    "No Combo, No Positional": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_no_pos_no_combo"
                        )
                    ),
                }
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                    "Fang and Claw": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fc")
                    ),
                    "Fang and Claw, No Positional": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_fc_no_pos"
                        )
                    ),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30
                    * 1000,  # is this actually 31.6? or 30+application delay or whatever?
                    skill_allowlist=self.__drg_weapon_skills,
                ),
                "Fang and Claw": None,
            },
        )

    @GenericJobClass.is_a_skill
    def geirskogul(self):
        name = "Geirskogul"
        if self._version >= "7.0":
            life_of_the_dragon_follow_up = FollowUp(
                skill=Skill(
                    name="Life of the Dragon",
                    buff_spec=StatusEffectSpec(damage_mult=1.15, duration=20 * 1000),
                ),
                delay_after_parent_application=0,
            )
            geirskogul_damage_follow_up = FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=280)},
                    has_aoe=True,  # is this needed here? What is the convention?
                    aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
                ),
                delay_after_parent_application=670,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
                primary_target_only=False,
            )
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=(
                None
                if self._version >= "7.0"
                else DamageSpec(potency=self._skill_data.get_potency(name))
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=0
            ),
            has_aoe=True,  # is this needed here? What is the convention?
            aoe_dropoff=(
                None
                if self._version >= "7.0"
                else self._skill_data.get_skill_data(name, "aoe_dropoff")
            ),
            follow_up_skills=(
                (
                    geirskogul_damage_follow_up,
                    life_of_the_dragon_follow_up,
                )
                if self._version >= "7.0"
                else tuple()
            ),
        )

    @GenericJobClass.is_a_skill
    def sonic_thrust(self):
        name = "Sonic Thrust"
        sonic_thrust_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                has_aoe=True,
            ),
            delay_after_parent_application=800,
            primary_target_only=False,
        )
        sonic_thrust_no_combo_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
                has_aoe=True,
            ),
            delay_after_parent_application=800,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Doom Spike",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    sonic_thrust_damage_follow_up,
                    self.__get_power_surge_follow_up(),
                ),
                "No Combo": (sonic_thrust_no_combo_damage_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def drakesbane(self):
        if self._version <= "6.55":
            return None
        name = "Drakesbane"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Wheeling Thrust", "Fang and Claw")),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def dragon_sight(self):
        if self._version >= "7.0":
            return None
        name = "Dragon Sight"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=0, animation_lock=600, application_delay=660
                ),
                "Left Eye": TimingSpec(base_cast_time=0, animation_lock=0),
            },
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    damage_mult=1.1, duration=20 * 1000
                ),
                "Left Eye": StatusEffectSpec(
                    damage_mult=1.05, duration=20 * 1000, is_party_effect=True
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def left_eye(self):
        if self._version >= "7.0":
            return None
        # add this is a potential buff for convenience
        name = "Left Eye"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=0),
            buff_spec=StatusEffectSpec(
                damage_mult=1.05, duration=20 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def mirage_dive(self):
        name = "Mirage Dive"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=800
            ),
        )

    @GenericJobClass.is_a_skill
    def nastrond(self):
        name = "Nastrond"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def coerthan_torment(self):
        name = "Coerthan Torment"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("Sonic Thrust",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=490
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def high_jump(self):
        name = "High Jump"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=800, application_delay=490
            ),
        )

    @GenericJobClass.is_a_skill
    def raiden_thrust(self):
        name = "Raiden Thrust"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def stardiver(self):
        name = "Stardiver"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1500, application_delay=1290
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def draconian_fury(self):
        name = "Draconian Fury"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=760
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def heavens_thrust(self):
        name = "Heavens' Thrust"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                ComboSpec(
                    combo_actions=self._skill_data.get_skill_data(name, "combo_action")
                ),
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=710
            ),
        )

    @GenericJobClass.is_a_skill
    def chaotic_spring(self):
        name = "Chaotic Spring (dot)"
        _chaotic_spring_follow_up = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    damage_class=DamageClass.PHYSICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=24 * 1000,
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
        )

        name = "Chaotic Spring"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(
                ComboSpec(
                    combo_actions=self._skill_data.get_skill_data(name, "combo_action")
                ),
            ),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_potency_no_positional(name)
                ),
                "No Combo, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_no_combo"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=450
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (_chaotic_spring_follow_up,),
                "No Combo": tuple(),
                "No Positional": (_chaotic_spring_follow_up,),
                "No Combo, No Positional": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def wyrmwind_thrust(self):
        name = "Wyrmwind Thrust"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1200
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def rise_of_the_dragon(self):
        if self._level < 92:
            return None
        name = "Rise of the Dragon"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def lance_barrage(self):
        if self._level < 96:
            return None
        name = "Lance Barrage"
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=940
            ),
        )

    @GenericJobClass.is_a_skill
    def spiral_blow(self):
        if self._level < 96:
            return None
        name = "Spiral Blow"
        spiral_blow_damage_follow_up = FollowUp(
            skill=Skill(name=name, damage_spec=DamageSpec(potency=300)),
            delay_after_parent_application=1380,
        )
        spiral_blow_no_combo_damage_follow_up = FollowUp(
            skill=Skill(name=name, damage_spec=DamageSpec(potency=140)),
            delay_after_parent_application=1380,
        )
        return Skill(
            name=name,
            is_GCD=True,
            combo_spec=(ComboSpec(combo_actions=("True Thrust", "Raiden Thrust")),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=0
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    spiral_blow_damage_follow_up,
                    self.__get_power_surge_follow_up(),
                ),
                "No Combo": (spiral_blow_no_combo_damage_follow_up,),
            },
        )

    @GenericJobClass.is_a_skill
    def starcross(self):
        if self._level < 100:
            return None
        name = "Starcross"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=600, application_delay=980
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def life_surge(self):
        name = "Life Surge"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=600),
            buff_spec=StatusEffectSpec(
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                duration=5 * 1000,
                num_uses=1,
                skill_allowlist=self.__drg_weapon_skills,
            ),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def true_north(self):
        name = "True North"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def winged_glide(self):
        name = "Winged Glide"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def elusive_jump(self):
        drg_follow_ups = (
            (
                FollowUp(
                    skill=Skill(
                        name="Enhanced Piercing Talon",
                        buff_spec=StatusEffectSpec(
                            duration=15 * 1000,
                            num_uses=1,
                            skill_allowlist=("Piercing Talon",),
                            add_to_skill_modifier_condition=True,
                        ),
                    ),
                    delay_after_parent_application=0,
                ),
            )
            if self._version >= "7.1"
            else tuple()
        )

        return Skill(
            name="Elusive Jump",
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, animation_lock=800),
            follow_up_skills=drg_follow_ups,
        )
