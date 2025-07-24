from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_blm_skills = SpecificSkills()

ALL_DATA = {
    "Ley Lines": {
        90: {
            "duration": {"6.55": 30 * 1000, "7.2": 20 * 1000},
        },
        100: {
            "duration": {"7.0": 30 * 1000, "7.2": 20 * 1000},
        },
    },
    "Enochian": {
        90: {
            "damage_mult": {"6.55": 1.23, "7.05": 1.25, "7.2": 1.22},
            "duration": {"6.55": 15 * 1000, "7.2": float("inf")},
        },
        100: {
            "damage_mult": {"7.0": 1.3, "7.05": 1.33, "7.1": 1.32, "7.2": 1.27},
            "duration": {"6.55": 15 * 1000, "7.2": float("inf")},
        },
    },
    "Thunder III": {
        90: {
            "potency": {"6.55": 50, "7.0": 120},
            "potency_thundercloud": {"6.55": 50 + 35 * 10},
            "cast_time": {"6.55": 2500, "7.0": 0},
        },
        100: {
            "potency": {"7.0": 160, "7.05": 120},
            "cast_time": {"6.55": 2500, "7.0": 0},
        },
    },
    "Thunder III (dot)": {
        90: {
            "potency": {"6.55": 35, "7.0": 50},
            "duration": {"6.55": 30 * 1000, "7.0": 27 * 1000},
        },
        100: {"potency": {"7.0": 45, "7.05": 50}, "duration": {"7.0": 27 * 1000}},
    },
    "Thunder IV": {
        90: {
            "potency": {"6.55": 50, "7.0": 80},
            "potency_thundercloud": {"6.55": 50 + 20 * 6},
            "cast_time": {"6.55": 2500, "7.0": 0},
        },
        100: {"potency": {"7.0": 80}, "cast_time": {"7.0": 0}},
    },
    "Thunder IV (dot)": {
        90: {
            "potency": {"6.55": 20, "7.0": 35},
            "duration": {"6.55": 18 * 1000, "7.0": 21 * 1000},
        },
        100: {"potency": {"7.0": 35}, "duration": {"7.0": 21 * 1000}},
    },
    "High Thunder (dot)": {
        100: {"potency": {"7.0": 55, "7.05": 60}, "duration": {"7.0": 30 * 1000}}
    },
    "High Thunder II (dot)": {
        100: {"potency": {"7.0": 40}, "duration": {"7.0": 24 * 1000}}
    },
    "Blizzard": {
        90: {"potency": {"6.55": 180}, "cast_time": {"6.55": 2500, "7.2": 2000}},
        100: {"potency": {"7.0": 180}, "cast_time": {"7.0": 2500, "7.2": 2000}},
    },
    "Fire": {
        90: {"potency": {"6.55": 180}, "cast_time": {"6.55": 2500, "7.2": 2000}},
        100: {"potency": {"7.0": 180}, "cast_time": {"6.55": 2500, "7.2": 2000}},
    },
    "Scathe": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Fire III": {
        90: {"potency": {"6.55": 260, "7.0": 280, "7.2": 290},
             "cast_time": {"6.55": 3500}},
        100: {"potency": {"7.0": 280, "7.2": 290},
              "cast_time": {"7.0": 3500}},
    },
    "Blizzard III": {
        90: {"potency": {"6.55": 260, "7.0": 280, "7.2": 290},
             "cast_time": {"6.55": 3500}},
        100: {"potency": {"7.0": 280, "7.2": 290},
              "cast_time": {"7.0": 3500}},
    },
    "Freeze": {
        90: {"potency": {"6.55": 120}, "cast_time": {"6.55": 2800, "7.2": 2000}},
        100: {"potency": {"7.0": 120}, "cast_time": {"7.0": 2800, "7.2": 2000}},
    },
    "Flare": {
        90: {
            "potency": {"6.55": 220, "7.0": 240},
            "potency_enhanced": {"6.55": 280},
            "aoe_dropoff": {"6.55": 0.4, "7.05": 0.3},
            "cast_time": {"6.55": 4000, "7.1": 3000, "7.2": 2000},
        },
        100: {
            "potency": {"7.0": 240},
            "aoe_dropoff": {"7.0": 0.4, "7.05": 0.3},
            "cast_time": {"7.0": 4000, "7.1": 3000, "7.2": 2000},
        },
    },
    "Blizzard IV": {
        90: {
            "potency": {"6.55": 310, "7.05": 320, "7.2": 300},
            "cast_time": {"6.55": 2500, "7.2": 2000},
        },
        100: {
            "potency": {"7.0": 310, "7.05": 320, "7.2": 300},
            "cast_time": {"7.0": 2500, "7.2": 2000},
        },
    },
    "Fire IV": {
        90: {
            "potency": {"6.55": 310, "7.05": 320},
            "cast_time": {"6.55": 2800, "7.2": 2000},
        },
        100: {
            "potency": {"7.0": 310, "7.05": 320, "7.2": 300},
            "cast_time": {"7.0": 2800, "7.2": 2000},
        },
    },
    "Foul": {
        90: {
            "potency": {"6.55": 600},
            "aoe_dropoff": {"6.55": 0.6, "7.2": 0.25},
        },
        100: {
            "potency": {"7.0": 600},
            "aoe_dropoff": {"7.0": 0.6, "7.2": 0.25},
        },
    },
    "Despair": {
        90: {"potency": {"6.55": 340, "7.05": 350}, "cast_time": {"6.55": 3000, "7.2": 2000}},
        100: {
            "potency": {"7.0": 340, "7.05": 350},
            "cast_time": {"7.0": 3000, "7.1": 0},
        },
    },
    "Xenoglossy": {90: {"potency": {"6.55": 880}}, 100: {"potency": {"7.0": 880, "7.2": 890}}},
    "High Fire II": {
        90: {"potency": {"6.55": 140, "7.0": 100}},
        100: {"potency": {"7.0": 100}},
    },
    "High Blizzard II": {
        90: {"potency": {"6.55": 140, "7.0": 100}},
        100: {"potency": {"7.0": 100}},
    },
    "Paradox": {
        90: {"potency": {"6.55": 500, "7.05": 520, "7.2": 540}},
        100: {"potency": {"7.0": 500, "7.05": 520, "7.2": 540}},
    },
    "High Thunder": {100: {"potency": {"7.0": 200, "7.05": 150}}},
    "High Thunder II": {100: {"potency": {"7.0": 100}}},
    "Flare Star": {100: {"potency": {"7.0": 400, "7.2": 500}, 
                         "cast_time": {"7.0": 3000, "7.2": 2000},}},
    "Firestarter": {
        90: {
            "allowlist": {"6.55": ("Fire",)},
            "duration": {"6.55": 30 * 1000, "7.2": float("inf")},
        },
        100: {
            "allowlist": {"7.0": ("Fire III",)},
            "duration": {"7.0": 30 * 1000, "7.2": float("inf")},
        },
    },
    "Astral Fire": {
        90: {
            "allowlist": {
                "6.55": (
                    "Blizzard",
                    "Transpose",
                    "Fire",
                    "Fire III",
                    "Fire IV",
                    "Blizzard IV",
                    "Blizzard III",
                    "Flare",
                    "Despair",
                    "High Fire II",
                    "High Blizzard II",
                    "Paradox",
                )
            },
            "duration": {"6.55": 15 * 1000, "7.2": float("inf")},
        },
        100: {
            "allowlist": {
                "7.0": (
                    "Blizzard",
                    "Transpose",
                    "Fire",
                    "Fire III",
                    "Fire IV",
                    "Blizzard IV",
                    "Blizzard III",
                    "Flare",
                    "Despair",
                    "High Fire II",
                    "High Blizzard II",
                    "Paradox",
                    "Manafont",
                    "Flare Star",
                )
            },
            "duration": {"7.0": 15 * 1000, "7.2": float("inf")},
        },
    },
    "Umbral Ice": {
        90: {
            "allowlist": {
                "6.55": (
                    "Blizzard",
                    "Transpose",
                    "Fire",
                    "Fire III",
                    "Fire IV",
                    "Blizzard IV",
                    "Blizzard III",
                    "Flare",
                    "Despair",
                    "High Fire II",
                    "High Blizzard II",
                    "Paradox",
                )
            }
        },
        100: {
            "allowlist": {
                "7.0": (
                    "Blizzard",
                    "Transpose",
                    "Fire",
                    "Fire III",
                    "Fire IV",
                    "Blizzard IV",
                    "Blizzard III",
                    "Flare",
                    "Despair",
                    "High Fire II",
                    "High Blizzard II",
                    "Paradox",
                    "Manafont",
                    "Flare Star",
                )
            }
        },
    },
}

for k, v in ALL_DATA.items():
    all_blm_skills.add_skill_data(k, v)
