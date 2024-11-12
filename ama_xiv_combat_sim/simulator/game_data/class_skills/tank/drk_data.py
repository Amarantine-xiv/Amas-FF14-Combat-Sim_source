from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_drk_skills = SpecificSkills()

ALL_DATA = {
    "Hard Slash": {
        90: {"potency": {"6.55": 170, "7.05": 180}},
        100: {"potency": {"7.0": 260, "7.05": 300}},
    },
    "Syphon Strike": {
        90: {"potency": {"6.55": 260}, "potency_no_combo": {"6.55": 120}},
        100: {
            "potency": {"7.0": 360, "7.05": 380},
            "potency_no_combo": {"7.0": 220, "7.05": 240},
        },
    },
    "Unleash": {90: {"potency": {"6.55": 120}}, 100: {"potency": {"7.0": 120}}},
    "Unmend": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Souleater": {
        90: {
            "potency": {"6.55": 340, "7.05": 360},
            "potency_no_combo": {"6.55": 120, "7.05": 140},
        },
        100: {
            "potency": {"7.0": 460, "7.05": 480},
            "potency_no_combo": {"7.0": 240, "7.05": 260},
        },
    },
    "Flood of Shadow": {90: {"potency": {"6.55": 160}}, 100: {"potency": {"7.0": 160}}},
    "Stalwart Soul": {
        90: {"potency": {"6.55": 140}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 160}, "potency_no_combo": {"7.0": 120}},
    },
    "Edge of Shadow": {90: {"potency": {"6.55": 460}}, 100: {"potency": {"7.0": 460}}},
    "Salted Earth (dot)": {
        90: {"potency": {"6.55": 50}},
        100: {"potency": {"7.0": 50}},
    },
    "Salt and Darkness": {
        90: {"potency": {"6.55": 500}},
        100: {"potency": {"7.0": 500}},
    },
    "Plunge": {90: {"potency": {"6.55": 150}}},
    "Abyssal Drain": {90: {"potency": {"6.55": 240}}, 100: {"potency": {"7.0": 240}}},
    "Carve and Spit": {
        90: {"potency": {"6.55": 510}},
        100: {"potency": {"7.0": 510, "7.05": 540}},
    },
    "Bloodspiller": {90: {"potency": {"6.55": 500}}, 100: {"potency": {"7.0": 580, "7.1": 600}}},
    "Quietus": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 240}}},
    "Shadowbringer": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Living Shadow": {
        90: {
            "potency_base": {"6.55": 350, "7.0": 420},
            "potency_shadowbringer": {"6.55": 500, "7.0": 570},
        },
        100: {
            "potency_base": {"7.0": 420},
            "potency_shadowbringer": {"7.0": 570},
            "potency_disesteem": {"7.0": 620},
        },
    },
    "Scarlet Delirium": {100: {"potency": {"7.0": 600, "7.1": 620}}},
    "Comeuppance": {100: {"potency": {"7.0": 700, "7.1": 720}}},
    "Torcleaver": {100: {"potency": {"7.0": 800, "7.1": 820}}},
    "Impalement": {100: {"potency": {"7.0": 320}}},
    "Disesteem": {100: {"potency": {"7.0": 800, "7.05": 1000}}},
}

for k, v in ALL_DATA.items():
    all_drk_skills.add_skill_data(k, v)
