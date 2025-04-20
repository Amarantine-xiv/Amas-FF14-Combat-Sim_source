from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)

from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


class TestRotationBuilder(TestClass):
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

    @TestClass.is_a_test
    def test_downtime_windows(self):
        # intentionally have really long delay
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
            enable_autos=True,
            fight_start_time=0,
            downtime_windows=((1, 10), (15.4, 20.2)),
        )

        rb.add(0, "test_instant_gcd")
        rb.add(2, "test_instant_gcd")
        rb.add(7, "test_simple_buff_gcd")
        rb.add(11.1, "test_instant_gcd")
        rb.add(15.3, "test_instant_gcd")
        rb.add(17.3, "test_instant_gcd")
        rb.add(
            18.1, "test_gcd"
        )  # this will snapshot at 20.1s, which is during downtime, so it should ghost
        rb.add(23.1, "test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(7000, None),
                self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000, 10500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11100, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(14500, 15000),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(15300, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            # this auto is delayed by casting
            (
                SnapshotAndApplicationEvents.EventTimes(20600, 21100),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(23100, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_downtime_windows_no_autos(self):
        # intentionally have really long delay
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
            enable_autos=True,
            fight_start_time=0,
            downtime_windows={
                "Default Target": (
                    (387.027, 399.01, DamageClass.AUTO),
                    (383, 500, DamageClass.PET),
                )
            },
        )

        rb.add(383, "test_physical_long_dot_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 385500),
                self.__skill_library.get_skill(
                    "test_physical_long_dot_gcd", "test_job"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 385500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 388500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 391500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 394500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 397500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 400500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 403500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 406500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 409500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 412500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385500, 386000),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(399010.0, 399510.0),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(403510.0, 404010.0),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(408010.0, 408510.0),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_downtime_windows_idempotent(self):
        # intentionally have really long delay
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
            enable_autos=True,
            fight_start_time=0,
            downtime_windows=((1, 10), (15.4, 20.2)),
        )

        rb.add(0, "test_instant_gcd")
        rb.add(2, "test_instant_gcd")
        rb.add(7, "test_simple_buff_gcd")
        rb.add(11.1, "test_instant_gcd")
        rb.add(15.3, "test_instant_gcd")
        rb.add(17.3, "test_instant_gcd")
        rb.add(
            18.1, "test_gcd"
        )  # this will snapshot at 20.1s, which is during downtime, so it should ghost
        rb.add(23.1, "test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(7000, None),
                self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000, 10500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11100, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(14500, 15000),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(15300, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            # this auto is delayed by casting
            (
                SnapshotAndApplicationEvents.EventTimes(20600, 21100),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(23100, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        # test double call
        _ = rb.get_skill_timing().get_q()
        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_downtime_windows_with_dot(self):
        # intentionally have really long delay
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
            enable_autos=True,
            fight_start_time=0,
            downtime_windows={"Default Target": ((387.027, 399.01),)},
        )

        rb.add(383, "test_physical_long_dot_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 385500),
                self.__skill_library.get_skill(
                    "test_physical_long_dot_gcd", "test_job"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 385500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 400500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 403500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 406500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 409500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385000, 412500),
                self.__skill_library.get_skill("test_physical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(385500, 386000),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(399010.0, 399510.0),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(403510.0, 404010.0),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(408010.0, 408510.0),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_multi_target_downtime_windows(self):
        # intentionally have really long delay
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
            enable_autos=True,
            fight_start_time=0,
            downtime_windows=({"Boss1": ((8, 14.7),), "Boss2": ((18.1, 100),)}),
            ignore_trailing_dots=True,
        )
        rb.add(0, "test_instant_gcd", targets="Boss1")
        rb.add(3, "test_magical_dot_gcd", targets="Boss1")
        rb.add(9, "test_instant_gcd", targets="Boss2")
        rb.add(12, "test_magical_dot_gcd", targets="Boss2")
        rb.add(15, "test_instant_gcd", targets="Boss1")
        rb.add(18, "test_instant_gcd", targets="Boss1")
        rb.add(21, "test_instant_gcd", targets="Boss1")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5000, 5500),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5000, 5500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5000, 17500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5500, 6000),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(14000, 14500),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(14000, 14500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(14000, 17500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(14700, 15200),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(15000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(18000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(21000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:6] for i in range(0, len(result))]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_multi_target_downtime_windows_with_shift(self):
        # intentionally have really long delay
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
            enable_autos=True,
            downtime_windows=({"Boss1": ((8, 14.7),), "Boss2": ((18.1, 100),)}),
            ignore_trailing_dots=True,
        )
        rb.add(0, "test_gcd", targets="Boss1")
        rb.add(3, "test_magical_dot_gcd", targets="Boss1")
        rb.add(9, "test_instant_gcd", targets="Boss2")
        rb.add(12, "test_magical_dot_gcd", targets="Boss2")
        rb.add(15, "test_instant_gcd", targets="Boss1")
        rb.add(18, "test_instant_gcd", targets="Boss1")
        rb.add(21, "test_instant_gcd", targets="Boss1")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(-500, 0),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, 3000),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, 3000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, 15000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4500, 5000),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6500, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11500, 12000),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11500, 12000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11500, 15000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(12200, 12700),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss2",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(12500, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(15500, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(18500, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
                ("Boss1",),
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:6] for i in range(0, len(result))]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_bonus_percent(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )
        rb = RotationBuilder(stats, self.__skill_library, fight_start_time=0)

        rb.add_next("test_combo_pos", skill_modifier=SkillModifier(bonus_percent=68))
        rb.add_next(
            "test_combo_pos",
            skill_modifier=SkillModifier(with_condition="No Combo", bonus_percent=29),
        )
        rb.add_next(
            "test_combo_pos",
            skill_modifier=SkillModifier(with_condition="To Ignore", bonus_percent=63),
        )
        rb.add_next(
            "test_combo_pos",
            skill_modifier=SkillModifier(with_condition="To Ignore", bonus_percent=29),
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_combo_pos", "test_job"),
                SkillModifier(with_condition=SimConsts.DEFAULT_CONDITION),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, None),
                self.__skill_library.get_skill("test_combo_pos", "test_job"),
                SkillModifier(with_condition="No Combo"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5000, None),
                self.__skill_library.get_skill("test_combo_pos", "test_job"),
                SkillModifier(with_condition="To Ignore, No Positional"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(7500, None),
                self.__skill_library.get_skill("test_combo_pos", "test_job"),
                SkillModifier(with_condition="To Ignore, No Combo"),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_damage_with_buff_follow_up(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )
        rb = RotationBuilder(stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_damage_with_debuff_follow_up")

        # include priority and event id
        expected = (
            (
                0,
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_damage_with_debuff_follow_up", "test_job"
                ),
                SkillModifier(),
                [True, True],
                (SimConsts.DEFAULT_TARGET,),
                0,
            ),
            (
                1,
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("follow_up_debuff", "test_job"),
                SkillModifier(),
                [True, True],
                (SimConsts.DEFAULT_TARGET,),
                1,
            ),
        )

        result = [x[0:7] for x in rb.get_skill_timing().get_q()]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_combo(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )
        rb = RotationBuilder(stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_combo0")
        rb.add_next("test_combo1")
        rb.add_next("test_combo1")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_combo0", "test_job"),
                SkillModifier(with_condition=SimConsts.COMBO_SUCCESS),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, None),
                self.__skill_library.get_skill("test_combo1", "test_job"),
                SkillModifier(with_condition=SimConsts.COMBO_SUCCESS),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5000, None),
                self.__skill_library.get_skill("test_combo1", "test_job"),
                SkillModifier(with_condition=SimConsts.COMBO_FAIL),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_job_resource(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )
        rb = RotationBuilder(stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_skill_add_gauge")
        rb.add_next("test_skill_use_gauge")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_skill_add_gauge", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(35, None),
                self.__skill_library.get_skill("test_skill_use_gauge", "test_job"),
                SkillModifier(with_condition="10 Gauge"),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_adding_conditional(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )
        rb = RotationBuilder(stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_skill_with_conditional")
        rb.add_next("test_instant_gcd")
        rb.add_next("test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_skill_with_conditional", "test_job"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(35, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(with_condition="test_skill_with_conditional"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2535, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_buff_with_num_uses_and_cast_reduction(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )
        rb = RotationBuilder(stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_num_uses_buff_with_cast_reduction")
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_num_uses_buff_with_cast_reduction", "test_job"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(35, 535),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(35 + 2500, 35 + 2500 + 500),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    35 + 5000 + 2000, 35 + 5000 + 2500
                ),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_auto_on_first_damage_instance(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job",
            version="test",
        )
        rb = RotationBuilder(
            stats, self.__skill_library, enable_autos=True, fight_start_time=0
        )
        rb.add_next("test_simple_buff_gcd")
        rb.add_next("test_instant_gcd")
        rb.add_next("test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, 3000),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_auto_on_first_damage_instance_timestamp(self):
        rb = RotationBuilder(
            self.__stats, self.__skill_library, enable_autos=True, fight_start_time=0
        )
        rb.add(0, "test_simple_buff_gcd")
        rb.add(2, "test_instant_gcd")
        rb.add(4, "test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2000, 2500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_job_auto_delay_reduction_trait(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job_haste",
            version="test",
        )
        rb = RotationBuilder(
            stats, self.__skill_library, enable_autos=True, fight_start_time=0
        )
        rb.add(0, "test_instant_gcd")
        rb.add(10, "test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill("Auto", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2750, 3250),
                self.__skill_library.get_skill("Auto", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5500, 6000),
                self.__skill_library.get_skill("Auto", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8250, 8750),
                self.__skill_library.get_skill("Auto", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_job_haste_trait(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=400,
            job_class="test_job_haste",
            version="test",
        )
        rb = RotationBuilder(
            stats, self.__skill_library, enable_autos=False, fight_start_time=0
        )
        rb.add_next("test_instant_gcd")
        rb.add_next("test_instant_gcd")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5500, 6000),
                self.__skill_library.get_skill("test_gcd", "test_job_haste"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_with_cond_follow_up(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(
            0,
            "test_follow_up_with_cond",
            skill_modifier=SkillModifier(with_condition="1"),
        )
        rb.add(
            10,
            "test_follow_up_with_cond",
            skill_modifier=SkillModifier(with_condition="2"),
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_follow_up_with_cond", "test_job"),
                SkillModifier(with_condition="1"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11940, 12440),
                self.__skill_library.get_skill("test_follow_up_with_cond", "test_job"),
                SkillModifier(with_condition="2"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11940, 12440),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11940, 15440),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_with_cond_buff_spec(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next(
            "test_buff_with_cond", skill_modifier=SkillModifier(with_condition="crit")
        )
        rb.add_next(
            "test_buff_with_cond", skill_modifier=SkillModifier(with_condition="dh")
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_buff_with_cond", self.__stats.job_class
                ),
                SkillModifier(with_condition="crit"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2440, None),
                self.__skill_library.get_skill(
                    "test_buff_with_cond", self.__stats.job_class
                ),
                SkillModifier(with_condition="dh"),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_with_cond_timing_spec(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next(
            "test_timing_spec_with_cond",
            skill_modifier=SkillModifier(with_condition="instant"),
        )
        rb.add_next(
            "test_timing_spec_with_cond",
            skill_modifier=SkillModifier(with_condition="cast"),
        )

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_timing_spec_with_cond", self.__stats.job_class
                ),
                SkillModifier(with_condition="instant"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4380, 4880),
                self.__skill_library.get_skill(
                    "test_timing_spec_with_cond", self.__stats.job_class
                ),
                SkillModifier(with_condition="cast"),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_snap_dots_to_server_tick_starting_at(self):
        rb = RotationBuilder(
            self.__stats,
            self.__skill_library,
            snap_dots_to_server_tick_starting_at=-1.5,
            fight_start_time=0,
        )
        rb.add(1.0, "test_magical_dot_gcd")
        rb.add(29.06, "test_magical_dot_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 4500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 7500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 10500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 13500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 16500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(31000, 31500),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(31000, 31500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(31000, 34500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(31000, 37500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(31000, 40500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(31000, 43500),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_ignore_trailing_dot(self):
        rb = RotationBuilder(
            self.__stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            fight_start_time=0,
        )
        rb.add(1, "test_magical_dot_gcd")
        rb.add(8, "test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 6440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 9440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 10440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_buff_then_damage(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_buff_then_damage")
        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_buff_then_damage", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "_test_buff_then_damage", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_flat_cast_time_reduction_add(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_gcd_1500_lock")
        rb.add(1.6, "test_flat_cast_time_reduction")
        rb.add(6, "test_gcd_1500_lock")
        rb.add(9, "test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(960, 1460),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1600, None),
                self.__skill_library.get_skill(
                    "test_flat_cast_time_reduction", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6000, 6500),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9000, 9500),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_flat_cast_time_reduction_add_next(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd_1500_lock")
        rb.add_next("test_flat_cast_time_reduction")
        rb.add_next("test_gcd_1500_lock")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(960, 1460),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1460 + 50, None),
                self.__skill_library.get_skill(
                    "test_flat_cast_time_reduction", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2440, 2940),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4880, 5380),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_add_next_const_and_no_speed_skills(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_haste_buff1")
        rb.add_next("test_gcd_1500_const_cast")
        rb.add_next("test_gcd_1500_no_haste")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_haste_buff1", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1000, 1500),
                self.__skill_library.get_skill(
                    "test_gcd_1500_const_cast", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2500 + 1460 - 500, 2500 + 1460),
                self.__skill_library.get_skill(
                    "test_gcd_1500_no_haste", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_add_const_and_no_speed_skills(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_haste_buff1")
        rb.add(3, "test_gcd_1500_const_cast")
        rb.add(6, "test_gcd_1500_no_haste")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_haste_buff1", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4000, 4500),
                self.__skill_library.get_skill(
                    "test_gcd_1500_const_cast", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6000 + 1460 - 500, 6000 + 1460),
                self.__skill_library.get_skill(
                    "test_gcd_1500_no_haste", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_stable_skill_sequence(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_instant_gcd_no_lock")
        rb.add_next("test_haste_buff1")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_haste_buff1", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd_no_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_simple_with_haste(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_haste_buff1")
        rb.add(1, "test_simple_buff_gcd")
        rb.add(3, "test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_haste_buff1", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1000, None),
                self.__skill_library.get_skill(
                    "test_simple_buff_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4330, 4830),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_simple_with_haste_followup(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_haste_follow_up")
        rb.add(3, "test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_haste_follow_up", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "_test_haste_follow_up", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4330, 4830),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_add_next_with_haste(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd")
        rb.add_next("test_haste_buff1")
        rb.add_next("test_gcd")
        rb.add_next("test_haste_buff2")
        rb.add_next("test_gcd_1500_lock")
        rb.add_next("test_gcd_1500_lock")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2440 + 5, None),
                self.__skill_library.get_skill(
                    "test_haste_buff1", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    2440 + 5 + 0.75 * 2440 - 500, 2440 + 5 + 0.75 * 2440
                ),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    2440 + 5 + 0.75 * 2440 + 5, None
                ),
                self.__skill_library.get_skill(
                    "test_haste_buff2", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    (2440 + 5 + 0.75 * 2440 + 5) + 980 - 500,
                    (2440 + 5 + 0.75 * 2440 + 5) + 980,
                ),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    ((2440 + 5 + 0.75 * 2440 + 5) + 1640) + 980 - 500,
                    ((2440 + 5 + 0.75 * 2440 + 5) + 1640) + 980,
                ),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_add_next_with_haste_followup(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd")
        rb.add_next("test_haste_follow_up")
        rb.add_next("test_gcd")
        rb.add_next("test_haste_buff2")
        rb.add_next("test_gcd_1500_lock")
        rb.add_next("test_gcd_1500_lock")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2440 + 5, None),
                self.__skill_library.get_skill(
                    "test_haste_follow_up", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2440 + 5, None),
                self.__skill_library.get_skill(
                    "_test_haste_follow_up", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    2440 + 5 + 0.75 * 2440 - 500, 2440 + 5 + 0.75 * 2440
                ),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    2440 + 5 + 0.75 * 2440 + 5, None
                ),
                self.__skill_library.get_skill(
                    "test_haste_buff2", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    (2440 + 5 + 0.75 * 2440 + 5) + 980 - 500,
                    (2440 + 5 + 0.75 * 2440 + 5) + 980,
                ),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    ((2440 + 5 + 0.75 * 2440 + 5) + 1640) + 980 - 500,
                    ((2440 + 5 + 0.75 * 2440 + 5) + 1640) + 980,
                ),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_gcd_ogcd_with_animation_locks(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd")
        rb.add_next("test_ogcd_animation_lock")
        rb.add_next("test_instant_gcd")
        rb.add_next("test_gcd_1500_lock")
        rb.add_next("test_ogcd_animation_lock")
        rb.add_next("test_ogcd_animation_lock")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2445, None),
                self.__skill_library.get_skill(
                    "test_ogcd_animation_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2480, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5880, 6380),
                self.__skill_library.get_skill(
                    "test_gcd_1500_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6430, None),
                self.__skill_library.get_skill(
                    "test_ogcd_animation_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6465, None),
                self.__skill_library.get_skill(
                    "test_ogcd_animation_lock", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9300, 9800),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_add_next_with_instants(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd")
        rb.add_next("test_instant_gcd")
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2445, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    2 * 2440 + 1940 + 5, 3 * 2440 + 5
                ),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    3 * 2440 + 1940 + 10, 4 * 2440 + 10
                ),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_add_next_simple(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2440 + 1940 + 5, 2 * 2440 + 5),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    2 * 2440 + 1940 + 10, 3 * 2440 + 10
                ),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(
                    3 * 2440 + 1940 + 15, 4 * 2440 + 15
                ),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_autos_with_buff_on_follow_up(self):
        rb = RotationBuilder(
            self.__stats, self.__skill_library, enable_autos=True, fight_start_time=0
        )
        rb.add(0.1, "test_auto_attack_buff_on_follow_up")  # comes out after first auto
        rb.add(2.54, "test_instant_gcd")
        rb.add(4, "test_simple_buff_gcd")  # should do nothing
        rb.add(17.44, "test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2040, 2540),
                self.__skill_library.get_skill(
                    "test_auto_attack_buff_on_follow_up", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2040, 2540),
                self.__skill_library.get_skill(
                    "test_auto_attack_buff_instant_follow_up", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2540, 3040),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2540, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4000, None),
                self.__skill_library.get_skill(
                    "test_simple_buff_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5120, 5620),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(7700, 8200),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10280, 10780),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(12860, 13360),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(16300, 16800),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(17440, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_autos_with_casts(self):
        rb = RotationBuilder(
            self.__stats, self.__skill_library, enable_autos=True, fight_start_time=0
        )
        rb.add(14.0, "test_gcd")  # will NOT auto
        rb.add(2.5, "test_gcd")  # will delay auto
        rb.add(8.0, "test_gcd")  # will delay auto

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(4440, 4940),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4940, 5440),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 10440),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10440, 10940),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(13880, 14380),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(15940, 16440),
                self.__skill_library.get_skill("test_gcd", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_autos_with_buffs(self):
        rb = RotationBuilder(
            self.__stats, self.__skill_library, enable_autos=True, fight_start_time=0
        )
        rb.add(0.1, "test_auto_attack_buff")  # comes out after first auto
        rb.add(2.54, "test_instant_gcd")
        rb.add(4, "test_simple_buff_gcd")  # should do nothing
        rb.add(17.44, "test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2040, 2540),
                self.__skill_library.get_skill(
                    "test_auto_attack_buff", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2540, 3040),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2540, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4000, None),
                self.__skill_library.get_skill(
                    "test_simple_buff_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5120, 5620),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(7700, 8200),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10280, 10780),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(12860, 13360),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(16300, 16800),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(17440, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_autos(self):
        rb = RotationBuilder(
            self.__stats, self.__skill_library, enable_autos=True, fight_start_time=0
        )
        rb.add(2.54, "test_instant_gcd")
        rb.add(17.44, "test_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2540, 3040),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2540, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5980, 6480),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9420, 9920),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(12860, 13360),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(16300, 16800),
                self.__skill_library.get_skill("Auto", self.__stats.job_class),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(17440, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def pass_through_skill_modifier(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0.2, "test_gcd", SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES))

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2140, 2640),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def simple_dot(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(1.0, "test_magical_dot_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 6440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 9440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 12440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 15440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def simple_ground_dot(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(1.0, "test_ground_dot_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_ground_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, False],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 6440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, False],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 9440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, False],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 12440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, False],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 15440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, False],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def dot_with_early_refresh(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(1.0, "test_magical_dot_gcd")
        rb.add(8.0, "test_magical_dot_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 6440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 9440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 10440),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 10440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 13440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 16440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 19440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 22440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def dot_with_early_refresh_from_instant_dot_gcd(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(1.0, "test_magical_dot_gcd")
        rb.add(8.0, "test_magical_dot_instant_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 6440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, None),
                self.__skill_library.get_skill(
                    "test_magical_dot_instant_gcd", "test_job"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, None),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, 11000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, 14000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, 17000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, 20000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def dot_refresh_with_other_follow_up(self):
        # this is a more complex test because dot refreshes are more likely to mess up the ordering
        # of skills
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)

        rb.add(1.0, "test_magical_dot_gcd_with_other_follow_up")
        rb.add(8.0, "test_magical_dot_gcd_with_other_follow_up")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill(
                    "test_magical_dot_gcd_with_other_follow_up", "test_job"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 3440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 6440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2940, 9440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 10440),
                self.__skill_library.get_skill(
                    "test_magical_dot_gcd_with_other_follow_up", "test_job"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 10440),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 10440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 13440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 16440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 19440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9940, 22440),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def skill_follow_up_test_non_dot(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_follow_up")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 3000 + 2440),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [False, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(7000 + 2440, None),
                self.__skill_library.get_skill("test_non_dot_follow_up", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def party_buff_application(self):
        # For a 2500 ms gcd, this spell speed should result in a 2440 sm (2.44s) GCD.
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)

        rb.add(0, "test_party_buff", job_class="test_job2")
        rb.add(3, "test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_party_buff", "test_job2"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4940, 5440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def skill_timing_test_no_buffs_no_dot(self):
        # For a 2500 ms gcd, this spell speed should result in a 2440 sm (2.44s) GCD.
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_gcd")
        rb.add(3.5, "test_gcd")
        rb.add(2.4, "test_ogcd")
        rb.add(4.0, "test_gcd_with_app_delay")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2400, None),
                self.__skill_library.get_skill("test_ogcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(3500 + 1940, 3500 + 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4000 + 1940, 4000 + 2440 + 100),
                self.__skill_library.get_skill("test_gcd_with_app_delay", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_dot_set_target(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_magical_dot_instant_gcd", targets="t1")

        # include priority and event id
        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_magical_dot_instant_gcd", "test_job"
                ),
                SkillModifier(),
                [True, True],
                ("t1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, 3000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, 6000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, 9000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1",),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, 12000),
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                ("t1",),
            ),
        )

        result = [x[1:6] for x in rb.get_skill_timing().get_q()]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_follow_up_all_target_only(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_follow_up_for_multi_target_main", targets="t1, t2")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_follow_up_for_multi_target_main", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
                ("t1", "t2"),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_folllow_up_for_multi_target", self.__stats.job_class
                ),
                SkillModifier(),
                [True, True],
                ("t1", "t2"),
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:6] for x in rb.get_skill_timing().get_q()]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_follow_up_primary_target_only(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_follow_up_for_multi_target_primary_only", targets="t1, t2")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_follow_up_for_multi_target_primary_only",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
                ("t1", "t2"),
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill(
                    "test_folllow_up_for_multi_target_primary_only",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
                ("t1",),
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [x[1:6] for x in rb.get_skill_timing().get_q()]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_off_class_job_condition(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_instant_gcd")
        rb.add(3, "test_off_class_conditional", job_class="test_job2")
        rb.add(6, "test_instant_gcd")
        rb.add(
            15,
            "test_off_class_conditional",
            job_class="test_job2",
            skill_modifier=SkillModifier(with_condition="mega"),
        )
        rb.add(20, "test_instant_gcd")

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
                SnapshotAndApplicationEvents.EventTimes(3000, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional", "test_job2"
                ),
                SkillModifier(with_condition="other"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6000, None),
                self.__skill_library.get_skill(
                    "test_instant_gcd",
                    self.__stats.job_class,
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(15000, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional", "test_job2"
                ),
                SkillModifier(with_condition="mega"),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(20000, None),
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
    def test_off_class_job_condition_with_on_job(self):
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

        rb = RotationBuilder(stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_instant_gcd")
        rb.add(3, "test_off_class_conditional")
        rb.add(6, "test_off_class_conditional", job_class="test_job2")
        rb.add(9, "test_instant_gcd")

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
                SnapshotAndApplicationEvents.EventTimes(3000, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional", "test_job2"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(6000, None),
                self.__skill_library.get_skill(
                    "test_off_class_conditional", "test_job2"
                ),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(9000, None),
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
    def test_channeling(self):
        rb = RotationBuilder(
            self.__stats,
            self.__skill_library,
            enable_autos=True,
            fight_start_time=0,
        )

        rb.add(0, "test_instant_gcd")
        rb.add(2, "test_channeling")
        rb.add(8, "test_instant_gcd")
        rb.add(12, "test_channeling")
        rb.add(25, "test_instant_gcd")
        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(0, 500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(0, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(2000, None),
                self.__skill_library.get_skill("test_channeling", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, 8500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(8000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(11440, 11940),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(12000, None),
                self.__skill_library.get_skill("test_channeling", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(22000, 22500),
                self.__skill_library.get_skill("Auto", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(25000, None),
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )
        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def skill_timing_test_with_add_and_add_next(self):
        # For a 2500 ms gcd, this spell speed should result in a 2440 sm (2.44s) GCD.
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")
        rb.add_next("test_ogcd")
        rb.add(10.0, "test_gcd")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4385, 4885),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4890, None),
                self.__skill_library.get_skill("test_ogcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000 + 1940, 10000 + 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000 + 4385, 10000 + 4885),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def skill_timing_test_with_add_and_add_next_and_other(self):
        # For a 2500 ms gcd, this spell speed should result in a 2440 sm (2.44s) GCD.
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(5.0, "test_party_buff", job_class="test_job2")
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")
        rb.add_next("test_ogcd")
        rb.add(10.0, "test_gcd")
        rb.add_next("test_gcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4385, 4885),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4890, None),
                self.__skill_library.get_skill("test_ogcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(5000, None),
                self.__skill_library.get_skill("test_party_buff", "test_job2"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000 + 1940, 10000 + 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(10000 + 4385, 10000 + 4885),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_chunk_moves(self):
        # For a 2500 ms gcd, this spell speed should result in a 2440 sm (2.44s) GCD.
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add_next("test_gcd")
        rb.add_next("test_gcd")
        #
        rb.add(100.0, "test_gcd")
        rb.add_next("test_gcd")
        #
        rb.add(20.0, "test_gcd")
        rb.add_next("test_gcd")
        rb.add_next("test_ogcd")

        expected = (
            (
                SnapshotAndApplicationEvents.EventTimes(1940, 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(4385, 4885),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(20000 + 1940, 20000 + 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(20000 + 4385, 20000 + 4885),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(20000 + 4890, None),
                self.__skill_library.get_skill("test_ogcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(100000 + 1940, 100000 + 2440),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
            (
                SnapshotAndApplicationEvents.EventTimes(100000 + 4385, 100000 + 4885),
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                [True, True],
            ),
        )

        result = rb.get_skill_timing().get_q()
        result = [result[i][1:5] for i in range(0, len(result))]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_non_strict_skill_naming(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.set_use_strict_skill_naming(False)

        rb.add_next("nonexistent skill")
        rb.add(10, "nonexistent skill")

        return True, ""
