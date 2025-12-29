from typing import NamedTuple

from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import OffensiveStatusEffectSpec

class OffensiveStatusEffectInfo(NamedTuple):
    name: str
    spec: OffensiveStatusEffectSpec