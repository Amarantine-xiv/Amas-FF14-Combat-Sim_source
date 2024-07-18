import ama_xiv_combat_sim.example_rotations.patch_655.melee as patch655
import ama_xiv_combat_sim.example_rotations.patch_70.melee as patch70


def add_melee_rotations_to_rotation_library(skill_library, rotation_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
            patch_use.add_vpr_rotations(skill_library, rotation_library)
        case "7.01":
            patch_use = patch70
            patch_use.add_vpr_rotations(skill_library, rotation_library)
        case _:
            raise RuntimeError("Bad version: {}".format(version))

    patch_use.add_drg_rotations(skill_library, rotation_library)
    patch_use.add_mnk_rotations(skill_library, rotation_library)
    patch_use.add_nin_rotations(skill_library, rotation_library)
    patch_use.add_rpr_rotations(skill_library, rotation_library)
    patch_use.add_sam_rotations(skill_library, rotation_library)
    