from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_war_skills = SpecificSkills()

ALL_DATA = {
    "Heavy Swing": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 220}}},
    "Maim": {
        90: {"potency": {"6.55": 300}, "potency_no_combo": {"6.55": 150}},
        100: {"potency": {"7.0": 340}, "potency_no_combo": {"7.0": 190}},
    },
    "Storm's Path": {
        90: {"potency": {"6.55": 440}, "potency_no_combo": {"6.55": 160}},
        100: {"potency": {"7.0": 480}, "potency_no_combo": {"7.0": 200}},
    },
    "Storm's Eye": {
        90: {"potency": {"6.55": 440}, "potency_no_combo": {"6.55": 160}},
        100: {"potency": {"7.0": 480}, "potency_no_combo": {"7.0": 200}},
    },
    "Upheaval": {90: {"potency": {"6.55": 400}}, 100: {"potency": {"7.0": 400}}},
    "Onslaught": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Fell Cleave": {90: {"potency": {"6.55": 520}}, 100: {"potency": {"7.0": 580}}},
    "Primal Rend": {90: {"potency": {"6.55": 700}}, 100: {"potency": {"7.0": 700}}},
    "Inner Chaos": {90: {"potency": {"6.55": 660}}, 100: {"potency": {"6.55": 660}}},
    "Chaotic Cyclone": {90: {"potency": {"6.55": 320}}, 100: {"potency": {"7.0": 300}}},
    "Tomahawk": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Overpower": {90: {"potency": {"6.55": 110}}, 100: {"potency": {"7.0": 110}}},
    "Mythril Tempest": {
        90: {"potency": {"6.55": 150}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 140}, "potency_no_combo": {"7.0": 100}},
    },
    "Orogeny": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Decimate": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 180}}},
    "Vengeance": {90: {"potency": {"6.55": 55}}},
    "Primal Wrath": {
        100: {"potency": {"7.0": 700}},
    },
    "Primal Ruination": {
        100: {"potency": {"7.0": 740, "7.01": 780}}
    },
    "Damnation": {100: {"potency": {"7.0": 55}}},
}

for k, v in ALL_DATA.items():
    all_war_skills.add_skill_data(k, v)
