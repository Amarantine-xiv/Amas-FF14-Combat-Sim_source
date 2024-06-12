from ama_xiv_combat_sim.example_rotations.add_rotation_to_rotation_library import (
    add_to_rotation_library,
)
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_NIN(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.56,
        main_stat=3360,
        det_stat=1697,
        crit_stat=2554,
        dh_stat=1582,
        speed_stat=400,
        job_class="NIN",
        version=skill_library.get_version(),
    )
    rotation_name = "NIN 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Huton")
    rb.add_next("Hide")
    rb.add_next("Suiton")
    rb.add_next("Kassatsu")
    rb.add_next("Spinning Edge")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Gust Slash")
    rb.add_next("Mug")
    rb.add_next("Bunshin")
    rb.add_next("Phantom Kamaitachi")
    rb.add_next("Trick Attack")
    rb.add_next("Aeolian Edge")
    rb.add_next("Dream Within a Dream")
    rb.add_next("Ten")
    rb.add_next("Jin")
    rb.add_next("Hyosho Ranryu")
    rb.add_next("Ten")
    rb.add_next("Chi")
    rb.add_next("Raiton")
    rb.add_next("Ten Chi Jin")
    rb.add_next("Fuma Shuriken")
    rb.add_next("Raiton")
    rb.add_next("Suiton")
    rb.add_next("Meisui")
    rb.add_next("Forked Raiju")
    rb.add_next("Bhavacakra")
    rb.add_next("Forked Raiju")
    rb.add_next("Bhavacakra")
    rb.add_next("Ten")
    rb.add_next("Chi")
    rb.add_next("Raiton")
    rb.add_next("Forked Raiju")
    return (rotation_name, rb)

def add_nin_rotations(skill_library, rotation_library):
    add_to_rotation_library(get_rotation_NIN(skill_library), rotation_library)    
    return rotation_library