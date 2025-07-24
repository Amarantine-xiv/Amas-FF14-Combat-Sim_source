from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_pld_skills = SpecificSkills()

ALL_DATA = {
    "Fast Blade": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 220}}},
    "Riot Blade": {
        90: {"potency": {"6.55": 300}, "potency_no_combo": {"6.55": 140}},
        100: {"potency": {"7.0": 330}, "potency_no_combo": {"7.0": 170}},
    },
    "Total Eclipse": {
        90: {"potency": {"6.55": 100, "7.2": 120}},
        100: {"potency": {"7.0": 100, "7.2": 120}},
    },
    "Shield Bash": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Shield Lob": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Prominence": {
        90: {"potency": {"6.55": 170, "7.2": 220}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 170, "7.2": 220}, "potency_no_combo": {"7.0": 100}},
    },
    "Circle of Scorn (dot)": {
        90: {"potency": {"6.55": 30}},
        100: {"potency": {"7.0": 30}},
    },
    "Circle of Scorn": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 140}}},
    "Goring Blade": {90: {"potency": {"6.55": 700}}, 100: {"potency": {"7.0": 700}}},
    "Royal Authority": {
        90: {"potency": {"6.55": 400}, "potency_no_combo": {"6.55": 140}},
        100: {
            "potency": {"7.0": 440, "7.05": 460},
            "potency_no_combo": {"7.0": 180, "7.05": 200},
        },
    },
    "Holy Spirit": {
        90: {
            "potency": {"6.55": 350},
            "potency_divine_might": {"6.55": 450},
            "potency_req": {"6.55": 650},
            "potency_divine_might_req": {"6.55": 450},
        },
        100: {
            "potency": {"7.0": 370, "7.05": 400},
            "potency_divine_might": {"7.0": 470, "7.05": 500},
            "potency_req": {"7.0": 670, "7.05": 700},
            "potency_divine_might_req": {"7.0": 470, "7.05": 500},
        },
    },
    "Requiescat": {
        90: {"potency": {"6.55": 320}},
        100: {"potency": {"7.0": 320}},
    },
    "Holy Circle": {
        90: {
            "potency": {"6.55": 100},
            "potency_divine_might": {"6.55": 200, "7.2": 250},
            "potency_req": {"6.55": 300, "7.2": 350},
            "potency_divine_might_req": {"6.55": 200, "7.2": 250},
        },
        100: {
            "potency": {"7.0": 100},
            "potency_divine_might": {"7.0": 200, "7.2": 250},
            "potency_req": {"7.0": 300, "7.2": 350},
            "potency_divine_might_req": {"7.0": 200, "7.2": 250},
        },
    },
    "Intervene": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Atonement": {
        90: {"potency": {"6.55": 400}},
        100: {"potency": {"7.0": 440, "7.05": 460}},
    },
    "Supplication": {
        90: {"potency": {"7.0": 420, "7.05": 460}},
        100: {"potency": {"7.0": 460, "7.05": 500}},
    },
    "Sepulchre": {
        90: {"potency": {"7.0": 380, "7.05": 440}},
        100: {"potency": {"7.0": 480, "7.05": 540}},
    },
    "Confiteor": {
        90: {
            "potency": {"6.55": 420},
            "potency_req": {"6.55": 920},
            "aoe_dropoff": {"6.55": 0.5, "7.2": 0.6},
        },
        100: {
            "potency": {"7.0": 440, "7.05": 500},
            "potency_req": {
                "7.0": 940,
                "7.05": 1000,
            },
            "aoe_dropoff": {"7.0": 0.5, "7.2": 0.6},
        },
    },
    "Expiacion": {
        90: {"potency": {"6.55": 450}},
        100: {"potency": {"7.0": 450}},
    },
    "Blade of Faith": {
        90: {
            "potency": {"6.55": 220},
            "potency_req": {"6.55": 720},
            "aoe_dropoff": {"6.55": 0.5, "7.2": 0.6},
        },
        100: {
            "potency": {"7.0": 240, "7.05": 260},
            "potency_req": {"7.0": 740, "7.05": 760},
            "aoe_dropoff": {"7.0": 0.5, "7.2": 0.6},
        },
    },
    "Blade of Truth": {
        90: {
            "potency": {"6.55": 320},
            "potency_req": {"6.55": 820},
            "aoe_dropoff": {"6.55": 0.5, "7.2": 0.6},
        },
        100: {
            "potency": {"7.0": 340, "7.05": 380},
            "potency_req": {"7.0": 840, "7.05": 880},
            "aoe_dropoff": {"7.0": 0.5, "7.2": 0.6},
        },
    },
    "Blade of Valor": {
        90: {
            "potency": {"6.55": 420},
            "potency_req": {"6.55": 920},
            "aoe_dropoff": {"6.55": 0.5, "7.2": 0.6},
        },
        100: {
            "potency": {"7.0": 440, "7.05": 500},
            "potency_req": {"7.0": 940, "7.05": 1000},
            "aoe_dropoff": {"7.0": 0.5, "7.2": 0.6},
        },
    },
    "Blade of Honor": {
        100: {"potency": {"7.0": 1000}, "aoe_dropoff": {"7.0": 0.5, "7.2": 0.6}},
    },
    "Imperator": {
        100: {"potency": {"7.0": 580}, "aoe_dropoff": {"7.0": 0.5, "7.2": 0.6}}
    },
}

for k, v in ALL_DATA.items():
    all_pld_skills.add_skill_data(k, v)
