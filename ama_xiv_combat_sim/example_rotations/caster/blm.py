from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.example_rotations.example_rotation_utils import (
    ExampleRotationUtils,
)
from ama_xiv_combat_sim.example_rotations.caster.blm_data import all_blm_rotations


def add_blm_rotations(skill_library, rotation_library):
    all_blm_rotations.set_version(skill_library.get_version())
    all_blm_rotations.set_level(skill_library.get_level())

    for rotation_key in all_blm_rotations.rotations:
        if not all_blm_rotations.rotation_is_valid(rotation_key):
            continue

        add_to_rotation_library(
            ExampleRotationUtils.get_example_rotation(
                skill_library, rotation_key, all_blm_rotations
            ),
            rotation_library,
        )
    return rotation_library
