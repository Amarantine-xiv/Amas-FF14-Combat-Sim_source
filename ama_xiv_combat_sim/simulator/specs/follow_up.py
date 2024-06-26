from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FollowUp:
    skill: Any  # This should be Skill, but we don't want to bother with forward declaring classes.
    delay_after_parent_application: int
    snapshot_buffs_with_parent: bool = True
    snapshot_debuffs_with_parent: bool = True
    dot_duration: int = None
    primary_target_only: bool = True
    
    def __post_init__(self):
        assert self.delay_after_parent_application is None or isinstance(
            self.delay_after_parent_application, int
        ), "Delay after parent application should an int to represent ms. Did you put it in seconds?"
        assert (
            self.delay_after_parent_application >= 0
        ), "Follow up skills must have delay_after_parent_application >= 0 (must occur AFTER the parent)"
        assert self.dot_duration is None or isinstance(
            self.dot_duration, int
        ), "Dot duration should either be none, or an int to represent ms. Did you put it in seconds?"

    def __hash__(self):
        return hash(self.skill.name)
