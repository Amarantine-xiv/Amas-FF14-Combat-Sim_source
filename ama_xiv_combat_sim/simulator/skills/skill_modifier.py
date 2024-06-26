import copy
from dataclasses import dataclass

from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.utils import Utils


@dataclass(frozen=False, order=True)
class SkillModifier:
    def __init__(
        self,
        with_condition=SimConsts.DEFAULT_CONDITION,
        guaranteed_crit=ForcedCritOrDH.DEFAULT,
        guaranteed_dh=ForcedCritOrDH.DEFAULT,
        force_combo=False,
        ignore_cast_times=False,
        ignore_application_delay=False,
        bonus_percent=None,
    ):
        self.guaranteed_crit = guaranteed_crit
        self.guaranteed_dh = guaranteed_dh
        self.with_condition = Utils.canonicalize_condition(with_condition)
        self.original_with_condition = copy.deepcopy(self.with_condition)
        self.force_combo = force_combo
        self.ignore_application_delay = ignore_application_delay
        self.ignore_cast_times = ignore_cast_times
        self.bonus_percent = bonus_percent



    def remove_from_condition(self, condition_to_remove):
        self.with_condition.discard(condition_to_remove)
        return self

    def add_to_condition(self, condition_to_add):
        if len(condition_to_add) == 0:
            return self

        if len(self.with_condition) == 0:
            self.with_condition = set()
        self.with_condition.update(Utils.canonicalize_condition(condition_to_add))
        return self

    def __eq__(self, other):
        return (
            (self.guaranteed_crit == other.guaranteed_crit)
            and (self.guaranteed_dh == other.guaranteed_dh)
            and (self.with_condition == other.with_condition)
        )
        
    def __str__(self):
        res = "Guaranteed crit: {}\n".format(self.guaranteed_crit)
        res += "Guaranteed dh: {}\n".format(self.guaranteed_dh)
        res += "with_condition {}\n".format(",".join(self.with_condition))
        return res
