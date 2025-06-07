import math

from dataclasses import dataclass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH


@dataclass(frozen=True)
class StatusEffectSpec:
    duration: int = 0
    max_duration: int = None
    num_uses: int = math.inf
    max_num_uses: int = None
    crit_rate_add: float = 0
    dh_rate_add: float = 0
    damage_mult: float = 1
    main_stat_add: float = 0
    main_stat_mult: float = 1
    # auto-attack time is ~= weapon_delay*(1-auto_attack_delay_reduction)
    auto_attack_delay_reduction: float = 0
    # this applies to cast/gcd timer (but NOT necessarily recast time).
    # cast/gcd time is ~= cast_time*(1-haste_time_reduction)
    haste_time_reduction: float = 0
    flat_cast_time_reduction: float = 0
    flat_gcd_recast_time_reduction: float = 0
    # If this buff is re-applied, indicates whether the duration should be extended
    extends_existing_duration: bool = True
    # A tuple of status effects (strings) that this skill will cause to expire on use.
    expires_status_effects: tuple = ()
    # Which skills this status effect can apply to. Can be used in combination with status_effect_denylist.
    skill_allowlist: tuple = None
    guaranteed_crit: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
    guaranteed_dh: ForcedCritOrDH = ForcedCritOrDH.DEFAULT
    add_to_skill_modifier_condition: bool = False
    extend_only: bool = (
        False  # only refresh the given named buff if it is already being applied
    )
    is_party_effect: bool = False
    clear_all_status_effects: bool = False
    damage_reduction: float = None
    # assume only 2 types.
    damage_reduction_phys: float = None
    damage_reduction_magic: float = None
    has_damage_reduction: bool = False

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
        assert (
            isinstance(self.flat_cast_time_reduction, int)
            or self.flat_cast_time_reduction == math.inf
        ), "flat_cast_time_reduction should be an int in ms. Did you put it in seconds?"
        assert isinstance(
            self.expires_status_effects, tuple
        ), "expires_status_effects should be a tuple. Did you accidentally make it a string?"
        assert (
            isinstance(self.skill_allowlist, tuple) or self.skill_allowlist == None
        ), f"skill_allowlist should be a tuple. Did you accidentally make it a string? {self.skill_allowlist}"

        if self.damage_reduction is not None and (
            self.damage_reduction_phys is not None
            or self.damage_reduction_magic is not None
        ):
            raise AssertionError(
                "Cannot specify both 'damage_reduction' and 'damage_reduction_phys' and/or 'damage_reduction_magic. Either specify damage_reduction to apply to both types, or each of _phys and _magic variants."
            )

        if (
            self.damage_reduction_phys is not None
            and self.damage_reduction_magic is None
        ) or (
            self.damage_reduction_phys is None
            and self.damage_reduction_magic is not None
        ):
            raise AssertionError(
                "Need to specify both damage_reduction_phys and damage_reduction_magic if one of them is specified."
            )

        if (
            self.damage_reduction is not None
            or self.damage_reduction_phys is not None
            or self.damage_reduction_magic is not None
        ):
            object.__setattr__(self, "has_damage_reduction", True)

        if self.damage_reduction is None:
            object.__setattr__(self, "damage_reduction", 0.0)

        if self.damage_reduction_phys is None:
            object.__setattr__(self, "damage_reduction_phys", 0.0)

        if self.damage_reduction_magic is None:
            object.__setattr__(self, "damage_reduction_magic", 0.0)

    def __str__(self):
        res = f"   duration:{self.duration}\n"
        res += f"   max_duration: {self.max_duration}\n"
        res += f"   crit_rate_add: {self.crit_rate_add}\n"
        res += f"   dh_rate_add: {self.dh_rate_add}\n"
        res += f"   damage_mult: {self.damage_mult}\n"
        res += f"   main_stat_add: {self.main_stat_add}\n"
        res += f"   auto_attack_delay_reduction: {self.auto_attack_delay_reduction}\n"
        res += f"   haste_time_reduction: {self.haste_time_reduction}\n"
        res += f"   flat_cast_time_reduction: {self.flat_cast_time_reduction}\n"
        res += f"   damage_reduction: {self.damage_reduction}\n"
        res += f"   damage_reduction_phys: {self.damage_reduction_phys}\n"
        res += f"   damage_reduction_magic: {self.damage_reduction_magic}"
        return res
