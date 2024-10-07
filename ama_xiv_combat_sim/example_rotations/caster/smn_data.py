from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_smn_rotations = SpecificRotations()

ALL_SMN_ROTATIONS = {
    "SMN": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3379,
                "det_stat": 1871,
                "crit_stat": 2514,
                "dh_stat": 1438,
                "speed_stat": 502,
                "job_class": "SMN",
            },
            "skills": (
                "Ruin III",
                "Summon Bahamut",
                "Searing Light",
                "Astral Impulse",
                "Grade 8 Tincture",
                "Astral Impulse",
                "Astral Impulse",
                "Energy Drain",
                "Enkindle Bahamut",
                "Astral Impulse",
                "Deathflare",
                "Fester",
                "Astral Impulse",
                "Fester",
                "Astral Impulse",
                "Summon Garuda II",
                "Swiftcast",
                "Slipstream",
                "Emerald Rite",
                "Emerald Rite",
                "Emerald Rite",
                "Emerald Rite",
                "Summon Titan II",
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
                "job_class": "SMN",
            },
            "skills": (
                "Ruin III",                
                "Summon Solar Bahamut",
                "Grade 2 Gemdraught",
                "Umbral Impulse",
                "Searing Light",
                "Umbral Impulse",
                "Umbral Impulse",
                "Energy Drain",
                "Umbral Impulse",
                "Exodus",
                "Necrotize",
                "Umbral Impulse",
                "Sunflare",
                "Necrotize",
                "Umbral Impulse",                
                "Searing Flash",
                "Summon Titan II",
                "Topaz Rite",
                "Mountain Buster",
                "Topaz Rite",
                "Mountain Buster",
                "Topaz Rite",
                "Mountain Buster",
                "Topaz Rite",
                "Mountain Buster",
                "Summon Garuda II",
                "Swiftcast",
                "Slipstream",
            ),
            "start_version": "7.05",            
        },
    },
}


for k, v in ALL_SMN_ROTATIONS.items():
    all_smn_rotations.add_rotation_data(k, v)
