import simulator.game_data.patch_655.class_skills.melee as patch655
import simulator.game_data.patch_70.class_skills.melee as patch70

def add_melee_skills_to_skill_library(skill_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
            skill_library = patch70.add_vpr_skills(skill_library)
        case _:
            raise RuntimeError("Bad version: {}".format(version))
    skill_library = patch_use.add_drg_skills(skill_library)
    skill_library = patch_use.add_mnk_skills(skill_library)
    skill_library = patch_use.add_nin_skills(skill_library)
    skill_library = patch_use.add_rpr_skills(skill_library)
    skill_library = patch_use.add_sam_skills(skill_library)
    return skill_library
