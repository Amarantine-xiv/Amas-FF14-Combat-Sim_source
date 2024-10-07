from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.brd import add_brd_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.dnc import add_dnc_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.mch import add_mch_skills

def add_ranged_skills_to_skill_library(skill_library):
    skill_library = add_brd_skills(skill_library)
    skill_library = add_dnc_skills(skill_library)
    skill_library = add_mch_skills(skill_library)    
    return skill_library
