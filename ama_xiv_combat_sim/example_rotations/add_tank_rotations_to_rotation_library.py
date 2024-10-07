from ama_xiv_combat_sim.example_rotations.tank.war import add_war_rotations
from ama_xiv_combat_sim.example_rotations.tank.pld import add_pld_rotations
from ama_xiv_combat_sim.example_rotations.tank.gnb import add_gnb_rotations
from ama_xiv_combat_sim.example_rotations.tank.drk import add_drk_rotations


def add_tank_rotations_to_rotation_library(skill_library, rotation_library):
    add_war_rotations(skill_library, rotation_library)
    add_pld_rotations(skill_library, rotation_library)
    add_gnb_rotations(skill_library, rotation_library)
    add_drk_rotations(skill_library, rotation_library)