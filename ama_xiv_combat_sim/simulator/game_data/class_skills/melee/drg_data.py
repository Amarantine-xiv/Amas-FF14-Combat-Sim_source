from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_drg_skills = SpecificSkills()

ALL_DATA = {
    "True Thrust": {90: {"potency": {"6.55": 230}}, 100: {"potency": {"7.0": 230}}},
    "Vorpal Thrust": {
        90: {"potency": {"6.55": 280}, "potency_no_combo": {"6.55": 130}},
    },
    "Piercing Talon": {
        90: {"potency": {"6.55": 150, "7.1": 200}, "enhanced potency": {"7.1": 350}},
        100: {"potency": {"7.0": 150, "7.1": 200}, "enhanced potency": {"7.1": 350}},
    },
    "Disembowel": {
        90: {"potency": {"6.55": 250}, "potency_no_combo": {"6.55": 140}},
    },
    "Lance Charge": {
        90: {
            "damage_mult": {"6.55": 1.1},
            "duration": {"6.55": 20 * 1000},
        },
        100: {
            "damage_mult": {"7.0": 1.1},
            "duration": {"7.0": 20 * 1000},
        },
    },
    "Doom Spike": {90: {"potency": {"6.55": 110}}, 100: {"potency": {"7.0": 110}}},
    "Spineshatter Dive": {90: {"potency": {"6.55": 250}}},
    "Dragonfire Dive": {
        90: {
            "potency": {"6.55": 300, "7.0": 500},
            "aoe_dropoff": {"6.55": 0.0, "7.0": 0.5},
        },
        100: {"potency": {"7.0": 500}, "aoe_dropoff": {"6.55": 0.0, "7.0": 0.5}},
    },
    "Battle Litany": {
        90: {"crit_rate_add": {"6.55": 0.10}, "duration": {"6.55": 15 * 1000}},
        100: {"crit_rate_add": {"7.0": 0.10}, "duration": {"7.0": 20 * 1000}},
    },
    "Fang and Claw": {
        90: {
            "potency": {"6.55": 300, "7.0": 300},
            "potency_no_pos": {"6.55": 260, "7.0": 260},
            "potency_no_combo": {"7.0": 140},
            "potency_no_pos_no_combo": {"7.0": 100},
            # 6.55 stuff
            "potency_wheeling": {"6.55": 400},
            "potency_wheeling_no_pos": {"6.55": 360},
        },
        100: {
            "potency": {"7.0": 340},
            "potency_no_pos": {"7.0": 300},
            "potency_no_combo": {"7.0": 180},
            "potency_no_pos_no_combo": {"7.0": 140},
        },
    },
    "Wheeling Thrust": {
        90: {
            "potency": {"6.55": 300, "7.0": 300},
            "potency_no_pos": {"6.55": 260, "7.0": 260},
            "potency_no_combo": {"7.0": 140},
            "potency_no_pos_no_combo": {"7.0": 100},
            # 6.55 stuff
            "potency_fc": {"6.55": 400},
            "potency_fc_no_pos": {"6.55": 360},
        },
        100: {
            "potency": {"7.0": 340},
            "potency_no_pos": {"7.0": 300},
            "potency_no_combo": {"7.0": 180},
            "potency_no_pos_no_combo": {"7.0": 140},
        },
    },
    "Geirskogul": {
        90: {
            "potency": {"6.55": 260, "7.0": 280},
            "aoe_dropoff": {"6.55": 0.3, "7.0": 0.5},
        },
        100: {"potency": {"7.0": 280}, "aoe_dropoff": {"7.0": 0.5}},
    },
    "Sonic Thrust": {
        90: {"potency": {"6.55": 120}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 120}, "potency_no_combo": {"7.0": 100}},
    },
    "Mirage Dive": {
        90: {"potency": {"6.55": 200, "7.1": 380}},
        100: {"potency": {"7.0": 200, "7.1": 380}},
    },
    "Nastrond": {
        90: {
            "potency": {"6.55": 360, "7.1": 720},
            "aoe_dropoff": {"6.55": 0.3, "7.0": 0.5},
        },
        100: {"potency": {"7.0": 360, "7.1": 720}, "aoe_dropoff": {"7.0": 0.5}},
    },
    "Coerthan Torment": {
        90: {"potency": {"6.55": 150}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 150}, "potency_no_combo": {"7.0": 100}},
    },
    "High Jump": {90: {"potency": {"6.55": 400}}, 100: {"potency": {"7.0": 400}}},
    "Raiden Thrust": {90: {"potency": {"6.55": 280}}, 100: {"potency": {"7.0": 320}}},
    "Stardiver": {
        90: {"potency": {"6.55": 620, "7.05": 620, "7.1": 720}},
        100: {"potency": {"7.0": 620, "7.05": 720, "7.1": 820, "7.2": 840}},
    },
    "Draconian Fury": {90: {"potency": {"6.55": 130}}, 100: {"potency": {"7.0": 130}}},
    "Heavens' Thrust": {
        90: {
            "potency": {"6.55": 480, "7.0": 400},
            "potency_no_combo": {"6.55": 100},
            "combo_action": {"6.55": ("Vorpal Thrust",)},
        },
        100: {
            "potency": {"7.0": 440, "7.2": 460},
            "potency_no_combo": {"7.0": 140, "7.2": 160},
            "combo_action": {"7.0": ("Lance Barrage",)},
        },
    },
    "Chaotic Spring (dot)": {
        90: {"potency": {"6.55": 45}, "duration": {"6.55": 24 * 1000}},
        100: {"potency": {"7.0": 45}, "duration": {"7.0": 24 * 1000}},
    },
    "Chaotic Spring": {
        90: {
            "potency": {"6.55": 300},
            "potency_no_combo": {"6.55": 140},
            "potency_no_pos": {"6.55": 260},
            "potency_no_pos_no_combo": {"6.55": 100},
            "combo_action": {"6.55": ("Disembowel",)},
        },
        100: {
            "potency": {"7.0": 340},
            "potency_no_combo": {"7.0": 180},
            "potency_no_pos": {"7.0": 300},
            "potency_no_pos_no_combo": {"7.0": 140},
            "combo_action": {"7.0": ("Spiral Blow",)},
        },
    },
    "Wyrmwind Thrust": {90: {"potency": {"6.55": 420}}, 100: {"potency": {"7.0": 440}}},
    "Rise of the Dragon": {100: {"potency": {"7.0": 550}}},
    "Lance Barrage": {
        100: {
            "potency": {"7.0": 340},
            "potency_no_combo": {"7.0": 130},
        }
    },
    "Spiral Blow": {
        100: {
            "potency": {"7.0": 340},
            "potency_no_combo": {"7.0": 140},
        }
    },
    "Starcross": {100: {"potency": {"7.0": 700, "7.05": 900, "7.1": 1000}}},
    "Drakesbane": {
        90: {"potency": {"7.0": 400}},
        100: {"potency": {"7.0": 440, "7.2": 460}},
    },
}

for k, v in ALL_DATA.items():
    all_drg_skills.add_skill_data(k, v)
