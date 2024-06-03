from kill_time_estimator.kill_time_estimator import KillTimeEstimator
from simulator.skills.skill_modifier import SkillModifier
from simulator.stats import Stats
from simulator.testing.create_test_skill_library import create_test_skill_library
from simulator.testing.job_class_test_fns import JobClassTestFns
from simulator.testing.test_class import TestClass
from simulator.timeline_builders.rotation_builder import RotationBuilder

class TestKillTimeEstimator(TestClass):
  def __init__(self):
    self.skill_library = create_test_skill_library()
    self.stats = Stats(wd=126, weapon_delay=3.44, main_stat=2945, det_stat=1620, crit_stat=2377, dh_stat=1048, speed_stat=708, job_class = 'test_job', job_class_fns=JobClassTestFns)

  def __get_rotation(self):
    rb = RotationBuilder(self.stats, self.skill_library, fight_start_time=0)
    for i in range(0, 20):
      rb.add(3*i, 'test_instant_gcd')
    return rb

  @TestClass.is_a_test
  def get_kill_time_no_lb(self):
    test_passed = True
    err_msg=""

    boss_hp=420690
    num_samples=20000

    to_add = (tuple(),
              ((17, 'LB 1', 'Exact Damage: 10000'),),
              ((17, 'LB 1', 'Exact Damage: 1000'),
               (20, 'LB 3', 'Mean Damage: 12354.7')))

    all_success = []

    for tmp in to_add:
      kte = KillTimeEstimator(boss_hp=boss_hp)
      rb = self.__get_rotation()
      for skill_to_add in tmp:
        rb.add(skill_to_add[0], skill_name=skill_to_add[1], skill_modifier=SkillModifier(with_condition=skill_to_add[2]))

      kte.add_rotation(rb)
      kill_times, _, _ = kte.estimate_kill_time(num_samples=num_samples, verbose=False)
      kill_time_success = list(filter(lambda x: x is not None, kill_times))
      num_success = len(kill_time_success)
      all_success.append(num_success)

    MARGIN = 0.97
    for i in range(1, len(all_success)):
      #lower all_success slightly to account for some sampling noise
      if MARGIN*all_success[i] < all_success[i-1]:
        test_passed = False
        err_msg = "Adding LB did not seem to have the intended effect on # of success. {} vs {} at index {} with margin {}.".format(all_success[i], all_success[i-1], i, MARGIN)

    return test_passed, err_msg
