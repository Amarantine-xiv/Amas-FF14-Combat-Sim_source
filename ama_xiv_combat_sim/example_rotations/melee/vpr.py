from simulator.stats import Stats
from simulator.timeline_builders.rotation_builder import RotationBuilder


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
        version="7.0",
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
        "Dreadwinder",
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
        "Dreadwinder",
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