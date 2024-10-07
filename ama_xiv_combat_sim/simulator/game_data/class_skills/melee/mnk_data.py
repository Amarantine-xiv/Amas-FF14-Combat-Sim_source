from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec

all_mnk_skills = SpecificSkills()

ALL_DATA = {
    "Demolish (dot)": {90: {"potency": {"6.55": 70}}},
    "Opo-opo Form": {
        90: {
            "allowlist": {
                "6.55": (
                    "Bootshine",
                    "Dragon Kick",
                    "Shadow of the Destroyer",
                )
            }
        },
        100: {
            "allowlist": {
                "7.0": (
                    "Bootshine",
                    "Dragon Kick",
                    "Shadow of the Destroyer",
                    "Leaping Opo",
                )
            }
        },
    },
    "Formless Fist": {
        90: {
            "allowlist": {
                "6.55": (
                    "Bootshine",
                    "Dragon Kick",
                    "Shadow of the Destroyer",
                    "True Strike",
                    "Snap Punch",
                    "Twin Snakes",
                    "Demolish",
                    "Rockbreaker",
                    "Four-point Fury",
                )
            },
        },
        100: {
            "allowlist": {
                "7.0": (
                    "Dragon Kick",
                    "Shadow of the Destroyer",
                    "Twin Snakes",
                    "Demolish",
                    "Rockbreaker",
                    "Four-point Fury",
                    "Fire's Reply",
                    "Leaping Opo",
                    # "Rising Raptor",
                    # "Pouncing Coeurl",
                    
                )
            },
        },
    },
    "Bootshine": {90: {"potency": {"6.55": 210}, "potency_leaden_fist": {"6.55": 310}}},
    "True Strike": {90: {"potency": {"6.55": 300}}},
    "Snap Punch": {90: {"potency": {"6.55": 310}, "potency_no_pos": {"6.55": 250}}},
    "Twin Snakes": {
        90: {"potency": {"6.55": 280}},
        100: {"potency": {"7.0": 380, "7.01": 420}},
    },
    "Demolish": {
        90: {
            "damage_spec": {
                "6.55": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=130),
                    "No Positional": DamageSpec(potency=70),
                }
            },
            "primary_application_delay": {"6.55": 1600},
            "potency": {"6.55": 130},
            "potency_no_pos": {"6.55": 70},
        },
        100: {
            "damage_spec": {
                "7.0": None,
            },
            "primary_application_delay": {"7.0": 0},
            "potency": {"7.0": 400, "7.01": 420},
            "potency_no_pos": {"7.0": 340, "7.01": 360},
        },
    },
    "Rockbreaker": {
        90: {"potency": {"6.55": 130}},
        100: {"potency": {"7.0": 130, "7.01": 150}},
    },
    "Four-point Fury": {
        90: {"potency": {"6.55": 120}},
        100: {"potency": {"7.0": 120, "7.01": 140}},
    },
    "Dragon Kick": {90: {"potency": {"6.55": 320}}, 100: {"potency": {"7.0": 320}}},
    "The Forbidden Chakra": {
        90: {"potency": {"6.55": 340}},
        100: {"potency": {"7.0": 400}},
    },
    "Elixir Field": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 800}}},
    "Celestial Revolution": {
        90: {"potency": {"6.55": 450}},
        100: {"potency": {"7.0": 450, "7.01": 600}},
    },
    "Riddle of Fire": {
        90: {"damage_mult": {"6.55": 1.15}, "duration": {"6.55": int(20.72 * 1000)}},
        100: {"damage_mult": {"7.0": 1.15}, "duration": {"7.0": int(20.72 * 1000)}},
    },
    "Brotherhood": {
        90: {"damage_mult": {"6.55": 1.05}, "duration": {"6.55": int(14.95 * 1000)}},
        100: {"damage_mult": {"7.0": 1.05}, "duration": {"7.0": int(19.95 * 1000)}},
    },
    "Riddle of Wind": {
        90: {"duration": {"6.55": int(15.78 * 1000)}},
        100: {"duration": {"7.0": int(15.78 * 1000)}},
    },
    "Enlightenment": {
        90: {"potency": {"6.55": 170}},
        100: {"potency": {"7.0": 170, "7.01": 200}},
    },
    "Six-sided Star": {
        90: {"damage_spec": {"6.55": DamageSpec(potency=130)}},
        100: {
            "damage_spec": {
                "7.0": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=780 + 5 * 80),
                    "10 Chakra": DamageSpec(potency=780 + 10 * 80),
                    "9 Chakra": DamageSpec(potency=780 + 9 * 80),
                    "8 Chakra": DamageSpec(potency=780 + 8 * 80),
                    "7 Chakra": DamageSpec(potency=780 + 7 * 80),
                    "6 Chakra": DamageSpec(potency=780 + 6 * 80),
                    "5 Chakra": DamageSpec(potency=780 + 5 * 80),
                    "4 Chakra": DamageSpec(potency=780 + 4 * 80),
                    "3 Chakra": DamageSpec(potency=780 + 3 * 80),
                    "2 Chakra": DamageSpec(potency=780 + 2 * 80),
                    "1 Chakra": DamageSpec(potency=780 + 1 * 80),
                    "0 Chakra": DamageSpec(potency=780),
                }
            }
        },
    },
    "Shadow of the Destroyer": {
        90: {"potency": {"6.55": 110}},
        100: {"potency": {"7.0": 110, "7.01": 120}},
    },
    "Rising Phoenix": {90: {"potency": {"6.55": 700}}, 100: {"potency": {"7.0": 900}}},
    "Phantom Rush": {
        90: {"potency": {"6.55": 1150}},
        100: {"potency": {"7.0": 1400, "7.05": 1500}},
    },
    "Leaping Opo": {100: {"potency": {"7.0": 260}, "potency_fury": {"7.0": 460}}},
    "Rising Raptor": {
        100: {
            "potency": {"7.0": 330, "7.01": 340},
            "potency_fury": {"7.0": 480, "7.01": 540},
        }
    },
    "Pouncing Coeurl": {
        100: {
            "potency": {"7.0": 400, "7.01": 370},
            "min_potency": {"7.0": 340, "7.01": 310},
            "potency_fury": {"7.0": 500, "7.01": 520},
            "min_potency_fury": {"7.0": 440, "7.01": 460},
            "potency_no_pos": {"7.0": 340, "7.01": 310},
            "potency_no_pos_fury": {"7.0": 440, "7.01": 460},
        }
    },
    "Elixir Burst": {100: {"potency": {"7.0": 900}}},
    "Wind's Reply": {100: {"potency": {"7.0": 800, "7.05": 900}}},
    "Fire's Reply": {100: {"potency": {"7.0": 1100, "7.05": 1200}}},
    "Raptor's Fury": {
        100: {
            "num_uses": {"7.0": 2, "7.01": 1},
            "allowlist": {
                "7.0": ("Rising Raptor",),
            },
        }
    },
    "Coeurl's Fury": {
        100: {
            "num_uses": {"7.0": 3, "7.01": 2},
            "allowlist": {
                "7.0": ("Pouncing Coeurl",),
            },
        }
    },
    "Opo-opo's Fury": {
        100: {
            "num_uses": {"7.0": 1},
            "allowlist": {
                "7.0": ("Leaping Opo",),
            },
        }
    },
}

for k, v in ALL_DATA.items():
    all_mnk_skills.add_skill_data(k, v)
