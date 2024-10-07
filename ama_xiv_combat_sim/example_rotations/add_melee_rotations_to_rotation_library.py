from ama_xiv_combat_sim.example_rotations.melee.drg import add_drg_rotations
from ama_xiv_combat_sim.example_rotations.melee.mnk import add_mnk_rotations
from ama_xiv_combat_sim.example_rotations.melee.nin import add_nin_rotations
from ama_xiv_combat_sim.example_rotations.melee.rpr import add_rpr_rotations
from ama_xiv_combat_sim.example_rotations.melee.sam import add_sam_rotations
from ama_xiv_combat_sim.example_rotations.melee.vpr import add_vpr_rotations

def add_melee_rotations_to_rotation_library(skill_library, rotation_library):
    add_drg_rotations(skill_library, rotation_library)
    add_mnk_rotations(skill_library, rotation_library)
    add_nin_rotations(skill_library, rotation_library)
    add_rpr_rotations(skill_library, rotation_library)
    add_sam_rotations(skill_library, rotation_library)
    add_vpr_rotations(skill_library, rotation_library)