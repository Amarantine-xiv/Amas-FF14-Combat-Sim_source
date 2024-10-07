from ama_xiv_combat_sim.example_rotations.ranged.dnc import add_dnc_rotations
from ama_xiv_combat_sim.example_rotations.ranged.mch import add_mch_rotations
from ama_xiv_combat_sim.example_rotations.ranged.brd import add_brd_rotations


def add_ranged_rotations_to_rotation_library(skill_library, rotation_library):
    add_brd_rotations(skill_library, rotation_library)
    add_dnc_rotations(skill_library, rotation_library)
    add_mch_rotations(skill_library, rotation_library)