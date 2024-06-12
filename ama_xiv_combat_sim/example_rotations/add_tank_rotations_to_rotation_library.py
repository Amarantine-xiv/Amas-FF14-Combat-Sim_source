import ama_xiv_combat_sim.example_rotations.patch_655.tank as patch655
import ama_xiv_combat_sim.example_rotations.patch_70.tank as patch70


def add_tank_rotations_to_rotation_library(skill_library, rotation_library, version="6.55"):
    match version:
        case "6.55":
            patch_use = patch655
        case "7.0":
            patch_use = patch70
        case _:
            raise RuntimeError("Bad version: {}".format(version))

    patch_use.add_war_rotations(skill_library, rotation_library)
    patch_use.add_pld_rotations(skill_library, rotation_library)
    patch_use.add_gnb_rotations(skill_library, rotation_library)
    patch_use.add_drk_rotations(skill_library, rotation_library)