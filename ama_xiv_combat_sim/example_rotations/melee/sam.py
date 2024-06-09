from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_SAM(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.64,
        main_stat=3367,
        det_stat=1736,
        crit_stat=2587,
        dh_stat=1494,
        speed_stat=508,
        job_class="SAM",
        version="6.55",
    )
    rotation_name = "SAM 6.55, 2.15 gcd"

    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=True,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    rb.add_next("Meikyo Shisui")
    rb.add_next("True North")
    rb.add_next("Gekko")
    rb.add_next("Grade 8 Tincture")
    rb.add_next("Kasha")
    rb.add_next("Yukikaze")
    rb.add_next("Midare Setsugekka")
    rb.add_next("Hissatsu: Senei")
    rb.add_next("Kaeshi: Setsugekka")
    rb.add_next("Meikyo Shisui")
    rb.add_next("Gekko")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Higanbana")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Ogi Namikiri")
    rb.add_next("Shoha")
    rb.add_next("Kaeshi: Namikiri")
    rb.add_next("Kasha")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Gekko")
    rb.add_next("Hissatsu: Gyoten")
    rb.add_next("Hakaze")
    rb.add_next("Hissatsu: Shinten")
    rb.add_next("Yukikaze")
    rb.add_next("Midare Setsugekka")
    rb.add_next("Kaeshi: Setsugekka")
    return (rotation_name, rb)


def get_rotation_SAM_manual(skill_library):
    stats = Stats(
        wd=132,
        weapon_delay=2.64,
        main_stat=3367,
        det_stat=1680,
        crit_stat=2587,
        dh_stat=1458,
        speed_stat=508,
        job_class="SAM",
        version="6.55",
    )
    rotation_name = "SAM 6.5, Manual"

    # From the log: https://www.fflogs.com/reports/nx6g4cLwadZh9WqB#fight=6&type=damage-done&source=69&start=2547849&end=2580747&view=events.
    # but not sure of the gear set. Best guess, taken from their current set on 2024-01-14 (which is the the 2.5 bis set).
    # Note: this currently has none of the party buffs.
    rb = RotationBuilder(
        stats,
        skill_library,
        enable_autos=False,
        ignore_trailing_dots=True,
        snap_dots_to_server_tick_starting_at=0,
    )
    # this doesn't appear in the logs, but we need to use it unless we want to add conditionals on everything
    rb.add(0.0, "Meikyo Shisui")
    rb.add(0.889, "Gekko")
    rb.add(1.561, "Grade 8 Tincture")
    rb.add(3.349, "Kasha")
    rb.add(5.848, "Yukikaze")
    rb.add(7.985, "Midare Setsugekka")
    rb.add(9.373, "Hissatsu: Senei")
    rb.add(10.118, "Kaeshi: Setsugekka")
    rb.add(11.466, "Meikyo Shisui")
    rb.add(12.309, "Gekko")
    rb.add(12.930, "Hissatsu: Shinten")
    rb.add(13.602, "Hissatsu: Gyoten")
    rb.add(14.446, "Higanbana")
    rb.add(15.833, "Hissatsu: Shinten")
    rb.add(16.597, "Ogi Namikiri")
    rb.add(18.016, "Shoha")
    rb.add(18.773, "Kaeshi: Namikiri")
    rb.add(20.955, "Gekko")
    rb.add(21.627, "Hissatsu: Shinten")
    rb.add(23.101, "Kasha")
    rb.add(23.722, "Hissatsu: Gyoten")
    rb.add(25.236, "Hakaze")
    rb.add(27.370, "Yukikaze")
    rb.add(28.665, "Hissatsu: Shinten")
    rb.add(29.517, "Midare Setsugekka")
    rb.add(31.688, "Kaeshi: Setsugekka")

    rb.add(0.889, "Auto")
    rb.add(4.096, "Auto")
    rb.add(6.417, "Auto")
    rb.add(9.544, "Auto")
    rb.add(11.867, "Auto")
    rb.add(14.189, "Auto")
    rb.add(18.104, "Auto")
    rb.add(20.423, "Auto")
    rb.add(22.741, "Auto")
    rb.add(25.058, "Auto")
    rb.add(27.370, "Auto")
    rb.add(29.688, "Auto")

    return (rotation_name, rb)
