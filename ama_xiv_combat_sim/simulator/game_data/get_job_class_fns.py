import ama_xiv_combat_sim.simulator.game_data.job_class_fns as unified
#we shouldn't put testing here...
import ama_xiv_combat_sim.simulator.game_data.testing.job_class_fns as testing

def get_job_class_fns(version):
    if version == 'test':
        return testing.JobClassFns
    else:
        return unified.JobClassFns
        