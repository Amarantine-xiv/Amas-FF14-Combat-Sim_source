from dataclasses import dataclass

from ama_xiv_combat_sim.simulator.calcs.stat_fns import StatFns


@dataclass(frozen=True)
class ProcessedStats:
    def __init__(self, stats):
        crit_rate, crit_bonus = StatFns.get_crit_stats(stats.crit_stat)
        object.__setattr__(self, "crit_rate", crit_rate)
        object.__setattr__(self, "crit_bonus", crit_bonus)
        object.__setattr__(self, "det_bonus", StatFns.fDet(stats.det_stat))
        object.__setattr__(self, "dh_rate", StatFns.get_dh_rate(stats.dh_stat))
        object.__setattr__(
            self, "job_mod", stats.job_class_fns.JOB_MODS[stats.job_class]
        )
        object.__setattr__(
            self,
            "trait_damage_mult",
            stats.job_class_fns.compute_trait_damage_mult(stats.job_class),
        )
        object.__setattr__(
            self,
            "trait_haste_time_reduction",
            stats.job_class_fns.compute_trait_haste_time_reduction(stats.job_class),
        )
        object.__setattr__(
            self,
            "trait_auto_attack_delay_reduction",
            stats.job_class_fns.compute_trait_auto_attack_delay_reduction(
                stats.job_class
            ),
        )

    def __str__(self):
        res = "Crit rate: {}\n".format(self.crit_rate)
        res += "Crit bonus: {}\n".format(self.crit_bonus)
        res += "Det bonus: {}\n".format(self.det_bonus)
        res += "DH Rate: {}\n".format(self.dh_rate)
        res += "Job mod: {}\n".format(self.job_mod)
        res += "Trait damage mult: {}\n".format(self.trait_damage_mult)
        res += "Trait haste time reduction: {}\n".format(
            self.trait_haste_time_reduction
        )
        res += "Trait auto attack delay reduction: {}\n".format(
            self.trait_auto_attack_delay_reduction
        )
        return res
