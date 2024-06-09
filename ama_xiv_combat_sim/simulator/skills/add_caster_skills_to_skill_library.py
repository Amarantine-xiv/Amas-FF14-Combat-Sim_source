import simulator.game_data.patch_655.class_skills.caster as patch655
import simulator.game_data.patch_70.class_skills.caster as patch70

def add_caster_skills_to_skill_library(skill_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
            patch_use.add_pct_skills(skill_library)
        case _:
            raise RuntimeError("Bad version: {}".format(version))
    skill_library = patch_use.add_blm_skills(skill_library)
    skill_library = patch_use.add_rdm_skills(skill_library)
    skill_library = patch_use.add_smn_skills(skill_library)
    return skill_library
