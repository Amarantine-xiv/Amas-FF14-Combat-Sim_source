from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

def get_auto_timing():
  return TimingSpec(base_cast_time=0, animation_lock=0, application_delay=532)

def get_shot_timing():
  return TimingSpec(base_cast_time=0, animation_lock=0, application_delay=758)

def get_cast_gcd_timing_spec():
  return TimingSpec(base_cast_time=1500, animation_lock=100)

def get_instant_timing_spec():
  return TimingSpec(base_cast_time=0, animation_lock=650)