from dataclasses import dataclass

from simulator.calcs.damage_class import DamageClass
from simulator.calcs.forced_crit_or_dh import ForcedCritOrDH

@dataclass(frozen=True)
class DamageSpec:
  potency: float = None
  damage_class: DamageClass = DamageClass.DIRECT
  guaranteed_crit: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
  guaranteed_dh: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
  # Used for overriding class trait damage multipliers where necessary. Set to
  # 1 if this damage instance should not use class traits for computing damage.
  trait_damage_mult_override: float = None
  pet_job_mod_override: float = None #only used if the damage_class is DamageClass.PET
  pet_scalar: float = 1.0 #only used if the damage_class is DamageClass.PET

  def  __str__(self):
    res = '   potency:{}\n'.format(self.potency)
    res += '   damage_class: {}\n'.format(self.damage_class)
    res += '   guaranteed_crit:{}\n'.format(self.guaranteed_crit)
    res += '   guaranteed_dh:{}'.format(self.guaranteed_dh)
    res += '   trait_damage_mult_override:{}\n'.format(self.trait_damage_mult_override)
    res += '   pet_job_mod_override:{}'.format(self.pet_job_mod_override)
    return res