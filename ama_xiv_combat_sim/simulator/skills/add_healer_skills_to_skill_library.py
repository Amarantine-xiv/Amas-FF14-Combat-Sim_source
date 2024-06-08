import simulator.game_data.patch_655.class_skills.healer as patch655
import simulator.game_data.patch_70.class_skills.healer as patch70

def add_healer_skills_to_skill_library(skill_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
        case _:
            raise RuntimeError("Bad version: {}".format(version))
    skill_library = patch_use.add_sch_skills(skill_library)
    skill_library = patch_use.add_whm_skills(skill_library)
    skill_library = patch_use.add_sge_skills(skill_library)
    skill_library = patch_use.add_ast_skills(skill_library)
    return skill_library
