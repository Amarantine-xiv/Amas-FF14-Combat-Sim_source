import copy
import math
import numpy as np
import time

from collections import namedtuple
from simulator.calcs.compute_damage_utils import ComputeDamageUtils
from simulator.trackers.damage_tracker import DamageTracker


class PerInstanceDamage(namedtuple('PerInstanceDamage', ['application_time', 'snapshot_time', 'skill_name', 'potency', 'skill_modifier_condition', 'status_effects', 'expected_damage', 'standard_deviation', 'event_id'])):
  pass

class DamageSimulator():
  def __init__(self, stats, dmg_instances, num_samples, verbose=False, save_damage_matrix=False):
    self.__dmg_instances = copy.deepcopy(dmg_instances)
    # defensively sort
    self.__dmg_instances.sort(key=lambda x: x[0])
    self.__stats = stats
    self.__damage_tracker = DamageTracker()
    start_time = time.time()
    self.__damage_matrix = None

    self.__compile_damage(num_samples, save_damage_matrix)
    end_time = time.time()
    if(verbose):
      print('Simulation time took: ' + str(end_time-start_time))

  # dmg_instances is a list in format: # (current_time, skill, (buffs, debuffs), event_id)
  def __compile_damage(self, num_samples, save_damage_matrix= False):
    for (t, skill, skill_modifier, status_effects, event_id) in self.__dmg_instances:
      base_damage = ComputeDamageUtils.get_base_damage(skill, skill_modifier, self.__stats, status_effects)
      assert base_damage is not None, "base_damage should not be None."

      (dh_rate, crit_rate, crit_bonus) = ComputeDamageUtils.compute_crit_rates_and_bonuses(self.__stats, skill, skill_modifier, status_effects)
      damage_mult = ComputeDamageUtils.compute_damage_mult(status_effects)

      damage_spec = skill.get_damage_spec(skill_modifier)
      trait_damage_mult = self.__stats.processed_stats.trait_damage_mult if damage_spec.trait_damage_mult_override is None else damage_spec.trait_damage_mult_override

      self.__damage_tracker.add_damage(base_damage, crit_rate, crit_bonus, dh_rate, trait_damage_mult, damage_mult, t, damage_spec.potency, skill_modifier, (status_effects[0], status_effects[1]))
    self.__damage_tracker.finalize()
    damage_matrix = self.__damage_tracker.compute_damage(num_samples)

    if len(self.__dmg_instances) == 0:
      fight_time = 0
    else:
      fight_time = (self.__dmg_instances[-1][0] - self.__dmg_instances[0][0])/1000 #convert to s
    self.__damage = np.sum(damage_matrix, axis=0)
    self.__dps = self.__damage/fight_time if fight_time > 0 else np.full(self.__damage.shape, math.inf)
    self.__per_skill_damage_mean = np.mean(damage_matrix, axis=1)
    self.__per_skill_damage_std = np.std(damage_matrix, axis=1)
    self.__event_ids = tuple(x[4] for x in self.__dmg_instances)

    if save_damage_matrix:
      self.__damage_matrix = damage_matrix

  @staticmethod
  def __add_damage_snapshots(per_skill_damage, rb):
    rot = rb.get_skill_timing().get_q()
    event_id_to_snapshot_time = {}
    for x in rot:
      event_id, snapshot_time, skill_name = x.event_id, x.event_times.primary, x.skill.name
      event_id_to_snapshot_time[event_id] = (snapshot_time, skill_name)

    for i in range(0,len(per_skill_damage)):
      event_id = per_skill_damage[i].event_id
      skill_name = per_skill_damage[i].skill_name
      assert event_id in event_id_to_snapshot_time.keys(), "Unknown event_id found: {}".format(event_id)
      assert skill_name == event_id_to_snapshot_time[event_id][1], "Skill names did not match on event id: {}. rotation name: {}, per_skill_damage name: {}".format(event_id, event_id_to_snapshot_time[event_id][1], skill_name)
      per_skill_damage[i] = per_skill_damage[i]._replace(snapshot_time= event_id_to_snapshot_time[event_id][0])
    return per_skill_damage

  def get_event_ids(self):
    return self.__event_ids

  def get_crit_and_dh_rates(self):
    return self.__damage_tracker.get_crit_and_dh_rates()

  def get_trait_damage_mult(self):
    return self.__damage_tracker.get_trait_damage_mult()

  def get_raw_damage(self):
    return self.__damage

  def get_dps(self):
    return (self.__dps)

  def get_damage_time(self):
    t = self.__damage_tracker.time
    return t

  def get_damage_matrix(self):
    return self.__damage_matrix

  def get_damage_ranges(self):
    skill_names = [x[1].name for x in self.__dmg_instances]
    damage_ranges = self.__damage_tracker.get_damage_ranges_and_probabilities()
    res = [(skill_names[i],
           damage_ranges[i][0],
           damage_ranges[i][1],
           damage_ranges[i][2],
           damage_ranges[i][3]) for i in range(0, len(skill_names))]
    return res

  def get_per_skill_damage(self, rb = None):
    t = self.__damage_tracker.time
    potencies = self.__damage_tracker.potency
    status_effects = self.__damage_tracker.status_effects
    skill_modifier_condition = self.__damage_tracker.skill_modifier_condition
    skill_names = [x[1].name for x in self.__dmg_instances]
    res = [PerInstanceDamage(t[i],
                             None, #Snapshot time- not known yet. Sus implementation.
                             skill_names[i],
                             potencies[i],
                             skill_modifier_condition[i],
                             status_effects[i],
                             self.__per_skill_damage_mean[i],
                             self.__per_skill_damage_std[i],
                             self.__event_ids[i]) for i in range(0, len(t))]
    if rb is not None:
      res = self.__add_damage_snapshots(res, rb)
    return res
