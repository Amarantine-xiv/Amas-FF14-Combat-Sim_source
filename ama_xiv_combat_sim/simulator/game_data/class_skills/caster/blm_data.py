from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_blm_skills = SpecificSkills()

ALL_DATA = {
    "Enochian": {
        90: {"damage_mult": {"6.55": 1.23}},
        100: {"damage_mult": {"7.0": 1.3, "7.05": 1.33}},
    },
    "Thunder III (dot)": {
        90: {"potency": {"6.55": 35}, "duration": {"6.55": 30 * 1000}},
        100: {"potency": {"7.0": 45, "7.05": 50}, "duration": {"7.0": 27 * 1000}},
    },
    "Thunder IV (dot)": {
        90: {"potency": {"6.55": 20}, "duration": {"6.55": 18 * 1000}},
        100: {"potency": {"7.0": 35}, "duration": {"7.0": 21 * 1000}},
    },
    "High Thunder (dot)": {
        100: {"potency": {"7.0": 55, "7.05": 60}, "duration": {"7.0": 30 * 1000}}
    },
    "High Thunder II (dot)": {
        100: {"potency": {"7.0": 40}, "duration": {"7.0": 24 * 1000}}
    },
    "Blizzard": {90: {"potency": {"6.55": 180}}, 100: {"potency": {"7.0": 180}}},
    "Fire": {90: {"potency": {"6.55": 180}}, 100: {"potency": {"7.0": 180}}},
    "Scathe": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Fire III": {90: {"potency": {"6.55": 260}}, 100: {"potency": {"7.0": 280}}},
    "Blizzard III": {90: {"potency": {"6.55": 260}}, 100: {"potency": {"7.0": 280}}},
    "Freeze": {90: {"potency": {"6.55": 120}}, 100: {"potency": {"7.0": 120}}},
    "Thunder III": {
        90: {"potency": {"6.55": 50}, "potency_thundercloud": {"6.55": 50 + 35 * 10}},
        100: {"potency": {"7.0": 160, "7.05": 120}},
    },
    "Flare": {
        90: {
            "potency": {"6.55": 220},
            "potency_enhanced": {"6.55": 280},
            "aoe_dropoff": {"6.55": 0.4},
        },
        100: {"potency": {"7.0": 240}, "aoe_dropoff": {"7.0": 0.4, "7.05": 0.3}},
    },
    "Blizzard IV": {
        90: {"potency": {"6.55": 310}},
        100: {"potency": {"7.0": 310, "7.05": 320}},
    },
    "Fire IV": {
        90: {"potency": {"6.55": 310}},
        100: {"potency": {"7.0": 310, "7.05": 320}},
    },
    "Thunder IV": {
        90: {"potency": {"6.55": 50}, "potency_thundercloud": {"6.55": 50 + 20 * 6}},
        100: {"potency": {"7.0": 80}},
    },
    "Foul": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Despair": {
        90: {"potency": {"6.55": 340}},
        100: {"potency": {"7.0": 340, "7.05": 350}},
    },
    "Xenoglossy": {90: {"potency": {"6.55": 880}}, 100: {"potency": {"7.0": 880}}},
    "High Fire II": {90: {"potency": {"6.55": 140}}, 100: {"potency": {"7.0": 100}}},
    "High Blizzard II": {
        90: {"potency": {"6.55": 140}},
        100: {"potency": {"7.0": 100}},
    },
    "Paradox": {
        90: {"potency": {"6.55": 500}},
        100: {"potency": {"7.0": 500, "7.05": 520}},
    },
    "High Thunder": {100: {"potency": {"7.0": 200, "7.05": 150}}},
    "High Thunder II": {100: {"potency": {"7.0": 100}}},
    "Flare Star": {100: {"potency": {"7.0": 400}}},
    "Firestarter": {
        90: {"allowlist": {"6.55": ("Fire",)}},
        100: {"allowlist": {"7.0": ("Fire III",)}},
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
