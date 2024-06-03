from simulator.stats import Stats
from simulator.timeline_builders.rotation_builder import RotationBuilder

def get_rotation_MNK(skill_library):
  stats = Stats(wd=132, weapon_delay=2.56, main_stat=3356, det_stat=1453, crit_stat=2647, dh_stat=1453, speed_stat=771, job_class = 'MNK')
  rotation_name = 'MNK 6.55, 1.94 gcd'
  rb = RotationBuilder(stats, skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)

  rb.add_next('Form Shift')
  rb.add_next('Dragon Kick')
  rb.add_next('Grade 8 Tincture')
  rb.add_next('Twin Snakes')
  rb.add_next('Riddle of Fire')
  rb.add_next('Demolish')
  rb.add_next('The Forbidden Chakra')
  rb.add_next('Bootshine')
  rb.add_next('Brotherhood')
  rb.add_next('Perfect Balance')
  rb.add_next('Dragon Kick')
  rb.add_next('Riddle of Wind')
  rb.add_next('Bootshine')
  rb.add_next('Dragon Kick')
  rb.add_next('Elixir Field')
  rb.add_next('Bootshine')
  rb.add_next('Perfect Balance')
  rb.add_next('Twin Snakes')
  rb.add_next('Dragon Kick')
  rb.add_next('Demolish')
  rb.add_next('Rising Phoenix')
  return (rotation_name, rb)
