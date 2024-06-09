import numpy as np

from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts

class DamageTracker():
  def __init__(self):
    self.base_damage=np.zeros((5000,1))
    self.crit_rate=np.zeros((5000,1))
    self.crit_bonus=np.zeros((5000,1))
    self.dh_rate = np.zeros((5000,1))
    self.trait_damage_mult = np.zeros((5000,1))
    self.damage_mult = np.ones((5000,1))
    self.time = np.zeros(5000)
    self.potency = np.zeros(5000)
    self.skill_modifier_condition = [""]*5000
    self.status_effects = [""]*5000
    self.it = 0
    self.isFinalized = False

    #for debugging
    self.base_damage=np.zeros((5000,1))

  def add_damage(self, base_damage, crit_rate, crit_bonus, dh_rate, trait_damage_mult, damage_mult, time, potency, skill_modifier, status_effects):
    if self.isFinalized:
      raise RuntimeError('DamageTracker is finalized. Cannot add damage instances.')
    self.base_damage[self.it] = base_damage
    self.crit_rate[self.it] = crit_rate
    self.crit_bonus[self.it] = crit_bonus
    self.dh_rate[self.it] = dh_rate
    self.trait_damage_mult[self.it] = trait_damage_mult
    self.damage_mult[self.it] = damage_mult
    self.time[self.it] = time
    self.potency[self.it] = potency
    self.skill_modifier_condition[self.it] = skill_modifier.with_condition
    self.status_effects[self.it] = status_effects
    self.it +=1

  def finalize(self):
    self.base_damage = self.base_damage[0:self.it]
    self.crit_rate = self.crit_rate[0:self.it]
    self.crit_bonus = self.crit_bonus[0:self.it]
    self.dh_rate = self.dh_rate[0:self.it]
    self.trait_damage_mult = self.trait_damage_mult[0:self.it]
    self.damage_mult = self.damage_mult[0:self.it]
    self.time = self.time[0:self.it]
    self.potency = self.potency[0:self.it]
    self.skill_modifier_condition = self.skill_modifier_condition[0:self.it]
    self.status_effects = self.status_effects[0:self.it]
    self.isFinalized = True

  # For each damage instance, returns the damage distrubtion of that instance

  def __get_damage(self, base_damage, crit_bonus, crit_rate, dh_rate, damage_mult, num_samples, base_damage_range=0.1):
    low_damage = 1-base_damage_range/2

    num_damage_instances = base_damage.shape[0]
    total_damage = np.floor(base_damage*(low_damage+base_damage_range*np.random.rand(num_damage_instances,num_samples)))
    total_damage += np.floor(np.multiply(total_damage, np.multiply(crit_bonus, crit_rate >= np.random.rand(num_damage_instances,num_samples))))
    total_damage += np.floor(np.multiply(total_damage, GameConsts.DH_DAMAGE_MULT_BONUS*(dh_rate >= np.random.rand(num_damage_instances,num_samples))))
    total_damage = np.floor(np.multiply(total_damage, self.trait_damage_mult))
    total_damage = np.floor(np.multiply(total_damage, damage_mult))
    return total_damage

  def get_damage_ranges_and_probabilities(self):
    if not self.isFinalized:
      raise RuntimeError('DamageTracker must be finalized before computing damage ranges')

    low_init_base_damage = np.floor(0.95*self.base_damage)
    high_init_base_damage = np.floor(1.05*self.base_damage)

    low_base_damage = self.__get_damage(low_init_base_damage, self.crit_bonus, 0, 0, self.damage_mult, 1, base_damage_range=0)
    high_base_damage = self.__get_damage(high_init_base_damage, self.crit_bonus, 0, 0, self.damage_mult, 1, base_damage_range=0)

    low_crit = self.__get_damage(low_init_base_damage, self.crit_bonus, 1, 0, self.damage_mult, 1, base_damage_range=0)
    high_crit = self.__get_damage(high_init_base_damage, self.crit_bonus, 1, 0, self.damage_mult, 1, base_damage_range=0)

    low_dh = self.__get_damage(low_init_base_damage, self.crit_bonus, 0, 1, self.damage_mult, 1, base_damage_range=0)
    high_dh = self.__get_damage(high_init_base_damage, self.crit_bonus, 0, 1, self.damage_mult, 1, base_damage_range=0)

    low_crit_dh = self.__get_damage(low_init_base_damage, self.crit_bonus, 1, 1, self.damage_mult, 1, base_damage_range=0)
    high_crit_dh = self.__get_damage(high_init_base_damage, self.crit_bonus, 1, 1, self.damage_mult, 1, base_damage_range=0)

    base_probability = np.multiply(1-self.crit_rate, 1-self.dh_rate)
    crit_probability = np.multiply(self.crit_rate, 1-self.dh_rate)
    dh_probability = np.multiply(1-self.crit_rate, self.dh_rate)
    crit_dh_probability = np.multiply(self.crit_rate, self.dh_rate)

    num_damage_instances = self.base_damage.shape[0]
    res = [tuple()]*num_damage_instances
    for i in range(0, num_damage_instances):
      res[i] = ( ['No crit, no DH', float(low_base_damage[i][0]), float(high_base_damage[i][0]), base_probability[i][0]],
                 ['Crit, no DH', float(low_crit[i][0]), float(high_crit[i][0]), crit_probability[i][0]],
                 ['No crit, DH', float(low_dh[i][0]), float(high_dh[i][0]), dh_probability[i][0]],
                 ['Crit, DH', float(low_crit_dh[i][0]), float(high_crit_dh[i][0]), crit_dh_probability[i][0]])
    return res

  def __sample_damage_instances(self, num_samples):
    if not self.isFinalized:
      raise RuntimeError('DamageTracker must be finalized before sampling damage')
    return self.__get_damage(self.base_damage, self.crit_bonus, self.crit_rate, self.dh_rate, self.damage_mult, num_samples)

  #Return matrix of [#of damages instances x # of samples]
  def compute_damage(self, num_samples):
    return self.__sample_damage_instances(num_samples)

  def get_crit_and_dh_rates(self):
    if not self.isFinalized:
      raise RuntimeError('DamageTracker must be finalized before calling get_crit_and_dh_rates')
    return (np.squeeze(self.crit_rate), np.squeeze(self.dh_rate))

  def get_trait_damage_mult(self):
    if not self.isFinalized:
      raise RuntimeError('DamageTracker must be finalized before calling get_trait_damage_mult')
    return np.squeeze(self.trait_damage_mult)

