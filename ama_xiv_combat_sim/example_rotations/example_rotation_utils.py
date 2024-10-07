from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


class ExampleRotationUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_example_rotation_with_rb(rotation_key, rb, rotation_info):
        if not rotation_info.rotation_is_valid(rotation_key):
            return None

        skills = rotation_info.get_skills(rotation_key)
        party_skills = rotation_info.get_party_skills(rotation_key)

        for party_skill in party_skills:
            t, skill_name, job_class = party_skill[0], party_skill[1], party_skill[2]
            if len(party_skill) > 3:
                skill_modifier = party_skill[3]
                rb.add(
                    t, skill_name, skill_modifier=skill_modifier, job_class=job_class
                )
            rb.add(t, skill_name, job_class=job_class)

        for sk in skills:
            rb.add_next(sk)

        return (rotation_key, rb)

    @staticmethod
    def get_example_rotation(skill_library, rotation_key, rotation_info):
        stats = rotation_info.get_stats(rotation_key)
        rb = RotationBuilder(
            stats,
            skill_library,
            ignore_trailing_dots=True,
            enable_autos=True,
            snap_dots_to_server_tick_starting_at=0,
        )

        return ExampleRotationUtils.get_example_rotation_with_rb(
            rotation_key, rb, rotation_info
        )
