from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.blm import add_blm_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.pct import add_pct_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.rdm import add_rdm_skills
from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.smn import add_smn_skills

def add_caster_skills_to_skill_library(skill_library):
    skill_library = add_blm_skills(skill_library)
    skill_library = add_pct_skills(skill_library)
    skill_library = add_rdm_skills(skill_library)
    skill_library = add_smn_skills(skill_library)
    return skill_library
