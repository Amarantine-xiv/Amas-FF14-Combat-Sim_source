import ama_xiv_combat_sim.simulator.game_data.patch_655.class_skills.melee as patch655
import ama_xiv_combat_sim.simulator.game_data.patch_70.class_skills.melee as patch70
import ama_xiv_combat_sim.simulator.game_data.patch_701.class_skills.melee as patch701
import ama_xiv_combat_sim.simulator.game_data.patch_705.class_skills.melee as patch705

def add_melee_skills_to_skill_library(skill_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
            skill_library = patch70.add_vpr_skills(skill_library)
        case "7.01":
            patch_use = patch701
            skill_library = patch701.add_vpr_skills(skill_library)
        case "7.05":
            patch_use = patch705
            skill_library = patch705.add_vpr_skills(skill_library)
        case _:
            raise RuntimeError(f"Bad version: {version}")
    skill_library = patch_use.add_drg_skills(skill_library)
    skill_library = patch_use.add_mnk_skills(skill_library)
    skill_library = patch_use.add_nin_skills(skill_library)
    skill_library = patch_use.add_rpr_skills(skill_library)
    skill_library = patch_use.add_sam_skills(skill_library)
    return skill_library
