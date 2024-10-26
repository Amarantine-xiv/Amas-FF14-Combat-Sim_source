from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_mch_skills = SpecificSkills()

ALL_DATA = {
    "Flamethrower (dot)": {
        90: {"potency": {"6.55": 80}},
        100: {"potency": {"7.0": 80}},
    },
    "Gauss Round": {90: {"potency": {"6.55": 130}}, 100: {"potency": {"7.0": 130}}},
    "Heat Blast": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 200}}},
    "Ricochet": {90: {"potency": {"6.55": 130}}, 100: {"potency": {"7.0": 130}}},
    "Auto Crossbow": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 160}}},
    "Heated Split Shot": {
        90: {"potency": {"6.55": 200}},
        100: {"potency": {"7.0": 220}},
    },
    "Drill": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Heated Slug Shot": {
        90: {"potency": {"6.55": 300}, "potency_no_combo": {"6.55": 120}},
        100: {"potency": {"7.0": 320}, "potency_no_combo": {"7.0": 140}},
    },
    "Heated Clean Shot": {
        90: {"potency": {"6.55": 380}, "potency_no_combo": {"6.55": 120}},
        100: {"potency": {"7.0": 400}, "potency_no_combo": {"7.0": 140}},
    },
    "Bioblaster (dot)": {90: {"potency": {"6.55": 50}}, 100: {"potency": {"7.0": 50}}},
    "Bioblaster": {90: {"potency": {"6.55": 50}}, 100: {"potency": {"7.0": 50}}},
    "Air Anchor": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Scattergun": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 160}}},
    "Chain Saw": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Blazing Shot": {100: {"potency": {"7.0": 220}}},
    "Checkmate": {100: {"potency": {"7.0": 160}}},
    "Double Check": {100: {"potency": {"7.0": 160}}},
    "Excavator": {100: {"potency": {"7.0": 600}}},
    "Full Metal Field": {100: {"potency": {"7.0": 700, "7.05": 900}}},
}

for k, v in ALL_DATA.items():
    all_mch_skills.add_skill_data(k, v)