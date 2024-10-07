from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_vpr_skills = SpecificSkills()

ALL_DATA = {
    "Combo Base": {
        100: {
            "potency_no_venom": {"7.0": 120, "7.05": 160},
            "potency_venom": {"7.0": 220, "7.05": 260},
        }
    },
    "Steel Fangs": {
        100: {
            "damage_spec": {
                "7.0": DamageSpec(potency=200),
                "7.05": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200),
                    "Honed Steel": DamageSpec(potency=300),
                },
            },
        }
    },
    "Hunter's Instinct": {
        100: {
            "duration": {"7.0": int(40 * 1000)},
        }
    },
    "Hunter's Sting": {
        100: {
            "potency": {"7.0": 260, "7.05": 300},
        }
    },
    "Noxious Gnash": {
        100: {
            "duration": {"7.0": 20 * 1000},
            "max_duration": {"7.0": 40 * 1000},
        }
    },
    "Dread Fangs": {
        100: {
            "potency": {"7.0": 140},
        }
    },
    "Reaving Fangs": {
        100: {
            "potency": {"7.05": 200},
            "potency_honed_reavers": {"7.05": 300},
        }
    },
    "Writhing Snap": {
        100: {
            "potency": {"7.0": 200},
        }
    },
    "Swiftscaled": {
        100: {
            "duration": {"7.0": 40 * 1000},
        }
    },
    "Swiftskin's Sting": {
        100: {
            "potency": {"7.0": 260, "7.05": 300},
        }
    },
    "Steel Maw": {
        100: {
            "damage_spec": {
                "7.0": DamageSpec(potency=100),
                "7.05": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                    "Honed Steel": DamageSpec(potency=120),
                },
            },
        }
    },
    "Hindstung Venom": {
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        }
    },
    "Flanksting Strike": {
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        }
    },
    "Hindsbane Venom": {
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        }
    },
    "Flanksbane Fang": {
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        }
    },
    "Flanksbane Venom": {
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        }
    },
    "Hindsting Strike": {
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        }
    },
    "Flankstung Venom": {
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        }
    },
    "Hindsbane Fang": {
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        }
    },
    "Dread Maw": {
        100: {
            "potency": {"7.0": 80},
        }
    },
    "Reaving Maw": {
        100: {
            "potency": {"7.05": 200},
            "potency_honed_reavers": {"7.05": 300},
        }
    },
    "Hunter's Bite": {
        100: {
            "potency": {"7.0": 120, "7.05": 130},
        }
    },
    "Swiftskin's Bite": {
        100: {
            "potency": {"7.0": 120, "7.05": 130},
        }
    },
    "Grimskin's Venom": {
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        }
    },
    "Jagged Maw": {
        100: {
            "potency": {"7.0": 140},
            "potency_venom": {"7.0": 160},
        }
    },
    "Grimhunter's Venom": {
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        }
    },
    "Bloodied Maw": {
        100: {
            "potency": {"7.0": 140},
            "potency_venom": {"7.0": 160},
        }
    },
    "Death Rattle": {
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        }
    },
    "Last Lash": {
        100: {
            "potency": {"7.0": 100},
        }
    },
    "Dreadwinder": {
        100: {
            "potency": {"7.0": 450},
        }
    },
    "Vicewinder": {
        100: {
            "potency": {"7.05": 500},
        }
    },
    "Hunter's Venom": {
        100: {
            "duration": {"7.0": 30 * 1000},
        }
    },
    "Hunter's Coil": {
        100: {
            "potency": {"7.0": 550, "7.05": 620},
            "potency_no_pos": {"7.0": 500, "7.05": 570},
        }
    },
    "Swiftskin's Venom": {
        100: {
            "duration": {"7.0": 30 * 1000},
        }
    },
    "Swiftskin's Coil": {
        100: {
            "potency": {"7.0": 550, "7.05": 620},
            "potency_no_pos": {"7.0": 500, "7.05": 570},
        }
    },
    "Pit of Dread": {
        100: {
            "potency": {"7.0": 200},
        }
    },
    "Vicepit": {
        100: {
            "potency": {"7.05": 220},
        }
    },
    "Fellhunter's Venom": {
        100: {
            "duration": {"7.0": 30 * 1000},
        }
    },
    "Hunter's Den": {
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        }
    },
    "Fellskin's Venom": {
        100: {
            "duration": {"7.0": 30 * 1000},
        }
    },
    "Swiftskin's Den": {
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        }
    },
    "Twinfang Bite": {
        100: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_venom": {"7.0": 150, "7.05": 170},
        }
    },
    "Twinblood Bite": {
        100: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_venom": {"7.0": 150, "7.05": 170},
        }
    },
    "Twinfang Thresh": {
        100: {
            "potency": {"7.0": 50},
            "potency_venom": {"7.0": 80},
        }
    },
    "Twinblood Thresh": {100: {"potency": {"7.0": 50}, "potency_venom": {"7.0": 80}}},
    "Poised for Twinfang": {
        100: {
            "duration": {"7.0": 60 * 1000},
        }
    },
    "Uncoiled Fury": {
        100: {
            "potency": {"7.0": 600, "7.05": 680},
        }
    },
    "Reawaken": {
        100: {
            "potency": {"7.0": 700, "7.05": 750},
        }
    },
    "First Generation": {
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        }
    },
    "Second Generation": {
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        }
    },
    "Third Generation": {
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        }
    },
    "Fourth Generation": {
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        }
    },
    "Poised for Twinblood": {
        100: {
            "duration": {"7.0": 60 * 1000},
        }
    },
    "Uncoiled Twinfang": {
        100: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_poised": {"7.0": 150, "7.05": 170},
        }
    },
    "Uncoiled Twinblood": {
        100: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_poised": {"7.0": 150, "7.05": 170},
        }
    },
    "Ouroboros": {
        100: {
            "potency": {"7.0": 1050, "7.05": 1150},
        }
    },
    "First Legacy": {
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        }
    },
    "Second Legacy": {
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        }
    },
    "Third Legacy": {
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        }
    },
    "Fourth Legacy": {
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        }
    },
}

for k, v in ALL_DATA.items():
    all_vpr_skills.add_skill_data(k, v)
