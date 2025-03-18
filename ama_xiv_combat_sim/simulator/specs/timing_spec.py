from dataclasses import dataclass
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts


@dataclass(frozen=True)
class TimingSpec:
    base_cast_time: int
    gcd_base_recast_time: int = (
        None  # after you use this skill, how long until you can use a gcd?
    )
    animation_lock: int = 650  # does not take into account ping
    application_delay: int = (
        0  # how long after the cast finishes does the skill get applied
    )
    affected_by_speed_stat: bool = True
    affected_by_haste_buffs: bool = True

    def __error_check(self):
        # This is such a common error, that we need to defend against it.
        assert isinstance(
            self.base_cast_time, int
        ), "base_cast_time should be an int in ms. Did you put it in seconds?"
        assert isinstance(
            self.gcd_base_recast_time, int
        ), "gcd_base_recast_time should be an int in ms. Did you put it in seconds?"
        assert isinstance(
            self.application_delay, int
        ), "application_delay should be an int in ms. Did you put it in seconds?"
        assert isinstance(
            self.animation_lock, int
        ), "animation_lock should be an int in ms. Did you put it in seconds?"

    def __post_init__(self):
        if self.gcd_base_recast_time is None:
            # assume a default of 2500ms recast time for all gcds, unless otherwise stated
            object.__setattr__(self, "gcd_base_recast_time", GameConsts.GCD_RECAST_TIME)
        self.__error_check()

    def __str__(self):
        res = "  Base cast time: {}\n".format(self.base_cast_time)
        res += "  gcd_base_recast_time: {}\n".format(self.gcd_base_recast_time)
        res += "  animation_lock: {}\n".format(self.animation_lock)
        res += "  application_delay: {}\n".format(self.application_delay)
        res += "  affected_by_speed_stat: {}\n".format(self.affected_by_speed_stat)
        res += "  affected_by_haste_buffs: {}\n".format(self.affected_by_haste_buffs)
        return res
