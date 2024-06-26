from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_RDM(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.44,
        main_stat=3379,
        det_stat=1601,
        crit_stat=2514,
        dh_stat=1708,
        speed_stat=502,
        job_class="RDM",
        healer_or_caster_strength=214,
        version=skill_library.get_version(),
    )
    rotation_name = "RDM 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Verthunder III")
    rb.add_next("Veraero III")
    rb.add_next("Swiftcast")
    rb.add_next("Acceleration")
    rb.add_next("Verthunder III")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Verthunder III")
    rb.add_next("Embolden")
    rb.add_next("Manafication")
    rb.add_next("Enchanted Riposte")
    rb.add_next("Fleche")
    rb.add_next("Enchanted Zwerchhau")
    rb.add_next("Contre Sixte")
    rb.add_next("Enchanted Redoublement")
    rb.add_next("Corps-a-corps")
    rb.add_next("Engagement")
    rb.add_next("Verholy")
    rb.add_next("Corps-a-corps")
    rb.add_next("Engagement")
    rb.add_next("Scorch")
    rb.add_next("Resolution")
    rb.add_next("Verfire")
    rb.add_next("Verthunder III")
    rb.add_next("Verstone")
    rb.add_next("Veraero III")
    rb.add_next("Jolt II")
    rb.add_next("Verthunder III")
    rb.add_next("Fleche")
    return (rotation_name, rb)

def add_rdm_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_RDM(skill_library), rotation_library)    
    return rotation_library