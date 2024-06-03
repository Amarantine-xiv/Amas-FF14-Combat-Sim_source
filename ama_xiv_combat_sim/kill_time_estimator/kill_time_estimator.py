import numpy as np
import re
from simulator.damage_simulator import DamageSimulator
from simulator.sim_consts import SimConsts
from simulator.timeline_builders.damage_builder import DamageBuilder

class KillTimeEstimator():
  def __init__(self, boss_hp):
    self.__all_rotations = []
    self.__boss_hp = boss_hp

  def add_rotation(self, rotation):
    self.__all_rotations.append(rotation)

  @staticmethod
  def get_lb_damage(condition, num_samples):
    res_mean = re.search(r"^{} (\d+)".format(SimConsts.LB_MEAN_DAMAGE), condition)
    res_exact = re.search(r"^{} (\d+)".format(SimConsts.LB_EXACT_DAMAGE), condition)

    if res_mean is None and res_exact is None:
      raise RuntimeError('LB conditional must be "Mean Damage: number", or "Exact Damage: number". Instead, got: {}'.format(condition))

    if res_mean is not None:
      damage = float(res_mean.groups()[0])
      return np.asarray(np.floor(damage*(0.95+0.1*np.random.rand(1,num_samples))))

    if res_exact is not None:
      damage = float(res_exact.groups()[0])
      return np.full((1, num_samples), damage)

  @staticmethod
  def process_damage_for_lb_usage(damage_matrix, per_skill_damage):
    for i in range(0, len(per_skill_damage)):
      if 'LB' in per_skill_damage[i].skill_name:
        condition = ",".join(per_skill_damage[i].skill_modifier_condition)
        damage_matrix[i,:] = KillTimeEstimator.get_lb_damage(condition, damage_matrix.shape[1])
    return damage_matrix

  def estimate_kill_time(self, num_samples=100000, verbose=True):
    all_damage = None
    all_t = []
    for i in range(0, len(self.__all_rotations)):
      rb = self.__all_rotations[i]
      if verbose:
        print('Processing rotation {}/{}'.format(i+1, len(self.__all_rotations)))
      stats = rb.get_stats()
      db = DamageBuilder(stats, rb._skill_library)
      sim = DamageSimulator(stats, db.get_damage_instances(rb.get_skill_timing()), num_samples, save_damage_matrix=True)
      damage_matrix = sim.get_damage_matrix()
      t = sim.get_damage_time()

      per_skill_damage = sim.get_per_skill_damage()
      damage_matrix = self.process_damage_for_lb_usage(damage_matrix, per_skill_damage)

      if all_damage is None:
        all_damage = damage_matrix
      else:
        all_damage = np.concatenate((all_damage, damage_matrix), axis=0)
      all_t.extend(t)

    idx_sort = np.argsort(all_t)
    all_t = np.asarray([all_t[idx_sort[i]] for i in range(0, len(idx_sort))])

    all_damage = all_damage[idx_sort,:]
    cumsum_damage = np.cumsum(all_damage,axis=0)

    kt_indexes_with_none = [ np.nonzero(cumsum_damage[:,i]>=self.__boss_hp)[0][0] if len(np.nonzero(cumsum_damage[:,i]>=self.__boss_hp)[0] > 0) else None for i in range(0, cumsum_damage.shape[1])]
    kt_indexes = list(filter(lambda x: x is not None, kt_indexes_with_none))

    num_failures = num_samples - len(kt_indexes)

    kill_times = all_t[kt_indexes]/1000.0
    # We add Nones on at the end so we don't need to keep track of how many failures we have separately.
    kill_times = np.concatenate((kill_times, [None]*num_failures))

    return kill_times, cumsum_damage, all_t