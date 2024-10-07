from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.drg import add_drg_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.mnk import add_mnk_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.nin import add_nin_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.rpr import add_rpr_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.sam import add_sam_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.vpr import add_vpr_skills

def add_melee_skills_to_skill_library(skill_library):
    skill_library = add_drg_skills(skill_library)
    skill_library = add_mnk_skills(skill_library)
    skill_library = add_nin_skills(skill_library)
    skill_library = add_rpr_skills(skill_library)
    skill_library = add_sam_skills(skill_library)
    skill_library = add_vpr_skills(skill_library)
    return skill_library
