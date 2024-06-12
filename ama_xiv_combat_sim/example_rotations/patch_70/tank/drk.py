from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


def get_rotation_DRK(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.96,
        main_stat=3311,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="DRK",
        version=skill_library.get_version(),
    )
    rotation_name = "DRK 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Hard Slash")
    rb.add_next("Edge of Shadow")
    rb.add_next("Syphon Strike")
    rb.add_next("Delirium")
    rb.add_next("Souleater")
    rb.add_next("Living Shadow")
    rb.add_next("Hard Slash")  # 4
    rb.add_next("Salted Earth")
    rb.add_next("Edge of Shadow")
    rb.add_next("Bloodspiller")
    rb.add_next("Shadowbringer")
    rb.add_next("Edge of Shadow")
    rb.add_next("Bloodspiller")  # 6
    rb.add_next("Carve and Spit")
    # rb.add_next("Plunge") #gone from 7.0
    rb.add_next("Bloodspiller")  # 7
    rb.add_next("Shadowbringer")
    rb.add_next("Edge of Shadow")
    rb.add_next("Syphon Strike")  # 8
    rb.add_next("Salt and Darkness")
    rb.add_next("Edge of Shadow")
    rb.add_next("Souleater")  # 9
    # rb.add_next("Plunge") #gone from 7.0
    rb.add_next("Hard Slash")  # 10
    rb.add_next("Syphon Strike")  # 11
    rb.add_next("Edge of Shadow")
    rb.add_next("Souleater")  # 12
    rb.add_next("Bloodspiller")  # 13
    return (rotation_name, rb)


def add_drk_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_DRK(skill_library), rotation_library)
    return rotation_library
