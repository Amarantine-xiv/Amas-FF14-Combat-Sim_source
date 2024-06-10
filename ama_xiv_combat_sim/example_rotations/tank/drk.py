from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_DRK(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.96,
        main_stat=3311,
        det_stat=2182,
        crit_stat=2596,
        dh_stat=940,
        speed_stat=400,
        tenacity=601,
        job_class="DRK",
        version="6.55",
    )
    rotation_name = "DRK 6.55"

    rb = RotationBuilder(
        stats,
        skill_library,
        ignore_trailing_dots=True,
        enable_autos=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Hard Slash")
    rb.add_next("Edge of Shadow")
    rb.add_next("Syphon Strike")
    rb.add_next("Delirium")
    rb.add_next("Souleater")
    rb.add_next("Living Shadow")
    rb.add_next("Hard Slash")  # 4
    rb.add_next("Salted Earth")
    rb.add_next("Edge of Shadow")
    rb.add_next("Bloodspiller")
    rb.add_next("Shadowbringer")
    rb.add_next("Edge of Shadow")
    rb.add_next("Bloodspiller")  # 6
    rb.add_next("Carve and Spit")
    rb.add_next("Plunge")
    rb.add_next("Bloodspiller")  # 7
    rb.add_next("Shadowbringer")
    rb.add_next("Edge of Shadow")
    rb.add_next("Syphon Strike")  # 8
    rb.add_next("Salt and Darkness")
    rb.add_next("Edge of Shadow")
    rb.add_next("Souleater")  # 9
    rb.add_next("Plunge")
    rb.add_next("Hard Slash")  # 10
    rb.add_next("Syphon Strike")  # 11
    rb.add_next("Edge of Shadow")
    rb.add_next("Souleater")  # 12
    rb.add_next("Bloodspiller")  # 13
    return (rotation_name, rb)


def get_drk_log_rotation(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.96,
        main_stat=3330,
        det_stat=2182,
        crit_stat=2576,
        dh_stat=940,
        speed_stat=400,
        tenacity=529,
        job_class="DRK",
        version="6.55",
    )
    rotation_name = "DRK Log"

    rb = RotationBuilder(
        stats, skill_library, ignore_trailing_dots=True, enable_autos=False
    )

    rb.add(
        0.396,
        "The Wanderer's Minuet",
        skill_modifier=SkillModifier(with_condition="Buff Only"),
        job_class="BRD",
    )

    rb.add(-0.183, "Plunge")
    rb.add(0.395, "Hard Slash")
    rb.add(0.795, "Auto")
    rb.add(1.683, "Edge of Shadow")
    rb.add(3.751, "Syphon Strike")
    rb.add(3.866, "Auto")
    rb.add(5.623, "Souleater")
    rb.add(6.872, "Auto")
    rb.add(8.121, "Hard Slash")
    rb.add(9.861, "Auto")
    rb.add(10.619, "Syphon Strike")
    rb.add(12.848, "Auto")
    rb.add(13.116, "Souleater")
    rb.add(15.612, "Hard Slash")
    rb.add(15.836, "Auto")
    rb.add(16.086, "Living Shadow")
    rb.add(18.112, "Syphon Strike")
    rb.add(18.824, "Auto")
    rb.add(20.606, "Souleater")

    return (rotation_name, rb)
