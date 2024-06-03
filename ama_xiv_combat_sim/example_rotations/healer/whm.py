from simulator.stats import Stats
from simulator.timeline_builders.rotation_builder import RotationBuilder

def get_rotation_WHM(skill_library):
  stats = Stats(wd=132, weapon_delay=3.44, main_stat=3369, det_stat=1941, crit_stat=2502, dh_stat=580, speed_stat=1296, job_class='WHM')
  rotation_name = 'WHM 6.55'

  rb = RotationBuilder(stats, skill_library, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
  rb.add_next('Grade 8 Tincture')
  rb.add_next('Glare III')
  rb.add_next('Dia')
  rb.add_next('Glare III')
  rb.add_next('Glare III')
  rb.add_next('Presence of Mind')
  rb.add_next('Glare III')
  rb.add_next('Assize')
  rb.add_next('Glare III', num_times=10)
  return (rotation_name, rb)