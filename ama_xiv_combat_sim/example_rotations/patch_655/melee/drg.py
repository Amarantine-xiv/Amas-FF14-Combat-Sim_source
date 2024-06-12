from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_DRG(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.8,
        main_stat=3379,
        det_stat=1818,
        crit_stat=2567,
        dh_stat=1818,
        speed_stat=400,
        job_class="DRG",
        version=skill_library.get_version(),
    )
    rotation_name = "DRG 6.55, 2.5 gcd"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("True Thrust")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Disembowel")
    rb.add_next("Lance Charge")
    rb.add_next("Dragon Sight")
    rb.add_next("Chaotic Spring")
    rb.add_next("Battle Litany")
    rb.add_next("Wheeling Thrust")
    rb.add_next("Geirskogul")
    rb.add_next("Life Surge")
    rb.add_next("Fang and Claw")
    rb.add_next("High Jump")
    rb.add_next("Mirage Dive")
    rb.add_next("Raiden Thrust")
    rb.add_next("Dragonfire Dive")
    rb.add_next("Vorpal Thrust")
    rb.add_next("Spineshatter Dive")
    rb.add_next("Life Surge")
    rb.add_next("Heavens' Thrust")
    rb.add_next("Fang and Claw")
    rb.add_next("Wheeling Thrust")
    rb.add_next("Raiden Thrust")
    rb.add_next("Wyrmwind Thrust")
    rb.add_next("Disembowel")
    rb.add_next("Chaotic Spring")
    rb.add_next("Wheeling Thrust")
    return (rotation_name, rb)

def add_drg_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_DRG(skill_library), rotation_library)    
    return rotation_library