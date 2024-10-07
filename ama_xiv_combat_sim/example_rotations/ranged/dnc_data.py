from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_dnc_rotations = SpecificRotations()

ALL_DNC_ROTATIONS = {
    "DNC": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3379,
                "det_stat": 1952,
                "crit_stat": 2557,
                "dh_stat": 1380,
                "speed_stat": 436,
                "job_class": "DNC",
            },
            "skills": (
                "Grade 8 Tincture",
                "Technical Step",
                "Step Action",
                "Step Action",
                "Step Action",
                "Step Action",
                "Quadruple Technical Finish",
                "Devilment",
                "Starfall Dance",
                "Flourish",
                "Fan Dance III",
                "Tillana",
                "Fan Dance IV",
                "Fountainfall",
                "Fan Dance",
                "Fan Dance III",
                "Standard Step",
                "Step Action",
                "Step Action",
                "Double Standard Finish",
            ),
            "start_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4886,
                "det_stat": 2091,
                "crit_stat": 3177,
                "dh_stat": 2134,
                "speed_stat": 420,
                "job_class": "DNC",
            },
            "skills": (                
                "Standard Step",
                "Step Action",
                "Step Action",
                "Grade 2 Gemdraught",
                "Double Standard Finish",
                "Technical Step",
                "Step Action",
                "Step Action",
                "Step Action",
                "Step Action",
                "Quadruple Technical Finish",                
                "Devilment",
                "Tillana",
                "Flourish",
                "Dance of the Dawn",
                "Fan Dance IV",
                "Last Dance",
                "Fan Dance III",
                "Finishing Move",
                "Starfall Dance",
                "Fountainfall",
                "Reverse Cascade",
                "Fountainfall",
                "Reverse Cascade",
            ),
            "start_version": "7.05",
        },
    },
}

for k, v in ALL_DNC_ROTATIONS.items():
    all_dnc_rotations.add_rotation_data(k, v)
