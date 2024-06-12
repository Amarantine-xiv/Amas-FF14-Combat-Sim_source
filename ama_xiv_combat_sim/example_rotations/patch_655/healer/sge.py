from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_SGE(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.8,
        main_stat=3369,
        det_stat=2211,
        crit_stat=2502,
        dh_stat=832,
        speed_stat=774,
        job_class="SGE",
        version=skill_library.get_version(),
    )
    rotation_name = "SGE 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Dosis III")
    rb.add_next("Eukrasia")
    rb.add_next("Eukrasian Dosis III")
    rb.add_next("Dosis III")
    rb.add_next("Dosis III")
    rb.add_next("Phlegma III")
    rb.add_next("Phlegma III")
    rb.add_next("Dosis III", num_times=5)
    return (rotation_name, rb)

def add_sge_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_SGE(skill_library), rotation_library)    
    return rotation_library