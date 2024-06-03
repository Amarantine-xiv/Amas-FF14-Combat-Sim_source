from .SAM.patch_6_4 import add_sam_skills
from .DRG.patch_6_4 import add_drg_skills
from .MNK.patch_6_4 import add_mnk_skills
from .RPR.patch_6_4 import add_rpr_skills
from .NIN.patch_6_4 import add_nin_skills

def add_melee_skills_to_skill_library(skill_library):
    skill_library = add_sam_skills(skill_library)
    skill_library = add_drg_skills(skill_library)
    skill_library = add_mnk_skills(skill_library)
    skill_library = add_rpr_skills(skill_library)
    skill_library = add_nin_skills(skill_library)
    return skill_library
  