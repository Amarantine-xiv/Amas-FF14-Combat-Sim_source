import math

from ama_xiv_combat_sim.simulator.sim_consts import SimConsts

class ChannelingTracker:
    def __init__(self):
        self.__channeling_windows = []
        self.__start_channeling_time = (
            None  # initialize so code checker stops complaining
        )
        self.__curr_channeling_spec = None
        self.__curr_num_uses = math.inf
        self.__reset_channeling()  # initialize so code checker stops complaining
        self.is_finalized = False

    def __is_channeling(self):
        return self.__start_channeling_time is not None

    def __reset_channeling(self):
        self.__start_channeling_time = None
        self.__curr_channeling_spec = None
        self.__curr_num_uses = math.inf

    def __start_channeling(self, t, channeling_spec):
        assert (
            self.__start_channeling_time is None
        ), "Internal error: we are already channeling. Please contact a dev."
        self.__start_channeling_time = t
        self.__curr_channeling_spec = channeling_spec
        self.__curr_num_uses = channeling_spec.num_uses

    def __end_channeling(self, t):
        self.__channeling_windows.append((self.__start_channeling_time, t))
        self.__reset_channeling()

    def process_channeling(self, t, skill, skill_modifier):
        assert (
            not self.is_finalized
        ), "Internal error: ChannelingTracker is already finalized. Please contact a dev."

        # special code for wait skills. Don't do anythinf if the user is just waiting.
        if SimConsts.WAIT_PREFIX in skill.name:
            return

        channeling_spec = skill.get_channeling_spec(skill_modifier)
        if channeling_spec:
            if self.__is_channeling():
                channel_end_time = min(
                    self.__start_channeling_time + self.__curr_channeling_spec.duration,
                    t,
                )
                self.__end_channeling(channel_end_time)
            self.__start_channeling(t, channeling_spec)
        else:
            if self.__is_channeling():
                if skill.name in self.__curr_channeling_spec.skill_allowlist:
                    self.__curr_num_uses -= 1
                    if self.__curr_num_uses > 0:
                        # if you're channeling, the only way to get here  is to be in the skill_allowlist AND not exhaust all counts
                        return

                channel_end_time = min(
                    self.__start_channeling_time + self.__curr_channeling_spec.duration,
                    t,
                )
                self.__end_channeling(channel_end_time)

    def finalize(self):
        assert (
            not self.is_finalized
        ), "Internal error: ChannelingTracker is already finalized. Please contact a dev."
        if self.__is_channeling():
            channel_end_time = (
                self.__start_channeling_time + self.__curr_channeling_spec.duration
            )
            self.__end_channeling(channel_end_time)
        self.__channeling_windows.sort()
        self.is_finalized = True

    def get_channeling_windows(self):
        assert (
            self.is_finalized
        ), "Internal error: ChannelingTracker is not yet finalized. Please contact a dev."
        return tuple(self.__channeling_windows)
