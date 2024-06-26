from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_AST(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.2,
        main_stat=3369,
        det_stat=2047,
        crit_stat=2409,
        dh_stat=472,
        speed_stat=1299,
        job_class="AST",
        version=skill_library.get_version(),
    )
    rotation_name = "AST 6.4"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Earthly Star")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Fall Malefic")
    rb.add_next("Lightspeed")
    rb.add_next("Combust III")
    rb.add_next("the Arrow")
    rb.add_next("Fall Malefic")
    rb.add_next("the Balance")
    rb.add_next("Fall Malefic")
    rb.add_next("Divination")
    rb.add_next("the Spire")
    rb.add_next("Fall Malefic")
    rb.add_next("Minor Arcana")
    rb.add_next("Fall Malefic")
    rb.add_next("Lord of Crowns")
    rb.add_next("Fall Malefic", num_times=6)
    return (rotation_name, rb)

def add_ast_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_AST(skill_library), rotation_library)    
    return rotation_library