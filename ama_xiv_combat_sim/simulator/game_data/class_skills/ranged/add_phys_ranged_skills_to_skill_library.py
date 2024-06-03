from .DNC.patch_6_4 import add_dnc_skills
from .BRD.patch_6_4 import add_brd_skills
from .MCH.patch_6_4 import add_mch_skills


def add_phys_ranged_skills_to_skill_library(skill_library):
    skill_library = add_dnc_skills(skill_library)
    skill_library = add_brd_skills(skill_library)
    skill_library = add_mch_skills(skill_library)
    return skill_library
  