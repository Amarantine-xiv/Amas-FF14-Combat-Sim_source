from dataclasses import dataclass

@dataclass(frozen=True)
class SimConsts:
  DEFAULT_CONDITION= ''
  COMBO_SUCCESS = ''
  COMBO_FAIL = 'No Combo'
  LB_MEAN_DAMAGE = "Mean Damage:"
  LB_EXACT_DAMAGE = "Exact Damage:"