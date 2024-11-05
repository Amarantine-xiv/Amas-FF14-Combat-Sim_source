import math

from dataclasses import dataclass

@dataclass(frozen=True)
class ChannelingSpec:
    duration: int = 0
    skill_allowlist: tuple = () #if empty, it assumes no skills are allowed
    num_uses: int = math.inf #to be used in conjunction with skill_allowlist, to indicate the ability to channel even if you're using the stated skills
    
    def __post_init__(self):
        assert (
            isinstance(self.duration, int) or self.duration == math.inf
        ), "duration should be an int in ms. Did you put it in seconds? Value was: {self.duration}"
        assert (
            isinstance(self.skill_allowlist, tuple)
        ), f"skill_allowlist should be a tuple. Did you accidentally make it a string? {self.skill_allowlist}"

    def __str__(self):
        res = f"   duration:{self.duration}\n"
        res += f"   skill_allowlist: {self.skill_allowlist}"
        res += f"   num_uses: {self.num_uses}"
        return res
