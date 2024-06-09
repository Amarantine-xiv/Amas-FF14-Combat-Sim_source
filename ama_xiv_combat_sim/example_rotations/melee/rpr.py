from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_RPR(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.2,
        main_stat=3379,
        det_stat=1764,
        crit_stat=2567,
        dh_stat=1558,
        speed_stat=436,
        job_class="RPR",
        version="6.55",
    )
    rotation_name = "RPR 6.55, Early Gluttony"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Harpe")
    rb.add_next("Shadow of Death")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Soul Slice")
    rb.add_next("Arcane Circle")
    rb.add_next("Gluttony")
    rb.add_next("Gibbet")
    rb.add_next("Gallows")
    rb.add_next("Plentiful Harvest")
    rb.add_next("Enshroud")
    rb.add_next("Void Reaping")
    rb.add_next("Cross Reaping")
    rb.add_next("Lemure's Slice")
    rb.add_next("Void Reaping")
    rb.add_next("Cross Reaping")
    rb.add_next("Lemure's Slice")
    rb.add_next("Communio")
    rb.add_next("Soul Slice")
    rb.add_next("Unveiled Gibbet")
    rb.add_next("Gibbet")
    return (rotation_name, rb)
