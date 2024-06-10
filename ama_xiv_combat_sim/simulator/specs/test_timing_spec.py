from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass

class TestTimingSpec(TestClass):

  @TestClass.is_a_test
  def gcd_override_gcd_test(self):
    test_passed = True
    err_msg=""
    timing_spec = TimingSpec(base_cast_time=2000)
    if timing_spec.gcd_base_recast_time != 2500:
      err_msg = "Recast time was expected to be 2500, but it was {}.".format(timing_spec.gcd_base_recast_time)
      test_passed = False
    return test_passed, err_msg

  @TestClass.is_a_test
  def gcd_override_set_recast_time(self):
    test_passed = True
    err_msg=""
    timing_spec = TimingSpec(base_cast_time=2000, gcd_base_recast_time=1500)
    if timing_spec.gcd_base_recast_time != 1500:
      err_msg = "Recast time was expected to be 1500, but it was {}.".format(timing_spec.gcd_base_recast_time)
      test_passed = False
    return test_passed, err_msg