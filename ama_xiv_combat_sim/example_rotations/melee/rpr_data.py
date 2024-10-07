from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_rpr_rotations = SpecificRotations()

ALL_RPR_ROTATIONS = {
    "RPR": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3379,
                "det_stat": 1764,
                "crit_stat": 2567,
                "dh_stat": 1558,
                "speed_stat": 436,
                "job_class": "RPR",
            },
            "skills": (
                "Harpe",
                "Shadow of Death",
                "Grade 8 Tincture",
                "Soul Slice",
                "Arcane Circle",
                "Gluttony",
                "Gibbet",
                "Gallows",
                "Plentiful Harvest",
                "Enshroud",
                "Void Reaping",
                "Cross Reaping",
                "Lemure's Slice",
                "Void Reaping",
                "Cross Reaping",
                "Lemure's Slice",
                "Communio",
                "Soul Slice",
                "Unveiled Gibbet",
                "Gibbet",
            ),
            "start_version": "6.55",
            "end_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4883,
                "det_stat": 2150,
                "crit_stat": 3120,
                "dh_stat": 2078,
                "speed_stat": 474,
                "job_class": "RPR",
            },
            "skills": (
                "Harpe",
                "Shadow of Death",
                "Grade 2 Gemdraught",
                "Soul Slice",
                "Arcane Circle",
                "Gluttony",
                "Executioner's Gibbet",                
                "Executioner's Gallows",
                "Soul Slice",
                "Plentiful Harvest",
                "Enshroud",
                "Void Reaping",
                "Sacrificium",
                "Cross Reaping",
                "Lemure's Slice",
                "Void Reaping",
                "Cross Reaping",
                "Lemure's Slice",
                "Communio",
                "Perfectio",
                "Unveiled Gibbet",
                "Gibbet",
                "Shadow of Death",
                "Slice",
            ),
            "start_version": "7.05",            
        },
    },
}

for k, v in ALL_RPR_ROTATIONS.items():
    all_rpr_rotations.add_rotation_data(k, v)
