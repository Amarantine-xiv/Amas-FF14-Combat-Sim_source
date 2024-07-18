from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.trackers.status_effects import StatusEffects


class TestRotationBuilderAndDamageBuilderIntegration(TestClass):
    def __init__(self):
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
    def two_skills_one_buff_override(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_skill_with_follow_up_buff1")
        rb.add(1, "test_skill_with_follow_up_buff_override")
        rb.add(2, "test_instant_gcd")
        rb.add(32, "test_instant_gcd")
        rb.add(41, "test_instant_gcd")

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]

        expected = [
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.5), StatusEffects()),
            ),
            (
                32000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.5), StatusEffects()),
            ),
            (
                41000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.5), StatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def two_skills_one_buff_different_duration(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_skill_with_follow_up_buff1")
        rb.add(1, "test_skill_with_follow_up_buff_other_duration")
        rb.add(2, "test_instant_gcd")
        rb.add(32, "test_instant_gcd")
        rb.add(41, "test_instant_gcd")

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.15), StatusEffects()),
            ),
            (
                32000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.15), StatusEffects()),
            ),
            (
                41000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(), StatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def two_skills_one_buff(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_skill_with_follow_up_buff1")
        rb.add(1, "test_skill_with_follow_up_buff2")
        rb.add(2, "test_instant_gcd")

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]

        # Buff should not be applied twice, since it's the same buff. Should only get 1 application.
        expected = [
            (
                2000,
                self.__skill_library.get_skill("test_instant_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.15), StatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def skill_modifier_pass_through(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0.6, "test_gcd", SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES))

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                3040,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(guaranteed_crit=ForcedCritOrDH.FORCE_YES),
                (StatusEffects(), StatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_buff_then_damage(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0, "test_buff_then_damage")

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]
        expected = [
            (
                0,
                self.__skill_library.get_skill("_test_buff_then_damage", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects()),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def buff_and_debuff_snapshotting(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0.0, "test_simple_buff_gcd")
        rb.add(0.0, "test_simple_debuff_gcd_2")
        rb.add(0.6, "test_gcd")
        rb.add(1.0, "test_magical_dot_gcd")
        rb.add(11.0, "test_gcd")

        db = DamageBuilder(self.__stats, self.__skill_library)
        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]

        expected = [
            (
                3040,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects(damage_mult=1.3)),
            ),
            (
                3440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects(damage_mult=1.3)),
            ),
            (
                6440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects(damage_mult=1.3)),
            ),
            (
                9440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects(damage_mult=1.3)),
            ),
            (
                12440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects(damage_mult=1.3)),
            ),
            (
                13440,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects(damage_mult=1.0)),
            ),
            (
                15440,
                self.__skill_library.get_skill("test_magical_dot_tick", "test_job"),
                SkillModifier(),
                (StatusEffects(crit_rate_add=0.05), StatusEffects(damage_mult=1.3)),
            ),
        ]
        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0.6, "test_gcd", targets="t1, t2")

        db = DamageBuilder(self.__stats, self.__skill_library)

        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]

        expected = [
            (
                3040,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(with_condition="Target 1"),
                (StatusEffects(), StatusEffects()),
            ),
            (
                3175,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(with_condition="Target 2"),
                (StatusEffects(), StatusEffects()),
            ),
        ]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target_with_buff(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0.0, "test_simple_buff_gcd")
        rb.add(1.6, "test_gcd", targets="t1, t2")

        db = DamageBuilder(self.__stats, self.__skill_library)

        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]

        expected = [
            (
                4040,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(with_condition="Target 1"),
                (StatusEffects(crit_rate_add=0.05), StatusEffects()),
            ),
            (
                4175,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(with_condition="Target 2"),
                (StatusEffects(crit_rate_add=0.05), StatusEffects()),
            ),
        ]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target_with_debuff(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)
        rb.add(0.0, "test_simple_debuff_gcd", targets="t1")
        rb.add(1.6, "test_gcd", targets="t1, t2")

        db = DamageBuilder(self.__stats, self.__skill_library)

        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]

        expected = [
            (
                4040,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(with_condition="Target 1"),
                (StatusEffects(), StatusEffects(damage_mult=1.2)),
            ),
            (
                4175,
                self.__skill_library.get_skill("test_gcd", "test_job"),
                SkillModifier(with_condition="Target 2"),
                (StatusEffects(), StatusEffects()),
            ),
        ]

        return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def multi_target_follow_up(self):
        rb = RotationBuilder(self.__stats, self.__skill_library, fight_start_time=0)        
        rb.add(0, "test_follow_up_for_multi_target_main", targets="t1, t2")

        db = DamageBuilder(self.__stats, self.__skill_library)

        result = db.get_damage_instances(rb.get_skill_timing())
        result = [result[i][0:-2] for i in range(0, len(result))]

        expected = [
            (
                0,
                self.__skill_library.get_skill("test_folllow_up_for_multi_target", "test_job"),
                SkillModifier(with_condition="Target 1"),
                (StatusEffects(), StatusEffects()),
            ),
            (
                135,
                self.__skill_library.get_skill("test_folllow_up_for_multi_target", "test_job"),
                SkillModifier(with_condition="Target 2"),
                (StatusEffects(), StatusEffects()),
            ),
        ]

        return self._compare_sequential(result, expected)