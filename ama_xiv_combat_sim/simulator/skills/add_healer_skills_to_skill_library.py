from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.ast import AstSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sch import SchSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.sge import SgeSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.healer.whm import WhmSkills


def add_healer_skills_to_skill_library(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()

    skill_library.add_all_skills_from(AstSkills(version=version, level=level))
    skill_library.add_all_skills_from(SchSkills(version=version, level=level))
    skill_library.add_all_skills_from(SgeSkills(version=version, level=level))
    skill_library.add_all_skills_from(WhmSkills(version=version, level=level))
    return skill_library
