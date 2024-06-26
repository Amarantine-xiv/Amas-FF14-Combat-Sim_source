from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_DNC(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.12,
        main_stat=3379,
        det_stat=1952,
        crit_stat=2557,
        dh_stat=1380,
        speed_stat=436,
        job_class="DNC",
        version=skill_library.get_version(),
    )
    rotation_name = "DNC 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )

    rb.add_next("Grade 8 Tincture")
    rb.add_next("Technical Step")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Quadruple Technical Finish")
    rb.add_next("Devilment")
    rb.add_next("Starfall Dance")
    rb.add_next("Flourish")
    rb.add_next("Fan Dance III")
    rb.add_next("Tillana")
    rb.add_next("Fan Dance IV")
    rb.add_next("Fountainfall")
    rb.add_next("Fan Dance")
    rb.add_next("Fan Dance III")
    rb.add_next("Standard Step")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Double Standard Finish")
    return (rotation_name, rb)


def get_rotation_DNC_extended(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.12,
        main_stat=3379,
        det_stat=1952,
        crit_stat=2557,
        dh_stat=1380,
        speed_stat=436,
        job_class="DNC",
        version=skill_library.get_version(),
    )
    rotation_name = "DNC 6.55 extended"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Double Standard Finish")
    rb.add_next("Technical Step")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Quadruple Technical Finish")
    rb.add_next("Devilment")
    rb.add_next("Starfall Dance")
    rb.add_next("Flourish")
    rb.add_next("Fan Dance III")
    rb.add_next("Fountainfall")
    rb.add_next("Fan Dance")
    rb.add_next("Fan Dance IV")
    rb.add_next("Tillana")
    rb.add_next("Fan Dance III")
    rb.add_next("Saber Dance")
    rb.add_next("Standard Step")
    rb.add_next("Step Action")
    rb.add_next("Step Action")
    rb.add_next("Double Standard Finish")
    rb.add_next("Saber Dance")
    rb.add_next("Reverse Cascade")
    rb.add_next("Saber Dance")
    return (rotation_name, rb)

def add_dnc_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_DNC(skill_library), rotation_library)    
    add_to_rotation_library(get_rotation_DNC_extended(skill_library), rotation_library)    
    return rotation_library