import copy

from typing import Any

from dataclasses import dataclass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.specs.channeling_spec import ChannelingSpec
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.shield_spec import ShieldSpec
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import OffensiveStatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.specs.trigger_spec import TriggerSpec
from ama_xiv_combat_sim.simulator.utils import Utils


@dataclass(frozen=True, order=True)
class Skill:
    # Note: All fields must be either 1) a primitive, 2) a class with the dataclass
    # decorator, or 3) defined with an appropriate __eq__ function.
    name: str
    damage_spec: Any = None
    timing_spec: Any = None
    offensive_buff_spec: Any = None
    offensive_debuff_spec: Any = None
    defensive_buff_spec: Any = None
    defensive_debuff_spec: Any = None
    channeling_spec: Any = None
    job_resource_spec: Any = tuple()
    heal_spec: Any = None
    shield_spec: Any = None
    trigger_spec: Any = None
    combo_spec: Any = tuple()
    status_effect_denylist: tuple = ()
    is_GCD: bool = None
    skill_type: Any = SkillType.UNKNOWN
    ignored_conditions_for_bonus_potency: tuple = tuple()
    job_resources_snapshot: bool = (
        True  # if True, job resource will snapshot. If False, job resources are compiled at application time
    )
    # # Follow up skills will be executed in the order given. Use this fact
    # # to control whether a buff applies before or after damage has gone out from
    # # the skill.
    follow_up_skills: Any = tuple()
    has_aoe: bool = (
        False  # whether the skill has an AOE component to it (damage, or debuff)
    )
    # how much potency is off from the primary skill. Requires damage_spec to be a dictionary.
    aoe_dropoff: float = None
    # the skill conditional to use by default if this skill is used by another class
    off_class_default_condition: str = SimConsts.DEFAULT_CONDITION

    @staticmethod
    def __canonicalize_dict(dict_to_use):
        tmp = {}
        for k, v in dict_to_use.items():
            tmp[frozenset(Utils.canonicalize_condition(k))] = v
        return tmp

    # will modify damage_spec in place
    def __process_aoe_dropoff(self, damage_spec, damage_dropoff):
        if not isinstance(damage_spec, dict):
            damage_spec = {SimConsts.DEFAULT_CONDITION: damage_spec}

        keys = tuple(damage_spec.keys())
        for key in keys:
            if len(key) > 0:
                new_key = f"{key}, {SimConsts.SECONDARY_TARGET}"
            else:
                new_key = SimConsts.SECONDARY_TARGET

            if damage_spec[key] is not None:
                new_damage_spec = copy.deepcopy(damage_spec[key])
                primary_potency = new_damage_spec.potency
                object.__setattr__(
                    new_damage_spec,
                    "potency",
                    (1 - damage_dropoff) * primary_potency,
                )
            else:
                new_damage_spec = None
            damage_spec[new_key] = new_damage_spec
        return damage_spec

    @staticmethod
    def __verify_dict_or_tuple(val, class_instance):
        if isinstance(val, tuple):
            for tmp in val:
                if not isinstance(tmp, class_instance):
                    return False
        elif isinstance(val, dict):
            for _, tmp in val.items():
                if not isinstance(tmp, tuple):
                    return False
        else:
            return False
        return True

    def __set_status_effect_stats(self):
        for spec_to_use, field_to_use in zip(
            [
                "offensive_buff_spec",
                "offensive_debuff_spec",
                "defensive_buff_spec",
                "defensive_debuff_spec",
            ],
            [
                "has_offensive_buff",
                "has_offensive_debuff",
                "has_defensive_buff",
                "has_defensive_debuff",
            ],
        ):
            res = False
            # check if there is a party effect on main skill
            spec = getattr(self, spec_to_use)
            if spec is not None:
                if isinstance(spec, OffensiveStatusEffectSpec):
                    res = True
                elif isinstance(spec, dict):
                    for _, se in spec.items():
                        if se is not None:
                            res = True
                            break

            # check if there is a party effect on any followup
            if isinstance(self.follow_up_skills, tuple):
                for follow_up in self.follow_up_skills:
                    if getattr(follow_up.skill, spec_to_use) is not None:
                        res = True
                    break
            elif isinstance(self.follow_up_skills, dict):
                for _, follow_ups in self.follow_up_skills.items():
                    for follow_up in follow_ups:

                        if getattr(follow_up.skill, spec_to_use) is not None:
                            res = True
                            break
            object.__setattr__(self, field_to_use, res)

    def __set_party_status_effect_stats(self):
        for spec_to_use, field_to_use in zip(
            ["offensive_buff_spec", "offensive_debuff_spec", "defensive_buff_spec", "defensive_debuff_spec"],
            ["has_offensive_party_buff", "has_offensive_party_debuff", "has_defensive_party_buff", "has_defensive_party_debuff"],
        ):
            res = False

            # check if there is a party effect on main skill
            spec = getattr(self, spec_to_use)
            if spec is not None:
                if isinstance(spec, OffensiveStatusEffectSpec) and spec.is_party_effect:
                    res = True
                elif isinstance(spec, dict):
                    for _, se in spec.items():
                        if se is not None and se.is_party_effect:
                            res = True
                            break

            # check if there is a party effect on any followup
            if isinstance(self.follow_up_skills, tuple):
                for follow_up in self.follow_up_skills:
                    sp = getattr(follow_up.skill, spec_to_use)
                    if isinstance(sp, dict):
                        for _, v in sp.items():
                            if v is not None and v.is_party_effect:
                                res = True
                                break
                    elif sp is not None and sp.is_party_effect:
                        res = True
                    break
            elif isinstance(self.follow_up_skills, dict):
                for _, follow_ups in self.follow_up_skills.items():
                    for follow_up in follow_ups:
                        sp = getattr(follow_up.skill, spec_to_use)
                        if isinstance(sp, dict):
                            for _, v in sp.items():
                                if v is not None and v.is_party_effect:
                                    res = True
                                    break
                        elif sp is not None and sp.is_party_effect:
                            res = True
                            break
            object.__setattr__(self, field_to_use, res)

    def __post_init__(self):
        assert isinstance(
            getattr(self, "name"), str
        ), f"Name of skill must be a str. Got: {self.name}"

        is_valid = self.__verify_dict_or_tuple(self.follow_up_skills, FollowUp)
        assert (
            is_valid
        ), f"follow_up_skills must be encoded as a tuple or a dict with values that are tuple for immutability: {self.follow_up_skills}"

        is_valid = self.__verify_dict_or_tuple(self.combo_spec, ComboSpec)
        assert (
            is_valid
        ), f"combo_spec must be encoded as a tuple or a dict with values that are tuple for immutability: {self.combo_spec}"
        is_valid = self.__verify_dict_or_tuple(self.job_resource_spec, JobResourceSpec)
        assert (
            is_valid
        ), f"job_resource_spec must be encoded as a tuple or a dict with values that are tuple: {self.job_resource_spec}"

        assert isinstance(
            self.status_effect_denylist, tuple
        ), "status_effect_denylist must be encoded as a tuple for immutability. Did you encode it as a single string by accident, when it should be a tuple of length 1?"

        if self.aoe_dropoff is not None:
            object.__setattr__(
                self,
                "damage_spec",
                self.__process_aoe_dropoff(self.damage_spec, self.aoe_dropoff),
            )
        if isinstance(self.damage_spec, dict):
            object.__setattr__(
                self, "damage_spec", self.__canonicalize_dict(self.damage_spec)
            )
        if isinstance(self.timing_spec, dict):
            object.__setattr__(
                self, "timing_spec", self.__canonicalize_dict(self.timing_spec)
            )
        if isinstance(self.offensive_buff_spec, dict):
            object.__setattr__(
                self,
                "offensive_buff_spec",
                self.__canonicalize_dict(self.offensive_buff_spec),
            )
        if isinstance(self.offensive_debuff_spec, dict):
            object.__setattr__(
                self,
                "offensive_debuff_spec",
                self.__canonicalize_dict(self.offensive_debuff_spec),
            )
        if isinstance(self.defensive_buff_spec, dict):
            object.__setattr__(
                self,
                "defensive_buff_spec",
                self.__canonicalize_dict(self.defensive_buff_spec),
            )
        if isinstance(self.defensive_debuff_spec, dict):
            object.__setattr__(
                self,
                "defensive_debuff_spec",
                self.__canonicalize_dict(self.defensive_debuff_spec),
            )
        if isinstance(self.heal_spec, dict):
            object.__setattr__(
                self, "heal_spec", self.__canonicalize_dict(self.heal_spec)
            )
        if isinstance(self.shield_spec, dict):
            object.__setattr__(
                self, "shield_spec", self.__canonicalize_dict(self.shield_spec)
            )
        if isinstance(self.trigger_spec, dict):
            object.__setattr__(
                self, "trigger_spec", self.__canonicalize_dict(self.trigger_spec)
            )
        if isinstance(self.follow_up_skills, dict):
            object.__setattr__(
                self,
                "follow_up_skills",
                self.__canonicalize_dict(self.follow_up_skills),
            )
        if isinstance(self.channeling_spec, dict):
            object.__setattr__(
                self,
                "channeling_spec",
                self.__canonicalize_dict(self.channeling_spec),
            )
        if isinstance(self.job_resource_spec, dict):
            object.__setattr__(
                self,
                "job_resource_spec",
                self.__canonicalize_dict(self.job_resource_spec),
            )
        if isinstance(self.combo_spec, dict):
            object.__setattr__(
                self, "combo_spec", self.__canonicalize_dict(self.combo_spec)
            )

        self.__set_party_status_effect_stats()
        self.__set_status_effect_stats()

    def __str__(self):
        res = f"---Skill name: {self.name}---\n"
        res += f"TimingSpec:\n{str(self.timing_spec)}\n"
        res += f"DamageSpec:\n{self.damage_spec}\n"
        res += f"Offensive Buffs:\n{self.offensive_buff_spec}\n"
        res += f"Offensive Debuffs:\n{self.offensive_debuff_spec}\n"
        res += f"Defensive Buffs:\n{self.defensive_buff_spec}\n"
        res += f"Defensive Debuffs:\n{self.defensive_debuff_spec}\n"
        res += f"Heal Spec:\n{self.heal_spec}\n"
        res += f"Shield Spec:\n{self.shield_spec}\n"
        res += f"Trigger Spec:\n{self.trigger_spec}\n"
        res += f"Follow up skills:\n{str(self.follow_up_skills)}\n"
        return res

    def get_combo_spec(self, skill_modifier):
        if len(self.combo_spec) == 0 or isinstance(self.combo_spec, tuple):
            return self.combo_spec
        key_to_use = Utils.get_best_key(
            self.combo_spec.keys(), skill_modifier.with_condition
        )
        return self.combo_spec[key_to_use]

    def get_job_resource_spec(self, skill_modifier):
        if len(self.job_resource_spec) == 0 or isinstance(
            self.job_resource_spec, tuple
        ):
            return self.job_resource_spec
        key_to_use = Utils.get_best_key(
            self.job_resource_spec.keys(), skill_modifier.with_condition
        )
        return self.job_resource_spec[key_to_use]

    def get_follow_up_skills(self, skill_modifier):
        if len(self.follow_up_skills) == 0 or isinstance(self.follow_up_skills, tuple):
            return self.follow_up_skills
        key_to_use = Utils.get_best_key(
            self.follow_up_skills.keys(), skill_modifier.with_condition
        )
        return self.follow_up_skills[key_to_use]

    @staticmethod
    def __get_spec(spec, classType, skill_modifier):
        if spec is None or isinstance(spec, classType):
            return spec
        key_to_use = Utils.get_best_key(spec, skill_modifier.with_condition)
        return spec[key_to_use]
    def get_offensive_buff_spec(self, skill_modifier):
        return self.__get_spec(
            self.offensive_buff_spec, OffensiveStatusEffectSpec, skill_modifier
        )
    def get_defensive_debuff_spec(self, skill_modifier):
        return self.__get_spec(
            self.defensive_debuff_spec, OffensiveStatusEffectSpec, skill_modifier
        )
    def get_defensive_buff_spec(self, skill_modifier):
        return self.__get_spec(
            self.defensive_buff_spec, OffensiveStatusEffectSpec, skill_modifier
        )

    def get_offensive_debuff_spec(self, skill_modifier):
        return self.__get_spec(
            self.offensive_debuff_spec, OffensiveStatusEffectSpec, skill_modifier
        )
    def get_timing_spec(self, skill_modifier):
        return self.__get_spec(self.timing_spec, TimingSpec, skill_modifier)

    def get_damage_spec(self, skill_modifier):
        return self.__get_spec(self.damage_spec, DamageSpec, skill_modifier)

    def get_channeling_spec(self, skill_modifier):
        return self.__get_spec(self.channeling_spec, ChannelingSpec, skill_modifier)

    def get_heal_spec(self, skill_modifier):
        return self.__get_spec(self.heal_spec, HealSpec, skill_modifier)

    def get_shield_spec(self, skill_modifier):
        return self.__get_spec(self.shield_spec, ShieldSpec, skill_modifier)

    def get_trigger_spec(self, skill_modifier):
        return self.__get_spec(self.trigger_spec, TriggerSpec, skill_modifier)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
