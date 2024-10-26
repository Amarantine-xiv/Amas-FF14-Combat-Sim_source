from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_nin_rotations = SpecificRotations()

ALL_NIN_ROTATIONS = {
    "NIN": {
        90: {
            "stats": {
                "wd": 132,
                "main_stat": 3360,
                "det_stat": 1697,
                "crit_stat": 2554,
                "dh_stat": 1582,
                "speed_stat": 400,
                "job_class": "NIN",
            },
            "skills": (
                "Huton",
                "Hide",
                "Suiton",
                "Kassatsu",
                "Spinning Edge",
                "Grade 8 Tincture",
                "Gust Slash",
                "Mug",
                "Bunshin",
                "Phantom Kamaitachi",
                "Trick Attack",
                "Aeolian Edge",
                "Dream Within a Dream",
                "Ten",
                "Jin",
                "Hyosho Ranryu",
                "Ten",
                "Chi",
                "Raiton",
                "Ten Chi Jin",
                "Fuma Shuriken",
                "Raiton",
                "Suiton",
                "Meisui",
                "Forked Raiju",
                "Bhavacakra",
                "Forked Raiju",
                "Bhavacakra",
                "Ten",
                "Chi",
                "Raiton",
                "Forked Raiju",
            ),
            "start_version": "6.55",
        },
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4861,
                "det_stat": 2387,
                "crit_stat": 3173,
                "dh_stat": 1842,
                "speed_stat": 420,
                "job_class": "NIN",
            },
            "skills": (                
                "Ten",
                "Chi",
                "Jin",
                "Suiton",
                "Kassatsu",
                "Spinning Edge",
                "Grade 2 Gemdraught",
                "Gust Slash",
                "Dokumori",
                "Bunshin",
                "Phantom Kamaitachi",
                "Armor Crush",
                "Kunai's Bane",
                "Hyosho Ranryu",
                "Dream Within a Dream",
                "Raiton",
                "Ten Chi Jin",
                "Fuma Shuriken",
                "Raiton",
                "Suiton",
                "Meisui",
                "Fleeting Raiju",
                "Zesho Meppo",
                "Tenri Jindo",
                "Fleeting Raiju",
                "Bhavacakra",
                "Raiton",
                "Fleeting Raiju",                
            ),
            "start_version": "7.05",
        },
    },
}

for k, v in ALL_NIN_ROTATIONS.items():
    all_nin_rotations.add_rotation_data(k, v)