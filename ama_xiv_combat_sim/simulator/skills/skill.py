from dataclasses import dataclass
from ama_xiv_combat_sim.simulator.utils import Utils
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from typing import Any

@dataclass(frozen=True, order=True)
class Skill:
  # Note: All fields must be either 1) a primitive, 2) a class with the dataclass
  # decorator, or 3) defined with an appropriate __eq__ function.
  name: str
  damage_spec: Any = None
  timing_spec: Any = None
  buff_spec: Any = None
  debuff_spec: Any = None
  job_resource_spec: Any = tuple()
  combo_spec: Any = tuple()
  status_effect_denylist: tuple = ()
  is_GCD: bool = None
  ignored_conditions_for_bonus_potency: tuple = tuple()
  job_resources_snapshot: bool = True #if True, job resource will snapshot. If False, job resources are compiled at application time
  # # Follow up skills will be executed in the order given. Use this fact
  # # to control whether a buff applies before or after damage has gone out from
  # # the skill.
  follow_up_skills: Any = tuple()

  @staticmethod
  def __canonicalize_dict(dict_to_use):
      tmp = {}
      for k,v in dict_to_use.items():
        tmp[frozenset(Utils.canonicalize_condition(k))] = v
      return tmp

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

  def __set_status_effect_stats(self, is_buff):
    spec_to_use = 'buff_spec' if is_buff else 'debuff_spec'
    field_to_use = 'has_buff' if is_buff else 'has_debuff'
    res = False

    #check if there is a party effect on main skill
    spec = getattr(self, spec_to_use)
    if spec is not None:
      if isinstance(spec, StatusEffectSpec):
        res = True
      elif isinstance(spec, dict):
        for _, se in spec.items():
          if se is not None:
            res = True
            break

    #check if there is a party effect on any followup
    if isinstance(self.follow_up_skills, tuple):
      for follow_up in self.follow_up_skills:
        if getattr(follow_up.skill, spec_to_use) is not None:
          res = True
        break
    elif isinstance(self.follow_up_skills, dict):
      for _, follow_ups in self.follow_up_skills.items():
        for follow_up in follow_ups:
          # print(follow_up)
          # print(getattr(follow_up.skill, spec_to_use))

          if getattr(follow_up.skill, spec_to_use) is not None:
            res = True
            break
    object.__setattr__(self, field_to_use, res)

  def __set_party_status_effect_stats(self, is_buff):
    spec_to_use = 'buff_spec' if is_buff else 'debuff_spec'
    field_to_use = 'has_party_buff' if is_buff else 'has_party_debuff'
    res = False

    #check if there is a party effect on main skill
    spec = getattr(self, spec_to_use)
    if spec is not None:
      if isinstance(spec, StatusEffectSpec) and spec.is_party_effect:
        res = True
      elif isinstance(spec, dict):
        for _, se in spec.items():
          if se is not None and se.is_party_effect:
            res = True
            break

    #check if there is a party effect on any followup
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
    is_valid = self.__verify_dict_or_tuple(self.follow_up_skills, FollowUp)
    assert is_valid, "follow_up_skills must be encoded as a tuple or a dict with values that are tuple for immutability: {}".format(self.follow_up_skills)

    is_valid = self.__verify_dict_or_tuple(self.combo_spec, ComboSpec)
    assert is_valid, "combo_spec must be encoded as a tuple or a dict with values that are tuple for immutability: {}".format(self.combo_spec)

    is_valid = self.__verify_dict_or_tuple(self.job_resource_spec, JobResourceSpec)
    assert is_valid, "job_resource_spec must be encoded as a tuple or a dict with values that are tuple: {}".format(self.job_resource_spec)

    assert isinstance(self.status_effect_denylist, tuple), "status_effect_denylist must be encoded as a tuple for immutability. Did you encode it as a single string by accident, when it should be a tuple of length 1?"

    if isinstance(self.damage_spec, dict):
      object.__setattr__(self, "damage_spec", self.__canonicalize_dict(self.damage_spec))
    if isinstance(self.timing_spec, dict):
      object.__setattr__(self, "timing_spec", self.__canonicalize_dict(self.timing_spec))
    if isinstance(self.buff_spec, dict):
      object.__setattr__(self, "buff_spec", self.__canonicalize_dict(self.buff_spec))
    if isinstance(self.debuff_spec, dict):
      object.__setattr__(self, "debuff_spec", self.__canonicalize_dict(self.debuff_spec))
    if isinstance(self.follow_up_skills, dict):
      object.__setattr__(self, "follow_up_skills", self.__canonicalize_dict(self.follow_up_skills))
    if isinstance(self.job_resource_spec, dict):
      object.__setattr__(self, "job_resource_spec", self.__canonicalize_dict(self.job_resource_spec))
    if isinstance(self.combo_spec, dict):
      object.__setattr__(self, "combo_spec", self.__canonicalize_dict(self.combo_spec))

    # This is shit code. I'm sorry but I'm in a hurry.
    self.__set_party_status_effect_stats(is_buff=True)
    self.__set_party_status_effect_stats(is_buff=False)
    self.__set_status_effect_stats(is_buff=True)
    self.__set_status_effect_stats(is_buff=False)

  def __str__(self):
    res = "---Skill name: {}---\n".format(self.name)
    res += "TimingSpec:\n{}\n".format(str(self.timing_spec))
    res += "DamageSpec:\n{}\n".format(self.damage_spec)
    res += "Buffs:\n{}\n".format(self.buff_spec)
    res += "Debuffs:\n{}\n".format(self.debuff_spec)
    res += "Follow up skills:\n{}\n".format(str(self.follow_up_skills))
    return res

  def get_combo_spec(self, skill_modifier):
    if len(self.combo_spec) == 0 or isinstance(self.combo_spec, tuple):
      return self.combo_spec
    key_to_use = Utils.get_best_key(self.combo_spec.keys(),
                                    skill_modifier.with_condition)
    return self.combo_spec[key_to_use]

  def get_job_resource_spec(self, skill_modifier):
    if len(self.job_resource_spec) == 0 or isinstance(self.job_resource_spec, tuple):
      return self.job_resource_spec
    key_to_use = Utils.get_best_key(self.job_resource_spec.keys(),
                                    skill_modifier.with_condition)
    return self.job_resource_spec[key_to_use]

  def get_follow_up_skills(self, skill_modifier):
    if len(self.follow_up_skills) == 0 or isinstance(self.follow_up_skills, tuple):
      return self.follow_up_skills
    key_to_use = Utils.get_best_key(self.follow_up_skills.keys(),
                                    skill_modifier.with_condition)
    return self.follow_up_skills[key_to_use]

  def get_buff_spec(self, skill_modifier):
    if self.buff_spec is None or isinstance(self.buff_spec, StatusEffectSpec):
      return self.buff_spec
    key_to_use = Utils.get_best_key(self.buff_spec.keys(),
                                    skill_modifier.with_condition)
    return self.buff_spec[key_to_use]

  def get_debuff_spec(self, skill_modifier):
    if self.debuff_spec is None or isinstance(self.debuff_spec, StatusEffectSpec):
      return self.debuff_spec
    key_to_use = Utils.get_best_key(self.debuff_spec.keys(),
                                    skill_modifier.with_condition)
    return self.debuff_spec[key_to_use]

  def get_timing_spec(self, skill_modifier):
    if self.timing_spec is None or isinstance(self.timing_spec, TimingSpec):
      return self.timing_spec
    key_to_use = Utils.get_best_key(self.timing_spec.keys(),
                                    skill_modifier.with_condition)
    return self.timing_spec[key_to_use]

  def get_damage_spec(self, skill_modifier):
    if self.damage_spec is None or isinstance(self.damage_spec, DamageSpec):
      return self.damage_spec

    key_to_use = Utils.get_best_key(self.damage_spec.keys(),
                                    skill_modifier.with_condition)
    return self.damage_spec[key_to_use]

  def __hash__(self):
    return hash(self.name)