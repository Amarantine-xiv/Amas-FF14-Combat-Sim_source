from ama_xiv_combat_sim.simulator.game_data.patch_655.lb_skills.add_lbs_to_skill_library import add_lbs_to_skill_library
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.skills.skill import Skill

def add_generic_skills_to_library(skill_library):
  for job_class in skill_library.get_jobs():
    skill_library.set_current_job_class(job_class)
    skill_library.add_skill(Skill(name='Grade 8 Tincture',
                                  is_GCD= False,
                                  timing_spec=TimingSpec(base_cast_time=0, animation_lock=1300, application_delay=890),
                                  buff_spec=StatusEffectSpec(duration= int(29.97*1000), main_stat_add=262)))
    skill_library.add_skill(Skill(name='Grade 7 Tincture',
                                  is_GCD=False,
                                  timing_spec=TimingSpec(base_cast_time=0, animation_lock=1300, application_delay=890),
                                  buff_spec=StatusEffectSpec(duration= int(29.97*1000), main_stat_add=223)))
    for i in range(0, 10000, 10):
      skill_name = "Wait {:.2f}s".format(i/1000)
      skill_library.add_skill(Skill(name=skill_name,
                                    is_GCD=False,
                                    timing_spec=TimingSpec(base_cast_time=0, animation_lock = i)))
  skill_library = add_lbs_to_skill_library(skill_library)

  return skill_library