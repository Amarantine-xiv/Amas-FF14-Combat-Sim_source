from simulator.game_data.get_job_class_fns import get_job_class_fns
from simulator.skills.skill import Skill
from simulator.specs.damage_spec import DamageSpec
from simulator.specs.timing_spec import TimingSpec


# the LB timings don't seem to work out based on the data I've seen for EW...not sure why?
# data is from: https://docs.google.com/document/d/1JK9BKbW49Kye5V60jD16rvzmliurLE1Ngq6Z7-WubKI
def __add_tank_lb(skill_library):
    skill_library.add_skill(
        Skill(
            name="LB 1",
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=1930, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 2",
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=3860, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 3",
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=3860, application_delay=0
            ),
        )
    )
    return skill_library


def __add_healer_lb(skill_library):
    skill_library.add_skill(
        Skill(
            name="LB 1",
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=2100, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 2",
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=5130, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 3",
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=8100, application_delay=0
            ),
        )
    )
    return skill_library


def __add_melee_lb(skill_library):
    skill_library.add_skill(
        Skill(
            name="LB 1",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=3860, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 2",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=3000, animation_lock=3860, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 3",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=4500, animation_lock=3700, application_delay=2200
            ),
        )
    )
    return skill_library


def __add_caster_lb(skill_library):
    skill_library.add_skill(
        Skill(
            name="LB 1",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=3100, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 2",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=3000, animation_lock=5100, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 3",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=4500, animation_lock=8100, application_delay=0
            ),
        )
    )
    return skill_library


def __add_phys_ranged_lb(skill_library):
    skill_library.add_skill(
        Skill(
            name="LB 1",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=2000, animation_lock=3100, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 2",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=3000, animation_lock=3100, application_delay=0
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="LB 3",
            damage_spec=DamageSpec(potency=0),
            timing_spec=TimingSpec(
                base_cast_time=4500, animation_lock=3700, application_delay=0
            ),
        )
    )
    return skill_library


def add_lbs_to_skill_library(skill_library):
    job_class_fns = get_job_class_fns(version="6.55")
    for job_class in skill_library.get_jobs():
        skill_library.set_current_job_class(job_class)

        if job_class_fns.isTank(job_class):
            skill_library = __add_tank_lb(skill_library)
        elif job_class_fns.isHealer(job_class):
            skill_library = __add_healer_lb(skill_library)
        elif job_class_fns.isMelee(job_class):
            skill_library = __add_melee_lb(skill_library)
        elif job_class_fns.isCaster(job_class):
            skill_library = __add_caster_lb(skill_library)
        elif job_class_fns.isPhysRanged(job_class):
            skill_library = __add_phys_ranged_lb(skill_library)
        else:
            raise RuntimeError(
                "Job does not belong to any known roles?: {}".format(job_class)
            )
    return skill_library
