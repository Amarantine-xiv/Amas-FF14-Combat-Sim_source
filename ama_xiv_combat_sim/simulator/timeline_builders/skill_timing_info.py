from dataclasses import dataclass, field
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)


@dataclass(frozen=True)
class SkillTimingInfo:
    snapshot_and_application_events: SnapshotAndApplicationEvents
    downtime_windows: dict = field(default_factory=dict)
