from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_mch_rotations = SpecificRotations()

ALL_MCH_ROTATIONS = {
    "MCH": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3376,
                "det_stat": 2114,
                "crit_stat": 2557,
                "dh_stat": 1254,
                "speed_stat": 400,
                "job_class": "MCH",
            },
            "skills": (
                "Grade 8 Tincture",
                "Heated Split Shot",
                "Gauss Round",
                "Ricochet",
                "Drill",
                "Barrel Stabilizer",
                "Heated Slug Shot",
                "Ricochet",
                "Heated Clean Shot",
                "Reassemble",
                "Gauss Round",
                "Air Anchor",
                "Reassemble",
                "Wildfire",
                "Chain Saw",
                "Automaton Queen",
                "Hypercharge",
                "Heat Blast",
                "Ricochet",
                "Heat Blast",
                "Gauss Round",
                "Heat Blast",
                "Ricochet",
                "Heat Blast",
                "Gauss Round",
                "Heat Blast",
                "Ricochet",
                "Drill",
                "Ricochet",
                "Heated Split Shot",
                "Heated Slug Shot",
                "Heated Clean Shot",
            ),
            "start_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4883,
                "det_stat": 2091,
                "crit_stat": 3177,
                "dh_stat": 2134,
                "speed_stat": 420,
                "job_class": "MCH",
            },
            "skills": (
                "Reassemble",
                "Grade 2 Gemdraught",
                "Air Anchor",
                "Checkmate",
                "Double Check",
                "Drill",
                "Barrel Stabilizer",
                "Chain Saw",
                "Excavator",
                "Automaton Queen",
                "Reassemble",
                "Drill",
                "Checkmate",
                "Wildfire",
                "Full Metal Field",
                "Double Check",
                "Hypercharge",                
                "Blazing Shot",
                "Checkmate",
                "Blazing Shot",
                "Double Check",
                "Blazing Shot",
                "Checkmate",
                "Blazing Shot",
                "Double Check",
                "Blazing Shot",
                "Checkmate",
                "Drill",
                "Double Check",
                "Checkmate",                
                "Heated Split Shot",
                "Double Check",
                "Heated Slug Shot",
                "Heated Clean Shot",
            ),
            "start_version": "7.05",
        },
    },
}

for k, v in ALL_MCH_ROTATIONS.items():
    all_mch_rotations.add_rotation_data(k, v)
