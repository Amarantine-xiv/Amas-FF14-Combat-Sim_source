from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_ast_skills = SpecificSkills()

ALL_DATA = {
    "Divination": {
        90: {"duration": {"6.55": 15 * 1000, "7.0": 20 * 1000}},
        100: {"duration": {"7.0": 20 * 1000}},
    },
    "Fall Malefic": {90: {"potency": {"6.55": 250}}, 100: {"potency": {"7.0": 270}}},
    "Combust III (dot)": {
        90: {"potency": {"6.55": 55, "7.0": 65}},
        100: {"potency": {"7.0": 70}},
    },
    "Gravity II": {
        90: {"potency": {"6.55": 130, "7.2": 140}},
        100: {"potency": {"7.0": 130, "7.2": 140}},
    },
    "Macrocosmos": {
        90: {"potency": {"6.55": 250}},
        100: {"potency": {"7.0": 250, "7.01": 270}},
    },
    "Lord of Crowns": {
        90: {"potency": {"6.55": 250, "7.0": 400}},
        100: {"potency": {"7.0": 400}},
    },
    "Stellar Explosion (pet)": {
        90: {
            "Earthly Dominance": {"6.55": 205},
            "Giant Dominance": {"6.55": 310},
            "Earthly Dominance (Heal)": {"6.55": 540},
            "Giant Dominance (Heal)": {"6.55": 720},
        },
        100: {
            "Earthly Dominance": {"7.0": 205},
            "Giant Dominance": {"7.0": 310},
            "Earthly Dominance (Heal)": {"7.0": 540},
            "Giant Dominance (Heal)": {"7.0": 720},
        },
    },
    "Oracle": {
        100: {
            "potency": {"7.0": 860},
            "aoe_dropoff": {"7.0": 0, "7.2": 0.5},
        }
    },
    "Collective Unconscious": {
        90: {"duration": {"6.55": 5*1000, "7.4": 10*1000}},
        100: {"duration": {"7.0": 5*1000, "7.4": 10*1000}},
    },
}

for k, v in ALL_DATA.items():
    all_ast_skills.add_skill_data(k, v)
