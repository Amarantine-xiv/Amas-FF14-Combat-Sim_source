from enum import Enum

class DamageClass(Enum):
    UNKNOWN = 0
    DIRECT = 1
    MAGICAL_DOT = 2
    PHYSICAL_DOT = 3
    AUTO = 4
    PET = 5