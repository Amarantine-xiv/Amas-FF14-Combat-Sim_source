from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.skill_timing_info import (
    SkillTimingInfo,
)
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.trackers.offensive_status_effects import (
    OffensiveStatusEffects,
)
from ama_xiv_combat_sim.simulator.utils import Utils


class TestDamageBuilder(TestClass):
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
    def test_combo(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_combo1", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1000,
            self.__skill_library.get_skill("test_combo0", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_combo1", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                0,
                self.__skill_library.get_skill("test_combo1", "test_job"),
                SkillModifier(with_condition=SimConsts.COMBO_FAIL),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
            (
                1000,
                self.__skill_library.get_skill("test_combo0", "test_job"),
                SkillModifier(with_condition=SimConsts.COMBO_SUCCESS),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
            (
                2000,
                self.__skill_library.get_skill("test_combo1", "test_job"),
                SkillModifier(with_condition=SimConsts.COMBO_SUCCESS),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_job_resource(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_skill_add_gauge", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1000,
            self.__skill_library.get_skill("test_skill_use_gauge", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1000,
                self.__skill_library.get_skill("test_skill_use_gauge", "test_job"),
                SkillModifier(with_condition="10 Gauge"),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            )
        ]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def skill_with_conditional(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_skill_with_conditional", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(with_condition="test_skill_with_conditional"),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def status_effect_priority(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill(
                "test_num_uses_buff_with_priority1", "test_job"
            ),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill(
                "test_num_uses_buff_with_priority2", "test_job"
            ),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(3000),
            3000,
            3000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(crit_rate_add=0.1), OffensiveStatusEffects()),
            ),
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(dh_rate_add=0.1), OffensiveStatusEffects()),
            ),
            (
                3000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def guaranteed_dh(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_guaranteed_dh_buff", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                    OffensiveStatusEffects(),
                ),
            ),
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def guaranteed_crit(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_guaranteed_crit_buff", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                    OffensiveStatusEffects(),
                ),
            ),
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def skill_allowlist_status_effect(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("simple_buff_with_allowlist", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1500,
            self.__skill_library.get_skill("test_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1500,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(crit_rate_add=0.05), OffensiveStatusEffects()),
            ),
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def with_cond_buff(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_buff_with_cond", "test_job"),
            SkillModifier(with_condition="crit"),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1500,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        # We are actually OVERRIDING the current buff from test_buff_with_cond with the dh version.
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_buff_with_cond", "test_job"),
            SkillModifier(with_condition="dh"),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(3000),
            3000,
            3500,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1500,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(crit_rate_add=0.1), OffensiveStatusEffects()),
            ),
            (
                3500,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(dh_rate_add=0.2), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def with_cond_debuff(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_debuff_with_cond", "test_job"),
            SkillModifier(with_condition="crit"),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1500,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        # We are actually OVERRIDING the current debuff from test_buff_with_cond with the dh version.
        rb_result.add(
            Utils.transform_time_to_prio(2000),
            2000,
            2000,
            self.__skill_library.get_skill("test_debuff_with_cond", "test_job"),
            SkillModifier(with_condition="dh"),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(3000),
            3000,
            3500,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1500,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects(crit_rate_add=0.15)),
            ),
            (
                3500,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects(dh_rate_add=0.25)),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def status_effect_denylist(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_buff_gcd_2", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_debuff_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_debuff_gcd_2", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2940) + 1,
            2940,
            3440,
            self.__skill_library.get_skill("test_gcd_with_denylist", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = (
            (
                3440,
                self.__skill_library.get_skill("test_gcd_with_denylist", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
        )
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def buff_and_debuff_snapshotting(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_debuff_gcd_2", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2540),
            2540,
            3040,
            self.__skill_library.get_skill("test_gcd", "test_job"),
            SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2940),
            2940,
            3440,
            self.__skill_library.get_skill("test_magical_dot_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2940) + 1,
            2940,
            3440,
            self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2940) + 2,
            2940,
            6440,
            self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2940) + 3,
            2940,
            9440,
            self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2940) + 4,
            2940,
            12440,
            self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(2940) + 5,
            2940,
            15440,
            self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(12940),
            12940,
            13440,
            self.__skill_library.get_skill("test_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                3040,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_dh=ForcedCritOrDH.FORCE_YES),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
            (
                3440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
            (
                6440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
            (
                9440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
            (
                12440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
            (
                13440,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.0),
                ),
            ),
            (
                15440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def buff_and_debuff_snapshotting_with_no_debuff_snapshot(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_debuff_gcd_2", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1500,
            self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
            SkillModifier(),
            [True, False],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            11000,
            self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
            SkillModifier(),
            [True, False],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                1500,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.3),
                ),
            ),
            (
                11000,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (
                    OffensiveStatusEffects(crit_rate_add=0.05),
                    OffensiveStatusEffects(damage_mult=1.0),
                ),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def priority_test(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            500,
            self.__skill_library.get_skill("test_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            1,
            0,
            0,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                500,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def default_buff_and_damage_order(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill(
                "test_default_buff_damage_order", "test_job"
            ),
            SkillModifier(),
            [True, True],
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                0,
                self.__skill_library.get_skill(
                    "test_default_buff_damage_order", "test_job"
                ),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
            targets=("t1", "t2"),
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                0,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
            (
                GameConsts.MULTI_TARGET_DELAY_PER_TARGET,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(with_condition=SimConsts.SECONDARY_TARGET),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target_with_debuff(self):
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_simple_debuff_gcd", "test_job"),
            SkillModifier(),
            [True, True],
            targets=("t1",),
        )
        rb_result.add(
            5000,
            5000,
            5000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
            targets=("t1", "t2"),
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                5000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects(damage_mult=1.2)),
            ),
            (
                5000 + GameConsts.MULTI_TARGET_DELAY_PER_TARGET,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(with_condition=SimConsts.SECONDARY_TARGET),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def snapshot_dot_downtime(self):
        downtime_windows = {"t1": ((3000, 10000, None),)}
        rb_result = SnapshotAndApplicationEvents()
        dot_times = [0, 3000, 6000, 9000, 12000]
        expected_times = [0, 12000]
        for dot_time in dot_times:
            rb_result.add(
                dot_time,
                0,
                dot_time,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                [True, True],
                targets=("t1",),
            )
        rb_result = SkillTimingInfo(
            snapshot_and_application_events=rb_result, downtime_windows=downtime_windows
        )
        
        db = DamageBuilder(self.__stats, self.__skill_library)        
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        
        expected = []
        for expected_time in expected_times:
            expected.append((
                expected_time,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ))        
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target_snapshot_downtime(self):
        downtime_windows = {"t2": ((3000, 10000, None),)}
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            2900,
            2900,
            3000,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
            targets=("t1", "t2"),
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result, downtime_windows=downtime_windows)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                3000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target_instant_downtime(self):
        downtime_windows = {"t2": ((3000, 10000, None),)}
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            2900,
            2900,
            2900,
            self.__skill_library.get_skill("test_instant_gcd", "test_job"),
            SkillModifier(),
            [True, True],
            targets=("t1", "t2"),
        )
        rb_result = SkillTimingInfo(snapshot_and_application_events=rb_result, downtime_windows=downtime_windows)

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb_result)
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                2900,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (OffensiveStatusEffects(), OffensiveStatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

# TEST:
# multi-target with downtime
# combo-check? (or do this in e2e)
