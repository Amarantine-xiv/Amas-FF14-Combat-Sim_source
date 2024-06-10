from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_SCH(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.12,
        main_stat=3369,
        det_stat=2087,
        crit_stat=2454,
        dh_stat=832,
        speed_stat=946,
        job_class="SCH",
        healer_or_caster_strength=351,
        version="6.55",
    )
    rotation_name = "SCH 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Broil IV")
    rb.add_next("Biolysis")
    rb.add_next("Aetherflow")
    rb.add_next("Broil IV")
    rb.add_next("Broil IV")
    rb.add_next("Chain Stratagem")
    rb.add_next("Broil IV")
    rb.add_next("Energy Drain")
    rb.add_next("Broil IV")
    rb.add_next("Energy Drain")
    rb.add_next("Broil IV")
    rb.add_next("Energy Drain")
    rb.add_next("Broil IV")
    rb.add_next("Broil IV")
    rb.add_next("Energy Drain")
    rb.add_next("Broil IV")
    rb.add_next("Energy Drain")
    rb.add_next("Broil IV")
    rb.add_next("Energy Drain")
    rb.add_next("Broil IV")
    rb.add_next("Broil IV")
    rb.add_next("Broil IV")
    return (rotation_name, rb)
