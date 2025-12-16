from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_whm_skills = SpecificSkills()

ALL_DATA = {
    "Glare III": {
        90: {"potency": {"6.55": 310}},
        100: {"potency": {"7.0": 330, "7.1": 340, "7.4": 350}},
    },
    "Glare IV": {100: {"potency": {"7.0": 640}}},
    "Assize": {90: {"potency": {"6.55": 400}}, 100: {"potency": {"7.0": 400}}},
    "Dia (dot)": {
        90: {"potency": {"6.55": 65}},
        100: {"potency": {"7.0": 70, "7.05": 75, "7.2": 80, "7.3": 85}},
    },
    "Dia": {
        90: {"potency": {"6.55": 65}},
        100: {"potency": {"7.0": 70, "7.05": 75, "7.2": 80, "7.3": 85}},
    },
    "Afflatus Misery": {
        90: {"potency": {"6.55": 1240}},
        100: {"potency": {"7.0": 1320, "7.1": 1360, "7.4": 1400}},
    },
    "Holy III": {
        90: {"potency": {"6.55": 150}, "cast time": {"6.55": 2500, "7.1": 1500}},
        100: {"potency": {"7.0": 150}, "cast time": {"7.0": 2500, "7.1": 1500}},
    },
    "Plenary Indulgence": {
        90: {"damage_reduction": {"6.55": 0.0, "7.4": 0.1}},
        100: {"damage_reduction": {"7.0": 0.0, "7.4": 0.1}},
    },
}

for k, v in ALL_DATA.items():
    all_whm_skills.add_skill_data(k, v)
