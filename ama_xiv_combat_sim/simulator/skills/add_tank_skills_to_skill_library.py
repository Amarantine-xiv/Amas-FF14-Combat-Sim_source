from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.drk import DrkSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.gnb import GnbSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.pld import PldSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.war import WarSkills

def add_tank_skills_to_skill_library(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()
    
    skill_library.add_all_skills_from(DrkSkills(version=version, level=level))
    skill_library.add_all_skills_from(GnbSkills(version=version, level=level))
    skill_library.add_all_skills_from(PldSkills(version=version, level=level))
    skill_library.add_all_skills_from(WarSkills(version=version, level=level))
    
    
    return skill_library
