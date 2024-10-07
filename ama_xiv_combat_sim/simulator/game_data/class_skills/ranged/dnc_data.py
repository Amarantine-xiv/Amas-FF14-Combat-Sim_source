from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_dnc_skills = SpecificSkills()

ALL_DATA = {
    "Cascade": {90: {"potency": {"6.55": 220}}, 100: {"potency": {"7.0": 220}}},
    "Fountain": {
        90: {"potency": {"6.55": 280}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 280}, "potency_no_combo": {"7.0": 120}},
    },
    "Windmill": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Standard Finish": {
        90: {"Double": {"6.55": 720}, "Single": {"6.55": 540}, "Zero": {"6.55": 360}},
        100: {"Double": {"7.0": 850}, "Single": {"7.0": 540}, "Zero": {"7.0": 360}},
    },
    "Reverse Cascade": {90: {"potency": {"6.55": 280}}, 100: {"potency": {"7.0": 280}}},
    "Bladeshower": {
        90: {"potency": {"6.55": 140}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 140}, "potency_no_combo": {"7.0": 100}},
    },
    "Fan Dance": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Rising Windmill": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 140}}},
    "Fountainfall": {90: {"potency": {"6.55": 340}}, 100: {"potency": {"7.0": 340}}},
    "Bloodshower": {90: {"potency": {"6.55": 180}}, 100: {"potency": {"7.0": 180}}},
    "Fan Dance II": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Fan Dance III": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 200}}},
    "Technical Finish": {
        90: {
            "Quadruple": {"6.55": 1200},
            "Triple": {"6.55": 900},
            "Double": {"6.55": 720},
            "Single": {"6.55": 540},
        },
        100: {
            "Quadruple": {"7.0": 1300},
            "Triple": {"7.0": 900},
            "Double": {"7.0": 720},
            "Single": {"7.0": 540},
        },
    },
    "Saber Dance": {90: {"potency": {"6.55": 480}}, 100: {"potency": {"7.0": 520}}},
    "Tillana": {90: {"potency": {"6.55": 360}}, 100: {"potency": {"7.0": 600}}},
    "Finishing Move": {100: {"potency": {"7.0": 850}}},
    "Fan Dance IV": {
        90: {"potency": {"6.55": 300}},
        100: {"potency": {"7.0": 300, "7.05": 420}},
    },
    "Starfall Dance": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Last Dance": {100: {"potency": {"7.0": 520}}},
    "Dance of the Dawn": {100: {"potency": {"7.0": 1000}}},
}

for k, v in ALL_DATA.items():
    all_dnc_skills.add_skill_data(k, v)
