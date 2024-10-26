from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec

all_nin_skills = SpecificSkills()

ALL_DATA = {
    "Bunshin": {
        90: {
            "potency_melee": {"6.55": 160},
            "potency_ranged": {"6.55": 160},
            "potency_area": {"6.55": 80},
            "allowlist": {
                "6.55": (
                    "Spinning Edge",
                    "Gust Slash",
                    "Throwing Dagger",
                    "Aeolian Edge",
                    "Death Blossom",
                    "Hakke Mujinsatsu",
                    "Armor Crush",
                    "Huraijin",
                    "Forked Raiju",
                    "Fleeting Raiju",
                )
            },
        },
        100: {
            "potency_melee": {"7.0": 160},
            "potency_ranged": {"7.0": 160},
            "potency_area": {"7.0": 80},
            "allowlist": {
                "7.0": (
                    "Spinning Edge",
                    "Gust Slash",
                    "Throwing Dagger",
                    "Aeolian Edge",
                    "Death Blossom",
                    "Hakke Mujinsatsu",
                    "Armor Crush",
                    "Forked Raiju",
                    "Fleeting Raiju",
                )
            },
        },
    },
    "Dream Within a Dream": {
        90: {"potency": {"6.55": 150}},
        100: {"potency": {"7.0": 150}},
    },
    "Doton (dot)": {90: {"potency": {"6.55": 80}}, 100: {"potency": {"7.0": 80}}},
    "Doton hollow nozuchi (dot)": {
        90: {"potency": {"6.55": 50}},
        100: {"potency": {"7.0": 50}},
    },
    "Spinning Edge": {90: {"potency": {"6.55": 220}}, 100: {"potency": {"6.55": 300}}},
    "Gust Slash": {
        90: {"potency": {"6.55": 320}, "potency_no_combo": {"6.55": 160}},
        100: {
            "potency": {"7.0": 380, "7.05": 400},
            "potency_no_combo": {"7.0": 220, "7.05": 240},
        },
    },
    "Throwing Dagger": {90: {"potency": {"6.55": 120}}, 100: {"potency": {"7.0": 120}}},
    "Mug": {90: {"potency": {"6.55": 150}, "duration": {"6.55": int(20.5 * 1000)}}},
    "Trick Attack": {
        90: {
            "potency": {"6.55": 400},
            "potency_no_pos": {"6.55": 300},
            "duration": {"6.55": int(15.77 * 1000)},
        },
    },
    "Aeolian Edge": {
        90: {
            "potency": {"6.55": 440},
            "potency_no_combo": {"6.55": 200},
            "potency_no_pos": {"6.55": 380},
            "potency_no_pos_no_combo": {"6.55": 140},
        },
        100: {
            "potency": {"7.0": 440},
            "potency_no_combo": {"7.0": 260},
            "potency_no_pos": {"7.0": 380},
            "potency_no_pos_no_combo": {"7.0": 200},
            "potency_increment_kaz": {"7.0": 100},
        },
    },
    "Death Blossom": {90: {"potency": {"6.55": 100}}, 100: {"potency": {"7.0": 100}}},
    "Hakke Mujinsatsu": {
        90: {"potency": {"6.55": 130}, "potency_no_combo": {"6.55": 100}},
        100: {"potency": {"7.0": 130}, "potency_no_combo": {"7.0": 100}},
    },
    "Armor Crush": {
        90: {
            "potency": {"6.55": 420},
            "potency_no_combo": {"6.55": 200},
            "potency_no_pos": {"6.55": 360},
            "potency_no_pos_no_combo": {"6.55": 140},
            "job_resource": {"6.55": tuple()},
        },
        100: {
            "potency": {"7.0": 480},
            "potency_no_combo": {"7.0": 280},
            "potency_no_pos": {"7.0": 420},
            "potency_no_pos_no_combo": {"7.0": 220},
            "job_resource": {"7.0": (JobResourceSpec(name="Kazematoi", change=2),)},
        },
    },
    "Dokumori": {
        100: {"potency": {"7.0": 300}, "duration": {"7.0": int(21.02 * 1000)}}
    },
    "Huraijin": {90: {"potency": {"6.55": 200}}},
    "Hellfrog Medium": {90: {"potency": {"6.55": 160}}, 100: {"potency": {"7.0": 160}}},
    "Bhavacakra": {
        90: {"potency": {"6.55": 350}, "potency_mesui": {"6.55": 500}},
        100: {"potency": {"7.0": 380}, "potency_mesui": {"7.0": 530}},
    },
    "Phantom Kamaitachi (pet)": {
        90: {"potency": {"6.55": 600}},
        100: {"potency": {"7.0": 600}},
    },
    "Forked Raiju": {
        90: {"potency": {"6.55": 560}},
        100: {"potency": {"7.0": 640, "7.05": 700}},
    },
    "Fleeting Raiju": {
        90: {"potency": {"6.55": 560}},
        100: {"potency": {"7.0": 640, "7.05": 700}},
    },
    "Fuma Shuriken": {90: {"potency": {"6.55": 450}}, 100: {"potency": {"7.0": 500}}},
    "Katon": {90: {"potency": {"6.55": 350}}, 100: {"potency": {"7.0": 350}}},
    "Raiton": {90: {"potency": {"6.55": 650}}, 100: {"potency": {"7.0": 740}}},
    "Hyoton": {90: {"potency": {"6.55": 350}}, 100: {"potency": {"7.0": 350}}},
    "Huton": {
        90: {"damage_spec": {"6.55": None}},
        100: {"damage_spec": {"7.0": DamageSpec(potency=240)}},
    },
    "Suiton": {90: {"potency": {"6.55": 500}}, 100: {"potency": {"7.0": 580}}},
    "Goka Mekkyaku": {90: {"potency": {"6.55": 600}}, 100: {"potency": {"7.0": 600}}},
    "Hyosho Ranryu": {90: {"potency": {"6.55": 1300}}, 100: {"potency": {"7.0": 1300}}},
    "Meisui": {
        90: {"allowlist": {"6.55": ("Bhavacakra",)}},
        100: {"allowlist": {"7.0": ("Bhavacakra", "Zesho Meppo")}},
    },
    "Kunai's Bane": {
        100: {"potency": {"7.0": 600}, "duration": {"7.0": int(16.26 * 1000)}}
    },
    "Deathfrog Medium": {100: {"potency": {"7.0": 300}}},
    "Zesho Meppo": {
        100: {
            "potency": {"7.0": 550, "7.05": 700},
            "potency_mesui": {"7.0": 700, "7.05": 850},
        }
    },
    "Tenri Jindo": {100: {"potency": {"7.0": 1000, "7.05": 1100}}},
}

for k, v in ALL_DATA.items():
    all_nin_skills.add_skill_data(k, v)