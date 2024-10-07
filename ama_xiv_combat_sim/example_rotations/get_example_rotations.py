
from ama_xiv_combat_sim.example_rotations.add_caster_rotations_to_rotation_library import add_caster_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_healer_rotations_to_rotation_library import add_healer_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_melee_rotations_to_rotation_library import add_melee_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_ranged_rotations_to_rotation_library import add_ranged_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_tank_rotations_to_rotation_library import add_tank_rotations_to_rotation_library

def get_example_rotations(skill_library):
    res = {}
    add_tank_rotations_to_rotation_library(skill_library, res)
    add_healer_rotations_to_rotation_library(skill_library, res)
    add_ranged_rotations_to_rotation_library(skill_library, res)
    add_caster_rotations_to_rotation_library(skill_library, res)
    add_melee_rotations_to_rotation_library(skill_library, res)
    
    return res
    
    