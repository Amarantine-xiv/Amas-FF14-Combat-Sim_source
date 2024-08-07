from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_VPR(skill_library):    
    if not skill_library.has_job_class('VPR'):
        return None
    stats = Stats(
        wd=132,
        weapon_delay=2.64,
        main_stat=3360,
        det_stat=1582,
        crit_stat=2554,
        dh_stat=1582,
        speed_stat=400,
        job_class="VPR",
        version=skill_library.get_version(),
    )
    rotation_name = "VPR 7.0"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    skill_seq = (
        "Vicewinder",
        "Serpent's Ire",
        "Grade 8 Tincture",
        "Hunter's Coil",
        "Twinfang Bite",
        "Twinblood Bite",
        "Swiftskin's Coil",
        "Twinblood Bite",
        "Twinfang Bite",
        "Reawaken",
        "First Generation",
        "First Legacy",
        "Second Generation",
        "Second Legacy",
        "Third Generation",
        "Third Legacy",
        "Fourth Generation",
        "Fourth Legacy",
        "Ouroboros",
        "Vicewinder",
        "Swiftskin's Coil",
        "Twinblood Bite",
        "Twinfang Bite",
        "Hunter's Coil",
        "Twinfang Bite",   
        "Twinblood Bite",
        "Uncoiled Fury",
        "Uncoiled Twinfang",
        "Uncoiled Twinblood",            
    )
    for e in skill_seq:
        rb.add_next(e)
        
    return (rotation_name, rb)

def add_vpr_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_VPR(skill_library), rotation_library)    
    return rotation_library