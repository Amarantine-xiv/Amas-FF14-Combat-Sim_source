import math

from dataclasses import dataclass

from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH


@dataclass(frozen=True)
class StatusEffectSpec:
    duration: int = 0
    max_duration: int = None
    num_uses: int = math.inf
    max_num_uses: int = None
    is_party_effect: bool = False
    is_single_target: bool = False #only need to specify for party effects that are single target
    add_to_skill_modifier_condition: bool = False
    # A tuple of status effects (strings) that this skill will cause to expire on use.
    expires_status_effects: tuple = ()
    # Which skills this status effect can apply to. Can be used in combination with status_effect_denylist.
    skill_allowlist: tuple = None
    # If this buff is re-applied, indicates whether the duration should be extended
    extends_existing_duration: bool = True
    extend_only: bool = (
        False  # only refresh the given named buff if it is already being applied
    )
    guaranteed_crit: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
    guaranteed_dh: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
    does_not_stack_with: frozenset[str] = (
        frozenset()
    )  # set of skill names this effect does not stack with
    clear_all_status_effects: bool = False
    
    def __post_init__(self):
        if self.max_duration is None:
            object.__setattr__(self, "max_duration", self.duration)
        if self.max_num_uses is None:
            object.__setattr__(self, "max_num_uses", self.num_uses)
        assert (
            isinstance(self.duration, int) or self.duration == math.inf
        ), f"duration should be an int in ms. Did you put it in seconds? Value: {self.duration}"
        assert (
            isinstance(self.max_duration, int) or self.max_duration == math.inf
        ), "max_duration should be an int in ms. Did you put it in seconds?"
        assert isinstance(
            self.expires_status_effects, tuple
        ), "expires_status_effects should be a tuple. Did you accidentally make it a string?"
        assert (
            isinstance(self.skill_allowlist, tuple) or self.skill_allowlist == None
        ), f"skill_allowlist should be a tuple. Did you accidentally make it a string? {self.skill_allowlist}"

    def __repr__(self):
        return f"{super().__repr__()}_{type(self).__name__}: ({', '.join('%s=%s' % item for item in vars(self).items())})"
