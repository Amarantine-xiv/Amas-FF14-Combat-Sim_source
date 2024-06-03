import math

from simulator.calcs.compute_damage_utils import ComputeDamageUtils
from simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from simulator.skills.skill_modifier import SkillModifier
from simulator.stats import Stats
from simulator.testing.create_test_skill_library import create_test_skill_library
from simulator.testing.job_class_test_fns import JobClassTestFns
from simulator.testing.test_class import TestClass
from simulator.trackers.status_effects import StatusEffects

class TestComputeDamageUtils(TestClass):
  def __init__(self):
    self.__stats = Stats(wd=126, weapon_delay=3.44, main_stat=2945, det_stat=1620, crit_stat=2377, dh_stat=1048, speed_stat=708, job_class = 'test_job', job_class_fns=JobClassTestFns)
    self.__skill_library = create_test_skill_library()

  @TestClass.is_a_test
  def test_guaranteed_dh_from_status_effects(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_gcd', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(guaranteed_dh=ForcedCritOrDH.FORCE_YES), StatusEffects()))
    expected_base_damage = 18507.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_dh_from_status_effects_and_dh_up(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_gcd', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(guaranteed_dh=ForcedCritOrDH.FORCE_YES, dh_rate_add=0.1), StatusEffects()))
    expected_base_damage = 18969.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_crit_rate_from_status_effects_no_guaranteed(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_gcd', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(crit_rate_add=0.1), StatusEffects()))
    #we shouldn't get any bonus from the crit rate buff, because it's not guaranteed crit
    expected_base_damage = 17742.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_from_status_effects(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_gcd', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(guaranteed_crit=ForcedCritOrDH.FORCE_YES, crit_rate_add=0.1), StatusEffects()))
    expected_base_damage = 18820.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_and_dh_from_status_effects(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_gcd', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(guaranteed_crit=ForcedCritOrDH.FORCE_YES, crit_rate_add=0.1), StatusEffects(guaranteed_dh=ForcedCritOrDH.FORCE_YES, dh_rate_add=0.1)))
    expected_base_damage = 20094.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_base_damage_with_default_condition(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_damage_spec_with_cond', self.__stats.job_class)
    expected_base_damage = 26885.0
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            SkillModifier(),
                                                            self.__stats,
                                                            (StatusEffects(), StatusEffects()))
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg += "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)

    return test_passed, err_msg

  @TestClass.is_a_test
  def test_base_damage_with_condition(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_damage_spec_with_cond', self.__stats.job_class)
    conditions_and_expected_base_damage = (('cond1', 5377.0),
                                           ('cond2', 10754.0))
    for cond, expected_base_damage in conditions_and_expected_base_damage:
      actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                              SkillModifier(with_condition=cond),
                                                              self.__stats,
                                                              (StatusEffects(), StatusEffects()))
      if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
        test_passed = False
        err_msg += "Base damage is not close. Expected: {}. Actual: {}. For cond: {}".format(expected_base_damage, actual_base_damage, cond)

    return test_passed, err_msg

  @TestClass.is_a_test
  def test_pet_tank(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=2.96, main_stat=2906, det_stat=1883, crit_stat=2352, dh_stat=868, speed_stat=650, tenacity=631, job_class = 'test_tank_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_pet_gcd', 'test_tank_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 8741.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_pet_non_tank(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_pet_gcd', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 8484.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_no_crit_no_dh(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_no_crit_dh', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(crit_rate_add=0.25, dh_rate_add=0.2), StatusEffects(crit_rate_add=0.07, dh_rate_add=0.12)))
    expected_base_damage = 17945.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_autos_not_sks(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job2', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('Auto', 'test_job2')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 3254.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_autos(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('Auto', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 3385.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_tank_autos(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_tank_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('Auto', 'test_tank_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 2713.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_healer_autos(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.12, main_stat=2947, det_stat=1695, crit_stat=2255, dh_stat=904, speed_stat=839, job_class = 'test_healer_job', healer_or_caster_strength=351, job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('Auto', 'test_healer_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 135.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_dh_dot_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_crit_dh_dot', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(crit_rate_add=0.25, dh_rate_add=0.2), StatusEffects(crit_rate_add=0.07, dh_rate_add=0.12)))
    expected_base_damage = 1804.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_dh_dot_no_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_crit_dh_dot', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 1419.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_dot_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_crit_dot', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(crit_rate_add=0.32), StatusEffects()))
    expected_base_damage = 1641.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_dot_no_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_crit_dot', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 1377.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_dh_dot_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_dh_dot', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects(dh_rate_add=0.32)))
    expected_base_damage = 1532.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_dh_dot_no_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_dh_dot', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 1419.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_dh_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_dh', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(dh_rate_add=0.2), StatusEffects(dh_rate_add=0.12)))
    expected_base_damage = 19971.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_crit', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(crit_rate_add=0.2), StatusEffects(crit_rate_add=0.12)))
    expected_base_damage = 21396.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_no_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_crit', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 17945.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_dh_no_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_dh', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 18492.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_dh_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_guaranteed_crit_dh', 'test_job')
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(crit_rate_add=0.32), StatusEffects(dh_rate_add=0.32)))
    expected_base_damage = 23527.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_dh_skill_modifier_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_gcd', 'test_job')
    skill_modifier = SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES, guaranteed_dh=ForcedCritOrDH.FORCE_YES)
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(crit_rate_add=0.32), StatusEffects(dh_rate_add=0.32)))
    expected_base_damage = 23527.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_crit_skill_modifier_with_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_gcd', 'test_job')
    skill_modifier = SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES)
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(crit_rate_add=0.2), StatusEffects(crit_rate_add=0.12)))
    expected_base_damage = 21396.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_guaranteed_dh_skill_modifier_no_buffs(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_job', job_class_fns=JobClassTestFns)
    skill = self.__skill_library.get_skill('test_gcd', 'test_job')
    skill_modifier = SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES)
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 18492.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_base_damage(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_gcd', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 17742.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_physical_dot_tick_damage(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_physical_dot_tick', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 2470.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_magical_dot_tick_damage(self):
    test_passed = True
    err_msg = ""

    skill = self.__skill_library.get_skill('test_magical_dot_tick', self.__stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            self.__stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 1921.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_tank_dot_tick_damage(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=2.96, main_stat=2906, det_stat=1883, crit_stat=2352, dh_stat=868, speed_stat=650, tenacity=631, job_class = 'test_tank_job', job_class_fns=JobClassTestFns)

    skill = self.__skill_library.get_skill('test_tank_dot_tick', stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 1103.0

    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_tank_base_damage(self):
    test_passed = True
    err_msg = ""

    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'test_tank_job', job_class_fns=JobClassTestFns)

    skill = self.__skill_library.get_skill('test_tank_gcd', stats.job_class)
    skill_modifier = SkillModifier()
    actual_base_damage = ComputeDamageUtils.get_base_damage(skill,
                                                            skill_modifier,
                                                            stats,
                                                            (StatusEffects(), StatusEffects()))
    expected_base_damage = 4374.0
    if not math.isclose(actual_base_damage, expected_base_damage, abs_tol=1e-4):
      test_passed = False
      err_msg = "Base damage is not close. Expected: {}. Actual: {}.".format(expected_base_damage, actual_base_damage)
    return test_passed, err_msg