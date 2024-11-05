from ama_xiv_combat_sim.simulator.game_data.lb_skills.add_lbs_to_skill_library import (
    add_lbs_to_skill_library,
)
from ama_xiv_combat_sim.simulator.game_data.generic_skills.generic_skills_data import (
    all_generic_skills,
)
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts

def __get_clear_all_job_resources_follow_up(name):
    res = FollowUp(
        skill=Skill(
            name=name,
            job_resource_spec=(JobResourceSpec(clear_all_resources_only=True),),
        ),
        delay_after_parent_application=0,
    )
    return res


def __get_clear_all_status_effects_follow_up(name):
    res = FollowUp(
        skill=Skill(
            name=name,
            buff_spec=StatusEffectSpec(clear_all_status_effects=True),
        ),
        delay_after_parent_application=0,
    )
    return res


def __get_clear_all_combos_follow_up(name):
    res = FollowUp(
        skill=Skill(name=name, combo_spec=(ComboSpec(break_all_combos_only=True),)),
        delay_after_parent_application=0,
    )
    return res


def __get_death():
    name = "Death"
    clear_all_job_resources_followup = __get_clear_all_job_resources_follow_up(name)
    clear_all_status_effects_followup = __get_clear_all_status_effects_follow_up(name)
    clear_all_combos_followup = __get_clear_all_combos_follow_up(name)
    res = Skill(
        name=name,
        is_GCD=False,
        timing_spec=TimingSpec(base_cast_time=0, animation_lock=0, application_delay=0),
        follow_up_skills=(
            clear_all_status_effects_followup,
            clear_all_combos_followup,
            clear_all_job_resources_followup,
        ),
    )
    return res


def __get_weakness():
    name = "Weakness"
    clear_all_job_resources_followup = __get_clear_all_job_resources_follow_up(name)
    clear_all_status_effects_followup = __get_clear_all_status_effects_follow_up(name)
    clear_all_combos_followup = __get_clear_all_combos_follow_up(name)
    apply_weakness_followup = FollowUp(
        skill=Skill(
            name=name,
            buff_spec=StatusEffectSpec(duration=int(100 * 1000), main_stat_mult=0.75),
        ),
        delay_after_parent_application=0,
    )
    res = Skill(
        name=name,
        is_GCD=False,
        timing_spec=TimingSpec(base_cast_time=0, animation_lock=0, application_delay=0),
        follow_up_skills=(
            clear_all_status_effects_followup,
            clear_all_combos_followup,
            clear_all_job_resources_followup,
            apply_weakness_followup,
        ),
    )
    return res


def __get_brink():
    name = "Brink of Death"
    clear_all_job_resources_followup = __get_clear_all_job_resources_follow_up(name)
    clear_all_status_effects_followup = __get_clear_all_status_effects_follow_up(name)
    clear_all_combos_followup = __get_clear_all_combos_follow_up(name)
    # Note: weakness will be cleared by clear_all_status_effects_followup
    apply_brink_followup = FollowUp(
        skill=Skill(
            name=name,
            buff_spec=StatusEffectSpec(duration=int(100 * 1000), main_stat_mult=0.50),
        ),
        delay_after_parent_application=0,
    )

    res = Skill(
        name=name,
        is_GCD=False,
        timing_spec=TimingSpec(base_cast_time=0, animation_lock=0, application_delay=0),
        follow_up_skills=(
            clear_all_status_effects_followup,
            clear_all_combos_followup,
            clear_all_job_resources_followup,
            apply_brink_followup,
        ),
    )

    return res


def __add_wait(skill_library):
    for i in range(0, 10000, 10):
        skill_name = f"{SimConsts.WAIT_PREFIX} {i/1000:.2f}s"        
        skill_library.add_skill(
            Skill(
                name=skill_name,
                is_GCD=False,
                timing_spec=TimingSpec(base_cast_time=0, animation_lock=i),
            )
        )
    return skill_library


def __get_pot(name, main_stat_add, version, level):
    all_generic_skills.set_version(version)
    all_generic_skills.set_level(level)
    res = Skill(
        name=name,
        is_GCD=False,
        timing_spec=TimingSpec(
            base_cast_time=0,
            animation_lock=all_generic_skills.get_skill_data(name, "animation_lock"),
            application_delay=all_generic_skills.get_skill_data(name, "application_delay"),
        ),
        buff_spec=StatusEffectSpec(
            duration=int(29.97 * 1000), main_stat_add=main_stat_add
        ),
    )
    return res


def add_generic_skills_to_library(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()
    for job_class in skill_library.get_jobs():
        skill_library.set_current_job_class(job_class)
        if version not in ["6.55"]:
            skill_library.add_skill(__get_pot("Grade 1 Gemdraught", 351, version, level))
        if version not in ["6.55", "7.0", "7.01"]:
            skill_library.add_skill(__get_pot("Grade 2 Gemdraught", 392, version, level))
            
        skill_library.add_skill(
            __get_pot(
                "Grade 8 Tincture",
                262,
                version,
                level,
            )
        )
        skill_library.add_skill(
            __get_pot(
                "Grade 7 Tincture",
                223,
                version,
                level,
            )
        )
        skill_library.add_skill(__get_death())
        skill_library.add_skill(__get_weakness())
        skill_library.add_skill(__get_brink())
        skill_library = __add_wait(skill_library)

    skill_library = add_lbs_to_skill_library(skill_library)

    return skill_library
