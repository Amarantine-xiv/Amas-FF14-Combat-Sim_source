from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_pct_rotations = SpecificRotations()

ALL_PCT_ROTATIONS = {
    "PCT": {
        90: {
            "stats": {
                "wd": 146,
                "main_stat": 4883,
                "det_stat": 2269,
                "crit_stat": 3140,
                "dh_stat": 1993,
                "speed_stat": 420,
                "job_class": "PCT",
            },
            "skills": (
                "Striking Muse",
                "Holy in White",                
                "Grade 2 Gemdraught",                
                "Pom Muse",
                "Wing Motif",
                "Starry Muse",
                "Hammer Stamp",
                "Subtractive Palette",
                "Blizzard in Cyan",
                "Stone in Yellow",
                "Thunder in Magenta",
                "Comet in Black",
                "Winged Muse",
                "Mog of the Ages",
                "Hammer Brush",                
                "Polishing Hammer",
                "Holy in White",
            ),
            "start_version": "7.05",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4883,
                "det_stat": 2269,
                "crit_stat": 3140,
                "dh_stat": 1993,
                "speed_stat": 420,
                "job_class": "PCT",
            },
            "skills": (
                "Rainbow Drip",
                "Striking Muse",
                "Holy in White",                
                "Grade 2 Gemdraught",                
                "Pom Muse",
                "Wing Motif",
                "Starry Muse",
                "Hammer Stamp",
                "Subtractive Palette",
                "Blizzard in Cyan",
                "Stone in Yellow",
                "Thunder in Magenta",
                "Comet in Black",
                "Winged Muse",
                "Mog of the Ages",
                "Star Prism",
                "Hammer Brush",                
                "Polishing Hammer",
                "Rainbow Drip",
                "Holy in White",                
                "Swiftcast",
                "Claw Motif",
                "Clawed Muse",
            ),
            "start_version": "7.05",
        }
    },
    "PCT 7.0": {
        100: {
            "stats": {
                "wd": 132,
                "main_stat": 3379,
                "det_stat": 1871,
                "crit_stat": 2514,
                "dh_stat": 1438,
                "speed_stat": 502,
                "job_class": "PCT",
            },
            "skills": (
                "Rainbow Drip",
                "Striking Muse",
                "Holy in White",                
                "Grade 2 Gemdraught",                
                "Pom Muse",
                "Wing Motif",
                "Starry Muse",
                "Hammer Stamp",
                "Subtractive Palette",
                "Blizzard in Cyan",
                "Stone in Yellow",
                "Thunder in Magenta",
                "Comet in Black",
                "Winged Muse",
                "Mog of the Ages",
                "Star Prism",
                "Hammer Brush",                
                "Polishing Hammer",
                "Rainbow Drip",
                "Holy in White",                
                "Swiftcast",
                "Claw Motif",
                "Clawed Muse",
            ),
            "start_version": "7.05",
        }
    },
}

for k, v in ALL_PCT_ROTATIONS.items():
    all_pct_rotations.add_rotation_data(k, v)
