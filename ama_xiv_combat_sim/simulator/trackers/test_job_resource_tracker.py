from simulator.skills.skill import Skill
from simulator.skills.skill_modifier import SkillModifier
from simulator.specs.job_resource_settings import JobResourceSettings
from simulator.specs.job_resource_spec import JobResourceSpec
from simulator.testing.test_class import TestClass
from simulator.testing.create_test_skill_library import create_test_skill_library
from simulator.trackers.job_resource_tracker import JobResourceTracker

class TestJobResourceTracker(TestClass):
  def __init__(self):
    self.__skill_library = create_test_skill_library()

  @TestClass.is_a_test
  def test_resource_expiry_with_refresh(self):
    job_resource_tracker = JobResourceTracker({'Gauge': JobResourceSettings(max_value=100, expiry_from_last_gain=15*1000, skill_allowlist=('test_instant_gcd',))})

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec=(JobResourceSpec("Gauge", 10, refreshes_duration_of_last_gained= True),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec=(JobResourceSpec("Gauge", 20, refreshes_duration_of_last_gained= True),))
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(10000, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(20000, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_instant_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(21000, test_skill)]
    expected = ['40 Gauge']
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_resource_expiry(self):
    job_resource_tracker = JobResourceTracker({'Gauge': JobResourceSettings(max_value=100, expiry_from_last_gain=15*1000, skill_allowlist=('test_instant_gcd',))})

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec=(JobResourceSpec("Gauge", 10, refreshes_duration_of_last_gained= True),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec=(JobResourceSpec("Gauge", 20, refreshes_duration_of_last_gained= True),))
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(20000, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_instant_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(21000, test_skill)]
    expected = ['20 Gauge']
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_resource_limits_compile(self):
    job_resource_tracker = JobResourceTracker({'Gauge': JobResourceSettings(max_value=100, skill_allowlist=('test_instant_gcd',))})

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec=(JobResourceSpec("Gauge", 10000),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec=(JobResourceSpec("Gauge", -2000),))
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(1000, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_instant_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(100, test_skill),
              job_resource_tracker.compile_job_resources(2000, test_skill)]
    expected = ['100 Gauge', '']
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_two_resources_one_empty_compile(self):
    job_resource_tracker = JobResourceTracker({'Gauge': JobResourceSettings(max_value=100, skill_allowlist=('test_gcd',)),
                                               'Heat': JobResourceSettings(max_value=50, skill_allowlist=('test_instant_gcd',))})

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec=(JobResourceSpec("Heat", 10),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec=(JobResourceSpec("Heat", 20),))
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(0, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_instant_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(1, test_skill)]
    expected = ['30 Heat']
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_two_resources_compile(self):
    job_resource_tracker = JobResourceTracker({'Gauge': JobResourceSettings(max_value=100, skill_allowlist=('test_instant_gcd',)),
                                               'Heat': JobResourceSettings(max_value=50, skill_allowlist=('test_instant_gcd',))})

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec=(JobResourceSpec("Gauge", 10),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec=(JobResourceSpec("Heat", 20, duration=10*1000),))
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(0, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_instant_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(1, test_skill),
              job_resource_tracker.compile_job_resources(15*1000, test_skill)]
    expected = ['30 Gauge, 20 Heat', '30 Gauge']
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_simple_expired(self):
    job_resource_tracker = JobResourceTracker(self.__skill_library.get_all_resource_settings('test_job'))

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec= (JobResourceSpec("Gauge", 10, duration=10*1000),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec= (JobResourceSpec("Gauge", 20, duration=10*1000),))
    job_resource_tracker.add_resource(0, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(10*1000, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_instant_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(15*1000, test_skill,)]
    expected = ['20 Gauge']
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_compile_not_in_allowlist(self):
    job_resource_tracker = JobResourceTracker(self.__skill_library.get_all_resource_settings('test_job'))

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec= (JobResourceSpec("Gauge", 10),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec= (JobResourceSpec("Gauge", 20),))
    job_resource_tracker.add_resource(5, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(10, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(0, test_skill),
              job_resource_tracker.compile_job_resources(20, test_skill)]
    expected = ['', '']
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_simple_compile(self):
    job_resource_tracker = JobResourceTracker(self.__skill_library.get_all_resource_settings('test_job'))

    resource_spec1 = Skill(name='resource_spec1',
                           job_resource_spec= (JobResourceSpec("Gauge", 10),))
    resource_spec2 = Skill(name='resource_spec2',
                           job_resource_spec= (JobResourceSpec("Gauge", 20),))
    job_resource_tracker.add_resource(5, resource_spec1, SkillModifier())
    job_resource_tracker.add_resource(10, resource_spec2, SkillModifier())
    test_skill = self.__skill_library.get_skill('test_instant_gcd', 'test_job')

    result = [job_resource_tracker.compile_job_resources(0, test_skill),
              job_resource_tracker.compile_job_resources(20, test_skill)]
    expected = ['', '30 Gauge']
    return self._compare_sequential(result, expected)