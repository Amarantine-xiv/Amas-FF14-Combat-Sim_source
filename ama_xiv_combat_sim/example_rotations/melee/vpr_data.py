from ama_xiv_combat_sim.example_rotations.specific_rotations import SpecificRotations


all_vpr_rotations = SpecificRotations()

ALL_VPR_ROTATIONS = {
    "VPR": {
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4861,
                "det_stat": 2387,
                "crit_stat": 3173,
                "dh_stat": 1842,
                "speed_stat": 420,
                "job_class": "VPR",
            },
            "skills": (
                "Slither",
                "Steel Fangs",
                "Serpent's Ire",
                "Swiftskin's Sting",
                "Vicewinder",
                "Grade 2 Gemdraught",
                "Hunter's Coil",
                "Twinfang Bite",
                "Twinblood Bite",
                "Swiftskin's Coil",
                "Twinblood Bite",
                "Twinfang Bite",
                "Reawaken",
                "First Generation",
                "First Legacy",
                "Second Generation",
                "Second Legacy",
                "Third Generation",
                "Third Legacy",
                "Fourth Generation",
                "Fourth Legacy",
                "Ouroboros",
                "Uncoiled Fury",
                "Uncoiled Twinfang",
                "Uncoiled Twinblood",
                "Uncoiled Fury",
                "Uncoiled Twinfang",
                "Uncoiled Twinblood",
                "Hindsting Strike",
                "Death Rattle",
                "Vicewinder",
                "Uncoiled Fury",
                "Uncoiled Twinfang",
                "Uncoiled Twinblood",
                "Hunter's Coil",
                "Twinfang Bite",
                "Twinblood Bite",
                "Swiftskin's Coil",
                "Twinfang Bite",
                "Twinblood Bite",
            ),
            "start_version": "7.05",
        }
    },
    # we leave this here for now so that the colab doesn't break with the old naming of rotations.
    "VPR 7.0": {
        100: {
            "stats": {
                "wd": 146,
                "main_stat": 4861,
                "det_stat": 2387,
                "crit_stat": 3173,
                "dh_stat": 1842,
                "speed_stat": 420,
                "job_class": "VPR",
            },
            "skills": (
                "Slither",
                "Steel Fangs",
                "Serpent's Ire",
                "Swiftskin's Sting",
                "Vicewinder",
                "Grade 2 Gemdraught",
                "Hunter's Coil",
                "Twinfang Bite",
                "Twinblood Bite",
                "Swiftskin's Coil",
                "Twinblood Bite",
                "Twinfang Bite",
                "Reawaken",
                "First Generation",
                "First Legacy",
                "Second Generation",
                "Second Legacy",
                "Third Generation",
                "Third Legacy",
                "Fourth Generation",
                "Fourth Legacy",
                "Ouroboros",
                "Uncoiled Fury",
                "Uncoiled Twinfang",
                "Uncoiled Twinblood",
                "Uncoiled Fury",
                "Uncoiled Twinfang",
                "Uncoiled Twinblood",
                "Hindsting Strike",
                "Death Rattle",
                "Vicewinder",
                "Uncoiled Fury",
                "Uncoiled Twinfang",
                "Uncoiled Twinblood",
                "Hunter's Coil",
                "Twinfang Bite",
                "Twinblood Bite",
                "Swiftskin's Coil",
                "Twinfang Bite",
                "Twinblood Bite",
            ),
            "start_version": "7.05",
        }
    },
}

for k, v in ALL_VPR_ROTATIONS.items():
    all_vpr_rotations.add_rotation_data(k, v)