from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_pct_skills = SpecificSkills()

ALL_DATA = {
    "Fire in Red": {
        90: {"potency": {"7.0": 380}},
        100: {"potency": {"7.0": 440}},
    },
    "Aero in Green": {90: {"potency": {"7.0": 420}}, 100: {"potency": {"7.0": 480}}},
    "Water in Blue": {90: {"potency": {"7.0": 460}}, 100: {"potency": {"7.0": 520}}},
    "Fire II in Red": {90: {"potency": {"7.0": 100}}, 100: {"potency": {"7.0": 120}}},
    "Mog of the Ages": {
        90: {"potency": {"7.0": 1300}},
        100: {"potency": {"7.0": 1300}},
    },
    "Pom Muse": {90: {"potency": {"7.0": 1100}}, 100: {"potency": {"7.0": 1100}}},
    "Winged Muse": {90: {"potency": {"7.0": 1100}}, 100: {"potency": {"7.0": 1100}}},
    "Aero II in Green": {
        90: {"potency": {"7.0": 120}},
        100: {"potency": {"7.0": 140}},
    },
    "Water II in Blue": {
        90: {"potency": {"7.0": 140}},
        100: {"potency": {"7.0": 160}},
    },
    "Hammer Stamp": {90: {"potency": {"7.0": 520}}, 100: {"potency": {"7.0": 560}}},
    "Blizzard in Cyan": {
        90: {"potency": {"7.0": 700}},
        100: {"potency": {"7.0": 800}},
    },
    "Blizzard II in Cyan": {
        90: {"potency": {"7.0": 220}},
        100: {"potency": {"7.0": 240}},
    },
    "Stone in Yellow": {90: {"potency": {"7.0": 740}}, 100: {"potency": {"7.0": 840}}},
    "Thunder in Magenta": {
        90: {"potency": {"7.0": 780}},
        100: {"potency": {"7.0": 880}},
    },
    "Stone II in Yellow": {
        90: {"potency": {"7.0": 240}},
        100: {"potency": {"7.0": 260}},
    },
    "Thunder II in Magenta": {
        90: {"potency": {"7.0": 260}},
        100: {"potency": {"7.0": 280}},
    },
    "Holy in White": {90: {"potency": {"7.0": 460}}, 100: {"potency": {"7.0": 520}}},
    "Hammer Brush": {90: {"potency": {"7.0": 580}}, 100: {"potency": {"7.0": 620}}},
    "Polishing Hammer": {90: {"potency": {"7.0": 640}}, 100: {"potency": {"7.0": 680}}},
    "Comet in Black": {90: {"potency": {"7.0": 780}}, 100: {"potency": {"7.0": 880}}},
    "Rainbow Drip": {100: {"potency": {"7.0": 1000}}},
    "Clawed Muse": {100: {"potency": {"7.0": 1100}}},
    "Fanged Muse": {100: {"potency": {"7.0": 1100}}},
    "Retribution of the Madeen": {100: {"potency": {"7.0": 1400}}},
    "Star Prism": {100: {"potency": {"7.0": 1400}}},
}

for k, v in ALL_DATA.items():
    all_pct_skills.add_skill_data(k, v)
