from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import OffensiveStatusEffectSpec
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass


class TestOffensiveStatusEffectSpec(TestClass):
    @TestClass.is_a_test
    def test_max_duration(self):
        test_passed = True
        err_msg = ""

        duration = 10000
        status_effect_spec = OffensiveStatusEffectSpec(duration=duration)
        if status_effect_spec.max_duration != duration:
            test_passed = False
            err_msg = "Max duration set incorrectly. Expected{} but got {}".format(
                duration, status_effect_spec.max_duration
            )

        return test_passed, err_msg

    @TestClass.is_a_test
    def test_set_max_duration(self):
        test_passed = True
        err_msg = ""

        duration = 10000
        max_duration = 30000
        status_effect_spec = OffensiveStatusEffectSpec(
            duration=duration, max_duration=max_duration
        )
        if status_effect_spec.max_duration != max_duration:
            test_passed = False
            err_msg = f"Max duration set incorrectly. Expected: {max_duration} vs actual {status_effect_spec.max_duration}".format()

        return test_passed, err_msg
