from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_smn_skills = SpecificSkills()

ALL_DATA = {
    "Fester": {70: {"potency": {"7.5": 340}}, 90: {"potency": {"6.55": 340}}},
    "Energy Drain": {
        70: {"potency": {"7.5": 200}},
        90: {"potency": {"6.55": 200}},
        100: {"potency": {"7.0": 200}},
    },
    "Painflare": {
        70: {"potency": {"7.5": 220}},
        90: {"potency": {"6.55": 150, "7.5": 220}},
        100: {"potency": {"7.0": 150, "7.5": 220}},
    },
    "Energy Siphon": {
        70: {"potency": {"6.55": 100}},
        90: {"potency": {"6.55": 100}},
        100: {"potency": {"7.0": 100}},
    },
    "Ruby Ruin III": {
        70: {"potency": {"7.5": 410}},
    },
    "Topaz Ruin III": {
        70: {"potency": {"7.5": 300}},
    },
    "Emerald Ruin III": {
        70: {"potency": {"7.5": 180}},
    },
    "Ruby Outburst": {
        70: {"potency": {"7.5": 160}},
    },
    "Topaz Outburst": {
        70: {"potency": {"7.5": 110}},
    },
    "Emerald Outburst": {
        70: {"potency": {"7.5": 70}},
    },
    "Ruin III": {
        70: {"potency": {"7.5": 300}, "potency_aethercharge": {"7.5": 350}},
        90: {"potency": {"6.55": 310}, "potency_aethercharge": {"6.55": 360}},
        100: {
            "potency": {"7.0": 360, "7.3": 400},
            "potency_aethercharge": {"7.0": 410, "7.3": 450},
        },
    },
    "Astral Impulse": {
        70: {"potency": {"7.5": 440}},
        90: {"potency": {"6.55": 440}},
        100: {"potency": {"7.0": 500}},
    },
    "Astral Flare": {
        70: {"potency": {"7.5": 180}},
        90: {"potency": {"6.55": 180}},
        100: {"potency": {"7.0": 180}},
    },
    "Deathflare": {
        70: {
            "potency": {"7.0": 500},
            "aoe_dropoff": {"7.5": 0.5},
        },
        90: {
            "potency": {"6.55": 500},
            "aoe_dropoff": {"6.55": 0.6, "7.25": 0.5},
        },
        100: {
            "potency": {"7.0": 500},
            "aoe_dropoff": {"7.0": 0.6, "7.25": 0.5},
        },
    },
    "Ruin IV": {
        70: {"potency": {"7.5": 430}},
        90: {"potency": {"6.55": 430}},
        100: {"potency": {"7.0": 490, "7.3": 520}},
    },
    "Searing Light": {
        70: {"damage_mult": {"7.5": 1.05}, "duration": {"7.5": 20 * 1000}},
        90: {
            "damage_mult": {"6.55": 1.03, "7.0": 1.05},
            "duration": {"6.55": 30 * 1000, "7.0": 20 * 1000},
        },
        100: {"damage_mult": {"6.55": 1.05}, "duration": {"6.55": 20 * 1000}},
    },
    "Akh Morn (pet)": {
        70: {
            "potency": {"6.55": 1300},
            "aoe_dropoff": {"7.5": 0.5},
        },
        90: {
            "potency": {"6.55": 1300},
            "aoe_dropoff": {"6.55": 0.6, "7.25": 0.5},
        },
        100: {
            "potency": {"7.0": 1300},
            "aoe_dropoff": {"7.0": 0.6, "7.25": 0.5},
        },
    },
    "Ruby Rite": {
        90: {"potency": {"6.55": 510}},
        100: {"potency": {"7.0": 540, "7.3": 580, "7.5": 620}},
    },
    "Topaz Rite": {90: {"potency": {"6.55": 330}}, 100: {"potency": {"7.0": 340}}},
    "Emerald Rite": {
        90: {"potency": {"6.55": 230}},
        100: {"potency": {"7.0": 240, "7.3": 280}},
    },
    "Outburst": {70: {"potency": {"7.5": 100}}},
    "Tri-disaster": {90: {"potency": {"6.55": 120}}, 100: {"potency": {"7.0": 120}}},
    "Fountain of Fire": {
        90: {"potency": {"6.55": 540}},
        100: {"potency": {"7.0": 580}},
    },
    "Brand of Purgatory": {
        90: {"potency": {"6.55": 240}},
        100: {"potency": {"7.0": 240}},
    },
    "Revelation (pet)": {
        90: {"potency": {"6.55": 1300}, "aoe_dropoff": {"6.55": 0.6, "7.25": 0.5}},
        100: {"potency": {"7.0": 1300}, "aoe_dropoff": {"7.0": 0.6, "7.25": 0.5}},
    },
    "Ruby Catastrophe": {
        90: {"potency": {"6.55": 210}},
        100: {"potency": {"7.0": 210}},
    },
    "Topaz Catastrophe": {
        90: {"potency": {"6.55": 140}},
        100: {"potency": {"7.0": 140}},
    },
    "Emerald Catastrophe": {
        90: {"potency": {"6.55": 100}},
        100: {"potency": {"7.0": 100}},
    },
    "Crimson Cyclone": {
        90: {"potency": {"6.55": 430}, "aoe_dropoff": {"6.55": 0.65, "7.3": 0.6}},
        100: {
            "potency": {"7.0": 490, "7.3": 520, "7.5": 560},
            "aoe_dropoff": {"7.0": 0.65, "7.3": 0.6},
        },
    },
    "Crimson Strike": {
        90: {"potency": {"6.55": 430}, "aoe_dropoff": {"6.55": 0.65, "7.3": 0.6}},
        100: {
            "potency": {"7.0": 490, "7.3": 520, "7.5": 560},
            "aoe_dropoff": {"7.0": 0.65, "7.3": 0.6},
        },
    },
    "Mountain Buster": {
        90: {
            "potency": {"6.55": 150},
            "aoe_dropoff": {"6.55": 0.7, "7.3": 0.6},
        },
        100: {
            "potency": {"7.0": 160},
            "aoe_dropoff": {"7.0": 0.7, "7.3": 0.6},
        },
    },
    "Slipstream (dot)": {90: {"potency": {"6.55": 30}}, 100: {"potency": {"7.0": 30}}},
    "Slipstream": {
        90: {"potency": {"6.55": 430}, "aoe_dropoff": {"6.55": 0.65, "7.3": 0.6}},
        100: {
            "potency": {"7.0": 490, "7.3": 520},
            "aoe_dropoff": {"7.0": 0.65, "7.3": 0.6},
        },
    },
    "Inferno 1 (pet)": {
        70: {"potency": {"7.5": 600}, "aoe_dropoff": {"7.5": 0.5}},
    },
    "Inferno (pet)": {
        90: {"potency": {"6.55": 750}, "aoe_dropoff": {"6.55": 0.6, "7.3": 0.5}},
        100: {
            "potency": {"7.0": 750, "7.1": 800},
            "aoe_dropoff": {"7.0": 0.6, "7.3": 0.5},
        },
    },
    "Earthen Fury 1 (pet)": {
        70: {"potency": {"7.5": 600}, "aoe_dropoff": {"7.5": 0.5}},
    },
    "Earthen Fury (pet)": {
        90: {"potency": {"6.55": 750}, "aoe_dropoff": {"6.55": 0.6, "7.3": 0.5}},
        100: {
            "potency": {"7.0": 750, "7.1": 800},
            "aoe_dropoff": {"7.0": 0.6, "7.3": 0.5},
        },
    },
    "Aerial Blast 1 (pet)": {
        70: {"potency": {"7.5": 600}, "aoe_dropoff": {"7.5": 0.5}},
    },
    "Aerial Blast (pet)": {
        90: {"potency": {"6.55": 750}, "aoe_dropoff": {"6.55": 0.6, "7.3": 0.5}},
        100: {
            "potency": {"7.0": 750, "7.1": 800},
            "aoe_dropoff": {"7.0": 0.6, "7.3": 0.5},
        },
    },
    "Scarlet Flame (pet)": {
        90: {"potency": {"6.55": 150}},
        100: {"potency": {"7.0": 150}},
    },
    "Necrotize": {100: {"potency": {"7.0": 420, "7.05": 440, "7.2": 460, "7.5": 500}}},
    "Searing Flash": {100: {"potency": {"7.0": 600, "7.41": 700}}},
    "Wyrmwave (pet)": {
        70: {"potency": {"7.5": 150}},
        90: {"potency": {"6.55": 150}},
        100: {"potency": {"7.0": 150}},
    },
    "Luxwave": {100: {"potency": {"7.0": 160}}},
    "Umbral Impulse": {100: {"potency": {"7.0": 600, "7.05": 620, "7.41": 640}}},
    "Umbral Flare": {100: {"potency": {"7.0": 280, "7.41": 300}}},
    "Sunflare": {
        100: {
            "potency": {"7.0": 600, "7.05": 700, "7.1": 800, "7.41": 1000},
            "aoe_dropoff": {"7.0": 0.6, "7.25": 0.5},
        }
    },
    "Exodus (pet)": {
        100: {
            "potency": {"7.0": 1400, "7.2": 1500},
            "aoe_dropoff": {"7.0": 0.6, "7.25": 0.5},
        }
    },
}

for k, v in ALL_DATA.items():
    all_smn_skills.add_skill_data(k, v)
