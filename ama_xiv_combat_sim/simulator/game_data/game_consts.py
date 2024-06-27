from dataclasses import dataclass


@dataclass(frozen=True)
class GameConsts:
    GCD_RECAST_TIME: float = 2500
    DOT_TICK_INTERVAL = 3000
    COMBO_EXPIRATION_TIME = 30 * 1000
    DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES = 500
    DH_DAMAGE_MULT_BONUS = 0.25
    MIN_GCD_RECAST_TIME = 1500
    MULTI_TARGET_DELAY_PER_TARGET = 135
    # level mods from akhmorning

    # Key is the version. This is interpreted as stats at max-level for now.
    # __LEVEL_DIVS = {"6.55": 1900, "7.0": 2780, "test": 1900}
    # __LEVEL_MAINS = {"6.55": 390, "7.0": 440, "test": 390}
    # __LEVEL_SUBS = {"6.55": 400, "7.0": 420, "test": 400}
    # __FAP_CONSTS = {"6.55": 195, "7.0": 225, "test": 195}
    # __FAP_TANK_CONSTS = {"6.55": 156, "7.0": 180, "test": 156}

    __LEVEL_DIVS = {"6.55": 1900, "7.0": 1900, "test": 1900}
    __LEVEL_MAINS = {"6.55": 390, "7.0": 390, "test": 390}
    __LEVEL_SUBS = {"6.55": 400, "7.0": 400, "test": 400}
    __FAP_CONSTS = {"6.55": 195, "7.0": 195, "test": 195}
    __FAP_TANK_CONSTS = {"6.55": 156, "7.0": 156, "test": 156}

    __SPEED_CONSTS = {"6.55": 130, "7.0": 130, "test": 130}
    __CRIT_CONSTS = {
        "6.55": (200, 50, 400),
        "7.0": (200, 50, 400),
        "test": (200, 50, 400),
    }

    __DH_CONSTS = {"6.55": 550, "7.0": 550, "test": 550}

    __DET_CONSTS = {"6.55": 140, "7.0": 140, "test": 140}

    __TEN_CONSTS = {"6.55": 100, "7.0": 100, "test": 100}

    @staticmethod
    def get_speed_const(version, level):
        return GameConsts.__SPEED_CONSTS[version]

    @staticmethod
    def get_crit_consts(version, level):
        return GameConsts.__CRIT_CONSTS[version]

    @staticmethod
    def get_dh_const(version, level):
        return GameConsts.__DH_CONSTS[version]

    @staticmethod
    def get_det_const(version, level):
        return GameConsts.__DET_CONSTS[version]

    @staticmethod
    def get_ten_const(version, level):
        return GameConsts.__TEN_CONSTS[version]

    @staticmethod
    def get_level_div(version, level):
        return GameConsts.__LEVEL_DIVS[version]

    @staticmethod
    def get_level_main(version, level):
        return GameConsts.__LEVEL_MAINS[version]

    @staticmethod
    def get_level_sub(version, level):
        return GameConsts.__LEVEL_SUBS[version]

    @staticmethod
    def get_fAP(version, level):
        return GameConsts.__FAP_CONSTS[version]

    @staticmethod
    def get_fAP_tank(version, level):
        return GameConsts.__FAP_TANK_CONSTS[version]

    BASE_SKILL_SPEED = 400
    BASE_SPELL_SPEED = 400

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
        #
        "BRD": 3.04,
        "MCH": 2.64,
        "DNC": 3.12,
        #
        "BLM": 3.28,
        "SMN": 3.12,
        "RDM": 3.44,
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
        #
        "BlackMage": "BLM",
        "Summoner": "SMN",
        "RedMage": "RDM",
        "Dancer": "DNC",
        "Bard": "BRD",
        "Machinist": "MCH",
    }
