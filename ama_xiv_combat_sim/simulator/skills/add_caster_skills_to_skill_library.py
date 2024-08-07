import ama_xiv_combat_sim.simulator.game_data.patch_655.class_skills.caster as patch655
import ama_xiv_combat_sim.simulator.game_data.patch_70.class_skills.caster as patch70
import ama_xiv_combat_sim.simulator.game_data.patch_701.class_skills.caster as patch701
import ama_xiv_combat_sim.simulator.game_data.patch_705.class_skills.caster as patch705

def add_caster_skills_to_skill_library(skill_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
            patch_use.add_pct_skills(skill_library)
        case "7.01":
            patch_use = patch701
            patch_use.add_pct_skills(skill_library)
        case "7.05":
            patch_use = patch705
            patch_use.add_pct_skills(skill_library)
        case _:
            raise RuntimeError(f"Bad version: {version}")
    skill_library = patch_use.add_blm_skills(skill_library)
    skill_library = patch_use.add_rdm_skills(skill_library)
    skill_library = patch_use.add_smn_skills(skill_library)
    return skill_library
