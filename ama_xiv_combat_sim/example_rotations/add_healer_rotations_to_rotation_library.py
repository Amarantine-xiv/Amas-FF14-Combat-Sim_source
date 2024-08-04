import ama_xiv_combat_sim.example_rotations.patch_655.healer as patch655
import ama_xiv_combat_sim.example_rotations.patch_70.healer as patch70


def add_healer_rotations_to_rotation_library(skill_library, rotation_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
        case "7.01":
            patch_use = patch70
        case "7.05":
            patch_use = patch70
        case _:
            raise RuntimeError("Bad version: {}".format(version))

    patch_use.add_sch_rotations(skill_library, rotation_library)
    patch_use.add_ast_rotations(skill_library, rotation_library)
    patch_use.add_sge_rotations(skill_library, rotation_library)
    patch_use.add_whm_rotations(skill_library, rotation_library)