import ama_xiv_combat_sim.simulator.game_data.patch_655.job_class_fns as patch655
import ama_xiv_combat_sim.simulator.game_data.patch_70.job_class_fns as patch70
#we shouldn't put testing here...
import ama_xiv_combat_sim.simulator.game_data.testing.job_class_fns as testing

def get_job_class_fns(version):
    match version:
        case "6.55":
            return patch655.JobClassFns
        case "7.0":
            return patch70.JobClassFns
        case "test":
            return testing.JobClassFns
        case _:
            raise RuntimeError("Bad version: {}".format(version))
        