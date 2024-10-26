from dataclasses import dataclass
from ama_xiv_combat_sim.simulator.game_data.get_job_class_fns import get_job_class_fns
from ama_xiv_combat_sim.simulator.processed_stats import ProcessedStats


@dataclass(frozen=True)
class Stats:
    wd: float
    weapon_delay: float
    main_stat: float
    det_stat: float
    dh_stat: float
    crit_stat: float
    speed_stat: float
    job_class: str
    version: str
    tenacity: float = None
    num_roles_in_party: float = 5
    healer_or_caster_strength: float = None    
    level: int = 90
    processed_stats = None
    job_class_fns = None

    def __post_init__(self):
        object.__setattr__(self, "job_class_fns", get_job_class_fns(self.version))
        object.__setattr__(self, "processed_stats", ProcessedStats(self, self.version, self.level))