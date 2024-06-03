from ama_xiv_combat_sim import simulator, example_rotations, rotation_analysis, kill_time_estimator
import sys
for i in ['simulator', 'example_rotations', 'rotation_analysis', 'kill_time_estimator']:
  sys.modules[i] = sys.modules['ama_xiv_combat_sim.'+i]