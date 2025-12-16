from dataclasses import dataclass, field

from ama_xiv_combat_sim.simulator.calcs.damage_instance_class import DamageInstanceClass
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec


@dataclass(frozen=True)
class DefensiveStatusEffectSpec(StatusEffectSpec):
    # value is the amount of reduction for that damage class
    damage_reductions: dict[DamageInstanceClass, float] = field(default_factory=dict)
    is_invuln: bool = False
    max_hp_mult: float = 1
    hp_recovery_up_via_healing_actions: float = 0
    healing_magic_potency_mult: float = 1
    compiles_damage_taken: bool = False
    increase_parry_rate: float = 0
    increase_block_chance: float = 0

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.damage_reductions, dict):
            assert isinstance(self.damage_reductions, float) or isinstance(
                self.damage_reductions, int
            ), "damage_reductions should be an int or float if it's not a dict"

            damage_reductions = {}
            # be specific in what we will by default cover
            for k in [
                DamageInstanceClass.UNKNOWN,
                DamageInstanceClass.PHYSICAL,
                DamageInstanceClass.MAGICAL,
            ]:
                damage_reductions[k] = self.damage_reductions
            object.__setattr__(self, "damage_reductions", damage_reductions)

    def __repr__(self):
        return f"{super().__repr__()}_{type(self).__name__}: ({', '.join('%s=%s' % item for item in vars(self).items())})"
