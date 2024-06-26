
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import create_test_skill_library
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.trackers.status_effects import StatusEffects

class TestDamageSimulator(TestClass):
  def __init__(self):
    self.__stats = Stats(wd=126, weapon_delay=3.44, main_stat=2945, det_stat=1620, crit_stat=2377, dh_stat=1048, speed_stat=708, job_class = 'test_job', version="test")
    self.__skill_library = create_test_skill_library()

  @TestClass.is_a_test
  def test_trait_damage_mult_override(self):
    stats = Stats(wd=126, weapon_delay=3.44, main_stat=2945, det_stat=1620, crit_stat=2377, dh_stat=1048, speed_stat=708, job_class = 'test_job2', version="test")
    dmg_instances = [
                 (0, self.__skill_library.get_skill('test_gcd', 'test_job2'), SkillModifier(), (StatusEffects(), StatusEffects()),1, 't1'),
                 (1000, self.__skill_library.get_skill('test_gcd_trait_override', 'test_job2'), SkillModifier(), (StatusEffects(), StatusEffects()),2, 't1')]

    sim = DamageSimulator(stats, dmg_instances, 2)
    expected_trait_damage_mult = [1.4, 1.0]
    actual_trait_damage_mult = sim.get_trait_damage_mult()
    return self._compare_sequential(actual_trait_damage_mult, expected_trait_damage_mult)

  @TestClass.is_a_test
  def test_guaranteed_crit_dh_dot(self):
    dmg_instances = [
                 (0, self.__skill_library.get_skill('test_guaranteed_crit_dot', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),1, 't1'),
                 (1000, self.__skill_library.get_skill('test_guaranteed_dh_dot', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),2, 't1'),
                 (2000, self.__skill_library.get_skill('test_guaranteed_crit_dh_dot', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),3, 't1')]

    sim = DamageSimulator(self.__stats, dmg_instances, 2)
    expected_crit = [1, self.__stats.processed_stats.crit_rate, 1]
    expected_dh = [self.__stats.processed_stats.dh_rate, 1, 1]
    (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
    (test_passed_crit, err_msg_crit) = self._compare_sequential(actual_crit, expected_crit)
    (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
    return test_passed_crit and test_passed_dh, err_msg_crit+err_msg_dh

  @TestClass.is_a_test
  def test_guaranteed_no_crit_dh(self):
    dmg_instances = [
                 (0, self.__skill_library.get_skill('test_gcd', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),1, 't1'),
                 (2000, self.__skill_library.get_skill('test_guaranteed_no_crit_dh', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),2, 't1')]

    sim = DamageSimulator(self.__stats, dmg_instances, 2)
    expected_crit = [self.__stats.processed_stats.crit_rate, 0]
    expected_dh = [self.__stats.processed_stats.dh_rate, 0]
    (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
    (test_passed_crit, err_msg_crit) = self._compare_sequential(actual_crit, expected_crit)
    (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
    return test_passed_crit and test_passed_dh, err_msg_crit+err_msg_dh

  @TestClass.is_a_test
  def test_guaranteed_crit_dh_from_status_effects(self):
    dmg_instances = [
                 (0, self.__skill_library.get_skill('test_instant_gcd', 'test_job'), SkillModifier(), (StatusEffects(guaranteed_crit=ForcedCritOrDH.FORCE_YES), StatusEffects()),1, 't1'),
                 (1000, self.__skill_library.get_skill('test_instant_gcd', 'test_job'), SkillModifier(), (StatusEffects(guaranteed_dh=ForcedCritOrDH.FORCE_YES), StatusEffects()),2, 't1')]

    sim = DamageSimulator(self.__stats, dmg_instances, 2)
    expected_crit = [1, self.__stats.processed_stats.crit_rate]
    expected_dh = [self.__stats.processed_stats.dh_rate, 1]
    (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
    (test_passed_crit, err_msg_crit) = self._compare_sequential(actual_crit, expected_crit)
    (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
    return test_passed_crit and test_passed_dh, err_msg_crit+err_msg_dh

  @TestClass.is_a_test
  def test_guaranteed_crit_dh(self):
    dmg_instances = [
                 (0, self.__skill_library.get_skill('test_guaranteed_crit', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),1, 't1'),
                 (1000, self.__skill_library.get_skill('test_guaranteed_dh', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),2, 't1'),
                 (2000, self.__skill_library.get_skill('test_guaranteed_crit_dh', 'test_job'), SkillModifier(), (StatusEffects(), StatusEffects()),3, 't1')]

    sim = DamageSimulator(self.__stats, dmg_instances, 2)
    expected_crit = [1, self.__stats.processed_stats.crit_rate, 1]
    expected_dh = [self.__stats.processed_stats.dh_rate, 1, 1]
    (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
    (test_passed_crit, err_msg_crit) = self._compare_sequential(actual_crit, expected_crit)
    (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
    return test_passed_crit and test_passed_dh, err_msg_crit+err_msg_dh

  @TestClass.is_a_test
  def test_guaranteed_crit_dh_with_skill_modifier(self):
    dmg_instances = [
                 (0, self.__skill_library.get_skill('test_gcd', 'test_job'), SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES), (StatusEffects(), StatusEffects()),1, 't1'),
                 (1000, self.__skill_library.get_skill('test_gcd', 'test_job'), SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES), (StatusEffects(), StatusEffects()),2, 't1'),
                 (2000, self.__skill_library.get_skill('test_gcd', 'test_job'), SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES, guaranteed_dh=ForcedCritOrDH.FORCE_YES), (StatusEffects(), StatusEffects()),3, 't1')]

    sim = DamageSimulator(self.__stats, dmg_instances, 2)
    expected_crit = [1, self.__stats.processed_stats.crit_rate, 1]
    expected_dh = [self.__stats.processed_stats.dh_rate, 1, 1]
    (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
    (test_passed_crit, err_msg_crit) = self._compare_sequential(actual_crit, expected_crit)
    (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
    return test_passed_crit and test_passed_dh, err_msg_crit+err_msg_dh