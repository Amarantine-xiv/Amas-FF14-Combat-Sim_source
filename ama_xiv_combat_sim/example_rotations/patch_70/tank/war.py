from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


def get_rotation_WAR(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.36,
        main_stat=3330,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="WAR",
        version=skill_library.get_version(),
    )
    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    # name for now
    rotation_name = "WAR 6.55"

    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")

    return (rotation_name, rb)


def get_rotation_WAR_extended(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.36,
        main_stat=3330,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="WAR",
        version=skill_library.get_version(),
    )
    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rotation_name = "WAR Extended 6.55"

    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")
    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")
    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")
    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")
    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")
    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")

    return (rotation_name, rb)


def get_rotation_WAR_party_buffs(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.36,
        main_stat=3330,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="WAR",
        version=skill_library.get_version(),
    )
    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rotation_name = "WAR 6.55 Party Buffs"

    # Party buffs
    rb.add(6.3, "Chain Stratagem", job_class="SCH")
    rb.add(7.1, "Battle Litany", job_class="DRG")
    rb.add(0.8, "Arcane Circle", job_class="RPR")
    rb.add(6.28, "Embolden", job_class="RDM")

    rb.add_next("Tomahawk")
    rb.add_next("Infuriate")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Storm's Eye")
    rb.add_next("Inner Release")
    rb.add_next("Inner Chaos")
    rb.add_next("Upheaval")
    rb.add_next("Onslaught")
    rb.add_next("Primal Rend")
    rb.add_next("Inner Chaos")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Onslaught")
    rb.add_next("Fell Cleave")
    rb.add_next("Fell Cleave")
    rb.add_next("Heavy Swing")
    rb.add_next("Maim")
    rb.add_next("Storm's Path")
    rb.add_next("Fell Cleave")
    rb.add_next("Inner Chaos")

    return (rotation_name, rb)


def add_war_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_WAR(skill_library), rotation_library)
    add_to_rotation_library(get_rotation_WAR_extended(skill_library), rotation_library)
    add_to_rotation_library(
        get_rotation_WAR_party_buffs(skill_library), rotation_library
    )
    return rotation_library
