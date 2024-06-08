import math
from dataclasses import dataclass


@dataclass(frozen=True)
class JobResourceSettings:
    max_value: int = 0
    skill_allowlist: tuple = ()
    expiry_from_last_gain: int = math.inf
    add_number_to_conditional: bool = True

    def __post_init__(self):
        assert isinstance(
            self.skill_allowlist, tuple
        ), "skill_allowlist must be encoded as a tuple. Did you encode it as a string?"
