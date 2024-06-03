from dataclasses import dataclass

@dataclass(frozen=True)
class GameConsts:
  GCD_RECAST_TIME: float = 2500
  DOT_TICK_INTERVAL = 3000
  COMBO_EXPIRATION_TIME = 30*1000
  DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES = 500
  DH_DAMAGE_MULT_BONUS = 0.25
  # level mods from akhmorning
  LEVEL_DIVS = {90: 1900}
  LEVEL_MAINS= {90: 390}
  LEVEL_SUBS= {90: 400}
  FAP_CONSTS = {90: 195}
  FAP_TANK_CONSTS = {90: 156}

  BASE_SKILL_SPEED = 400
  BASE_SPELL_SPEED = 400

  WEAPON_DELAYS = {
    'PLD': 2.24,
    'WAR': 3.36, 
    'DRK': 2.96,
    'GNB': 2.80,
    #
    'DRG': 2.80,
    'RPR': 3.20,
    'MNK': 2.56,
    'SAM': 2.64,
    'NIN': 2.56,
    #
    'BRD': 3.04,
    'MCH': 2.64,
    'DNC': 3.12,
    #
    'BLM': 3.28,
    'SMN': 3.12,
    'RDM': 3.44,
    #
    'WHM': 3.44,
    'SCH': 3.12,
    'AST': 3.20,
    'SGE': 2.80
  }

  # these are not really consts- they depend on your race (eg, lala, au'ra, etc. too).
  HEALER_CASTER_STRENGTH= {
    "SCH": 351,
    "WHM": 214,
    "SGE": 234,
    "AST": 195,
    "SMN": 351,
    "RDM": 214,
    "BLM": 175,
  }

  JOB_NAME_TO_3_CODE = {
    'Warrior': 'WAR',
    'Paladin': 'PLD',
    'Gunbreaker': 'GNB',
    'DarkKnight': 'DRK',
    #
    'WhiteMage': 'WHM',
    'Scholar': 'SCH',
    'Astrologian': 'AST',
    'Sage': 'SGE',
    #
    'Ninja': 'NIN',
    'Monk': 'MNK',
    'Reaper': 'RPR',
    'Dragoon': 'DRG',
    'Samurai': 'SAM',
    #
    'BlackMage': 'BLM',
    'Summoner': 'SMN',
    'RedMage': 'RDM',
    'Dancer': 'DNC',
    'Bard': 'BRD',
    'Machinist': 'MCH'
  }