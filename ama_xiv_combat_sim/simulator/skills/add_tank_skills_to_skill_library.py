from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.war import add_war_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.gnb import add_gnb_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.pld import add_pld_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.drk import add_drk_skills

def add_tank_skills_to_skill_library(skill_library):
    skill_library = add_war_skills(skill_library)
    skill_library = add_gnb_skills(skill_library)
    skill_library = add_pld_skills(skill_library)
    skill_library = add_drk_skills(skill_library)
    return skill_library
