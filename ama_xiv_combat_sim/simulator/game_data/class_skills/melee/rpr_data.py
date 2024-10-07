from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_rpr_skills = SpecificSkills()

ALL_DATA = {
    "Enhanced Harpe": {
        90: {"duration": {"6.55": int(20 * 1000)}},
        100: {"duration": {"7.0": int(10 * 1000)}},
    },
    "Slice": {90: {"potency": {"6.55": 320}}, 100: {"potency": {"7.0": 420}}},
    "Waxing Slice": {
        90: {"potency": {"6.55": 400}, "potency_no_combo": {"6.55": 160}},
        100: {"potency": {"7.0": 500}, "potency_no_combo": {"7.0": 260}},
    },
    "Shadow of Death": {90: {"potency": {"6.55": 300}}, 100: {"potency": {"7.0": 300}}},
    "Harpe": {90: {"potency": {"6.55": 300}}, 100: {"potency": {"7.0": 300}}},
    "Spinning Scythe": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 160}}},
    "Infernal Slice": {
        90: {"potency": {"6.55": 500}, "potency_no_combo": {"6.55": 180}},
        100: {"potency": {"7.0": 600}, "potency_no_combo": {"7.0": 280}},
    },
    "Whorl of Death": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Nightmare Scythe": {
        90: {"potency": {"6.55": 180}, "potency_no_combo": {"6.55": 120}},
        100: {"potency": {"7.0": 200}, "potency_no_combo": {"7.0": 140}},
    },
    "Blood Stalk": {90: {"potency": {"6.55": 340}}, 100: {"potency": {"7.0": 340}}},
    "Grim Swathe": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 140}}},
    "Soul Slice": {
        90: {"potency": {"6.55": 460}},
        100: {"potency": {"7.0": 460, "7.05": 520}},
    },
    "Soul Scythe": {90: {"potency": {"6.55": 180}}, 100: {"potency": {"7.0": 180}}},
    "Enhanced Gibbet": {
        90: {"allowlist": {"6.55": ("Gibbet",)}},
        100: {"allowlist": {"7.0": ("Gibbet", "Executioner's Gibbet")}},
    },
    "Enhanced Gallows": {
        90: {"allowlist": {"6.55": ("Gallows",)}},
        100: {"allowlist": {"7.0": ("Gallows", "Executioner's Gallows")}},
    },
    "Gibbet": {
        90: {
            "potency": {"6.55": 460},
            "potency_no_pos": {"6.55": 400},
            "potency_gibbet": {"6.55": 520},
            "potency_no_pos_gibbet": {"6.55": 460},
        },
        100: {
            "potency": {"7.0": 560},
            "potency_no_pos": {"7.0": 500},
            "potency_gibbet": {"7.0": 620},
            "potency_no_pos_gibbet": {"7.0": 560},
        },
    },
    "Gallows": {
        90: {
            "potency": {"6.55": 460},
            "potency_no_pos": {"6.55": 400},
            "potency_gallows": {"6.55": 520},
            "potency_no_pos_gallows": {"6.55": 460},
        },
        100: {
            "potency": {"7.0": 560},
            "potency_no_pos": {"7.0": 500},
            "potency_gallows": {"7.0": 620},
            "potency_no_pos_gallows": {"7.0": 560},
        },
    },
    "Guillotine": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 200}}},
    "Unveiled Gibbet": {90: {"potency": {"6.55": 400}}, 100: {"potency": {"7.0": 440}}},
    "Unveiled Gallows": {
        90: {"potency": {"6.55": 400}},
        100: {"potency": {"7.0": 440}},
    },
    "Arcane Circle": {
        90: {"duration": {"6.55": int(19.98 * 1000)}},
        100: {"duration": {"7.0": int(19.98 * 1000)}},
    },
    "Gluttony": {90: {"potency": {"6.55": 520}}, 100: {"potency": {"7.0": 520}}},
    "Void Reaping": {
        90: {"potency": {"6.55": 460}, "potency_enhanced": {"6.55": 520}},
        100: {"potency": {"7.0": 500}, "potency_enhanced": {"7.0": 560}},
    },
    "Cross Reaping": {
        90: {"potency": {"6.55": 460}, "potency_enhanced": {"6.55": 520}},
        100: {"potency": {"7.0": 500}, "potency_enhanced": {"7.0": 560}},
    },
    "Grim Reaping": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 200}}},
    "Harvest Moon": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 800}}},
    "Lemure's Slice": {90: {"potency": {"6.55": 240}}, 100: {"potency": {"7.0": 280}}},
    "Lemure's Scythe": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Plentiful Harvest": {
        90: {"base_potency": {"6.55": 720}, "potency_increment": {"6.55": 40}},
        100: {"base_potency": {"7.0": 720}, "potency_increment": {"7.0": 40}},
    },
    "Communio": {90: {"potency": {"6.55": 1100}}, 100: {"potency": {"7.0": 1100}}},
    "Sacrificium": {100: {"potency": {"7.0": 530}}},
    "Executioner's Gibbet": {
        100: {
            "potency": {"7.0": 760},
            "potency_no_pos": {"7.0": 700},
            "potency_enhanced": {"7.0": 820},
            "potency_no_pos_enhanced": {"7.0": 760},
        },
    },
    "Executioner's Gallows": {
        100: {
            "potency": {"7.0": 760},
            "potency_no_pos": {"7.0": 700},
            "potency_enhanced": {"7.0": 820},
            "potency_no_pos_enhanced": {"7.0": 760},
        },
    },
    "Executioner's Guillotine": {100: {"potency": {"7.0": 300}}},
    "Perfectio": {100: {"potency": {"7.0": 1200, "7.05": 1300}}},
}

for k, v in ALL_DATA.items():
    all_rpr_skills.add_skill_data(k, v)
