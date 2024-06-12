from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


def get_rotation_GNB(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.80,
        main_stat=3311,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="GNB",
        version=skill_library.get_version(),
    )
    rotation_name = "GNB 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Keen Edge")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Brutal Shell")
    rb.add_next("No Mercy")
    rb.add_next("Bloodfest")
    rb.add_next("Gnashing Fang")
    rb.add_next("Jugular Rip")
    rb.add_next("Sonic Break")
    rb.add_next("Blasting Zone")
    rb.add_next("Bow Shock")
    rb.add_next("Double Down")
    # rb.add_next("Rough Divide") gone from 7.0
    rb.add_next("Savage Claw")
    rb.add_next("Abdomen Tear")
    # rb.add_next("Rough Divide") gone from 7.0
    rb.add_next("Wicked Talon")
    rb.add_next("Eye Gouge")
    rb.add_next("Solid Barrel")
    rb.add_next("Burst Strike")
    rb.add_next("Hypervelocity")
    rb.add_next("Keen Edge")
    return (rotation_name, rb)


def add_gnb_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_GNB(skill_library), rotation_library)

    return rotation_library
