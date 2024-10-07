from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations

all_ast_rotations = SpecificRotations()

ALL_AST_ROTATIONS = {
    "AST": {
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4883,
                "det_stat": 2831,
                "crit_stat": 3041,
                "dh_stat": 906,
                "speed_stat": 528,
                "job_class": "AST",
            },
            "skills": (
                "Earthly Star",
                "Fall Malefic",
                "Grade 2 Gemdraught",
                "Combust III",
                "Lightspeed",
                "Fall Malefic",
                "Fall Malefic",
                "Divination",
                "the Balance",
                "Fall Malefic",
                "Lord of Crowns",
                "Umbral Draw",
                "Fall Malefic",
                "the Spear",
                "Oracle",
                "Fall Malefic",
                "Fall Malefic",
                "Fall Malefic",
                "Fall Malefic",
                "Fall Malefic",
                "Combust III",
                "Fall Malefic",
            ),
            "start_version": "7.05",
        }
    },
}

for k, v in ALL_AST_ROTATIONS.items():
    all_ast_rotations.add_rotation_data(k, v)