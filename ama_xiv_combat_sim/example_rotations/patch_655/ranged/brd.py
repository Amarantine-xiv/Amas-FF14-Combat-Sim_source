from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_BRD(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.04,
        main_stat=3379,
        det_stat=1885,
        crit_stat=2598,
        dh_stat=1344,
        speed_stat=479,
        job_class="BRD",
        version=skill_library.get_version(),
    )
    rotation_name = "BRD 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Stormbite")
    rb.add_next("The Wanderer's Minuet")
    rb.add_next("Raging Strikes")
    rb.add_next("Caustic Bite")
    rb.add_next("Empyreal Arrow")
    rb.add_next("Bloodletter")
    rb.add_next("Refulgent Arrow")
    rb.add_next("Radiant Finale")
    rb.add_next("Battle Voice")
    rb.add_next("Refulgent Arrow")
    rb.add_next("Sidewinder")
    rb.add_next("Refulgent Arrow")
    rb.add_next("Barrage")
    rb.add_next("Refulgent Arrow")
    rb.add_next("Burst Shot")
    rb.add_next("Refulgent Arrow")
    rb.add_next("Empyreal Arrow")
    rb.add_next("Iron Jaws")
    rb.add_next("Pitch Perfect")
    return (rotation_name, rb)

def add_brd_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_BRD(skill_library), rotation_library)    
    return rotation_library