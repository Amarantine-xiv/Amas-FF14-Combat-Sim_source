from dataclasses import dataclass
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts
from ama_xiv_combat_sim.simulator.game_data.get_job_class_fns import get_job_class_fns
from ama_xiv_combat_sim.simulator.processed_stats import ProcessedStats


@dataclass(frozen=True)
class Stats:
    wd: float = None
    weapon_delay: float = None
    main_stat: float = None
    det_stat: float = None
    dh_stat: float = None
    crit_stat: float = None
    speed_stat: float = None
    job_class: str = ""
    version: str = ""
    tenacity: float = None
    num_roles_in_party: float = 5
    healer_or_caster_strength: float = None    
    level: int = 90
    processed_stats = None
    job_class_fns = None

    def __post_init__(self):
        object.__setattr__(self, "job_class_fns", get_job_class_fns(self.version))
        object.__setattr__(self, "processed_stats", ProcessedStats(self, self.version, self.level))
        if self.weapon_delay is None:
            object.__setattr__(self, "weapon_delay", GameConsts.WEAPON_DELAYS[self.job_class])
        