from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.ast import add_ast_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sge import add_sge_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sch import add_sch_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.whm import add_whm_skills

def add_healer_skills_to_skill_library(skill_library):
    skill_library = add_sch_skills(skill_library)
    skill_library = add_whm_skills(skill_library)
    skill_library = add_sge_skills(skill_library)
    skill_library = add_ast_skills(skill_library)
    return skill_library
