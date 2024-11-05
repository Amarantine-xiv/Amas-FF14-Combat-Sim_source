from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.trackers.channeling_tracker import (
    ChannelingTracker,
)


class TestChannelingTracker(TestClass):
    def __init__(self):
        super().__init__()
        self.__skill_library = create_test_skill_library()

    @TestClass.is_a_test
    def test_simple_channeling(self):
        ce = ChannelingTracker()
        ce.process_channeling(
            t=0,
            skill=self.__skill_library.get_skill("test_channeling", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.finalize()
        expected = ((0, 10000),)
        actual = ce.get_channeling_windows()

        return self._compare_sequential(actual, expected)

    @TestClass.is_a_test
    def test_simple_channeling_interrupt(self):
        ce = ChannelingTracker()
        ce.process_channeling(
            t=0,
            skill=self.__skill_library.get_skill("test_channeling", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=2000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.finalize()
        expected = ((0, 2000),)
        actual = ce.get_channeling_windows()

        return self._compare_sequential(actual, expected)

    @TestClass.is_a_test
    def test_simple_channeling_interrupt_another_channeling(self):
        ce = ChannelingTracker()
        ce.process_channeling(
            t=0,
            skill=self.__skill_library.get_skill("test_channeling", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=2000,
            skill=self.__skill_library.get_skill("test_channeling", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.finalize()
        expected = ((0, 2000), (2000, 12000))
        actual = ce.get_channeling_windows()

        return self._compare_sequential(actual, expected)

    @TestClass.is_a_test
    def test_simple_channeling_interrupt_complex(self):
        ce = ChannelingTracker()
        ce.process_channeling(
            t=1000,
            skill=self.__skill_library.get_skill("test_channeling", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=2000,
            skill=self.__skill_library.get_skill("test_channeling", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=7000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.finalize()
        expected = ((1000, 2000), (2000, 7000))
        actual = ce.get_channeling_windows()

        return self._compare_sequential(actual, expected)

    @TestClass.is_a_test
    def test_simple_channeling_num_uses_simple(self):
        ce = ChannelingTracker()
        ce.process_channeling(
            t=0,
            skill=self.__skill_library.get_skill(
                "test_channeling_num_uses", "test_job"
            ),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=2000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.finalize()
        expected = ((0, 10000),)
        actual = ce.get_channeling_windows()

        return self._compare_sequential(actual, expected)

    @TestClass.is_a_test
    def test_simple_channeling_num_uses_exhaust(self):
        ce = ChannelingTracker()
        ce.process_channeling(
            t=0,
            skill=self.__skill_library.get_skill(
                "test_channeling_num_uses", "test_job"
            ),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=2000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=3000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=5000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.finalize()
        expected = ((0, 5000),)
        actual = ce.get_channeling_windows()

        return self._compare_sequential(actual, expected)

    @TestClass.is_a_test
    def test_simple_channeling_num_uses_exhaust2(self):
        ce = ChannelingTracker()
        ce.process_channeling(
            t=0,
            skill=self.__skill_library.get_skill(
                "test_channeling_num_uses", "test_job"
            ),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=1000,
            skill=self.__skill_library.get_skill("test_ogcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=2000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=3000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.process_channeling(
            t=5000,
            skill=self.__skill_library.get_skill("test_gcd", "test_job"),
            skill_modifier=SkillModifier(),
        )
        ce.finalize()
        expected = ((0, 1000),)
        actual = ce.get_channeling_windows()

        return self._compare_sequential(actual, expected)
