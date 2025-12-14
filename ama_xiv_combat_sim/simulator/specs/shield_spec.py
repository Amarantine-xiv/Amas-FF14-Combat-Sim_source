from dataclasses import dataclass


@dataclass(frozen=True)
class ShieldSpec:
    is_party_effect: bool = False
    shield_on_max_hp: float = 0  # for shields granted as % of max hp
    shield_on_your_max_hp: float = 0  # primarily for pld...
    does_not_stack_with: frozenset[str] = frozenset()  # set of skill names this ShieldSpec will not stack with    
    shield_mult_on_hp_restored: float = (
        0  # shield on hp restored (eg, patch 7.3 concitation would be 1.8)
    ),
    shield_as_perc_of_max_hp: float = 0,
    duration: int = 0 #time in ms
    potency: int = 0 # use this to calc shield strength as if it was a heal, but applied as a shield
    is_party_effect: bool = False
    is_aoe: bool = False
    potency: float = 0