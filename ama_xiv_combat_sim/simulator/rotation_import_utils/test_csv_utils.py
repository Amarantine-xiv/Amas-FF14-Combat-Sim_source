import copy
import os

from ama_xiv_combat_sim.simulator.rotation_import_utils.csv_utils import CSVUtils
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)


class TestCSVUtils(TestClass):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.realpath(__file__))
        self.__test_csv_filename1 = os.path.join(base_dir, "test_rotation1.csv")
        self.__test_bulk_filename1 = os.path.join(base_dir, "test_bulk_rotation1.csv")
        self.__test_bulk_filename2 = os.path.join(base_dir, "test_bulk_rotation2.csv")
        self.__test_bulk_filename3 = os.path.join(base_dir, "test_bulk_rotation3.csv")
        self.__test_bulk_filename4 = os.path.join(base_dir, "test_bulk_rotation4.csv")
        self.__test_bulk_filename5 = os.path.join(base_dir, "test_bulk_rotation5.csv")
        self.__test_csv_filename_nonexistent_skill = os.path.join(
            base_dir, "test_rotation_nonexistent_skill.csv"
        )
        self.__test_csv_filename_downtime_windows = os.path.join(
            base_dir, "test_rotation_downtime_windows.csv"
        )
        self.__test_csv_filename_multitarget = os.path.join(
            base_dir, "test_rotation_multitarget.csv"
        )
        self.__test_csv_rotation_stats = os.path.join(
            base_dir, "test_rotation_stats.csv"
        )
        self.__test_csv_filename_enable_autos = os.path.join(
            base_dir, "test_rotation_enable_autos.csv"
        )
        self.__test_csv_filename_lb = os.path.join(base_dir, "test_rotation_lb.csv")
        self.__test_csv_filename_start_time = os.path.join(
            base_dir, "test_rotation_start_time.csv"
        )

        self.__skill_library = create_test_skill_library()

        self.__stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )

    def __do_rb_compare(self, result_rbs, expected):
        test_passed = True
        err_msg = ""
        if expected.keys() != result_rbs.keys():
            test_passed = False
            err_msg = f"Did not get expected keys for rotations. Expected: {expected.keys()} vs. Acual: {result_rbs.keys()}"

        for player_name, rb in result_rbs.items():
            result = rb.get_skill_timing().get_q()
            result = [x[1:4] for x in rb.get_skill_timing().get_q()]

            is_passed, this_err_msg = self._compare_sequential(
                result, expected[player_name]
            )
            test_passed &= is_passed
            err_msg += this_err_msg

        return test_passed, err_msg

    @TestClass.is_a_test
    def test_csv_read1(self):
        rb = RotationBuilder(
            self.__stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(rb, self.__test_csv_filename1)

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1650, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3300, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3500, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]

        for tmp, tmp2 in zip(result, expected):
            if tmp != tmp2:
                print("---")
                for i, _ in enumerate(tmp):
                    if tmp[i] != tmp2[i]:
                        print(f"{tmp[i]} vs {tmp2[i]}")

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_read_start_time(self):
        rb = RotationBuilder(
            self.__stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(
            rb, self.__test_csv_filename_start_time
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(100000, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(101650, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(102500, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(103300, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(103500, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]

        for tmp, tmp2 in zip(result, expected):
            if tmp != tmp2:
                print("---")
                for i, _ in enumerate(tmp):
                    if tmp[i] != tmp2[i]:
                        print(f"{tmp[i]} vs {tmp2[i]}")

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_read(self):
        stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job2",
            version="test",
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(rb, self.__test_csv_filename1)

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1650, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3300, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional",
                    "test_job",
                ),
                SkillModifier(with_condition="other"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3500, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_read_headers_nonexistentskill(self):
        stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job2",
            version="test",
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(
            rb, self.__test_csv_filename_nonexistent_skill
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1650, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3300, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional",
                    "test_job",
                ),
                SkillModifier(with_condition="other"),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_read_headers_downtime_windows(self):
        stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job2",
            version="test",
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=True,  # enable autos and check them
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(
            rb, self.__test_csv_filename_downtime_windows
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill(
                    "Auto",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1650, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3300, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional",
                    "test_job",
                ),
                SkillModifier(with_condition="other"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000, 10500),
                self.__skill_library.get_skill(
                    "Auto",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(14500, 15000),
                self.__skill_library.get_skill(
                    "Auto",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(19000, 19500),
                self.__skill_library.get_skill(
                    "Auto",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(100100, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_reader_multitarget(self):
        stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(
            rb, self.__test_csv_filename_multitarget
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_aoe_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3000, None),
                self.__skill_library.get_skill(
                    "test_instant_aoe_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
                ("Boss1", "Boss2", "Boss3"),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6000, None),
                self.__skill_library.get_skill(
                    "test_instant_aoe_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
                ("Boss1", "Boss2"),
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:6] for x in rb.get_skill_timing().get_q()]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_read_headers_stats(self):
        rb = RotationBuilder(
            None,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(rb, self.__test_csv_rotation_stats)
        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1650, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3300, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional",
                    "test_job",
                ),
                SkillModifier(with_condition="other"),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]
        test_passed1, err_msg1 = self._compare_sequential(result, expected)

        expected_stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            tenacity=900,
            job_class="test_job2",
            version="test",
        )

        actual_stats = rb.get_stats()
        test_passed2 = True
        err_msg2 = ""
        if expected_stats != actual_stats:
            test_passed2 = False
            err_msg2 = "Stats did not match"

        return test_passed1 and test_passed2, ",".join([err_msg1, err_msg2])

    @TestClass.is_a_test
    def test_csv_read_headers_enable_autos(self):
        stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job2",
            version="test",
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(
            rb, self.__test_csv_filename_enable_autos
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill(
                    "Auto",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1650, None),
                self.__skill_library.get_skill(
                    "test_ogcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3300, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional",
                    "test_job",
                ),
                SkillModifier(with_condition="other"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4500, 5000),
                self.__skill_library.get_skill(
                    "Auto",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(7500, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_lb(self):
        stats = Stats(
            wd=126,
            weapon_delay=4.5,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job2",
            version="test",
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        rb, _ = CSVUtils.populate_rotation_from_csv(rb, self.__test_csv_filename_lb)

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5650, 7850),
                self.__skill_library.get_skill(
                    "LB 3",
                    self.__stats.job_class,
                ),
                SkillModifier("Mean Damage: 10000"),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:5] for x in rb.get_skill_timing().get_q()]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_csv_read_bulk1(self):
        rb = RotationBuilder(
            None,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            {"player1": copy.deepcopy(rb), "player2": copy.deepcopy(rb)},
            {
                "player1": self.__test_bulk_filename1,
                "player2": self.__test_bulk_filename2,
            },
        )

        expected = {
            "player1": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job",
                    ),
                    SkillModifier(),
                ),
                # buff distributed correctly to player 1
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
            ),
            "player2": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job2"),
                    SkillModifier(),
                ),
            ),
        }
        return self.__do_rb_compare(result_rbs, expected)

    @TestClass.is_a_test
    def test_csv_read_bulk_with_targetted_buff(self):
        rb = RotationBuilder(
            None,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            {
                "player1": copy.deepcopy(rb),
                "player2": copy.deepcopy(rb),
                "player3": copy.deepcopy(rb),
            },
            {
                "player1": self.__test_bulk_filename1,
                "player2": self.__test_bulk_filename2,
                "player3": self.__test_bulk_filename3,
            },
        )

        expected = {
            "player1": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(2000, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
            ),
            "player2": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job2"),
                    SkillModifier(),
                ),
            ),
            "player3": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(2000, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job2"),
                    SkillModifier(),
                ),
            ),
        }

        return self.__do_rb_compare(result_rbs, expected)

    @TestClass.is_a_test
    def test_csv_read_bulk_with_targetted_buff_multi(self):
        rb = RotationBuilder(
            None,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            rb,
            {
                "player1": self.__test_bulk_filename1,
                "player2": self.__test_bulk_filename1,
                "player3": self.__test_bulk_filename5,
                "player4": self.__test_bulk_filename1,
            },
        )

        expected = {
            "player1": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
            ),
            "player2": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
            ),
            "player3": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job2"),
                    SkillModifier(),
                ),
            ),
            "player4": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
            ),
        }
        return self.__do_rb_compare(result_rbs, expected)

    @TestClass.is_a_test
    def test_csv_read_bulk_overriding_condition(self):
        rb = RotationBuilder(
            None,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            {"player1": copy.deepcopy(rb), "player2": copy.deepcopy(rb)},
            {
                "player1": self.__test_bulk_filename1,
                "player2": self.__test_bulk_filename4,
            },
        )

        expected = {
            "player1": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job",
                    ),
                    SkillModifier(),
                ),
                # buff distributed correctly to player 1
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(with_condition="blahblah"),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                    SkillModifier(),
                ),
            ),
            "player2": (
                (
                    SnapshotAndApplicationEvents.EventTimes(0, None),
                    self.__skill_library.get_skill(
                        "test_instant_gcd",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(1200, None),
                    self.__skill_library.get_skill(
                        "test_party_buff",
                        "test_job2",
                    ),
                    SkillModifier(),
                ),
                (
                    SnapshotAndApplicationEvents.EventTimes(3000, None),
                    self.__skill_library.get_skill("test_instant_gcd", "test_job2"),
                    SkillModifier(),
                ),
            ),
        }

        return self.__do_rb_compare(result_rbs, expected)