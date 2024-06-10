from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.skills.skill import Skill


class JobResourceTracker:
    def __init__(self, resource_names_and_configs):
        self.__resources = {}  # key: resource name. value: list of (time, change)
        self.__resource_conigs = {}
        for resource_name, resource_config in resource_names_and_configs.items():
            self.__resources[resource_name] = []
            self.__resource_conigs[resource_name] = resource_config

    def add_resource(self, curr_t, skill, skill_modifier):
        for resource_spec in skill.get_job_resource_spec(skill_modifier):
            name = resource_spec.name
            self.__resources[name].append(
                (curr_t, curr_t + resource_spec.duration, resource_spec)
            )

    def get_resource_timeline(self, name):
        return self.__resources[name]

    # pylint: disable=all
    def compile_job_resources(self, curr_t, skill=Skill(name="")):
        res = []
        for job_resource_name in self.__resources.keys():
            if (
                skill.name
                not in self.__resource_conigs[job_resource_name].skill_allowlist
            ):
                continue

            job_resource_config = self.__resource_conigs[job_resource_name]
            total_resource = 0
            self.__resources[job_resource_name].sort(key=lambda x: x[0])

            last_refresh_time = None
            for start_time, end_time, resource_spec in self.__resources[
                job_resource_name
            ]:

                if last_refresh_time is None:
                    last_refresh_time = start_time

                if (
                    last_refresh_time + job_resource_config.expiry_from_last_gain
                    < start_time
                ):
                    total_resource = 0
                if resource_spec.refreshes_duration_of_last_gained:
                    last_refresh_time = start_time

                if curr_t < start_time or curr_t > end_time:
                    continue

                total_resource += resource_spec.change
                total_resource = min(total_resource, job_resource_config.max_value)
                total_resource = max(0, total_resource)

            if (
                last_refresh_time
                and last_refresh_time + job_resource_config.expiry_from_last_gain
                < curr_t
            ):
                total_resource = 0

            if total_resource > 0:
                if job_resource_config.add_number_to_conditional:
                    res.append("{} {}".format(total_resource, job_resource_name))
                else:
                    res.append("{}".format(job_resource_name))
        return ", ".join(res)
