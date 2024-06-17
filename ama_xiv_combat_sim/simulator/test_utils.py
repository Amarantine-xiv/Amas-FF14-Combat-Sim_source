from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.utils import Utils
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import create_test_skill_library
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass

#@title UtilsTest
class TestUtils(TestClass):
  def __init__(self):
    self.__skill_library = create_test_skill_library()

  @TestClass.is_a_test
  def test_get_best_keys(self):
    test_passed = True
    err_msg = ""
    keys = [frozenset(['a', 'b', 'c']),
            frozenset(['a', 'b']),
            frozenset([SimConsts.DEFAULT_CONDITION])]

    conditions = [set(['a', 'b']),
                  set(['a', 'b', 'c']),
                  set(['d']),
                  set([SimConsts.DEFAULT_CONDITION])]
    expected = [frozenset(['a', 'b']),
                frozenset(['a', 'b', 'c']),
                frozenset([SimConsts.DEFAULT_CONDITION]),
                frozenset([SimConsts.DEFAULT_CONDITION])]

    for i in range(0, len(conditions)):
      result = Utils.get_best_key(keys, conditions[i])
      if result != expected[i]:
        test_passed = False
        err_msg += 'Expected: {}. Actual: {}\n'.format(", ".join(result), ", ".join(expected[i]))

    return test_passed, err_msg

  @TestClass.is_a_test
  def test_bonus_percent_infer(self):
    test_passed = True
    err_msg = ''
    skill = self.__skill_library.get_skill('test_combo_pos', 'test_job')

    inputs = [SkillModifier(with_condition='', bonus_percent=68),
              SkillModifier(with_condition='No Combo', bonus_percent=29),
              SkillModifier(with_condition='To Ignore', bonus_percent=63),
              SkillModifier(with_condition='To Ignore', bonus_percent=29)]
    expected_outputs = (Utils.canonicalize_condition(SimConsts.DEFAULT_CONDITION),
                        Utils.canonicalize_condition('No Combo'),
                        Utils.canonicalize_condition('To Ignore, No Positional'),
                        Utils.canonicalize_condition('To Ignore, No Combo'))

    for i in range(0, len(inputs)):
      init_skill_modifier = inputs[i]
      try:
        result = Utils.canonicalize_condition(Utils.get_positional_condition(skill, init_skill_modifier))
      except ValueError as v:
        result = init_skill_modifier
        test_passed = False
        err_msg += str(v)
      if result != expected_outputs[i]:
        print(",".join(init_skill_modifier.with_condition))
        test_passed = False
        err_msg += "Conditions did not match for example {}. Expected: '{}'. Actual: '{}'\n".format(i, ", ".join(expected_outputs[i]), ",".join(result))

    return test_passed, err_msg
