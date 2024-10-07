from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_whm_rotations = SpecificRotations()

ALL_WHM_ROTATIONS = {
    "WHM": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3369,
                "det_stat": 1941,
                "crit_stat": 2502,
                "dh_stat": 580,
                "speed_stat": 1296,
                "job_class": "WHM",
            },
            "skills": (
                "Grade 8 Tincture",
                "Glare III",
                "Dia",
                "Glare III",
                "Glare III",
                "Presence of Mind",
                "Glare III",
                "Assize",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
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
                "dh_stat": 906,
                "speed_stat": 528,
                "job_class": "WHM",
            },
            "skills": (
                "Glare III",                
                "Grade 2 Gemdraught",                
                "Dia",
                "Glare III",
                "Glare III",                
                "Presence of Mind",
                "Glare IV",
                "Assize",                
                "Glare IV",                
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",
                "Glare III",                
                "Glare IV",
                "Dia",
            ),
            "start_version": "7.05",
        },
    },
}

for k, v in ALL_WHM_ROTATIONS.items():
    all_whm_rotations.add_rotation_data(k, v)

