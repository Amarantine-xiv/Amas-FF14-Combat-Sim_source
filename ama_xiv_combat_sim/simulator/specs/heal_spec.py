from dataclasses import dataclass


@dataclass(frozen=True)
class HealSpec:
    potency: float = 0
    hot_potency: float = 0  # Healing Over Time potency
    duration: int = 0  # time is in ms
    is_party_effect: bool = False
    heals_damage_at_fraction_taken: float = 0
    is_aoe: bool = False

    min_potency: float = None
    max_potency: float = None
    min_potency_at_fraction_of_max_hp: float = None
    max_potency_at_fraction_of_max_hp: float = None
    guaranteed_crit: bool = False

    def __post_init__(self):
        if self.duration > 0:
            assert (
                self.hot_potency > 0
            ), "Specified a duration in HealSpec, but hot_potency was 0."
