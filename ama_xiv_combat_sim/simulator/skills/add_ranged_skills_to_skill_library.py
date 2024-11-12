from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.brd import BrdSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.dnc import DncSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.ranged.mch import MchSkills

def add_ranged_skills_to_skill_library(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()
    
    skill_library.add_all_skills_from(BrdSkills(version=version, level=level))
    skill_library.add_all_skills_from(DncSkills(version=version, level=level))
    skill_library.add_all_skills_from(MchSkills(version=version, level=level))
    return skill_library
