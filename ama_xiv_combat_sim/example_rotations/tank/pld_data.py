from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_pld_rotations = SpecificRotations()

ALL_PLD_ROTATIONS = {
    "PLD": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3311,
                "det_stat": 2182,
                "crit_stat": 2596,
                "dh_stat": 940,
                "speed_stat": 400,
                "tenacity": 601,
                "job_class": "PLD",
            },
            "skills": (
                "Holy Spirit",
                "Fast Blade",
                "Grade 8 Tincture",
                "Riot Blade",
                "Royal Authority",
                "Fight or Flight",
                "Requiescat",
                "Goring Blade",
                "Circle of Scorn",
                "Expiacion",
                "Confiteor",
                "Intervene",
                "Blade of Faith",
                "Intervene",
                "Blade of Truth",
                "Blade of Valor",
                "Holy Spirit",
                "Atonement",
                "Atonement",
                "Atonement",
            ),
            "start_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4820,
                "det_stat": 2310,
                "crit_stat": 3174,
                "dh_stat": 1470,
                "speed_stat": 420,
                "tenacity": 868,
                "job_class": "PLD",
            },
            "skills": (
                "Holy Spirit",
                "Fast Blade",
                "Riot Blade",
                "Grade 2 Gemdraught",                
                "Royal Authority",
                "Fight or Flight",
                "Imperator",
                "Confiteor",
                "Circle of Scorn",
                "Expiacion",
                "Blade of Faith",
                "Intervene",
                "Blade of Truth",
                "Intervene",
                "Blade of Valor",
                "Blade of Honor",                                
                "Goring Blade",
                "Atonement",
                "Supplication",
                "Sepulchre",
                "Holy Spirit",
            ),
            "start_version": "7.05",
        }
    },
}

for k, v in ALL_PLD_ROTATIONS.items():
    all_pld_rotations.add_rotation_data(k, v)
