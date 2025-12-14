from ama_xiv_combat_sim.simulator.skills.add_caster_skills_to_skill_library import (
    add_caster_skills_to_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.add_healer_skills_to_skill_library import (
    add_healer_skills_to_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.add_melee_skills_to_skill_library import (
    add_melee_skills_to_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.add_ranged_skills_to_skill_library import (
    add_ranged_skills_to_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.add_tank_skills_to_skill_library import (
    add_tank_skills_to_skill_library,
)

import ama_xiv_combat_sim.simulator.game_data.generic_skills.add_generic_skills_to_library as add_generic_skills_to_library

from ama_xiv_combat_sim.simulator.skills.skill_library import SkillLibrary


def create_skill_library(version="6.55", level=100)->SkillLibrary:
    skill_library = SkillLibrary(version, level)
    skill_library = add_tank_skills_to_skill_library(skill_library)
    skill_library = add_healer_skills_to_skill_library(skill_library)
    skill_library = add_ranged_skills_to_skill_library(skill_library)
    skill_library = add_caster_skills_to_skill_library(skill_library)    
    skill_library = add_melee_skills_to_skill_library(skill_library)
    
    skill_library = add_generic_skills_to_library.add_generic_skills_to_library(
        skill_library
    )

    return skill_library
