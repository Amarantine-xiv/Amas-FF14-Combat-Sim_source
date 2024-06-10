from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import create_test_skill_library
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder

class TestEndToEnd(TestClass):
  def __init__(self):
    self.__skill_library = create_test_skill_library()
    self.__relative_tol=5e-3

  @TestClass.is_a_test
  def test_simple(self):
    test_passed = True
    err_msg=""
    stats = Stats(wd=126, weapon_delay=3.44, main_stat=2945, det_stat=1620, crit_stat=2377, dh_stat=1048, speed_stat=708, job_class = 'test_job', version="test")

    rb = RotationBuilder(stats, self.__skill_library)
    db = DamageBuilder(stats, self.__skill_library)

    rb.add(1.0, 'test_magical_dot_gcd')
    dmg_instances = db.get_damage_instances(rb.get_skill_timing())
    # just make sure it actually runs and doesn't die
    sim = DamageSimulator(stats, dmg_instances, 2)
    return test_passed, err_msg

  @TestClass.is_a_test
  def test_skill_modifier_with_condition(self):
    test_passed = True
    err_msg=""
    stats = Stats(wd=126, weapon_delay=3.44, main_stat=2945, det_stat=1620, crit_stat=2377, dh_stat=1048, speed_stat=708, job_class = 'test_job', version="test")

    rb = RotationBuilder(stats, self.__skill_library)
    db = DamageBuilder(stats, self.__skill_library)

    rb.add(0.0, 'test_damage_spec_with_cond', skill_modifier=SkillModifier(with_condition='cond1'))
    rb.add(2.0, 'test_damage_spec_with_cond', skill_modifier=SkillModifier(with_condition='cond2'))
    rb.add(4.0, 'test_damage_spec_with_cond')
    expected_damage = (6508.0, 13020.4, 32594.1)

    dmg_instances = db.get_damage_instances(rb.get_skill_timing())
    sim = DamageSimulator(stats, dmg_instances, 100000)
    per_skill_damage = sim.get_per_skill_damage()
    actual_damage = tuple(per_skill_damage[i].expected_damage for i in range(0,3))

    return self._compare_sequential(actual_damage, expected_damage, self.__relative_tol)
