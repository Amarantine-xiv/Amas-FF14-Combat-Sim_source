from dataclasses import dataclass


@dataclass(frozen=True)
class TriggerSpec:
    triggers: tuple[str] = tuple()

    def __post_init__(self):
        assert isinstance(self.triggers, tuple), "'triggers' field should be a tuple."
