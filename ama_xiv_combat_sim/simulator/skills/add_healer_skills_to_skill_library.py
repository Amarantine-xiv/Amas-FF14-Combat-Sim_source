import ama_xiv_combat_sim.simulator.game_data.patch_655.class_skills.healer as patch655
import ama_xiv_combat_sim.simulator.game_data.patch_70.class_skills.healer as patch70
import ama_xiv_combat_sim.simulator.game_data.patch_701.class_skills.healer as patch701
import ama_xiv_combat_sim.simulator.game_data.patch_705.class_skills.healer as patch705

def add_healer_skills_to_skill_library(skill_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
        case "7.01":
            patch_use = patch701
        case "7.05":
            patch_use = patch705
        case _:
            raise RuntimeError(f"Bad version: {version}")
    skill_library = patch_use.add_sch_skills(skill_library)
    skill_library = patch_use.add_whm_skills(skill_library)
    skill_library = patch_use.add_sge_skills(skill_library)
    skill_library = patch_use.add_ast_skills(skill_library)
    return skill_library
