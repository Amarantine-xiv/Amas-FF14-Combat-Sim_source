from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_rdm_skills = SpecificSkills()

ALL_DATA = {
    "Riposte": {90: {"potency": {"6.55": 130}}, 100: {"potency": {"7.0": 130}}},
    "Corps-a-corps": {90: {"potency": {"6.55": 130}}, 100: {"potency": {"7.0": 130}}},
    "Verthunder II": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 140}}},
    "Veraero II": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 140}}},
    "Verfire": {90: {"potency": {"6.55": 340}}, 100: {"potency": {"7.0": 380}}},
    "Verstone": {90: {"potency": {"6.55": 340}}, 100: {"potency": {"7.0": 380}}},
    "Zwerchhau": {
        90: {"potency": {"6.55": 150}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 150}, "potency_no_combo": {"7.0": 100}},
    },
    "Displacement": {90: {"potency": {"6.55": 180}}, 100: {"potency": {"7.0": 180}}},
    "Engagement": {90: {"potency": {"6.55": 180}}, 100: {"potency": {"7.0": 180}}},
    "Fleche": {90: {"potency": {"6.55": 460}}, 100: {"potency": {"7.0": 480}}},
    "Redoublement": {
        90: {"potency": {"6.55": 230}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 230}, "potency_no_combo": {"7.0": 100}},
    },
    "Moulinet": {90: {"potency": {"6.55": 60}}, 100: {"potency": {"7.0": 60}}},
    "Contre Sixte": {
        90: {"potency": {"6.55": 380}},
        100: {"potency": {"7.0": 400, "7.05": 420}},
    },
    "Embolden": {
        90: {"duration": {"6.55": int(19.95 * 1000)}},
        100: {"duration": {"7.0": int(19.95 * 1000)}},
    },
    "Manafication": {
        90: {"duration": {"6.55": 15 * 1000}},
        100: {
            "duration": {
                "7.0": 15 * 1000,
                "7.01": 30 * 1000,
            },
        },
    },
    "Jolt II": {90: {"potency": {"6.55": 320}}, 100: {"potency": {"7.0": 280}}},
    "Jolt III": {90: {"potency": {"7.0": 360}},
                 100: {"potency": {"7.0": 360}}},
    "Impact": {
        90: {"potency": {"6.55": 210}, "potency_acceleration": {"6.55": 260}},
        100: {"potency": {"7.0": 210}, "potency_acceleration": {"7.0": 260}},
    },
    "Verflare": {
        90: {"potency": {"6.55": 600}},
        100: {"potency": {"7.0": 620, "7.1": 650}},
    },
    "Verholy": {
        90: {"potency": {"6.55": 600}},
        100: {"potency": {"7.0": 620, "7.1": 650}},
    },
    "Reprise": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Scorch": {
        90: {"potency": {"6.55": 680}},
        100: {"potency": {"7.0": 700, "7.1": 750}},
    },
    "Verthunder III": {
        90: {"potency": {"6.55": 380}},
        100: {"potency": {"7.0": 420, "7.05": 440}},
    },
    "Veraero III": {
        90: {"potency": {"6.55": 380}},
        100: {"potency": {"7.0": 420, "7.05": 440}},
    },
    "Resolution": {
        90: {"potency": {"6.55": 750}},
        100: {"potency": {"7.0": 800, "7.1": 850}},
    },
    "Vice of Thorns": {100: {"potency": {"7.0": 700, "7.2": 800}}},
    "Grand Impact": {100: {"potency": {"7.0": 600}}},
    "Prefulgence": {100: {"potency": {"7.0": 900, "7.2": 1000}}},
    "Enchanted Riposte": {
        90: {"potency": {"6.55": 280}},
        100: {"potency": {"7.0": 300}},
    },
    "Enchanted Zwerchhau": {
        90: {"potency": {"6.55": 340}, "potency_no_combo": {"6.55": 150}},
        100: {"potency": {"7.0": 360}, "potency_no_combo": {"7.0": 170}},
    },
    "Enchanted Redoublement": {
        90: {"potency": {"6.55": 500}, "potency_no_combo": {"6.55": 130}},
        100: {"potency": {"7.0": 540}, "potency_no_combo": {"7.0": 170}},
    },
    "Enchanted Moulinet": {
        90: {"potency": {"6.55": 130}},
        100: {"potency": {"7.0": 130}},
    },
    "Enchanted Moulinet Deux": {
        90: {"potency": {"7.0": 140}},
        100: {"potency": {"7.0": 140}},
    },
    "Enchanted Moulinet Trois": {
        90: {"potency": {"7.0": 150}},
        100: {"potency": {"7.0": 150}},
    },
    "Enchanted Reprise": {
        90: {"potency": {"6.55": 340}},
        100: {"potency": {"7.0": 380, "7.05": 420}},
    },
}

for k, v in ALL_DATA.items():
    all_rdm_skills.add_skill_data(k, v)
