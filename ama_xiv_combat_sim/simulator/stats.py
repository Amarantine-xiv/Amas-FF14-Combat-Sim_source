from dataclasses import dataclass
from typing import Any
from .processed_stats import ProcessedStats
from .game_data.job_class_fns import JobClassFns

@dataclass(frozen=True)
class Stats():
  wd: float
  weapon_delay: float
  main_stat: float
  det_stat: float
  dh_stat: float
  crit_stat: float
  speed_stat: float
  job_class: str
  tenacity: float = None
  num_roles_in_party: float = 5
  healer_or_caster_strength: float= None
  level: int = 90
  job_class_fns: Any = JobClassFns

  def __post_init__(self):
    object.__setattr__(self, "processed_stats", ProcessedStats(self))