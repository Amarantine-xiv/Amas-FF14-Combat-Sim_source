from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_sam_skills = SpecificSkills()

ALL_DATA = {
    "Hakaze": {90: {"potency": {"6.55": 200}}},
    "Gyofu": {100: {"potency": {"7.0": 240, "7.05": 230, "7.1": 240}}},
    "Jinpu": {
        90: {
            "potency": {"6.55": 280},
            "potency_no_combo": {"6.55": 120},
            "combo_actions": {"6.55": ("Hakaze",)},
        },
        100: {
            "potency": {"7.0": 320, "7.05": 300},
            "potency_no_combo": {"7.0": 160, "7.05": 140},
            "combo_actions": {"7.0": ("Gyofu",)},
        },
    },
    "Enpi": {
        90: {"potency": {"6.55": 100}, "potency_enhanced": {"6.55": 260}},
        100: {"potency": {"7.0": 100}, "potency_enhanced": {"7.0": 260}},
    },
    "Shifu": {
        90: {
            "potency": {"6.55": 280},
            "potency_no_combo": {"6.55": 120},
            "combo_actions": {"6.55": ("Hakaze",)},
        },
        100: {
            "potency": {"7.0": 320, "7.05": 300},
            "potency_no_combo": {"7.0": 160, "7.05": 140},
            "combo_actions": {"7.0": ("Gyofu",)},
        },
    },
    "Gekko": {
        90: {
            "potency": {"6.55": 380, "7.05": 370},
            "potency_no_combo": {"6.55": 170, "7.05": 160},
            "potency_no_pos": {"6.55": 330, "7.05": 320},
            "potency_no_pos_no_combo": {"6.55": 120, "7.05": 110},
        },
        100: {
            "potency": {"7.0": 440, "7.05": 420},
            "potency_no_combo": {"7.0": 230, "7.05": 210},
            "potency_no_pos": {"7.0": 390, "7.05": 370},
            "potency_no_pos_no_combo": {"7.0": 180, "7.05": 160},
        },
    },
    "Higanbana (dot)": {90: {"potency": {"6.55": 45}}, 100: {"potency": {"7.0": 50}}},
    "Higanbana": {90: {"potency": {"6.55": 200}}, 100: {"potency": {"7.0": 200}}},
    "Tenka Goken": {90: {"potency": {"6.55": 300}}, 100: {"potency": {"7.0": 300}}},
    "Midare Setsugekka": {
        90: {"potency": {"6.55": 640, "7.05": 620}},
        100: {"potency": {"7.0": 700, "7.05": 640}},
    },
    "Kaeshi: Higanbana": {90: {"potency": {"6.55": 200}}},
    "Kaeshi: Goken": {90: {"potency": {"6.55": 300}}, 100: {"potency": {"7.0": 300}}},
    "Kaeshi: Setsugekka": {
        90: {"potency": {"6.55": 640, "7.05": 620}},
        100: {"potency": {"7.0": 700, "7.05": 640}},
    },
    "Mangetsu": {
        90: {"potency": {"6.55": 120}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 120}, "potency_no_combo": {"7.0": 100}},
    },
    "Kasha": {
        90: {
            "potency": {"6.55": 380, "7.05": 370},
            "potency_no_combo": {"6.55": 170, "7.05": 160},
            "potency_no_pos": {"6.55": 330, "7.05": 320},
            "potency_no_pos_no_combo": {"6.55": 120, "7.05": 110},
        },
        100: {
            "potency": {"7.0": 440, "7.05": 420},
            "potency_no_combo": {"7.0": 230, "7.05": 210},
            "potency_no_pos": {"7.0": 390, "7.05": 370},
            "potency_no_pos_no_combo": {"7.0": 180, "7.05": 160},
        },
    },
    "Oka": {
        90: {"potency": {"6.55": 120}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 120}, "potency_no_combo": {"7.0": 100}},
    },
    "Yukikaze": {
        90: {
            "potency": {"6.55": 300, "7.05": 290},
            "potency_no_combo": {"6.55": 120, "7.05": 110},
            "combo_actions": {"6.55": ("Hakaze",)},
        },
        100: {
            "potency": {"7.0": 360, "7.05": 340},
            "potency_no_combo": {"7.0": 180, "7.05": 160},
            "combo_actions": {"7.0": ("Gyofu",)},
        },
    },
    "Hissatsu: Shinten": {
        90: {"potency": {"6.55": 250}},
        100: {"potency": {"7.0": 250}},
    },
    "Hissatsu: Gyoten": {
        90: {"potency": {"6.55": 100}},
        100: {"potency": {"7.0": 100}},
    },
    "Hissatsu: Yaten": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Hissatsu: Kyuten": {
        90: {"potency": {"6.55": 120}},
        100: {"potency": {"7.0": 120}},
    },
    "Hissatsu: Guren": {90: {"potency": {"6.55": 500}}, 100: {"potency": {"7.0": 500}}},
    "Hissatsu: Senei": {
        90: {"potency": {"6.55": 860, "7.05": 800}},
        100: {"potency": {"7.0": 860, "7.05": 800}},
    },
    "Shoha": {90: {"potency": {"6.55": 560}}, 100: {"potency": {"7.0": 640}}},
    "Shoha II": {90: {"potency": {"6.55": 200}}},
    "Fuko": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Ogi Namikiri": {90: {"potency": {"6.55": 860}}, 100: {"potency": {"7.0": 900}}},
    "Kaeshi: Namikiri": {
        90: {"potency": {"6.55": 860}},
        100: {"potency": {"7.0": 900}},
    },
    "Zanshin": {100: {"potency": {"7.0": 900, "7.05": 820, "7.1": 900}}},
    "Tendo Goken": {100: {"potency": {"7.0": 420, "7.05": 410}}},
    "Tendo Setsugekka": {
        100: {
            "potency": {"7.0": 1020},
            "gcd_base_recast_time": {"7.0": 3200, "7.01": 2500},
        }
    },
    "Tendo Kaeshi Goken": {100: {"potency": {"7.0": 420, "7.05": 410}}},
    "Tendo Kaeshi Setsugekka": {
        100: {
            "potency": {"7.0": 1020},
            "gcd_base_recast_time": {"7.0": 3200, "7.01": 2500},
        }
    },
}

for k, v in ALL_DATA.items():
    all_sam_skills.add_skill_data(k, v)
