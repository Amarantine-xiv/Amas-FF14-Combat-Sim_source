from simulator.stats import Stats
from simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_SMN(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=3.12,
        main_stat=3379,
        det_stat=1871,
        crit_stat=2514,
        dh_stat=1438,
        speed_stat=502,
        job_class="SMN",
        version="6.55",
    )
    rotation_name = "SMN 6.55 Fast Garuda"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Ruin III")
    rb.add_next("Summon Bahamut")
    rb.add_next("Searing Light")
    rb.add_next("Astral Impulse")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Astral Impulse")
    rb.add_next("Astral Impulse")
    rb.add_next("Energy Drain")
    rb.add_next("Enkindle Bahamut")
    rb.add_next("Astral Impulse")
    rb.add_next("Deathflare")
    rb.add_next("Fester")
    rb.add_next("Astral Impulse")
    rb.add_next("Fester")
    rb.add_next("Astral Impulse")
    rb.add_next("Summon Garuda II")
    rb.add_next("Swiftcast")
    rb.add_next("Slipstream")
    rb.add_next("Emerald Rite")
    rb.add_next("Emerald Rite")
    rb.add_next("Emerald Rite")
    rb.add_next("Emerald Rite")
    rb.add_next("Summon Titan II")
    return (rotation_name, rb)
