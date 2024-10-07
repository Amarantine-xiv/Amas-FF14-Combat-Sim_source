from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations

all_sge_rotations = SpecificRotations()

ALL_SGE_ROTATIONS = {
    "SGE": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3369,
                "det_stat": 1941,
                "crit_stat": 2502,
                "dh_stat": 580,
                "speed_stat": 1296,
                "job_class": "SGE",
            },
            "skills": (
                "Grade 8 Tincture",
                "Dosis III",
                "Eukrasia",
                "Eukrasian Dosis III",
                "Dosis III",
                "Dosis III",
                "Phlegma III",
                "Phlegma III",
                "Dosis III",
                "Dosis III",
                "Dosis III",
                "Dosis III",
                "Dosis III",
            ),
            "start_version": "6.55",
            "end_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4883,
                "det_stat": 2831,
                "crit_stat": 3041,
                "dh_stat": 1014,
                "speed_stat": 420,
                "job_class": "SGE",
            },
            "skills": (
                "Eukrasia",
                "Grade 2 Gemdraught",
                "Toxikon II",
                "Eukrasian Dosis III",
                "Dosis III",
                "Dosis III",
                "Dosis III",
                "Phlegma III",
                "Psyche",
                "Phlegma III",                
                "Dosis III",
                "Dosis III",
                "Dosis III",
                "Dosis III",
                "Eukrasia",
                "Eukrasian Dosis III",
                "Dosis III",
                "Dosis III",
                "Dosis III",
            ),
            "start_version": "7.05",
        },
    },
}

for k, v in ALL_SGE_ROTATIONS.items():
    all_sge_rotations.add_rotation_data(k, v)
