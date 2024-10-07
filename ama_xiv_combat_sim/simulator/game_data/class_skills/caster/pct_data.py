from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_pct_skills = SpecificSkills()

ALL_DATA = {
    "Fire in Red": {100: {"potency": {"7.0": 440}}},
    "Aero in Green": {100: {"potency": {"7.0": 480}}},
    "Water in Blue": {100: {"potency": {"7.0": 520}}},
    "Fire II in Red": {100: {"potency": {"7.0": 120}}},
    "Mog of the Ages": {100: {"potency": {"7.0": 1300}}},
    "Pom Muse": {100: {"potency": {"7.0": 1100}}},
    "Winged Muse": {100: {"potency": {"7.0": 1100}}},
    "Aero II in Green": {100: {"potency": {"7.0": 140}}},
    "Water II in Blue": {100: {"potency": {"7.0": 160}}},
    "Hammer Stamp": {100: {"potency": {"7.0": 560}}},
    "Blizzard in Cyan": {100: {"potency": {"7.0": 800}}},
    "Blizzard II in Cyan": {100: {"potency": {"7.0": 240}}},
    "Stone in Yellow": {100: {"potency": {"7.0": 840}}},
    "Thunder in Magenta": {100: {"potency": {"7.0": 880}}},
    "Stone II in Yellow": {100: {"potency": {"7.0": 260}}},
    "Thunder II in Magenta": {100: {"potency": {"7.0": 280}}},
    "Holy in White": {100: {"potency": {"7.0": 520}}},
    "Hammer Brush": {100: {"potency": {"7.0": 620}}},
    "Polishing Hammer": {100: {"potency": {"7.0": 680}}},
    "Comet in Black": {100: {"potency": {"7.0": 880}}},
    "Rainbow Drip": {100: {"potency": {"7.0": 1000}}},
    "Clawed Muse": {100: {"potency": {"7.0": 1100}}},
    "Fanged Muse": {100: {"potency": {"7.0": 1100}}},
    "Retribution of the Madeen": {100: {"potency": {"7.0": 1400}}},
    "Star Prism": {100: {"potency": {"7.0": 1400}}},
}

for k, v in ALL_DATA.items():
    all_pct_skills.add_skill_data(k, v)
