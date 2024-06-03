import math
from dataclasses import dataclass

@dataclass(frozen=True)
class JobResourceSpec:
  name: str = ""
  change: int= 0
  duration: int = math.inf

  # Does not refresh the charges on their own. This is for keeping tracking of
  # expirations of an entire resource at once (like enochian). See
  # JobResourceSettings.expiry_from_last_gain
  refreshes_duration_of_last_gained: bool = False