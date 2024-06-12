from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_BLM(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.28,
        main_stat=3375,
        det_stat=1764,
        crit_stat=545,
        dh_stat=1547,
        speed_stat=2469,
        job_class="BLM",
        version=skill_library.get_version(),
    )
    rotation_name = "BLM 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
        fight_start_time=0,
    )
    rb.add_next("Fire III")
    rb.add_next("Thunder III")
    rb.add_next("Triplecast")
    rb.add_next("Fire IV")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Fire IV")
    rb.add_next("Amplifier")
    rb.add_next("Ley Lines")
    rb.add_next("Fire IV")
    rb.add_next("Swiftcast")
    rb.add_next("Fire IV")
    rb.add_next("Triplecast")
    rb.add_next("Despair")
    rb.add_next("Manafont")
    rb.add_next("Fire IV")
    rb.add_next("Despair")
    rb.add_next("Blizzard III")
    rb.add_next("Xenoglossy")
    rb.add_next("Paradox")
    rb.add_next("Blizzard IV")
    rb.add_next("Thunder III")

    return (rotation_name, rb)

def add_blm_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_BLM(skill_library), rotation_library)    
    return rotation_library