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
        self.__test_csv_filename1 = (
            "../ama_xiv_combat_sim/simulator/rotation_import_utils/test_rotation1.csv"
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

    @TestClass.is_a_test
    def test_csv_read(self):
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
                    "test_job2",
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
    def test_csv_read_off_class_conditional_on_job(self):
        self.__stats = Stats(
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
                    "test_job2",
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
        return self._compare_sequential(result, expected)
