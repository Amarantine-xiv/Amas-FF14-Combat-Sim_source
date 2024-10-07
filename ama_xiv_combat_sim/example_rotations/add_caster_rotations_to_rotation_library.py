from ama_xiv_combat_sim.example_rotations.caster.blm import add_blm_rotations
from ama_xiv_combat_sim.example_rotations.caster.pct import add_pct_rotations
from ama_xiv_combat_sim.example_rotations.caster.rdm import add_rdm_rotations
from ama_xiv_combat_sim.example_rotations.caster.smn import add_smn_rotations


def add_caster_rotations_to_rotation_library(skill_library, rotation_library):
    add_blm_rotations(skill_library, rotation_library)
    add_pct_rotations(skill_library, rotation_library)
    add_rdm_rotations(skill_library, rotation_library)
    add_smn_rotations(skill_library, rotation_library)