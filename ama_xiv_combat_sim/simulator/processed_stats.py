from dataclasses import dataclass

from ama_xiv_combat_sim.simulator.calcs.stat_fns import StatFns


@dataclass(frozen=True)
class ProcessedStats:
    def __init__(self, stats, version, level):
        crit_rate, crit_bonus = StatFns.get_crit_stats(stats.crit_stat, version, level)
        object.__setattr__(self, "crit_rate", crit_rate)
        object.__setattr__(self, "crit_bonus", crit_bonus)
        object.__setattr__(
            self, "det_bonus", StatFns.fDet(stats.det_stat, version, level)
        )
        object.__setattr__(
            self, "dh_rate", StatFns.get_dh_rate(stats.dh_stat, version, level)
        )
        object.__setattr__(
            self, "job_mod", stats.job_class_fns.JOB_MODS[stats.job_class]
        )
        object.__setattr__(
            self,
            "trait_damage_mult",
            stats.job_class_fns.compute_trait_damage_mult(
                stats.job_class, version, level
            ),
        )
        object.__setattr__(
            self,
            "trait_haste_time_reduction",
            stats.job_class_fns.compute_trait_haste_time_reduction(
                stats.job_class, version, level
            ),
        )
        object.__setattr__(
            self,
            "trait_auto_attack_delay_reduction",
            stats.job_class_fns.compute_trait_auto_attack_delay_reduction(
                stats.job_class, version, level
            ),
        )

    def __str__(self):
        res = f"Crit rate: {self.crit_rate}\n"
        res += f"Crit bonus: {self.crit_bonus}\n"
        res += f"Det bonus: {self.det_bonus}\n"
        res += f"DH Rate: {self.dh_rate}\n"
        res += f"Job mod: {self.job_mod}\n"
        res += f"Trait damage mult: {self.trait_damage_mult}\n"
        res += f"Trait haste time reduction: {self.trait_haste_time_reduction}\n"
        res += f"Trait auto attack delay reduction: {self.trait_auto_attack_delay_reduction}\n"
        return res
