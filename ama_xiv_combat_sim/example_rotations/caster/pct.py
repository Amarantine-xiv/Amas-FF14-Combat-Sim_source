from simulator.stats import Stats
from simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_PCT(skill_library):
    if not skill_library.has_job_class("PCT"):
        return None
        
    stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1871,
            crit_stat=2514,
            dh_stat=1438,
            speed_stat=502,
            job_class="PCT",
            version="7.0",
        )
    rotation_name = "PCT 7.0"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )

    skill_seq = (
        ("Rainbow Drip"),
        ("Grade 8 Tincture"),
        ("Holy in White"),
        ("Pom Muse"),
        ("Swiftcast"),
        ("Wing Motif"),        
        ("Striking Muse"),
        ("Fire in Red"),
        ("Starry Muse"),
        ("Star Prism"),
        ("Hammer Stamp"),
        ("Winged Muse"),
        ("Hammer Brush"),
        ("Mog of the Ages"),
        ("Polishing Hammer"),
        ("Subtractive Palette"),
        ("Stone in Yellow"),
        ("Thunder in Magenta"),
        ("Comet in Black"),
        ("Claw Motif"),
        ("Clawed Muse"),
        ("Holy in White"),
        ("Rainbow Drip"),
        ("Blizzard in Cyan"),
        ("Aero in Green"),
        ("Water in Blue"),
        ("Fire in Red"),
        ("Maw Motif"),
        ("Aero in Green"),
        ("Fanged Muse"),
        ("Water in Blue"),
    )
    
    for e in skill_seq:
        rb.add_next(e)
        
    return (rotation_name, rb)