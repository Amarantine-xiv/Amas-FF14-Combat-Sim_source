from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_mnk_rotations = SpecificRotations()

ALL_MNK_ROTATIONS = {
    "MNK": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3356,
                "det_stat": 1453,
                "crit_stat": 2647,
                "dh_stat": 1453,
                "speed_stat": 771,
                "job_class": "MNK",
            },
            "skills": (
                "Form Shift",
                "Dragon Kick",
                "Grade 8 Tincture",
                "Twin Snakes",
                "Riddle of Fire",
                "Demolish",
                "The Forbidden Chakra",
                "Bootshine",
                "Brotherhood",
                "Perfect Balance",
                "Dragon Kick",
                "Riddle of Wind",
                "Bootshine",
                "Dragon Kick",
                "Elixir Field",
                "Bootshine",
                "Perfect Balance",
                "Twin Snakes",
                "Dragon Kick",
                "Demolish",
                "Rising Phoenix",
            ),
            "start_version": "6.55",
            "end_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4861,
                "det_stat": 2071,
                "crit_stat": 3156,
                "dh_stat": 1639,
                "speed_stat": 956,
                "job_class": "MNK",
            },
            "skills": (
                "Dragon Kick",
                "Perfect Balance",
                "Grade 2 Gemdraught",
                "Leaping Opo",
                "Dragon Kick",
                "Brotherhood",
                "Riddle of Fire",
                "Leaping Opo",
                "The Forbidden Chakra",
                "Riddle of Wind",
                "Elixir Burst",
                "Dragon Kick",
                "Wind's Reply",
                "Fire's Reply",
                "Leaping Opo",
                "Perfect Balance",
                "Dragon Kick",
                "Leaping Opo",
                "Dragon Kick",
                "Elixir Burst",
                "Leaping Opo",
            ),
            "start_version": "7.05",
        },
    },
}

for k, v in ALL_MNK_ROTATIONS.items():
    all_mnk_rotations.add_rotation_data(k, v)
