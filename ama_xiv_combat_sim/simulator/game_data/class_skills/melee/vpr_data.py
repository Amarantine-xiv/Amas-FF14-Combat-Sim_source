from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.game_data.specific_skills import (
    SpecificSkills,
)

all_vpr_skills = SpecificSkills()

ALL_DATA = {
    "Combo Base": {
        90: {
            "potency_no_venom": {"7.0": 120, "7.05": 160},
            "potency_venom": {"7.0": 220, "7.05": 260},
        },
        100: {
            "potency_no_venom": {"7.0": 120, "7.05": 160},
            "potency_venom": {"7.0": 220, "7.05": 260},
        },
    },
    "Steel Fangs": {
        90: {
            "damage_spec": {
                "7.0": DamageSpec(potency=200),
                "7.05": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200),
                    "Honed Steel": DamageSpec(potency=300),
                },
            },
        },
        100: {
            "damage_spec": {
                "7.0": DamageSpec(potency=200),
                "7.05": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=200),
                    "Honed Steel": DamageSpec(potency=300),
                },
            },
        },
    },
    "Hunter's Instinct": {
        90: {
            "duration": {"7.0": int(40 * 1000)},
        },
        100: {
            "duration": {"7.0": int(40 * 1000)},
        },
    },
    "Hunter's Sting": {
        90: {
            "potency": {"7.0": 260, "7.05": 300},
        },
        100: {
            "potency": {"7.0": 260, "7.05": 300},
        },
    },
    "Noxious Gnash": {
        90: {
            "duration": {"7.0": 20 * 1000},
            "max_duration": {"7.0": 40 * 1000},
        },
        100: {
            "duration": {"7.0": 20 * 1000},
            "max_duration": {"7.0": 40 * 1000},
        },
    },
    "Dread Fangs": {
        90: {
            "potency": {"7.0": 140},
        },
        100: {
            "potency": {"7.0": 140},
        },
    },
    "Reaving Fangs": {
        90: {
            "potency": {"7.05": 200},
            "potency_honed_reavers": {"7.05": 300},
        },
        100: {
            "potency": {"7.05": 200},
            "potency_honed_reavers": {"7.05": 300},
        },
    },
    "Writhing Snap": {
        90: {
            "potency": {"7.0": 200},
        },
        100: {
            "potency": {"7.0": 200},
        },
    },
    "Swiftscaled": {
        90: {
            "duration": {"7.0": 40 * 1000},
        },
        100: {
            "duration": {"7.0": 40 * 1000},
        },
    },
    "Swiftskin's Sting": {
        90: {
            "potency": {"7.0": 260, "7.05": 300},
        },
        100: {
            "potency": {"7.0": 260, "7.05": 300},
        },
    },
    "Steel Maw": {
        90: {
            "damage_spec": {
                "7.0": DamageSpec(potency=100),
                "7.05": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                    "Honed Steel": DamageSpec(potency=120),
                },
            },
        },
        100: {
            "damage_spec": {
                "7.0": DamageSpec(potency=100),
                "7.05": {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                    "Honed Steel": DamageSpec(potency=120),
                },
            },
        },
    },
    "Hindstung Venom": {
        90: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
    },
    "Flanksting Strike": {
        90: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
    },
    "Hindsbane Venom": {
        90: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
    },
    "Flanksbane Fang": {
        90: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
    },
    "Flanksbane Venom": {
        90: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
    },
    "Hindsting Strike": {
        90: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
    },
    "Flankstung Venom": {
        90: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
    },
    "Hindsbane Fang": {
        90: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
        100: {
            "potency": {"7.0": 360, "7.05": 400},
            "potency_no_pos": {"7.0": 300, "7.05": 340},
            "potency_venom": {"7.0": 460, "7.05": 500},
            "potency_no_pos_venom": {"7.0": 400, "7.05": 440},
        },
    },
    "Dread Maw": {
        90: {
            "potency": {"7.0": 80},
        },
        100: {
            "potency": {"7.0": 80},
        },
    },
    "Reaving Maw": {
        90: {
            "potency": {"7.05": 100},
            "potency_honed_reavers": {"7.05": 120},
        },
        100: {
            "potency": {"7.05": 100},
            "potency_honed_reavers": {"7.05": 120},
        },
    },
    "Hunter's Bite": {
        90: {
            "potency": {"7.0": 120, "7.05": 130},
        },
        100: {
            "potency": {"7.0": 120, "7.05": 130},
        },
    },
    "Swiftskin's Bite": {
        90: {
            "potency": {"7.0": 120, "7.05": 130},
        },
        100: {
            "potency": {"7.0": 120, "7.05": 130},
        },
    },
    "Grimskin's Venom": {
        90: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
    },
    "Jagged Maw": {
        90: {
            "potency": {"7.0": 140},
            "potency_venom": {"7.0": 160},
        },
        100: {
            "potency": {"7.0": 140},
            "potency_venom": {"7.0": 160},
        },
    },
    "Grimhunter's Venom": {
        90: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 40 * 1000, "7.05": 60 * 1000},
        },
    },
    "Bloodied Maw": {
        90: {
            "potency": {"7.0": 140},
            "potency_venom": {"7.0": 160},
        },
        100: {
            "potency": {"7.0": 140},
            "potency_venom": {"7.0": 160},
        },
    },
    "Death Rattle": {
        90: {
            "potency": {"7.0": 250, "7.05": 280},
        },
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        },
    },
    "Last Lash": {
        90: {
            "potency": {"7.0": 100},
        },
        100: {
            "potency": {"7.0": 100},
        },
    },
    "Dreadwinder": {
        90: {
            "potency": {"7.0": 450},
        },
        100: {
            "potency": {"7.0": 450},
        },
    },
    "Vicewinder": {
        90: {
            "potency": {"7.05": 500},
        },
        100: {
            "potency": {"7.05": 500},
        },
    },
    "Hunter's Venom": {
        90: {
            "duration": {"7.0": 30 * 1000},
        },
        100: {
            "duration": {"7.0": 30 * 1000},
        },
    },
    "Hunter's Coil": {
        90: {
            "potency": {"7.0": 550, "7.05": 620},
            "potency_no_pos": {"7.0": 500, "7.05": 570},
        },
        100: {
            "potency": {"7.0": 550, "7.05": 620},
            "potency_no_pos": {"7.0": 500, "7.05": 570},
        },
    },
    "Swiftskin's Venom": {
        90: {
            "duration": {"7.0": 30 * 1000},
        },
        100: {
            "duration": {"7.0": 30 * 1000},
        },
    },
    "Swiftskin's Coil": {
        90: {
            "potency": {"7.0": 550, "7.05": 620},
            "potency_no_pos": {"7.0": 500, "7.05": 570},
        },
        100: {
            "potency": {"7.0": 550, "7.05": 620},
            "potency_no_pos": {"7.0": 500, "7.05": 570},
        },
    },
    "Pit of Dread": {
        90: {
            "potency": {"7.0": 200},
        },
        100: {
            "potency": {"7.0": 200},
        },
    },
    "Vicepit": {
        90: {
            "potency": {"7.05": 220},
        },
        100: {
            "potency": {"7.05": 220},
        },
    },
    "Fellhunter's Venom": {
        90: {
            "duration": {"7.0": 30 * 1000},
        },
        100: {
            "duration": {"7.0": 30 * 1000},
        },
    },
    "Hunter's Den": {
        90: {
            "potency": {"7.0": 250, "7.05": 280},
        },
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        },
    },
    "Fellskin's Venom": {
        90: {
            "duration": {"7.0": 30 * 1000},
        },
        100: {
            "duration": {"7.0": 30 * 1000},
        },
    },
    "Swiftskin's Den": {
        90: {
            "potency": {"7.0": 250, "7.05": 280},
        },
        100: {
            "potency": {"7.0": 250, "7.05": 280},
        },
    },
    "Twinfang Bite": {
        90: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_venom": {"7.0": 150, "7.05": 170},
        },
        100: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_venom": {"7.0": 150, "7.05": 170},
        },
    },
    "Twinblood Bite": {
        90: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_venom": {"7.0": 150, "7.05": 170},
        },
        100: {
            "potency": {"7.0": 100, "7.05": 120},
            "potency_venom": {"7.0": 150, "7.05": 170},
        },
    },
    "Twinfang Thresh": {
        90: {
            "potency": {"7.0": 50},
            "potency_venom": {"7.0": 80},
        },
        100: {
            "potency": {"7.0": 50},
            "potency_venom": {"7.0": 80},
        },
    },
    "Twinblood Thresh": {
        90: {"potency": {"7.0": 50}, "potency_venom": {"7.0": 80}},
        100: {"potency": {"7.0": 50}, "potency_venom": {"7.0": 80}},
    },
    "Poised for Twinfang": {
        90: {
            "duration": {"7.0": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 60 * 1000},
        },
    },
    "Uncoiled Fury": {
        90: {
            "potency": {"7.0": 600, "7.05": 680},
        },
        100: {
            "potency": {"7.0": 600, "7.05": 680},
        },
    },
    "Reawaken": {
        90: {
            "potency": {"7.0": 700, "7.05": 750},
        },
        100: {
            "potency": {"7.0": 700, "7.05": 750},
        },
    },
    "First Generation": {
        90: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
    },
    "Second Generation": {
        90: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
    },
    "Third Generation": {
        90: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
    },
    "Fourth Generation": {
        90: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
        100: {
            "potency": {"7.0": 600, "7.05": 680},
            "potency_no_combo": {"7.0": 400, "7.05": 480},
        },
    },
    "Poised for Twinblood": {
        90: {
            "duration": {"7.0": 60 * 1000},
        },
        100: {
            "duration": {"7.0": 60 * 1000},
        },
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
            "potency": {"7.0": 250, "7.05": 280, "7.2": 320},
        }
    },
    "Second Legacy": {
        100: {
            "potency": {"7.0": 250, "7.05": 280, "7.2": 320},
        }
    },
    "Third Legacy": {
        100: {
            "potency": {"7.0": 250, "7.05": 280, "7.2": 320},
        }
    },
    "Fourth Legacy": {
        100: {
            "potency": {"7.0": 250, "7.05": 280, "7.2": 320},
        }
    },
}

for k, v in ALL_DATA.items():
    all_vpr_skills.add_skill_data(k, v)
