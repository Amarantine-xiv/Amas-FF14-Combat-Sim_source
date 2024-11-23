from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
    get_shot_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings


class GenericJobClass:
    auto_timing_spec = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()
    shot_timing_spec = get_shot_timing()

    def __init__(self, version, level, skill_data):
        self._job_class = ""
        self._version = version
        self._level = level

        self._skill_data = skill_data
        self._skill_data.set_version(version)
        self._skill_data.set_level(level)

    @staticmethod
    def is_a_skill(f):
        f.__is_a_skill__ = True
        return f

    def __get_all_skills_methods(self):
        methods = []
        for fn_name in dir(self):
            fn = getattr(self, fn_name)
            if getattr(fn, "__is_a_skill__", False):
                methods.append(fn)
        return methods

    def get_skills(self):
        res = []
        for skill_method in self.__get_all_skills_methods():
            sk = skill_method()
            if sk is None:
                continue

            if isinstance(sk, list) or isinstance(sk, tuple):
                for _sk in sk:
                    res.append(_sk)
            elif isinstance(sk, Skill):
                res.append(sk)
            else:
                raise TypeError(f"get_skills() get an unsupported type of : {type(sk)}")
        return res

    @staticmethod
    def is_a_resource(f):
        f.__is_a_resource__ = True
        return f

    def __get_all_resource_methods(self):
        methods = []
        for fn_name in dir(self):
            fn = getattr(self, fn_name)
            if getattr(fn, "__is_a_resource__", False):
                methods.append(fn)
        return methods

    def get_resources(self):
        res = []
        for resource_method in self.__get_all_resource_methods():
            sk = resource_method()
            if sk is not None:
                assert (
                    len(sk) == 2
                ), f"Resource method does not return 2 elements: {resource_method}"
                assert isinstance(
                    sk[0], str
                ), f"Resource method return 1 must be string: {resource_method}"
                assert isinstance(
                    sk[1], JobResourceSettings
                ), f"Resource method return 1 must be JobResourceSettings: {resource_method}"
                res.append(sk)
        return res

    def get_status_effect_priority(self):
        return None

    # tuple of tuples of (combo_group, combo_breaker)
    # combo_group is the group to be broken
    # combo_breaker is a list of what breaks that group
    def get_combo_breakers(self):
        return None

    def get_job_class(self):
        return self._job_class
