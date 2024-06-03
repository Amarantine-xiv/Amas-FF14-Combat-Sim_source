from dataclasses import dataclass

@dataclass(frozen=True)
class ComboSpec:
  combo_actions: tuple = tuple()
  combo_group: int = 0
  combo_auto_succeed: bool = False