import math

from dataclasses import dataclass

from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec


@dataclass(frozen=True)
class OffensiveStatusEffectSpec(StatusEffectSpec):
    crit_rate_add: float = 0
    dh_rate_add: float = 0
    damage_mult: float = 1
    main_stat_add: float = 0
    main_stat_mult: float = 1
    # auto-attack time is ~= weapon_delay*(1-auto_attack_delay_reduction)
    auto_attack_delay_reduction: float = 0
    # this applies to cast/gcd timer (but NOT necessarily recast time).
    # cast/gcd time is ~= cast_time*(1-haste_time_reduction)
    haste_time_reduction: float = 0
    flat_cast_time_reduction: float = 0
    flat_gcd_recast_time_reduction: float = 0    

    def __post_init__(self):
        super().__post_init__()
        assert (
            isinstance(self.flat_cast_time_reduction, int)
            or self.flat_cast_time_reduction == math.inf
        ), "flat_cast_time_reduction should be an int in ms. Did you put it in seconds?"

    def __repr__(self):
        return f"{super().__repr__()}_{type(self).__name__}: ({', '.join('%s=%s' % item for item in vars(self).items())})"
