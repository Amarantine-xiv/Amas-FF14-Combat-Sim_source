from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_SAM(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.64,
        main_stat=3367,
        det_stat=1736,
        crit_stat=2587,
        dh_stat=1494,
        speed_stat=508,
        job_class="SAM",
        version=skill_library.get_version(),
    )
    rotation_name = "SAM 6.55, 2.15 gcd"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Meikyo Shisui")
    rb.add_next("True North")
    rb.add_next("Gekko")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Kasha")
    rb.add_next("Yukikaze")
    rb.add_next("Midare Setsugekka")
    rb.add_next("Hissatsu: Senei")
    rb.add_next("Kaeshi: Setsugekka")
    rb.add_next("Meikyo Shisui")
    rb.add_next("Gekko")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Higanbana")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Ogi Namikiri")
    rb.add_next("Shoha")
    rb.add_next("Kaeshi: Namikiri")
    rb.add_next("Kasha")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Gekko")
    rb.add_next("Hissatsu: Gyoten")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Yukikaze")
    rb.add_next("Midare Setsugekka")
    rb.add_next("Kaeshi: Setsugekka")
    return (rotation_name, rb)

def add_sam_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_SAM(skill_library), rotation_library)    
    return rotation_library