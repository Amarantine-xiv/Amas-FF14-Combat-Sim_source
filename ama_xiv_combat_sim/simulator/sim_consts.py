from dataclasses import dataclass


@dataclass(frozen=True)
class SimConsts:
    DEFAULT_CONDITION = ""
    COMBO_SUCCESS = ""
    COMBO_FAIL = "No Combo"
    DEFAULT_TARGET = "Default Target"
    LB_MEAN_DAMAGE = "Mean Damage"
    LB_EXACT_DAMAGE = "Exact Damage"
    WAIT_PREFIX= "Wait"
  