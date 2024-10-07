from ama_xiv_combat_sim.example_rotations.healer.ast import add_ast_rotations
from ama_xiv_combat_sim.example_rotations.healer.sch import add_sch_rotations
from ama_xiv_combat_sim.example_rotations.healer.sge import add_sge_rotations
from ama_xiv_combat_sim.example_rotations.healer.whm import add_whm_rotations


def add_healer_rotations_to_rotation_library(skill_library, rotation_library):
    add_whm_rotations(skill_library, rotation_library)
    add_sge_rotations(skill_library, rotation_library)
    add_sch_rotations(skill_library, rotation_library)
    add_ast_rotations(skill_library, rotation_library)
    
    