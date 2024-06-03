from dataclasses import dataclass

from simulator.calcs.forced_crit_or_dh import ForcedCritOrDH

@dataclass(frozen=True)
class StatusEffects():
  crit_rate_add: float= 0
  dh_rate_add: float= 0
  damage_mult: float= 1
  main_stat_add: float= 0
  auto_attack_delay_mult: float= 1
  haste_time_mult: float= 1
  flat_cast_time_reduction: float = 0
  guaranteed_crit: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
  guaranteed_dh: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
  status_effects: tuple = tuple()

  def __eq__(self, other):
    # All but the status_effects tuple. That does not have a functional impact.
    return self.crit_rate_add == other.crit_rate_add and \
          self.dh_rate_add == other.dh_rate_add and \
          self.damage_mult == other.damage_mult and \
          self.main_stat_add == other.main_stat_add and \
          self.auto_attack_delay_mult == other.auto_attack_delay_mult and \
          self.haste_time_mult == other.haste_time_mult and \
          self.flat_cast_time_reduction == other.flat_cast_time_reduction and \
          self.guaranteed_crit == other.guaranteed_crit and \
          self.guaranteed_dh == other.guaranteed_dh