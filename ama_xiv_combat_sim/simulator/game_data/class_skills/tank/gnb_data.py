from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_gnb_skills = SpecificSkills()

ALL_DATA = {
    "Keen Edge": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 300}}},
    "Brutal Shell": {
        90: {"potency": {"6.55": 300}, "potency_no_combo": {"6.55": 160}},
        100: {"potency": {"7.0": 380}, "potency_no_combo": {"7.0": 240}},
    },
    "Demon Slice": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Lightning Shot": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Solid Barrel": {
        90: {"potency": {"6.55": 360}, "potency_no_combo": {"6.55": 140}},
        100: {"potency": {"7.0": 460}, "potency_no_combo": {"7.0": 240}},
    },
    "Burst Strike": {
        90: {"potency": {"6.55": 380, "7.4": 340}},
        100: {"potency": {"7.0": 460, "7.4": 420}},
    },
    "Demon Slaughter": {
        90: {"potency": {"6.55": 160}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 160}, "potency_no_combo": {"7.0": 100}},
    },
    "Sonic Break (dot)": {
        90: {
            "potency": {"6.55": 60, "7.4": 120},
            "duration": {"6.55": 30 * 1000, "7.4": 15 * 1000},
        },
        100: {
            "potency": {"7.0": 60, "7.4": 120},
            "duration": {"6.55": 30 * 1000, "7.4": 15 * 1000},
        },
    },
    "Sonic Break": {
        90: {"potency": {"6.55": 300, "7.4": 340}},
        100: {"potency": {"7.0": 300, "7.4": 340}},
    },
    "Rough Divide": {90: {"potency": {"6.55": 150}}},
    "Gnashing Fang": {
        90: {"potency": {"6.55": 380, "7.4": 330}},
        100: {"potency": {"7.0": 500, "7.4": 440}},
    },
    "Savage Claw": {
        90: {"potency": {"6.55": 460, "7.4": 410}},
        100: {"potency": {"7.0": 560, "7.4": 500}},
    },
    "Wicked Talon": {
        90: {"potency": {"6.55": 540, "7.4": 490}},
        100: {"potency": {"7.0": 620, "7.4": 560}},
    },
    "Bow Shock (dot)": {90: {"potency": {"6.55": 60}}, 100: {"potency": {"7.0": 60}}},
    "Bow Shock": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Jugular Rip": {
        90: {"potency": {"6.55": 200, "7.4": 180}},
        100: {"potency": {"7.0": 240, "7.4": 220}},
    },
    "Abdomen Tear": {
        90: {"potency": {"6.55": 240, "7.4": 220}},
        100: {"potency": {"7.0": 280, "7.4": 260}},
    },
    "Eye Gouge": {
        90: {"potency": {"6.55": 280, "7.4": 260}},
        100: {"potency": {"7.0": 320, "7.4": 300}},
    },
    "Fated Circle": {90: {"potency": {"6.55": 300}}, 100: {"potency": {"7.0": 300}}},
    "Blasting Zone": {90: {"potency": {"6.55": 720}}, 100: {"potency": {"7.0": 800}}},
    "Hypervelocity": {
        90: {"potency": {"6.55": 180, "7.1": 160, "7.4": 140}},
        100: {"potency": {"7.0": 220, "7.1": 200, "7.4": 180}},
    },
    "Double Down": {
        90: {"potency": {"6.55": 1200, "7.4": 1000}},
        100: {"potency": {"7.0": 1200, "7.4": 1000}},
    },
    "Fated Brand": {100: {"potency": {"7.0": 120}}},
    "Reign of Beasts": {100: {"potency": {"7.0": 800, "7.2": 1000, "7.4": 800}}},
    "Noble Blood": {100: {"potency": {"7.0": 1000, "7.2": 1100, "7.4": 900}}},
    "Lion Heart": {100: {"potency": {"7.0": 1200, "7.4": 1000}}},
}

for k, v in ALL_DATA.items():
    all_gnb_skills.add_skill_data(k, v)
