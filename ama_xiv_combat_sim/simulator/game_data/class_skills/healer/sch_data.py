from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_sch_skills = SpecificSkills()

ALL_DATA = {
    "Broil IV": {
        90: {"potency": {"6.55": 295}},
        100: {"potency": {"7.0": 310, "7.3": 320}},
    },
    "Ruin II": {90: {"potency": {"6.55": 220}}, 100: {"potency": {"7.0": 220}}},
    "Energy Drain": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Art of War II": {90: {"potency": {"6.55": 180}}, 100: {"potency": {"7.0": 180}}},
    "Chain Stratagem": {
        90: {"duration": {"6.55": 15 * 1000, "7.0": 20 * 1000}},
        100: {"duration": {"7.0": 20 * 1000}},
    },
    "Biolysis (dot)": {
        90: {"potency": {"6.55": 70}},
        100: {"potency": {"7.0": 75, "7.2": 80}},
    },
    "Baneful Impaction (dot)": {100: {"potency": {"7.0": 140}}},
}

for k, v in ALL_DATA.items():
    all_sch_skills.add_skill_data(k, v)
