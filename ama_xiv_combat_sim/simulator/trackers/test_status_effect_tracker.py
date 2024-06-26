import math

from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.trackers.status_effects import StatusEffects
from ama_xiv_combat_sim.simulator.trackers.status_effect_tracker import (
    StatusEffectTracker,
)


class TestStatusEffectTracker(TestClass):
    def __init__(self):
        self.__skill_library = create_test_skill_library()

    @TestClass.is_a_test
    def conditional_addition_with_num_uses_and_allowlist(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff1 = Skill(
            name="buff1",
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=2,
                skill_allowlist=("test1",),
            ),
        )
        test1 = Skill(name="test1")
        test2 = Skill(name="test2")

        se.add_to_status_effects(0, buff1, SkillModifier())

        skills_to_use = [test1, test2, test1, test1]
        expected = (
            ((StatusEffects(), "buff1"), (StatusEffects(), "")),
            ((StatusEffects(), ""), (StatusEffects(), "")),
            ((StatusEffects(), "buff1"), (StatusEffects(), "")),
            ((StatusEffects(), ""), (StatusEffects(), "")),
        )

        for i in range(0, len(skills_to_use)):
            se.expire_status_effects(t=0)
            result = (
                se.compile_buffs(t=0, skill=skills_to_use[i]),
                se.compile_debuffs(t=0, skill=skills_to_use[i]),
            )
            if result != expected[i]:
                test_passed = False
                err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                    expected, result
                )
        return test_passed, err_msg

    @TestClass.is_a_test
    def conditional_addition(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff1 = Skill(
            name="buff1",
            buff_spec=StatusEffectSpec(add_to_skill_modifier_condition=True),
        )
        test1 = Skill(name="test1")

        se.add_to_status_effects(0, buff1, SkillModifier())
        result = (se.compile_buffs(0, skill=test1), se.compile_debuffs(0, skill=test1))
        expected = ((StatusEffects(), "buff1"), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def status_effect_priority(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker(
            ("test_num_uses_buff_with_priority1", "test_num_uses_buff_with_priority2")
        )

        se.add_to_status_effects(
            0,
            self.__skill_library.get_skill(
                "test_num_uses_buff_with_priority1", "test_job"
            ),
            SkillModifier(),
        )
        se.add_to_status_effects(
            0,
            self.__skill_library.get_skill(
                "test_num_uses_buff_with_priority2", "test_job"
            ),
            SkillModifier(),
        )
        test_instant_gcd = self.__skill_library.get_skill(
            "test_instant_gcd", "test_job"
        )

        se.expire_status_effects(t=1000)
        result = (
            se.compile_buffs(1000, skill=test_instant_gcd),
            se.compile_debuffs(1000, skill=test_instant_gcd),
        )
        expected = ((StatusEffects(crit_rate_add=0.1), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        se.expire_status_effects(t=1000)
        result = (
            se.compile_buffs(1000, skill=test_instant_gcd),
            se.compile_debuffs(1000, skill=test_instant_gcd),
        )
        expected = ((StatusEffects(dh_rate_add=0.1), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        se.expire_status_effects(t=1000)
        result = (
            se.compile_buffs(1000, skill=test_instant_gcd),
            se.compile_debuffs(1000, skill=test_instant_gcd),
        )
        expected = ((StatusEffects(), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        return test_passed, err_msg

    @TestClass.is_a_test
    def num_uses_compile(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff1 = Skill(
            name="buff1",
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.05,
                duration=30000,
                skill_allowlist=("test1",),
                num_uses=1,
            ),
        )
        test1 = Skill(name="test1")

        se.add_to_status_effects(0, buff1, SkillModifier())

        result = (se.compile_buffs(0, skill=test1), se.compile_debuffs(0, skill=test1))
        expected = ((StatusEffects(crit_rate_add=0.05), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        se.expire_status_effects(t=0)
        result = (se.compile_buffs(0, skill=test1), se.compile_debuffs(0, skill=test1))
        expected = ((StatusEffects(), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        return test_passed, err_msg

    @TestClass.is_a_test
    def allow_list_status_effect(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff1 = Skill(
            name="buff1",
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.05, duration=30000, skill_allowlist=("test1",)
            ),
        )
        test1 = Skill(name="test1")
        test2 = Skill(name="test2")

        se.add_to_status_effects(0, buff1, SkillModifier())

        result = (se.compile_buffs(0, skill=test1), se.compile_debuffs(0, skill=test1))
        expected = ((StatusEffects(crit_rate_add=0.05), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        se.expire_status_effects(t=0)
        result = (se.compile_buffs(0, skill=test2), se.compile_debuffs(0, skill=test2))
        expected = ((StatusEffects(), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        return test_passed, err_msg

    @TestClass.is_a_test
    def expires_status_effect_duration(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff1 = Skill(
            name="buff1", buff_spec=StatusEffectSpec(crit_rate_add=0.05, duration=30000)
        )
        buff2 = Skill(
            name="buff2",
            buff_spec=StatusEffectSpec(
                dh_rate_add=0.05, duration=10000, expires_status_effects=("buff1",)
            ),
        )

        se.add_to_status_effects(0, buff1, SkillModifier())
        se.add_to_status_effects(10000, buff2, SkillModifier())

        se.expire_status_effects(11000)
        result = (se.compile_buffs(11000), se.compile_debuffs(11000))
        expected = ((StatusEffects(dh_rate_add=0.05), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        return test_passed, err_msg

    @TestClass.is_a_test
    def no_refresh_status_effect(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff1 = Skill(
            name="buff", buff_spec=StatusEffectSpec(crit_rate_add=0.05, duration=30000)
        )
        buff2 = Skill(
            name="buff",
            buff_spec=StatusEffectSpec(
                crit_rate_add=0.12, duration=30000, extends_existing_duration=False
            ),
        )

        se.add_to_status_effects(0, buff1, SkillModifier())
        se.add_to_status_effects(10000, buff2, SkillModifier())
        se.expire_status_effects(29000)

        result = (se.compile_buffs(29000), se.compile_debuffs(29000))
        expected = ((StatusEffects(crit_rate_add=0.12), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        se.expire_status_effects(31000)
        result = (se.compile_buffs(31000), se.compile_debuffs(31000))
        expected = ((StatusEffects(), ""), (StatusEffects(), ""))
        if result != expected:
            test_passed = False
            err_msg += "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )

        return test_passed, err_msg

    @TestClass.is_a_test
    def prepull_buff(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff = Skill(
            name="buff", buff_spec=StatusEffectSpec(main_stat_add=262, duration=30000)
        )

        se.add_to_status_effects(-2000, buff, SkillModifier())
        se.expire_status_effects(5000)

        result = (se.compile_buffs(5000), se.compile_debuffs(5000))
        expected = ((StatusEffects(main_stat_add=262), ""), (StatusEffects(), ""))

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def buff_override(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()

        buff1 = Skill(
            name="buff", buff_spec=StatusEffectSpec(crit_rate_add=0.1, duration=30000)
        )
        buff2 = Skill(
            name="buff", buff_spec=StatusEffectSpec(crit_rate_add=0.5, duration=30000)
        )
        debuff1 = Skill(
            name="debuff",
            debuff_spec=StatusEffectSpec(dh_rate_add=0.01, duration=30000),
        )
        debuff2 = Skill(
            name="debuff",
            debuff_spec=StatusEffectSpec(dh_rate_add=0.05, duration=30000),
        )

        se.add_to_status_effects(0, buff1, SkillModifier())
        se.add_to_status_effects(1000, buff2, SkillModifier())
        se.add_to_status_effects(2000, debuff1, SkillModifier())
        se.add_to_status_effects(3000, debuff2, SkillModifier())

        result = (se.compile_buffs(3001), se.compile_debuffs(3001))
        expected = (
            (StatusEffects(crit_rate_add=0.5), ""),
            (StatusEffects(dh_rate_add=0.05), ""),
        )

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def simple_buff_expiry(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            1000,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
        )
        # test_simple_buff_gcd_2 should expire after 18000 ms
        se.add_to_status_effects(
            8000,
            self.__skill_library.get_skill("test_simple_buff_gcd_2", "test_job"),
            SkillModifier(),
        )
        # test_simple_buff_gcd_2 should expire after 19000 ms
        se.add_to_status_effects(
            9000,
            self.__skill_library.get_skill("test_simple_debuff_gcd_2", "test_job"),
            SkillModifier(),
        )

        se.expire_status_effects(19001)
        result = (se.compile_buffs(19001), se.compile_debuffs(19001))
        expected = ((StatusEffects(crit_rate_add=0.05), ""), (StatusEffects(), ""))

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def multiple_auto_attack_buffs(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            100,
            self.__skill_library.get_skill("test_auto_attack_buff", "test_job"),
            SkillModifier(),
        )
        se.add_to_status_effects(
            100,
            self.__skill_library.get_skill("test_auto_attack_buff2", "test_job"),
            SkillModifier(),
        )

        result = (se.compile_buffs(101), se.compile_debuffs(101))
        expected = (
            (StatusEffects(auto_attack_delay_mult=math.pow(0.75, 2)), ""),
            (StatusEffects(), ""),
        )

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def simple_buffs(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            100,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
        )
        se.add_to_status_effects(
            100,
            self.__skill_library.get_skill("test_simple_buff_gcd_2", "test_job"),
            SkillModifier(),
        )
        se.add_to_status_effects(
            100,
            self.__skill_library.get_skill("test_simple_debuff_gcd", "test_job"),
            SkillModifier(),
        )
        se.add_to_status_effects(
            100,
            self.__skill_library.get_skill("test_simple_debuff_gcd_2", "test_job"),
            SkillModifier(),
        )

        result = (se.compile_buffs(101), se.compile_debuffs(101))
        expected = (
            (StatusEffects(crit_rate_add=0.11, dh_rate_add=0.2), ""),
            (StatusEffects(damage_mult=1.56), ""),
        )

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def test_buff_override(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            100,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
        )
        # this should simply override the first buff
        se.add_to_status_effects(
            500,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
        )

        result = (se.compile_buffs(501), se.compile_debuffs(501))
        expected = (
            (StatusEffects(crit_rate_add=0.05, dh_rate_add=0.0), ""),
            (StatusEffects(), ""),
        )

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def late_refresh(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            0,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
        )
        # test_simple_buff_gcd should expire after 30000 ms
        se.expire_status_effects(31000)
        se.add_to_status_effects(
            31000,
            self.__skill_library.get_skill("test_simple_buff_gcd", "test_job"),
            SkillModifier(),
        )
        se.expire_status_effects(61000 - 1)
        result = (se.compile_buffs(61000 - 1), se.compile_debuffs(61000 - 1))
        expected = ((StatusEffects(crit_rate_add=0.05), ""), (StatusEffects(), ""))

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def with_cond_simple_buff(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            0,
            self.__skill_library.get_skill("test_buff_with_cond", "test_job"),
            SkillModifier(with_condition="dh"),
        )

        result = (se.compile_buffs(1), se.compile_debuffs(1))
        expected = ((StatusEffects(dh_rate_add=0.2), ""), (StatusEffects(), ""))

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def with_cond_simple_debuff(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            0,
            self.__skill_library.get_skill("test_debuff_with_cond", "test_job"),
            SkillModifier(with_condition="crit"),
        )
        se.expire_status_effects(100)
        result = (se.compile_buffs(101), se.compile_debuffs(101))
        expected = ((StatusEffects(), ""), (StatusEffects(crit_rate_add=0.15), ""))

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg

    @TestClass.is_a_test
    def test_targetted_debuff(self):
        test_passed = True
        err_msg = ""
        se = StatusEffectTracker()
        se.add_to_status_effects(
            0,
            self.__skill_library.get_skill("test_simple_debuff_gcd", "test_job"),
            SkillModifier(),
            ("t1",)
        )
        se.add_to_status_effects(
            1,
            self.__skill_library.get_skill("test_simple_debuff_gcd_2", "test_job"),
            SkillModifier(),
            ("t2",)
        )
        result = (se.compile_buffs(101), se.compile_debuffs(101, target="t1"))
        expected = ((StatusEffects(), ""), (StatusEffects(damage_mult=1.2), ""))

        if result != expected:
            test_passed = False
            err_msg = "Expected and actual status effects do not match.\nExpected{}.\nActual:{}".format(
                expected, result
            )
        return test_passed, err_msg