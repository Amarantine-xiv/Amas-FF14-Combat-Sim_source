from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.blm import BlmSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.pct import PctSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.rdm import RdmSkills
from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.smn import SmnSkills

def add_caster_skills_to_skill_library(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()
    
    skill_library.add_all_skills_from(BlmSkills(version=version, level=level))    
    skill_library.add_all_skills_from(RdmSkills(version=version, level=level))
    skill_library.add_all_skills_from(SmnSkills(version=version, level=level))
    
    if version >= "7.0":
        skill_library.add_all_skills_from(PctSkills(version=version, level=level))
    return skill_library
