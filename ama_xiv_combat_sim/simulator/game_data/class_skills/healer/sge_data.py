from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_sge_skills = SpecificSkills()

ALL_DATA = {
    "Dosis III": {
        90: {"potency": {"6.55": 330}},
        100: {"potency": {"7.0": 360, "7.1": 370}},
    },
    "Phlegma III": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Toxikon II": {
        90: {"potency": {"6.55": 330}},
        100: {"potency": {"7.0": 360, "7.1": 370}},
    },
    "Dyskrasia II": {90: {"potency": {"6.55": 170}}, 100: {"potency": {"7.0": 170}}},
    "Pneuma": {
        90: {"potency": {"6.55": 330}},
        100: {"potency": {"7.0": 360, "7.1": 370}},
    },
    "Eukrasian Dosis III (dot)": {
        90: {"potency": {"6.55": 75}, "potency_dysk": {"7.0": 40}},
        100: {"potency": {"7.0": 75, "7.2": 80}, "potency_dysk": {"7.0": 40}},
    },
    "Psyche": {100: {"potency": {"7.0": 600}}},
}

for k, v in ALL_DATA.items():
    all_sge_skills.add_skill_data(k, v)
