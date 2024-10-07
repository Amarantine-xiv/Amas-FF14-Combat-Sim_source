import copy
from dataclasses import dataclass


class SkillLibrary:
    def __init__(self, version, level=100):
        self.__skills = {}
        self.__status_effect_priority = {}
        self.__job_resources = (
            {}
        )  # dict of dict. keys are jobs, vals are dicts of {name} to JobResourceSettings.
        self.__current_job_class = None
        self.__combo_breakers = (
            {}
        )  # dict of dict. keys are jobs, vals are dicts of {name} to ComboBreakers.
        self.__version = version
        self.__level = level

    def get_version(self):
        return self.__version

    def get_level(self):
        return self.__level

    def add_combo_breaker(self, combo_group, combo_breaker):
      #combo_group is the group to be broken
      #combo_breaker is what breaks that group
        assert isinstance(
            combo_breaker, tuple
        ), "combo_breaker group should be a tuple of ints"
        self.__combo_breakers[self.__current_job_class][combo_group] = combo_breaker

    def add_resource(self, name, job_resource_settings):
        self.__job_resources[self.__current_job_class][name] = job_resource_settings

    def get_all_combo_breakers(self, job_class):
        return copy.deepcopy(self.__combo_breakers[job_class])

    # Returns dict[resource_name]-->JobResourceSettings
    def get_all_resource_settings(self, job_class):
        return copy.deepcopy(self.__job_resources[job_class])

    def has_skill(self, skill_name, job_class):
        return skill_name in self.__skills[job_class]

    def print_skill_names(self, job_class):
        for skill_name in self.__skills[job_class].keys():
            print(skill_name)

    def has_job_class(self, job_class):
        return job_class in self.__skills.keys()

    def get_skill(self, skill_name, job_class):
        try:
            return self.__skills[job_class][skill_name]
        except:
            raise KeyError("Not in skill library: {}/{}".format(job_class, skill_name))

    def set_current_job_class(self, job_name):
        if job_name not in self.__skills:
            self.__skills[job_name] = {}

        if job_name not in self.__status_effect_priority:
            self.__status_effect_priority[job_name] = tuple()

        if job_name not in self.__job_resources:
            self.__job_resources[job_name] = {}

        if job_name not in self.__combo_breakers:
            self.__combo_breakers[job_name] = {}

        self.__current_job_class = job_name

    def set_status_effect_priority(self, status_effect_priority):
        assert isinstance(
            status_effect_priority, tuple
        ), "status_effect_priority needs to be a tuple. Did you accidentally make it a string?"
        self.__status_effect_priority[self.__current_job_class] = status_effect_priority

    def get_status_effect_priority(self, job_name):
        return self.__status_effect_priority[job_name]

    def get_jobs(self):
        return tuple(self.__skills.keys())

    def add_skill(self, skill):
        skill_name = skill.name
        if skill_name in self.__skills[self.__current_job_class]:
            raise RuntimeError(
                "Duplicate skill being added to the skill library (this is probably a naming error). Job: {}, Skill name: {}".format(
                    self.__current_job_class, skill_name
                )
            )
        self.__skills[self.__current_job_class][skill.name] = skill

    def print_skills(self):
        for job_name in self.__skills:
            for skill_name in self.__skills[job_name]:
                print("Job name: {}, Skill name: {}".format(job_name, skill_name))
                
    
