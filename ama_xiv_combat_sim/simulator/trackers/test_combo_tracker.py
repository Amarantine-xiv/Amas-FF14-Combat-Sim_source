from simulator.game_data.game_consts import GameConsts
from simulator.skills.skill import Skill
from simulator.skills.skill_modifier import SkillModifier
from simulator.sim_consts import SimConsts
from simulator.specs.combo_spec import ComboSpec
from simulator.testing.test_class import TestClass
from simulator.testing.create_test_skill_library import create_test_skill_library
from simulator.trackers.combo_tracker import ComboTracker

class TestComboTracker(TestClass):
  def __init__(self):
    self.__skill_library = create_test_skill_library()

  @TestClass.is_a_test
  def test_combo_expiry(self):
    combo_tracker = ComboTracker({0: (1,)})

    combo0 = Skill(name='combo0',
                  combo_spec=(ComboSpec(combo_group=0), ComboSpec(combo_group=1)))
    combo1 = Skill(name='combo1',
                  combo_spec=(ComboSpec(combo_group=0,
                                        combo_actions=('combo0',)),))
    combo2 = Skill(name='combo2',
                  combo_spec=(ComboSpec(combo_auto_succeed=True,
                                        combo_group=0,
                                        combo_actions=('combo0',)),))

    result = [combo_tracker.compile_and_update_combo(0, combo0, SkillModifier()),
              combo_tracker.compile_and_update_combo(GameConsts.COMBO_EXPIRATION_TIME+1, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(2*GameConsts.COMBO_EXPIRATION_TIME+1, combo2, SkillModifier())]
    expected = [SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_FAIL,
                SimConsts.COMBO_SUCCESS]
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_combo_breakers(self):
    combo_tracker = ComboTracker({0: (1,)})

    combo0 = Skill(name='combo0',
                  combo_spec=(ComboSpec(combo_group=0), ComboSpec(combo_group=1)))
    combo1 = Skill(name='combo1',
                  combo_spec=(ComboSpec(combo_group=0,
                                        combo_actions=('combo0',)),))
    combo2 = Skill(name='combo2',
                  combo_spec=(ComboSpec(combo_group=1,
                                        combo_actions=()),))
    combo3 = Skill(name='combo3',
                  combo_spec=(ComboSpec(combo_group=1,
                                        combo_auto_succeed=True,
                                        combo_actions=('combo2',)),))

    result = [combo_tracker.compile_and_update_combo(0, combo0, SkillModifier()),
              combo_tracker.compile_and_update_combo(1, combo2, SkillModifier()),
              combo_tracker.compile_and_update_combo(2, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(3, combo3, SkillModifier())]
    expected = [SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_FAIL,
                SimConsts.COMBO_SUCCESS]
    return self._compare_sequential(result, expected)

    @TestClass.is_a_test
    def test_multiple_combo_chains(self):
      combo_tracker = ComboTracker()

      combo0 = Skill(name='combo0',
                    combo_spec=(ComboSpec(combo_group=0), ComboSpec(combo_group=1)))
      combo1 = Skill(name='combo1',
                    combo_spec=(ComboSpec(combo_group=0,
                                          combo_actions=('combo0',)),))
      combo2 = Skill(name='combo2',
                    combo_spec=(ComboSpec(combo_group=1,
                                          combo_actions=('combo0',)),))
      combo3 = Skill(name='combo3',
                    combo_spec=(ComboSpec(combo_group=1,
                                          combo_auto_succeed=True,
                                          combo_actions=('combo0',)),))

      result = [combo_tracker.compile_and_update_combo(0, combo0, SkillModifier()),
                combo_tracker.compile_and_update_combo(1, combo1, SkillModifier()),
                combo_tracker.compile_and_update_combo(2, combo2, SkillModifier()),
                combo_tracker.compile_and_update_combo(3, combo1, SkillModifier()),
                combo_tracker.compile_and_update_combo(4, combo2, SkillModifier()),
                combo_tracker.compile_and_update_combo(5, combo3, SkillModifier())]
      expected = [SimConsts.COMBO_SUCCESS,
                  SimConsts.COMBO_SUCCESS,
                  SimConsts.COMBO_SUCCESS,
                  SimConsts.COMBO_FAIL,
                  SimConsts.COMBO_FAIL,
                  SimConsts.COMBO_SUCCESS]
      return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_combo_auto_succeed(self):
    combo_tracker = ComboTracker()

    combo0 = Skill(name='combo0',
                   combo_spec=(ComboSpec(),))
    combo1 = Skill(name='combo1',
                   combo_spec=(ComboSpec(combo_auto_succeed= True,
                                         combo_actions = ('combo0',)),))
    combo2 = Skill(name='combo2',
                   combo_spec=(ComboSpec(combo_actions = ('combo1',)),))
    result = [combo_tracker.compile_and_update_combo(0, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(1, combo2, SkillModifier()),
              combo_tracker.compile_and_update_combo(2, combo0, SkillModifier()),
              combo_tracker.compile_and_update_combo(3, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(4, combo2, SkillModifier()),
              combo_tracker.compile_and_update_combo(5, combo2, SkillModifier())]
    expected = [SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_FAIL]
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_simple_chain(self):
    combo_tracker = ComboTracker()

    combo0 = Skill(name='combo0',
                   combo_spec=(ComboSpec(),))
    combo1 = Skill(name='combo1',
                   combo_spec=(ComboSpec(combo_actions = ('combo0',)),))
    combo2 = Skill(name='combo2',
                   combo_spec=(ComboSpec(combo_actions = ('combo1',)),))

    result = [combo_tracker.compile_and_update_combo(0, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(1, combo2, SkillModifier()),
              combo_tracker.compile_and_update_combo(2, combo0, SkillModifier()),
              combo_tracker.compile_and_update_combo(3, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(4, combo2, SkillModifier()),
              combo_tracker.compile_and_update_combo(5, combo2, SkillModifier())]
    expected = [SimConsts.COMBO_FAIL,
                SimConsts.COMBO_FAIL,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_SUCCESS,
                SimConsts.COMBO_FAIL]
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_multi_combo_actions(self):
    combo_tracker = ComboTracker()

    combo1 = Skill(name='combo1',
                   combo_spec=(ComboSpec(),))
    combo2 = Skill(name='combo2',
                   combo_spec=(ComboSpec(combo_group= 0,
                                         combo_actions= ('combo0','combo1')),))

    result = [combo_tracker.compile_and_update_combo(0, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(1, combo2, SkillModifier())]
    expected = [SimConsts.COMBO_SUCCESS, SimConsts.COMBO_SUCCESS]
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_combo_groups(self):
    combo_tracker = ComboTracker()

    combo0 = Skill(name='combo0',
                   combo_spec=(ComboSpec(combo_group= 1),))
    combo1 = Skill(name='combo1',
                   combo_spec=(ComboSpec(combo_group= 2),))
    combo2 = Skill(name='combo2',
                   combo_spec=(ComboSpec(combo_group= 1,
                                         combo_actions= ('combo0',)),))

    result = [combo_tracker.compile_and_update_combo(0, combo0, SkillModifier()),
              combo_tracker.compile_and_update_combo(1, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(2, combo2, SkillModifier())]
    expected = [SimConsts.COMBO_SUCCESS, SimConsts.COMBO_SUCCESS, SimConsts.COMBO_SUCCESS]
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_simple_combo_fail(self):
    combo_tracker = ComboTracker()

    combo0 = Skill(name='combo0',
                   combo_spec=(ComboSpec(combo_actions = ('no',)),))

    result = [combo_tracker.compile_and_update_combo(0, combo0, SkillModifier())]
    expected = [SimConsts.COMBO_FAIL]
    return self._compare_sequential(result, expected)

  @TestClass.is_a_test
  def test_simple_combo(self):
    combo_tracker = ComboTracker()

    combo0 = Skill(name='combo0',
                   combo_spec=(ComboSpec(),))
    combo1 = Skill(name='combo1',
                   combo_spec=(ComboSpec(combo_actions = ('combo0',)),))
    combo2 = Skill(name='combo2',
                   combo_spec=(ComboSpec(combo_actions = ('no',)),))

    result = [combo_tracker.compile_and_update_combo(0, combo0, SkillModifier()),
              combo_tracker.compile_and_update_combo(1, combo1, SkillModifier()),
              combo_tracker.compile_and_update_combo(2, combo2, SkillModifier())]
    expected = [SimConsts.COMBO_SUCCESS, SimConsts.COMBO_SUCCESS, SimConsts.COMBO_FAIL]
    return self._compare_sequential(result, expected)