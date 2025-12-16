from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_brd_skills = SpecificSkills()

ALL_DATA = {
    "Stormbite (dot)": {90: {"potency": {"6.55": 25}}, 100: {"potency": {"7.0": 25}}},
    "Caustic Bite (dot)": {
        90: {"potency": {"6.55": 20}},
        100: {"potency": {"7.0": 20}},
    },
    "Bloodletter": {
        90: {"potency": {"6.55": 110, "7.0": 130}},
        100: {"potency": {"7.0": 130}},
    },
    "Mage's Ballad": {90: {"potency": {"6.55": 100}}},
    "Army's Paeon": {90: {"potency": {"6.55": 100}}},
    "Rain of Death": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Battle Voice": {
        90: {"duration": {"6.55": 15 * 1000, "7.0": 20 * 1000}},
        100: {"duration": {"7.0": 20 * 1000}},
    },
    "The Wanderer's Minuet": {90: {"potency": {"6.55": 100}}},
    "Pitch Perfect": {
        90: {
            "1 Repertoire": {"6.55": 100},
            "2 Repertoire": {"6.55": 220},
            "3 Repertoire": {"6.55": 360},
            "aoe_dropoff": {"6.55": 0.5, "7.2": 0.55, "7.25": 0.5},
        },
        100: {
            "1 Repertoire": {"7.0": 100},
            "2 Repertoire": {"7.0": 220},
            "3 Repertoire": {"7.0": 360},
            "aoe_dropoff": {"7.0": 0.5, "7.2": 0.55, "7.25": 0.5},
        },
    },
    "Empyreal Arrow": {90: {"potency": {"6.55": 240}}, 100: {"potency": {"7.0": 260}}},
    "Iron Jaws": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Sidewinder": {90: {"potency": {"6.55": 320}}, 100: {"potency": {"7.0": 400}}},
    "Caustic Bite": {90: {"potency": {"6.55": 150}}, 100: {"potency": {"7.0": 150}}},
    "Stormbite": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Refulgent Arrow": {
        90: {"potency": {"6.55": 280, "7.0": 260}},
        100: {"potency": {"7.0": 280}},
    },
    "Shadowbite": {
        90: {
            "potency": {"6.55": 170, "7.2": 180, "7.25": 200},
            "potency_barrage": {"6.55": 270, "7.2": 280, "7.25": 300},
        },
        100: {
            "potency": {"7.0": 170, "7.2": 180, "7.25": 200},
            "potency_barrage": {"7.0": 270, "7.2": 280, "7.25": 300},
        },
    },
    "Burst Shot": {
        90: {"potency": {"6.55": 220, "7.0": 200}},
        100: {"potency": {"7.0": 220}},
    },
    # TODO: fix lvl 90. Need to see in game.
    "Apex Arrow": {
        90: {
            "20 Soul Voice": {"6.55": 100},
            "25 Soul Voice": {"6.55": 125},
            "30 Soul Voice": {"6.55": 150},
            "35 Soul Voice": {"6.55": 175},
            "40 Soul Voice": {"6.55": 200},
            "45 Soul Voice": {"6.55": 225},
            "50 Soul Voice": {"6.55": 250},
            "55 Soul Voice": {"6.55": 275},
            "60 Soul Voice": {"6.55": 300},
            "65 Soul Voice": {"6.55": 325},
            "70 Soul Voice": {"6.55": 350},
            "75 Soul Voice": {"6.55": 375},
            "80 Soul Voice": {"6.55": 400},
            "85 Soul Voice": {"6.55": 425},
            "90 Soul Voice": {"6.55": 450},
            "95 Soul Voice": {"6.55": 475},
            "100 Soul Voice": {"6.55": 500},
        },
        100: {
            "20 Soul Voice": {"7.0": 120, "7.4": 140},
            "25 Soul Voice": {"7.0": 150, "7.4": 140 + int(1 * 35)},
            "30 Soul Voice": {"7.0": 180, "7.4": 140 + int(2 * 35)},
            "35 Soul Voice": {"7.0": 210, "7.4": 140 + int(3 * 355)},
            "40 Soul Voice": {"7.0": 240, "7.4": 140 + int(4 * 35)},
            "45 Soul Voice": {"7.0": 270, "7.4": 140 + int(5 * 35)},
            "50 Soul Voice": {"7.0": 300, "7.4": 140 + int(6 * 35)},
            "55 Soul Voice": {"7.0": 330, "7.4": 140 + int(7 * 35)},
            "60 Soul Voice": {"7.0": 360, "7.4": 140 + int(8 * 35)},
            "65 Soul Voice": {"7.0": 390, "7.4": 140 + int(9 * 35)},
            "70 Soul Voice": {"7.0": 420, "7.4": 140 + int(10 * 35)},
            "75 Soul Voice": {"7.0": 450, "7.4": 140 + int(11 * 35)},
            "80 Soul Voice": {"7.0": 480, "7.4": 140 + int(12 * 35)},
            "85 Soul Voice": {"7.0": 510, "7.4": 140 + int(13 * 35)},
            "90 Soul Voice": {"7.0": 540, "7.4": 140 + int(14 * 35)},
            "95 Soul Voice": {"7.0": 570, "7.4": 140 + int(15 * 35)},
            "100 Soul Voice": {"7.0": 600, "7.4": 700},
        },
    },
    "Ladonsbite": {
        90: {"potency": {"6.55": 130, "7.2": 140}},
        100: {"potency": {"7.0": 130, "7.2": 140}},
    },
    "Blast Arrow": {
        90: {
            "potency": {"6.55": 600, "7.4": 700},
            "aoe_dropoff": {"7.0": 0.6, "7.25": 0.5},
        },
        100: {
            "potency": {"7.0": 600, "7.4": 700},
            "aoe_dropoff": {"7.0": 0.6, "7.25": 0.5},
        },
    },
    "Radiant Finale": {
        90: {"duration": {"6.55": 15 * 1000, "7.0": 20 * 1000}},
        100: {"duration": {"7.0": 20 * 1000}},
    },
    "Heartbreak Shot": {100: {"potency": {"7.0": 180}}},
    "Resonant Arrow": {
        100: {
            "potency": {"7.0": 600, "7.3": 640},
            "aoe_dropoff": {"7.0": 0.5, "7.2": 0.55, "7.25": 0.5},
        }
    },
    "Radiant Encore": {
        100: {
            "3 Encore": {"7.0": 900, "7.3": 1000, "7.4": 1100},
            "2 Encore": {"7.0": 600, "7.3": 700, "7.4": 800},
            "1 Encore": {"7.0": 500, "7.3": 600, "7.4": 700},
            "aoe_dropoff": {"7.0": 0.5, "7.2": 0.55, "7.25": 0.5},
        }
    },
    "Troubadour": {
        90: {
            "damage_reduction": {"6.55": 0.1},
        },
        100: {
            "damage_reduction": {"6.55": 0.15},
        },
    },
}

for k, v in ALL_DATA.items():
    all_brd_skills.add_skill_data(k, v)
