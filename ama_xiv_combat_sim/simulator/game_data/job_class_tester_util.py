import numpy as np

from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.skills.create_skill_library import (
    create_skill_library,
)
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


class JobClassTesterUtil(TestClass):
    def __init__(self, skill_library):
        super().__init__()
        self.__skill_library = skill_library
        self.__relative_tol = 6e-3

    def test_skills(self, stats, skills_and_expected_damage):
        test_passed = True
        err_msg = ""

        for sk, skill_modifier, expected_damage in skills_and_expected_damage:
            rb = RotationBuilder(stats, self.__skill_library)
            rb.add_next(sk, skill_modifier=skill_modifier)

            db = DamageBuilder(stats, self.__skill_library)
            sim = DamageSimulator(
                rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
            )
            actual_damage = np.mean(sim.get_raw_damage())
            diff = abs(float(expected_damage - actual_damage))
            if diff / expected_damage >= self.__relative_tol:
                test_passed = False
                err_msg += f"Did not get expected damage for '{sk}' / {skill_modifier}. Expected: {expected_damage}. Actual: {int(round(actual_damage, 0))}.\n"
        return test_passed, err_msg

    def test_rotation_damage(self, rb, expected_damage_instances):
        test_passed = True
        err_msg = ""

        db = DamageBuilder(rb.get_stats(), self.__skill_library)
        sim = DamageSimulator(
            rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
        )
        results = [
            (x.skill_name, x.expected_damage) for x in sim.get_per_skill_damage()
        ]

        if len(results) != len(expected_damage_instances):
            test_passed = False
            err_msg += f"Expected {len(expected_damage_instances)} skills returned. Instead got {len(results)}. Skill names: {list(res[0] for res in results)}\n"
            return test_passed, err_msg
        for i, result in enumerate(results):
            result_skill_name, expected_skill_name = (
                result[0],
                expected_damage_instances[i][0],
            )
            if result_skill_name != expected_skill_name:
                test_passed = False
                err_msg += f"Name did not match. Expected: '{expected_skill_name}'. Actual: '{result_skill_name}'\n"
            result_damage, expected_damage = (
                result[1],
                expected_damage_instances[i][1],
            )
            diff = abs(result_damage - expected_damage)

            if diff / max(1e-6, expected_damage) >= 0.005:
                test_passed = False
                err_msg += f"Did not get expected damage for damage instance '{result_skill_name}'. Expected: {expected_damage}. Actual: {int(round(result_damage, 0))}.\n"
        return test_passed, err_msg

    def test_aggregate_rotation(self, rb, expected_damage, expected_total_time):
        test_passed = True
        err_msg = ""

        db = DamageBuilder(rb.get_stats(), self.__skill_library)
        sim = DamageSimulator(
            rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
        )
        actual_damage = np.mean(sim.get_raw_damage())
        damage_diff = abs(float(expected_damage - actual_damage))
        if damage_diff / expected_damage >= self.__relative_tol:
            test_passed = False
            err_msg += f"Did not get expected damage for rotation. Expected: {expected_damage}. Actual: {int(round(actual_damage, 0))}.\n"

        actual_total_time = max(sim.get_damage_time()) - min(sim.get_damage_time())
        if abs(expected_total_time - actual_total_time) > 1e-3:
            test_passed = False
            err_msg += f"Did not get expected total time for rotation. Expected: {expected_total_time}. Actual: {int(round(actual_total_time, 0))}.\n"

        return test_passed, err_msg

    def test_multi_target_skills(self, stats, skills_and_expected_damages):
        test_passed = True
        err_msg = ""

        for i, (
            sk,
            targets,
            skill_modifier,
            expected_damages,
        ) in enumerate(skills_and_expected_damages):
            assert isinstance(
                expected_damages, tuple
            ), "Expected damages must be tuples. Perhaps you forgot a comma?"

            rb = RotationBuilder(stats, self.__skill_library)
            rb.add_next(sk, skill_modifier=skill_modifier, targets=targets)

            db = DamageBuilder(stats, self.__skill_library)
            sim = DamageSimulator(
                rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
            )
            actual_per_skill_damage = sim.get_per_skill_damage()
            if len(expected_damages) != len(actual_per_skill_damage):
                test_passed = False
                err_msg += f"# skills return did not match. Expected: {len(expected_damages)}, Returned: {len(actual_per_skill_damage)}. Entry #: {i}.\n"
                return test_passed, err_msg

            for i, tmp in enumerate(zip(expected_damages, actual_per_skill_damage)):
                expected_damage, per_skill = tmp
                diff = abs(float(expected_damage - per_skill.expected_damage))
                if diff / expected_damage >= self.__relative_tol:
                    test_passed = False
                    err_msg += f"Did not get expected damage for {sk} / {skill_modifier}. Expected: {expected_damage} . Actual: {int(round(per_skill.expected_damage, 0))} at position {i}.\n"
        return test_passed, err_msg
