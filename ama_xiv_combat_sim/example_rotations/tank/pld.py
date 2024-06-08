from simulator.stats import Stats
from simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_PLD(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.24,
        main_stat=3311,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="PLD",
        version="6.55",
    )
    rotation_name = "PLD 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )

    rb.add_next("Holy Spirit")
    rb.add_next("Fast Blade")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Riot Blade")
    rb.add_next("Royal Authority")
    rb.add_next("Fight or Flight")
    rb.add_next("Requiescat")
    rb.add_next("Goring Blade")
    rb.add_next("Circle of Scorn")
    rb.add_next("Expiacion")
    rb.add_next("Confiteor")
    rb.add_next("Intervene")
    rb.add_next("Blade of Faith")
    rb.add_next("Intervene")
    rb.add_next("Blade of Truth")
    rb.add_next("Blade of Valor")
    rb.add_next("Holy Spirit")
    rb.add_next("Atonement")
    rb.add_next("Atonement")
    rb.add_next("Atonement")
    return (rotation_name, rb)
