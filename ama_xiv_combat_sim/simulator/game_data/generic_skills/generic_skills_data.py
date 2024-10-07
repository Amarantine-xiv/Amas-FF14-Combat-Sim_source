from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_generic_skills = SpecificSkills()

ALL_GENERIC_DATA = {
    "Grade 8 Tincture": {
        90: {
            "animation_lock": {"6.55": 1300, "7.0": 650},
            "application_delay": {"6.55": 890, "7.0": 625},
        },
        100: {
            "animation_lock": {"7.0": 650},
            "application_delay": {"6.55": 890, "7.0": 625},
        },
    },
    "Grade 7 Tincture": {
        90: {
            "animation_lock": {"6.55": 1300, "7.0": 650},
            "application_delay": {"6.55": 890, "7.0": 625},
        },
        100: {"animation_lock": {"7.0": 650}, "application_delay": {"7.0": 625}},
    },
    "Grade 1 Gemdraught": {
        90: {"animation_lock": {"7.0": 650}, "application_delay": {"7.0": 625}},
        100: {"animation_lock": {"7.0": 650}, "application_delay": {"7.0": 625}}
    },
    "Grade 2 Gemdraught": {
        90: {"animation_lock": {"7.0": 650}, "application_delay": {"7.0": 625}},
        100: {"animation_lock": {"7.05": 650}, "application_delay": {"7.0": 625}}
    },
}

for k, v in ALL_GENERIC_DATA.items():
    all_generic_skills.add_skill_data(k, v)
