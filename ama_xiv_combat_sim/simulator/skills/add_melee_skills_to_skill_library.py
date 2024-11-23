from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.drg import DrgSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.mnk import MnkSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.nin import NinSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.rpr import RprSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.sam import SamSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.vpr import VprSkills


def add_melee_skills_to_skill_library(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()

    skill_library.add_all_skills_from(DrgSkills(version=version, level=level))
    skill_library.add_all_skills_from(MnkSkills(version=version, level=level))
    skill_library.add_all_skills_from(NinSkills(version=version, level=level))
    skill_library.add_all_skills_from(RprSkills(version=version, level=level))
    skill_library.add_all_skills_from(SamSkills(version=version, level=level))

    if version >= "7.0":
        skill_library.add_all_skills_from(VprSkills(version=version, level=level))

    return skill_library
