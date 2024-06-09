from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.trackers.status_effects import StatusEffects

class StatusEffectTracker():
  def __init__(self, status_effects_priority=tuple()):
    self.buffs = {}
    self.debuffs = {}
    self.__status_effects_priority = status_effects_priority

  @staticmethod
  def __expire_status_effects(t, status_effects):
    se_skill_names = list(status_effects.keys())
    for se_skill_name in se_skill_names:
      (_, end_time, num_uses, _) = status_effects[se_skill_name]
      if t > end_time or num_uses == 0:
        del status_effects[se_skill_name]

  def expire_status_effects(self, t):
    self.__expire_status_effects(t, self.buffs)
    self.__expire_status_effects(t, self.debuffs)

  @staticmethod
  def __add_to_status_effects(status_effects, start_time, skill_name, status_effect_spec):
    if skill_name not in status_effects:
      #check if the status effect needs to exist before it's extended
      if status_effect_spec.extend_only:
        return

      prev_start_time = start_time
      end_time = start_time + status_effect_spec.duration
      status_effects[skill_name] = (start_time, end_time, status_effect_spec.num_uses, status_effect_spec)
    else:
      prev_start_time, prev_end_time, prev_num_uses, prev_status_effect_spec = status_effects[skill_name]
      time_left = max(prev_end_time - start_time, 0)
      if status_effect_spec.extends_existing_duration:
        new_duration = min(status_effect_spec.max_duration, time_left + status_effect_spec.duration)
      else:
        new_duration = time_left
      new_num_uses = min(prev_num_uses+status_effect_spec.num_uses, status_effect_spec.max_num_uses)
      # Note that this overrides the existing status_effect_spec. This is on purpose,
      # as that seems generally how the game works.
      status_effects[skill_name] = (prev_start_time, start_time + new_duration, new_num_uses, status_effect_spec)

      if status_effect_spec != prev_status_effect_spec:
        prev_status_effect_spec_has_speed = (prev_status_effect_spec.auto_attack_delay_reduction > 0 or
                                             prev_status_effect_spec.haste_time_reduction > 0  or
                                             prev_status_effect_spec.flat_cast_time_reduction > 0)
        if prev_status_effect_spec_has_speed:
          print('---Warning: overwrote previous status effect spec. Rotation timings may be off.')

  def __expire_named_effect(self, expired_effect_name, t):
    if expired_effect_name in self.buffs.keys():
      start_time, _, prev_num_uses, prev_status_effect_spec = self.buffs[expired_effect_name]
      self.buffs[expired_effect_name] = (start_time, t, prev_num_uses, prev_status_effect_spec)
    if expired_effect_name in self.debuffs.keys():
      start_time, _, prev_num_uses, prev_status_effect_spec = self.debuffs[expired_effect_name]
      self.debuffs[expired_effect_name] = (start_time,t, prev_num_uses, prev_status_effect_spec)

  def add_to_status_effects(self, t, skill, skill_modifier):
    buff_spec = skill.get_buff_spec(skill_modifier)
    debuff_spec = skill.get_debuff_spec(skill_modifier)

    if buff_spec is not None:
      self.__add_to_status_effects(self.buffs, t, skill.name, buff_spec)
      for expired_effect_name in buff_spec.expires_status_effects:
        self.__expire_named_effect(expired_effect_name, t)

    if debuff_spec is not None:
      self.__add_to_status_effects(self.debuffs, t, skill.name, debuff_spec)
      for expired_effect_name in debuff_spec.expires_status_effects:
        self.__expire_named_effect(expired_effect_name, t)

  @staticmethod
  def __get_valid_status_effects(curr_t, status_effects, status_effect_denylist, skill_name):
    res = []
    for status_effect_skill_name in status_effects.keys():
      (start_time, end_time, num_uses, spec) = status_effects[status_effect_skill_name]
      if curr_t < start_time:
        continue
      if status_effect_skill_name in status_effect_denylist:
        continue
      if spec.skill_allowlist is not None and skill_name not in spec.skill_allowlist:
        continue
      res.append(status_effect_skill_name)
    return tuple(res)

  def __delete_lower_priority_status_effects(self, valid_status_effects):
    valid_status_effects = list(valid_status_effects)

    for i in range (0, len(self.__status_effects_priority)):
      status_effect = self.__status_effects_priority[i]
      if status_effect in valid_status_effects:
        for j in range(i+1, len(self.__status_effects_priority)):
          status_effect_to_delete = self.__status_effects_priority[j]
          try:
            idx = valid_status_effects.index(status_effect_to_delete)
            del valid_status_effects[idx]
          except ValueError:
            pass
        break
    return tuple(valid_status_effects)

  def __compile_status_effects(self, curr_t, status_effects, status_effect_denylist, skill_name):
    crit_rate_add = 0.0
    dh_rate_add = 0.0
    damage_mult = 1.0
    main_stat_add = 0.0
    auto_attack_delay_mult = 1.0
    haste_time_mult = 1.0
    flat_cast_time_reduction = 0
    guaranteed_crit = ForcedCritOrDH.DEFAULT
    guaranteed_dh = ForcedCritOrDH.DEFAULT
    skill_modifier_conditions = []

    valid_status_effects = self.__get_valid_status_effects(curr_t, status_effects, status_effect_denylist, skill_name)
    valid_and_prioritized_status_effects = self.__delete_lower_priority_status_effects(valid_status_effects)

    for status_effect_skill_name in valid_and_prioritized_status_effects:
      (start_time, end_time, num_uses, spec) = status_effects[status_effect_skill_name]
      status_effects[status_effect_skill_name] = (start_time, end_time, num_uses-1, spec)
      tmp = status_effects[status_effect_skill_name]
      crit_rate_add += spec.crit_rate_add
      dh_rate_add += spec.dh_rate_add
      damage_mult *= spec.damage_mult
      main_stat_add += spec.main_stat_add
      auto_attack_delay_mult *= (1-spec.auto_attack_delay_reduction)
      haste_time_mult *= (1-spec.haste_time_reduction)
      flat_cast_time_reduction += spec.flat_cast_time_reduction
      if spec.guaranteed_crit is not ForcedCritOrDH.DEFAULT:
        assert guaranteed_crit is ForcedCritOrDH.DEFAULT, "Cannot force 2 different crit statuses on a skill. Be sure to only have 1 forced crit status on all buffs/debuffs."
        guaranteed_crit = spec.guaranteed_crit

      if spec.guaranteed_dh is not ForcedCritOrDH.DEFAULT:
        assert guaranteed_dh is ForcedCritOrDH.DEFAULT, "Cannot force 2 different direct hit statuses on a skill. Be sure to only have 1 forced direct hit status on all buffs/debuffs."
        guaranteed_dh = spec.guaranteed_dh

      if spec.add_to_skill_modifier_condition:
        skill_modifier_conditions.append(status_effect_skill_name)

    status_effects = StatusEffects(crit_rate_add=crit_rate_add,
                                   dh_rate_add=dh_rate_add,
                                   damage_mult=damage_mult,
                                   main_stat_add=main_stat_add,
                                   auto_attack_delay_mult=auto_attack_delay_mult,
                                   haste_time_mult=haste_time_mult,
                                   flat_cast_time_reduction=flat_cast_time_reduction,
                                   guaranteed_crit=guaranteed_crit,
                                   guaranteed_dh=guaranteed_dh,
                                   status_effects = tuple(valid_and_prioritized_status_effects))
    return (status_effects, ", ".join(skill_modifier_conditions))

  def compile_buffs(self, t, skill=Skill(name='')):
    status_effect_denylist = skill.status_effect_denylist
    return self.__compile_status_effects(t, self.buffs, status_effect_denylist, skill.name)

  def compile_debuffs(self, t, skill=Skill(name='')):
    status_effect_denylist = skill.status_effect_denylist
    return self.__compile_status_effects(t, self.debuffs, status_effect_denylist, skill.name)