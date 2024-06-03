from .SCH.patch_6_4 import add_sch_skills
from .WHM.patch_6_4 import add_whm_skills
from .SGE.patch_6_4 import add_sge_skills
from .AST.patch_6_4 import add_ast_skills

def add_healer_skills_to_skill_library(skill_library):
  skill_library = add_sch_skills(skill_library)
  skill_library = add_whm_skills(skill_library)
  skill_library = add_sge_skills(skill_library)
  skill_library = add_ast_skills(skill_library)
  return skill_library