from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_whm_skills = SpecificSkills()

ALL_DATA = {
    "Glare III": {90: {"potency": {"6.55": 310}},
                  100: {"potency": {"7.0": 330}}},
    "Glare IV": {100: {"potency": {"7.0": 640}}},
    "Assize": {90: {"potency": {"6.55": 400}},
               100: {"potency": {"7.0": 400}}},
    "Dia (dot)": {90: {"potency": {"6.55": 65}},
                  100: {"potency": {"7.0": 70, "7.05": 75}}},
    "Dia": {90: {"potency": {"6.55": 65}},
            100: {"potency": {"7.0": 70, "7.05": 75}}},
    "Afflatus Misery": {90: {"potency": {"6.55": 1240}},
                        100: {"potency": {"7.0": 1320}}},
    "Holy III": {90: {"potency": {"6.55": 150}},
                 100: {"potency": {"7.0": 150}}},
}

for k, v in ALL_DATA.items():
    all_whm_skills.add_skill_data(k, v)
