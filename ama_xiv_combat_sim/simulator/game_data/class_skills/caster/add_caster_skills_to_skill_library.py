from .RDM.patch_6_4 import add_rdm_skills
from .BLM.patch_6_4 import add_blm_skills
from .SMN.patch_6_4 import add_smn_skills

def add_caster_skills_to_skill_library(skill_library):
  skill_library = add_rdm_skills(skill_library)
  skill_library = add_blm_skills(skill_library)
  skill_library = add_smn_skills(skill_library)
  return skill_library