
from ama_xiv_combat_sim.example_rotations.add_caster_rotations_to_rotation_library import add_caster_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_healer_rotations_to_rotation_library import add_healer_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_melee_rotations_to_rotation_library import add_melee_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_ranged_rotations_to_rotation_library import add_ranged_rotations_to_rotation_library
from ama_xiv_combat_sim.example_rotations.add_tank_rotations_to_rotation_library import add_tank_rotations_to_rotation_library

def add_to_rotation_library(rotation_name_and_rb, rotation_library):
    rotation_name, rb = rotation_name_and_rb
    if rotation_name in rotation_library:
        print('Updating rotation "{}" in the rotation library.'.format(rotation_name))
    rotation_library[rotation_name] = rb


def get_example_rotations(skill_library, version=None):
    res = {}
    if version is None:
        version = skill_library.get_version()
    add_tank_rotations_to_rotation_library(skill_library, res, version)
    add_healer_rotations_to_rotation_library(skill_library, res, version)
    add_ranged_rotations_to_rotation_library(skill_library, res, version)
    add_caster_rotations_to_rotation_library(skill_library, res, version)
    add_melee_rotations_to_rotation_library(skill_library, res, version)    
    
    return res