from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_blm_rotations = SpecificRotations()

ALL_BLM_ROTATIONS = {
    "BLM": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3375,
                "det_stat": 1764,
                "crit_stat": 545,
                "dh_stat": 1547,
                "speed_stat": 2469,
                "job_class": "BLM",
            },
            "skills": (
                "Sharpcast",
                "Fire III",
                "Thunder III",
                "Triplecast",
                "Fire IV",
                "Grade 8 Tincture",
                "Fire IV",
                "Amplifier",
                "Ley Lines",
                "Fire IV",
                "Swiftcast",
                "Fire IV",
                "Triplecast",
                "Despair",
                "Manafont",
                "Fire IV",
                "Sharpcast",
                "Despair",
                "Blizzard III",
                "Xenoglossy",
                "Paradox",
                "Blizzard IV",
                "Thunder III",
            ),
            "start_version": "6.55",
            "end_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4882,
                "det_stat": 1572,
                "crit_stat": 3321,
                "dh_stat": 1882,
                "speed_stat": 1047,
                "job_class": "BLM",
            },
            "skills": (            
                "Fire III",
                "High Thunder",
                "Swiftcast",
                "Amplifier",
                "Fire IV",
                "Grade 2 Gemdraught",
                "Fire IV",
                "Xenoglossy",
                "Triplecast",
                "Ley Lines",
                "Fire IV",
                "Fire IV",
                "Despair",
                "Manafont",
                "Triplecast",
                "Fire IV",
                "Fire IV",
                "Flare Star",
                "Fire IV",
                "High Thunder",
                "Paradox",
                "Fire IV",
                "Fire IV",
                "Fire IV",
                "Despair",
            ),
            "start_version": "7.05",            
        },
    },
}

for k, v in ALL_BLM_ROTATIONS.items():
    all_blm_rotations.add_rotation_data(k, v)
