from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import create_test_skill_library
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import SnapshotAndApplicationEvents
from ama_xiv_combat_sim.simulator.utils import Utils

class TestSnapshotAndApplicationEvents(TestClass):
  def __init__(self):
    self.__skill_library = create_test_skill_library()

  @TestClass.is_a_test
  def test_get_last_event(self):
    test_passed = True
    err_msg = ""
    rb_result = SnapshotAndApplicationEvents()
    rb_result.add(Utils.transform_time_to_prio(2940), 2940, 3440, self.__skill_library.get_skill('test_magical_dot_gcd', 'test_job'), SkillModifier(), [True, True])
    rb_result.add(Utils.transform_time_to_prio(2940)+1, 2940, 3440, self.__skill_library.get_skill('test_magical_dot_tick', 'test_job'), SkillModifier(), [True, True])
    rb_result.add(Utils.transform_time_to_prio(2940)+5, 2940, 15440, self.__skill_library.get_skill('test_magical_dot_tick', 'test_job'), SkillModifier(), [True, True])
    rb_result.add(Utils.transform_time_to_prio(12940), 12940, 13440, self.__skill_library.get_skill('test_gcd', 'test_job'), SkillModifier(), [True, True])

    actual_last_event_time = rb_result.get_last_event_time()
    expected_last_event_time = 15440
    if actual_last_event_time != expected_last_event_time:
      err_msg = "Last event time was expected to be {}, but was {}.".format(expected_last_event_time, actual_last_event_time)
      test_passed = False
    return test_passed, err_msg