from dataclasses import dataclass

from ama_xiv_combat_sim.simulator.utils import Utils


@dataclass(frozen=True)
class GameConsts:
    GCD_RECAST_TIME: float = 2500
    DOT_TICK_INTERVAL = 3000
    COMBO_EXPIRATION_TIME = 30 * 1000
    DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES = 500
    DH_DAMAGE_MULT_BONUS = 0.25
    MIN_GCD_RECAST_TIME = 1500
    MULTI_TARGET_DELAY_PER_TARGET = 135
    MAX_MAINSTAT_FRACTION = 0.10
    PARRY_DMG_REDUCTION = 0.15
    # level mods from akhmorning

    # Key is the version. This is interpreted as stats at max-level for now.
    kTestStr = "test"
    __LEVEL_DIV_TEST = 1900
    __LEVEL_MAIN_TEST = 390
    __LEVEL_SUB_TEST = 400

    __FAP_CONST_TEST = 195
    __FAP_TANK_CONST_TEST = 156
    __TEN_CONST_TEST = 100
    __DH_CONST_TEST = 550
    __SPEED_CONST_TEST = 130
    __CRIT_CONST_TEST = (200, 50, 400)
    __DET_CONST_TEST = 140

    __LEVEL_DIVS = {90: 1900, 100: 2780}
    __LEVEL_MAINS = {90: 390, 100: 440}
    __LEVEL_SUBS = {90: 400, 100: 420}

    __FAP_CONSTS = {90: 195, 100: 237}
    __FAP_TANK_CONSTS = {90: 156, 100: 190}
    __TEN_CONSTS = {90: 100, 100: 112}

    __DH_CONSTS = {90: 550, 100: 550}
    __DET_CONSTS = {90: 140, 100: 140}
    __SPEED_CONSTS = {90: 130, 100: 130}

    __CRIT_CONSTS = {
        90: (200, 50, 400),
        100: (200, 50, 400),
    }

    __BASE_SKILL_SPEED = {90: 400, 100: 420}
    __BASE_SPELL_SPEED = {90: 400, 100: 420}

    DAMAGE_VARIANCE = 0.05
    MAX_LEVEL = 100

    @staticmethod
    def get_speed_const(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__SPEED_CONST_TEST
        return GameConsts.__SPEED_CONSTS[level]

    @staticmethod
    def get_crit_consts(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__CRIT_CONST_TEST
        return GameConsts.__CRIT_CONSTS[level]

    @staticmethod
    def get_dh_const(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__DH_CONST_TEST
        return GameConsts.__DH_CONSTS[level]

    @staticmethod
    def get_det_const(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__DET_CONST_TEST
        return GameConsts.__DET_CONSTS[level]

    @staticmethod
    def get_ten_const(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__TEN_CONST_TEST
        return GameConsts.__TEN_CONSTS[level]

    @staticmethod
    def get_level_div(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__LEVEL_DIV_TEST
        return GameConsts.__LEVEL_DIVS[level]

    @staticmethod
    def get_level_main(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__LEVEL_MAIN_TEST
        return GameConsts.__LEVEL_MAINS[level]

    @staticmethod
    def get_level_sub(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__LEVEL_SUB_TEST
        return GameConsts.__LEVEL_SUBS[level]

    @staticmethod
    def get_fAP(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__FAP_CONST_TEST
        return GameConsts.__FAP_CONSTS[level]

    @staticmethod
    def get_fAP_tank(version, level):
        if version == GameConsts.kTestStr:
            return GameConsts.__FAP_TANK_CONST_TEST
        return GameConsts.__FAP_TANK_CONSTS[level]

    @staticmethod
    def get_base_skill_speed(version, level):
        return GameConsts.__BASE_SKILL_SPEED[level]

    @staticmethod
    def get_base_spell_speed(version, level):
        return GameConsts.__BASE_SPELL_SPEED[level]

    WEAPON_DELAYS = {
        "PLD": 2.24,
        "WAR": 3.36,
        "DRK": 2.96,
        "GNB": 2.80,
        #
        "DRG": 2.80,
        "RPR": 3.20,
        "MNK": 2.56,
        "SAM": 2.64,
        "NIN": 2.56,
        "VPR": 2.64,
        #
        "BRD": 3.04,
        "MCH": 2.64,
        "DNC": 3.12,
        #
        "BLM": 3.28,
        "SMN": 3.12,
        "RDM": 3.44,
        "PCT": 2.96,
        #
        "WHM": 3.44,
        "SCH": 3.12,
        "AST": 3.20,
        "SGE": 2.80,
    }

    # these are not really consts- they depend on your race (eg, lala, au'ra, etc. too).
    HEALER_CASTER_STRENGTH = {
        "SCH": 351,
        "WHM": 214,
        "SGE": 234,
        "AST": 195,
        "SMN": 351,
        "RDM": 214,
        "BLM": 175,
        "PCT": 214,  # guess for now
    }

    JOB_NAME_TO_3_CODE = {
        "Warrior": "WAR",
        "Paladin": "PLD",
        "Gunbreaker": "GNB",
        "DarkKnight": "DRK",
        #
        "WhiteMage": "WHM",
        "Scholar": "SCH",
        "Astrologian": "AST",
        "Sage": "SGE",
        #
        "Ninja": "NIN",
        "Monk": "MNK",
        "Reaper": "RPR",
        "Dragoon": "DRG",
        "Samurai": "SAM",
        "Viper": "VPR",
        #
        "BlackMage": "BLM",
        "Summoner": "SMN",
        "RedMage": "RDM",
        "Pictomancer": "PCT",
        #
        "Dancer": "DNC",
        "Bard": "BRD",
        "Machinist": "MCH",
    }

    JOB_3_CODE_TO_ROLE = {
        "WAR": "Tank",
        "GNB": "Tank",
        "PLD": "Tank",
        "DRK": "Tank",
        #
        "WHM": "Healer",
        "AST": "Healer",
        "SGE": "Healer",
        "SCH": "Healer",
        #
        "BRD": "Ranged",
        "DNC": "Ranged",
        "MCH": "Ranged",
        #
        "SMN": "Caster",
        "RDM": "Caster",
        "BLM": "Caster",
        "PCT": "Caster",
        #
        "MNK": "Melee",
        "DRG": "Melee",
        "SAM": "Melee",
        "RPR": "Melee",
        "NIN": "Melee",
        "VPR": "Melee",
    }
