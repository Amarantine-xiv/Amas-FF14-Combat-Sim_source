from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_brd_rotations = SpecificRotations()

ALL_BRD_ROTATIONS = {
    "BRD": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3379,
                "det_stat": 1885,
                "crit_stat": 2598,
                "dh_stat": 1344,
                "speed_stat": 479,
                "job_class": "BRD",
            },
            "skills": (
                "Grade 8 Tincture",
                "Stormbite",
                "The Wanderer's Minuet",
                "Raging Strikes",
                "Caustic Bite",
                "Empyreal Arrow",
                "Bloodletter",
                "Refulgent Arrow",
                "Radiant Finale",
                "Battle Voice",
                "Refulgent Arrow",
                "Sidewinder",
                "Refulgent Arrow",
                "Barrage",
                "Refulgent Arrow",
                "Burst Shot",
                "Refulgent Arrow",
                "Empyreal Arrow",
                "Iron Jaws",
                "Pitch Perfect",
            ),
            "start_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4886,
                "det_stat": 2091,
                "crit_stat": 3177,
                "dh_stat": 2080,
                "speed_stat": 474,
                "job_class": "BRD",
            },
            "skills": (                                
                "Stormbite",
                "The Wanderer's Minuet",
                "Empyreal Arrow",
                "Caustic Bite",
                "Wait 0.90s",
                "Battle Voice",
                "Burst Shot",
                "Radiant Finale",
                "Raging Strikes",
                "Burst Shot",
                "Heartbreak Shot",
                "Radiant Encore",
                "Barrage",
                "Refulgent Arrow",
                "Sidewinder",
                "Resonant Arrow",
                "Empyreal Arrow",
                "Refulgent Arrow",
                "Burst Shot",
                "Iron Jaws",
                "Heartbreak Shot",
                "Burst Shot",                
                "Pitch Perfect",
            ),
            "start_version": "7.05",
        },
    },
   
}

for k, v in ALL_BRD_ROTATIONS.items():
    all_brd_rotations.add_rotation_data(k, v)

