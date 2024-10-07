from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.example_rotations.example_rotation_utils import (
    ExampleRotationUtils,
)
from ama_xiv_combat_sim.example_rotations.healer.sge_data import all_sge_rotations
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


def add_sge_rotations(skill_library, rotation_library):
    all_sge_rotations.set_version(skill_library.get_version())
    all_sge_rotations.set_level(skill_library.get_level())

    for rotation_key in all_sge_rotations.rotations:
        if not all_sge_rotations.rotation_is_valid(rotation_key):
            continue

        stats = all_sge_rotations.get_stats(rotation_key)
        rb = RotationBuilder(
            stats,
            skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        add_to_rotation_library(
            ExampleRotationUtils.get_example_rotation_with_rb(
                rotation_key, rb, all_sge_rotations
            ),
            rotation_library,
        )
    return rotation_library
