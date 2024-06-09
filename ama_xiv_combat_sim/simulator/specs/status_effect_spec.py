import math

from dataclasses import dataclass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH

@dataclass(frozen=True)
class StatusEffectSpec:
  duration: int = 0
  max_duration: int = None
  num_uses: int = math.inf
  max_num_uses: int = None
  crit_rate_add: float= 0
  dh_rate_add: float= 0
  damage_mult: float= 1
  main_stat_add: float= 0
  #auto-attack time is ~= weapon_delay*(1-auto_attack_delay_reduction)
  auto_attack_delay_reduction: float = 0
  #this applies to cast/gcd timer (but NOT necessarily recast time).
  # cast/gcd time is ~= cast_time*(1-haste_time_reduction)
  haste_time_reduction: float = 0
  flat_cast_time_reduction: float = 0
  # If this buff is re-applied, indicates whether the duration should be extended
  extends_existing_duration: bool = True
  #A tuple of status effects (strings) that this skill will cause to expire on use.
  expires_status_effects: tuple = ()
  # Which skills this status effect can apply to. Can be used in combination with status_effect_denylist.
  skill_allowlist: tuple = None
  guaranteed_crit: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
  guaranteed_dh: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
  add_to_skill_modifier_condition: bool = False
  extend_only: bool = False #only refresh the given named buff if it is already being applied
  is_party_effect:bool = False

  def __post_init__(self):
    if self.max_duration is None:
      object.__setattr__(self, 'max_duration', self.duration)
    if self.max_num_uses is None:
      object.__setattr__(self, 'max_num_uses', self.num_uses)
    assert isinstance(self.duration, int) or self.duration == math.inf, "duration should be an int in ms. Did you put it in seconds?"
    assert isinstance(self.max_duration, int) or self.max_duration == math.inf, "max_duration should be an int in ms. Did you put it in seconds?"
    assert isinstance(self.flat_cast_time_reduction, int) or self.flat_cast_time_reduction==math.inf, "flat_cast_time_reduction should be an int in ms. Did you put it in seconds?"
    assert isinstance(self.expires_status_effects, tuple), "expires_status_effects should be a tuple. Did you accidentally make it a string?"
    assert isinstance(self.skill_allowlist, tuple) or self.skill_allowlist == None, "skill_allowlist should be a tuple. Did you accidentally make it a string? {}".format(self.skill_allowlist)

  def  __str__(self):
    res = '   duration:{}\n'.format(self.duration)
    res += '   max_duration: {}\n'.format(self.max_duration)
    res += '   crit_rate_add: {}\n'.format(self.crit_rate_add)
    res += '   dh_rate_add: {}\n'.format(self.dh_rate_add)
    res += '   damage_mult: {}\n'.format(self.damage_mult)
    res += '   main_stat_add: {}'.format(self.main_stat_add)
    res += '   auto_attack_delay_reduction: {}'.format(self.auto_attack_delay_reduction)
    res += '   haste_time_reduction: {}'.format(self.haste_time_reduction)
    res += '   flat_cast_time_reduction: {}'.format(self.flat_cast_time_reduction)
    return res
