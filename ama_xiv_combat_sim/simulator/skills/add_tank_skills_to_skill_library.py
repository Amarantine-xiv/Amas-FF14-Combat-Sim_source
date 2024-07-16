import ama_xiv_combat_sim.simulator.game_data.patch_655.class_skills.tank as patch655
import ama_xiv_combat_sim.simulator.game_data.patch_70.class_skills.tank as patch70
import ama_xiv_combat_sim.simulator.game_data.patch_701.class_skills.tank as patch701


def add_tank_skills_to_skill_library(skill_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
        case "7.01":
            patch_use = patch701
        case _:
            raise RuntimeError(f"Bad version: {version}")

    skill_library = patch_use.add_war_skills(skill_library)
    skill_library = patch_use.add_gnb_skills(skill_library)
    skill_library = patch_use.add_pld_skills(skill_library)
    skill_library = patch_use.add_drk_skills(skill_library)
    return skill_library
