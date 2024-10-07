from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_brd_skills = SpecificSkills()

ALL_DATA = {
    "Stormbite (dot)": {90: {"potency": {"6.55": 25}},
                        100: {"potency": {"7.0": 25}}},
    "Caustic Bite (dot)": {90: {"potency": {"6.55": 20}},
                           100: {"potency": {"7.0": 20}}},
    "Bloodletter": {90: {"potency": {"6.55": 110}},
                    100: {"potency": {"7.0": 130}}},
    "Mage's Ballad": {90: {"potency": {"6.55": 100}}},
    "Army's Paeon": {90: {"potency": {"6.55": 100}}},
    "Rain of Death": {90: {"potency": {"6.55": 100}},
                      100: {"potency": {"7.0": 100}}},
    "Battle Voice": {90: {"duration": {"6.55": 15 * 1000}},
                     100: {"duration": {"7.0": 20 * 1000}}},
    "The Wanderer's Minuet": {90: {"potency": {"6.55": 100}}},
    "Pitch Perfect": {
        90: {
            "1 Repertoire": {"6.55": 100},
            "2 Repertoire": {"6.55": 220},
            "3 Repertoire": {"6.55": 360},
        },
        100: {
            "1 Repertoire": {"7.0": 100},
            "2 Repertoire": {"7.0": 220},
            "3 Repertoire": {"7.0": 360},
        }
    },
    "Empyreal Arrow": {90: {"potency": {"6.55": 240}},
                       100: {"potency": {"7.0": 260}}},    
    "Iron Jaws": {90: {"potency": {"6.55": 100}},
                  100: {"potency": {"7.0": 100}}},    
    "Sidewinder": {90: {"potency": {"6.55": 320}},
                   100: {"potency": {"7.0": 400}}},
    
    "Caustic Bite": {90: {"potency": {"6.55": 150}},
                     100: {"potency": {"7.0": 150}}},
    
    "Stormbite": {90: {"potency": {"6.55": 100}},
                  100: {"potency": {"7.0": 100}}},
    "Refulgent Arrow": {90: {"potency": {"6.55": 280}},
                        100: {"potency": {"7.0": 280}}},
    "Shadowbite": {90: {"potency": {"6.55": 170}, "potency_barrage": {"6.55": 270}},
                   100: {"potency": {"7.0": 170}, "potency_barrage": {"7.0": 270}}},
    "Burst Shot": {90: {"potency": {"6.55": 220}},
                   100: {"potency": {"7.0": 220}}},
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
            "20 Soul Voice": {"7.0": 120},
            "25 Soul Voice": {"7.0": 150},
            "30 Soul Voice": {"7.0": 180},
            "35 Soul Voice": {"7.0": 210},
            "40 Soul Voice": {"7.0": 240},
            "45 Soul Voice": {"7.0": 270},
            "50 Soul Voice": {"7.0": 300},
            "55 Soul Voice": {"7.0": 330},
            "60 Soul Voice": {"7.0": 360},
            "65 Soul Voice": {"7.0": 390},
            "70 Soul Voice": {"7.0": 420},
            "75 Soul Voice": {"7.0": 450},
            "80 Soul Voice": {"7.0": 480},
            "85 Soul Voice": {"7.0": 510},
            "90 Soul Voice": {"7.0": 540},
            "95 Soul Voice": {"7.0": 570},
            "100 Soul Voice": {"7.0": 600},
        }
    },
    "Ladonsbite": {90: {"potency": {"6.55": 130}},
                   100: {"potency": {"7.0": 130}}},
    "Blast Arrow": {90: {"potency": {"6.55": 600}},
                    100: {"potency": {"7.0": 600}}},
    "Radiant Finale": {90: {"duration": {"6.55": int(15 * 1000)}},
                       100: {"duration": {"7.0": int(20 * 1000)}}},
    "Heartbreak Shot": {100: {"potency": {"7.0": 180}}},
    "Resonant Arrow": {100: {"potency": {"7.0": 600}}},
    "Radiant Encore": {
        100: {
            "3 Encore": {"7.0": 900},
            "2 Encore": {"7.0": 600},
            "1 Encore": {"7.0": 500},
        }
    },
}

for k, v in ALL_DATA.items():
    all_brd_skills.add_skill_data(k, v)
