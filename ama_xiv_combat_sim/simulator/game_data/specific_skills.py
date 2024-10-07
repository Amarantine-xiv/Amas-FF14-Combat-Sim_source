from ama_xiv_combat_sim.simulator.utils import Utils

class SpecificSkills:
    def __init__(self):
        self.skills = {}
        self.version = None
        self.level = -1

    def set_version(self, version):
        self.version = version

    def set_level(self, level):
        self.level = level

    def add_skill_data(self, skill_name, vals):
        assert skill_name not in self.skills, f"Skill already exists: {skill_name}"
        self.skills[skill_name] = vals

    def get_skill_data(self, skill_name, param_name):
        assert skill_name in self.skills, f"Skill does not exist: {skill_name}"
        assert (
            self.level in self.skills[skill_name]
        ), f"Skill '{skill_name}' does not have specs for specified level: {self.level}"
        assert (
            param_name in self.skills[skill_name][self.level]
        ), f"Skill '{skill_name}' does not have requested param: {param_name}"

        return Utils.get_greatest_dict_key_val_less_than_query(
            self.skills[skill_name][self.level][param_name], self.version
        )
    
    # convenience function
    def get_potency(self, skill_name):
        res = self.get_skill_data(skill_name, "potency")
        assert res is not None, f'Could not find appropriate level/patch version for skill: {skill_name}'
        return res
    
    # convenience functions
    def get_potency_no_combo(self, skill_name):
        res = self.get_skill_data(skill_name, "potency_no_combo")
        assert res is not None, f'Could not find appropriate level/patch version for skill: {skill_name}'
        return res
    
    def get_potency_no_positional(self, skill_name):
        res = self.get_skill_data(skill_name, "potency_no_pos")
        assert res is not None, f'Could not find appropriate level/patch version for skill: {skill_name}'
        return res