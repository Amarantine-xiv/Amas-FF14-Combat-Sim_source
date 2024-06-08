import math
from simulator.game_data.game_consts import GameConsts
from simulator.sim_consts import SimConsts

class ComboTracker:
  def __init__(self, combo_breakers = None):
    self.last_combo_skill_used = {}
    self.combo_breakers = {} if combo_breakers is None else combo_breakers

  def __combo_succeded(self, curr_t, combo_spec, skill_modifier):
    if combo_spec.combo_auto_succeed or \
       skill_modifier.force_combo or \
       len(combo_spec.combo_actions) == 0 or \
       (self.last_combo_skill_used[combo_spec.combo_group][0] + GameConsts.COMBO_EXPIRATION_TIME >= curr_t and \
        self.last_combo_skill_used[combo_spec.combo_group][1] in combo_spec.combo_actions):
      return True
    return False

  def __update_combo(self, curr_t, combo_spec, combo_succeeded, skill_name):
    if combo_succeeded:
      self.last_combo_skill_used[combo_spec.combo_group] = (curr_t, skill_name)
    else:
      self.last_combo_skill_used[combo_spec.combo_group] = (-math.inf, None)

    for combo_group_to_be_broken, breakers in self.combo_breakers.items():
      if combo_spec.combo_group in breakers:
        self.last_combo_skill_used[combo_group_to_be_broken] = (-math.inf, None)

  def compile_and_update_combo(self, curr_t, skill, skill_modifier):
    combo_specs = skill.get_combo_spec(skill_modifier)

    combo_succeeded = True
    for combo_spec in combo_specs:
      if combo_spec.combo_group not in self.last_combo_skill_used.keys():
        self.last_combo_skill_used[combo_spec.combo_group] = (-math.inf, None)

      curr_combo_succeeded = self.__combo_succeded(curr_t, combo_spec, skill_modifier)
      combo_succeeded = combo_succeeded and curr_combo_succeeded
      self.__update_combo(curr_t, combo_spec, curr_combo_succeeded, skill.name)

    return SimConsts.COMBO_SUCCESS if combo_succeeded else SimConsts.COMBO_FAIL