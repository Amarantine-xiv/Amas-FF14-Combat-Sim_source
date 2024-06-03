from .WAR.patch_6_4 import add_war_skills
from .GNB.patch_6_4 import add_gnb_skills
from .PLD.patch_6_4 import add_pld_skills
from .DRK.patch_6_4 import add_drk_skills

def add_tank_skills_to_skill_library(skill_library):
  skill_library = add_war_skills(skill_library)
  skill_library = add_gnb_skills(skill_library)
  skill_library = add_pld_skills(skill_library)
  skill_library = add_drk_skills(skill_library)
  return skill_library