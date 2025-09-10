from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass

from ama_xiv_combat_sim.simulator.calcs.damage_instance_class import DamageInstanceClass


class TestDefensiveStatusEffectSpec(TestClass):

    @TestClass.is_a_test
    def test_specific_reductions(self):
        test_passed = True
        err_msg = ""
        spec = DefensiveStatusEffectSpec(
            damage_reductions={
                DamageInstanceClass.PHYSICAL: 0.1,
                DamageInstanceClass.MAGICAL: 0.05,
            },
        )
        dr_keys = tuple(spec.damage_reductions.keys())
        if (
            DamageInstanceClass.PHYSICAL not in dr_keys
            or DamageInstanceClass.MAGICAL not in dr_keys
        ):
            err_msg = "defensive_spec is missing expected damage reductions"
            test_passed = False
        return test_passed, err_msg

    @TestClass.is_a_test
    def test_all_reductions(self):
        test_passed = True
        err_msg = ""
        spec = DefensiveStatusEffectSpec(
            damage_reductions=0.2,
        )
        dr_keys = set(spec.damage_reductions.keys())
        expected_types = set(
            [
                DamageInstanceClass.UNKNOWN,
                DamageInstanceClass.PHYSICAL,
                DamageInstanceClass.MAGICAL,
            ]
        )
        if dr_keys != expected_types:
            err_msg = f"DefensiveStatusEffectSpec is missing expected damage reductions: {dr_keys}"
            test_passed = False
        for k, v in spec.damage_reductions.items():
            if v != 0.2:
                err_msg += f"\nDefensiveStatusEffectSpec did not have the right reduction value for: {k}"
                test_passed = False
        return test_passed, err_msg

    @TestClass.is_a_test
    def test_reductions_invalid(self):
        test_passed = True
        err_msg = ""

        try:
            _ = DefensiveStatusEffectSpec(
                damage_reductions=(0.2, 0.3),
            )
            err_msg = "Did not catch bad specification of damage_reductions."
            test_passed = False
        except AssertionError:
            pass

        return test_passed, err_msg
