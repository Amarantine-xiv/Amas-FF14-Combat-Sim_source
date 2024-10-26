from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.trackers.status_effects import StatusEffects


class TestDamageSimulator(TestClass):
    def __init__(self):
        super().__init__()
        self.__stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=708,
            job_class="test_job",
            version="test",
        )
        self.__skill_library = create_test_skill_library()
        self.__relative_tol = 6e-3

    @TestClass.is_a_test
    def test_trait_damage_mult_override(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=708,
            job_class="test_job2",
            version="test",
        )
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job2"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_gcd_trait_override", "test_job2"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
        ]

        sim = DamageSimulator(stats, dmg_instances, 2)
        expected_trait_damage_mult = [1.4, 1.0]
        actual_trait_damage_mult = sim.get_trait_damage_mult()
        return self._compare_sequential(
            actual_trait_damage_mult, expected_trait_damage_mult
        )

    @TestClass.is_a_test
    def test_guaranteed_crit_dh_dot(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_guaranteed_crit_dot", "test_job"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_guaranteed_dh_dot", "test_job"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill(
                    "test_guaranteed_crit_dh_dot", "test_job"
                ),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        expected_crit = [1, self.__stats.processed_stats.crit_rate, 1]
        expected_dh = [self.__stats.processed_stats.dh_rate, 1, 1]
        (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
        (test_passed_crit, err_msg_crit) = self._compare_sequential(
            actual_crit, expected_crit
        )
        (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
        return test_passed_crit and test_passed_dh, err_msg_crit + err_msg_dh

    @TestClass.is_a_test
    def test_guaranteed_no_crit_dh(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill(
                    "test_guaranteed_no_crit_dh", "test_job"
                ),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
        ]

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        expected_crit = [self.__stats.processed_stats.crit_rate, 0]
        expected_dh = [self.__stats.processed_stats.dh_rate, 0]
        (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
        (test_passed_crit, err_msg_crit) = self._compare_sequential(
            actual_crit, expected_crit
        )
        (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
        return test_passed_crit and test_passed_dh, err_msg_crit + err_msg_dh

    @TestClass.is_a_test
    def test_guaranteed_crit_dh_from_status_effects(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (
                    StatusEffects(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                    StatusEffects(),
                ),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (
                    StatusEffects(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                    StatusEffects(),
                ),
                2,
                "t1",
            ),
        ]

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        expected_crit = [1, self.__stats.processed_stats.crit_rate]
        expected_dh = [self.__stats.processed_stats.dh_rate, 1]
        (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
        (test_passed_crit, err_msg_crit) = self._compare_sequential(
            actual_crit, expected_crit
        )
        (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
        return test_passed_crit and test_passed_dh, err_msg_crit + err_msg_dh

    @TestClass.is_a_test
    def test_guaranteed_crit_dh(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_guaranteed_crit", "test_job"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_guaranteed_dh", "test_job"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill("test_guaranteed_crit_dh", "test_job"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        expected_crit = [1, self.__stats.processed_stats.crit_rate, 1]
        expected_dh = [self.__stats.processed_stats.dh_rate, 1, 1]
        (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
        (test_passed_crit, err_msg_crit) = self._compare_sequential(
            actual_crit, expected_crit
        )
        (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
        return test_passed_crit and test_passed_dh, err_msg_crit + err_msg_dh

    @TestClass.is_a_test
    def test_guaranteed_crit_dh_with_skill_modifier(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        expected_crit = [1, self.__stats.processed_stats.crit_rate, 1]
        expected_dh = [self.__stats.processed_stats.dh_rate, 1, 1]
        (actual_crit, actual_dh) = sim.get_crit_and_dh_rates()
        (test_passed_crit, err_msg_crit) = self._compare_sequential(
            actual_crit, expected_crit
        )
        (test_passed_dh, err_msg_dh) = self._compare_sequential(actual_dh, expected_dh)
        return test_passed_crit and test_passed_dh, err_msg_crit + err_msg_dh

    @TestClass.is_a_test
    def test_get_expected_damage_per_damage_instance(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        actual_expected_damage_per_damage_instance = (
            sim.get_expected_damage_per_damage_instance()
        )
        expected_damage_per_damage_instance = [29861.59, 26761.51, 37197.00]
        return self._compare_sequential(
            actual_expected_damage_per_damage_instance,
            expected_damage_per_damage_instance,
            relative_tol=self.__relative_tol,
        )

    @TestClass.is_a_test
    def test_get_variance_damage_per_damage_instance(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        actual_variance_per_damage_instance = sim.get_variance_per_damage_instance()
        expected_variance_per_damage_instance = [8482156.56, 38493911.5, 1153200.0]
        return self._compare_sequential(
            actual_variance_per_damage_instance,
            expected_variance_per_damage_instance,
            relative_tol=self.__relative_tol,
        )

    @TestClass.is_a_test
    def test_get_expected_damage(self):
        test_passed = True
        err_msg = ""
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]
        expected_expected_damage = 93820.10

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        actual_expected_damage = sim.get_expected_damage()

        diff = abs(float(expected_expected_damage - actual_expected_damage))
        if diff / expected_expected_damage >= self.__relative_tol:
            test_passed = False
            err_msg += f"Did not get expected expected damage. Expected: {expected_expected_damage}. Actual: {round(actual_expected_damage, 2)}.\n"
        return test_passed, err_msg

    @TestClass.is_a_test
    def test_get_damage_variance(self):
        test_passed = True
        err_msg = ""
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]
        expected_damage_variance = 48129268.11

        sim = DamageSimulator(self.__stats, dmg_instances, 2)
        actual_damage_variance = sim.get_damage_variance()

        diff = abs(float(expected_damage_variance - actual_damage_variance))
        if diff / expected_damage_variance >= self.__relative_tol:
            test_passed = False
            err_msg += f"Did not get expected expected damage. Expected: {expected_damage_variance}. Actual: {round(actual_damage_variance, 2)}.\n"
        return test_passed, err_msg

    @TestClass.is_a_test
    def test_get_per_skill_damage_mean_and_stds(self):
        dmg_instances = [
            (
                0,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                1,
                "t1",
            ),
            (
                1000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
                2,
                "t1",
            ),
            (
                2000,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    guaranteed_dh=ForcedCritOrDH.FORCE_YES,
                ),
                (StatusEffects(), StatusEffects()),
                3,
                "t1",
            ),
        ]

        # no samples
        sim = DamageSimulator(self.__stats, dmg_instances, 0)
        per_skill_damage = sim.get_per_skill_damage()

        expected_means = [29867, 26763, 37201]
        expected_stds = [2912, 6204, 1074]
        actual_means = list(
            curr_per_skill_damage.expected_damage
            for curr_per_skill_damage in per_skill_damage
        )
        actual_stds = list(
            curr_per_skill_damage.standard_deviation
            for curr_per_skill_damage in per_skill_damage
        )
        (test_passed_expected_damage, err_msg_expected_damage) = (
            self._compare_sequential(actual_means, expected_means, relative_tol=1e-3)
        )
        (test_passed_std, err_msg_std) = self._compare_sequential(
            actual_stds, expected_stds, relative_tol=1e-3
        )
        return (
            test_passed_expected_damage and test_passed_std,
            err_msg_expected_damage + err_msg_std,
        )
