from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_gnb_rotations = SpecificRotations()

ALL_GNB_ROTATIONS = {
    "GNB": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3311,
                "det_stat": 2182,
                "crit_stat": 2596,
                "dh_stat": 940,
                "speed_stat": 400,
                "tenacity": 601,
                "job_class": "GNB",
            },
            "skills": (
                "Keen Edge",
                "Grade 8 Tincture",
                "Brutal Shell",
                "No Mercy",
                "Bloodfest",
                "Gnashing Fang",
                "Jugular Rip",
                "Sonic Break",
                "Blasting Zone",
                "Bow Shock",
                "Double Down",
                "Rough Divide",
                "Savage Claw",
                "Abdomen Tear",
                "Rough Divide",
                "Wicked Talon",
                "Eye Gouge",
                "Solid Barrel",
                "Burst Strike",
                "Hypervelocity",
                "Keen Edge",
            ),
            "start_version": "6.55",
            "end_version": "6.55",
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
                "job_class": "GNB",
            },
            "skills": (
                "Lightning Shot",
                "Bloodfest",
                "Keen Edge",                
                "Grade 2 Gemdraught",                
                "Brutal Shell",                
                "No Mercy",
                "Sonic Break",
                "Bow Shock",
                "Double Down",
                "Blasting Zone",
                "Gnashing Fang",
                "Jugular Rip",
                "Savage Claw",
                "Abdomen Tear",
                "Wicked Talon",
                "Eye Gouge",
                "Reign of Beasts",
                "Noble Blood",
                "Lion Heart",
            ),
            "start_version": "7.05",
        },
    },
}

for k, v in ALL_GNB_ROTATIONS.items():
    all_gnb_rotations.add_rotation_data(k, v)
