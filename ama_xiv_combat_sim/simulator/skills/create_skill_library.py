import ama_xiv_combat_sim.simulator.game_data.patch_655.generic_skills.add_generic_skills_to_library as add_generic_skills_to_library655
import ama_xiv_combat_sim.simulator.game_data.patch_70.generic_skills.add_generic_skills_to_library as add_generic_skills_to_library70

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

from ama_xiv_combat_sim.simulator.skills.skill_library import SkillLibrary


def create_skill_library(version="6.55"):
    skill_library = SkillLibrary(version)
    skill_library = add_tank_skills_to_skill_library(skill_library, version)
    skill_library = add_healer_skills_to_skill_library(skill_library, version)
    skill_library = add_melee_skills_to_skill_library(skill_library, version)
    skill_library = add_caster_skills_to_skill_library(skill_library, version)
    skill_library = add_ranged_skills_to_skill_library(skill_library, version)

    # Ugly. Clean up as above for class skills.
    match version:
        case "6.55":
            skill_library = (
                add_generic_skills_to_library655.add_generic_skills_to_library(
                    skill_library
                )
            )
        case "7.0":
            skill_library = (
                add_generic_skills_to_library70.add_generic_skills_to_library(
                    skill_library
                )
            )
        case _:
            raise RuntimeError("Bad version: {}".format(version))

    return skill_library
