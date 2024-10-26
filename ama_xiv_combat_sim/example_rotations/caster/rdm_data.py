from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_rdm_rotations = SpecificRotations()

ALL_RDM_ROTATIONS = {
    "RDM": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3379,
                "det_stat": 1601,
                "crit_stat": 2514,
                "dh_stat": 1708,
                "speed_stat": 502,
                "job_class": "RDM",
            },
            "skills": (
                "Verthunder III",
                "Veraero III",
                "Swiftcast",
                "Acceleration",
                "Verthunder III",
                "Grade 8 Tincture",
                "Verthunder III",
                "Embolden",
                "Manafication",
                "Enchanted Riposte",
                "Fleche",
                "Enchanted Zwerchhau",
                "Contre Sixte",
                "Enchanted Redoublement",
                "Corps-a-corps",
                "Engagement",
                "Verholy",
                "Corps-a-corps",
                "Engagement",
                "Scorch",
                "Resolution",
                "Verfire",
                "Verthunder III",
                "Verstone",
                "Veraero III",
                "Jolt II",
                "Verthunder III",
                "Fleche",
            ),
            "start_version": "6.55",
            "end_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4883,
                "det_stat": 2108,
                "crit_stat": 3061,
                "dh_stat": 2125,
                "speed_stat": 528,
                "job_class": "RDM",
            },
            "skills": (
                "Veraero III",
                "Verthunder III",                
                "Swiftcast",
                "Grade 2 Gemdraught",
                "Verthunder III",
                "Fleche",
                "Acceleration",
                "Verthunder III",                
                "Embolden",
                "Manafication",                
                "Enchanted Riposte",
                "Contre Sixte",
                "Enchanted Zwerchhau",
                "Engagement",
                "Enchanted Redoublement",                
                "Corps-a-corps",
                "Verholy",
                "Vice of Thorns",
                "Scorch",
                "Engagement",
                "Corps-a-corps",                
                "Resolution",
                "Prefulgence",
                "Grand Impact",
                "Acceleration",
                "Verfire",
                "Grand Impact",                
                "Verthunder III",
                "Fleche",                
                "Veraero III",
                "Verfire",
                "Verthunder III",
                "Verstone",
                "Veraero III",
                "Swiftcast",
                "Veraero III",
                "Contre Sixte",
            ),
            "start_version": "7.05",
        }
    },
}

for k, v in ALL_RDM_ROTATIONS.items():
    all_rdm_rotations.add_rotation_data(k, v)