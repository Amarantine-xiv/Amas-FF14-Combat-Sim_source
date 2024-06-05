import numpy as np

from simulator.damage_simulator import DamageSimulator
from simulator.skills.create_skill_library import create_skill_library
from simulator.skills.skill_modifier import SkillModifier
from simulator.sim_consts import SimConsts
from simulator.stats import Stats
from simulator.testing.test_class import TestClass
from simulator.timeline_builders.damage_builder import DamageBuilder
from simulator.timeline_builders.rotation_builder import RotationBuilder
from simulator.utils import Utils

class TestJobs(TestClass):
  def __init__(self):
    self.__skill_library = create_skill_library()
    self.__relative_tol = 5e-3

  def __test_skills(self, stats, skills_and_expected_damage):
    test_passed=True
    err_msg=""

    for sk, skill_modifier, expected_damage in skills_and_expected_damage:
      rb = RotationBuilder(stats, self.__skill_library)
      rb.add_next(sk, skill_modifier=skill_modifier)

      db = DamageBuilder(stats, self.__skill_library)
      sim = DamageSimulator(rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000)
      dps = sim.get_dps()
      actual_damage = np.mean(sim.get_raw_damage())
      diff = abs(float(expected_damage - actual_damage))
      if diff/expected_damage >= self.__relative_tol:
        test_passed = False
        err_msg += "Did not get expected damage for {} / {}. Expected: {}. Actual: {}.\n".format(sk, skill_modifier, expected_damage, actual_damage)
    return test_passed, err_msg

  def __test_rotation_damage(self, rb, expected_damage_instances):
    test_passed=True
    err_msg=""

    db = DamageBuilder(rb.get_stats(), self.__skill_library)
    sim = DamageSimulator(rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000)
    result = [(x.skill_name, x.expected_damage) for x in sim.get_per_skill_damage()]

    if len(result) != len(expected_damage_instances):
      test_passed = False
      err_msg += "Expected {} skills returned. Instead got {}.\n".format(len(expected_damage_instances), len(result))
      return test_passed, err_msg
    for i in range(0, len(result)):
      result_skill_name, expected_skill_name = result[i][0], expected_damage_instances[i][0]
      if result_skill_name != expected_skill_name:
        test_passed = False
        err_msg += "Name did not match. Expected: {}. Actual: {}\n".format(expected_skill_name, result_skill_name)

      result_damage, expected_damage = result[i][1], expected_damage_instances[i][1]
      diff = abs (result_damage-expected_damage)
      if diff/max(1e-6,expected_damage) >= 0.005:
        test_passed = False
        err_msg += "Did not get expected damage for damage instance {}. Expected: {}. Actual: {}.\n".format(result_skill_name, expected_damage, result_damage)
    return test_passed, err_msg

  def __test_aggregate_rotation(self, rb, expected_damage, expected_total_time):
    test_passed=True
    err_msg=""

    db = DamageBuilder(rb.get_stats(), self.__skill_library)
    sim = DamageSimulator(rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000)
    dps = sim.get_dps()
    actual_damage = np.mean(sim.get_raw_damage())
    damage_diff = abs(float(expected_damage - actual_damage))
    if damage_diff/expected_damage >= self.__relative_tol:
      test_passed = False
      err_msg += "Did not get expected damage for rotation. Expected: {}. Actual: {}.\n".format(expected_damage, actual_damage)

    actual_total_time = max(sim.get_damage_time())-min(sim.get_damage_time())
    if abs(expected_total_time - actual_total_time) > 1e-3:
      test_passed = False
      err_msg += "Did not get expected total time for rotation. Expected: {}. Actual: {}.\n".format(expected_total_time, actual_total_time)

    return test_passed, err_msg

  @TestClass.is_a_test
  def test_war_skills(self):
    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'WAR')
    skills_and_expected_damage = (('Auto', SkillModifier(), 2641.6),
                                  ('Heavy Swing', SkillModifier(),5193.9),
                                  ('Maim', SkillModifier(force_combo=True), 7796.1),
                                  ('Maim', SkillModifier(), 3903.4),
                                  ("Storm's Path", SkillModifier(force_combo=True), 11448.0),
                                  ("Storm's Path", SkillModifier(), 6505.5),
                                  ("Storm's Eye", SkillModifier(force_combo=True), 11446.4),
                                  ("Storm's Eye", SkillModifier(), 6501.2),
                                  ('Upheaval', SkillModifier(), 10418.6),
                                  ('Onslaught', SkillModifier(), 3900.5),
                                  ('Fell Cleave', SkillModifier(), 13521.6),
                                  ('Primal Rend', SkillModifier(), 31574.8),
                                  ('Inner Chaos', SkillModifier(), 29773.5),
                                  ('Tomahawk', SkillModifier(), 3898.4),
                                  ('Overpower', SkillModifier(), 2859.7),
                                  ('Mythril Tempest', SkillModifier(force_combo=True), 3896.3),
                                  ('Mythril Tempest', SkillModifier(), 2602.5),
                                  ('Orogeny', SkillModifier(), 3903.3),
                                  ('Decimate', SkillModifier(), 5201.7),
                                  ('Vengeance', SkillModifier(with_condition='Retaliation'), 1424.1))
    return self.__test_skills(stats, skills_and_expected_damage)

  @TestClass.is_a_test
  def test_war_aggregate_rotation(self):
    stats = Stats(wd=126, weapon_delay=3.36, main_stat=2910, det_stat=1980, crit_stat=2313, dh_stat=868, speed_stat=592, tenacity=631, job_class = 'WAR')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True)
    rb.add_next('Heavy Swing')
    rb.add_next('Maim')
    rb.add_next('Grade 8 Tincture')
    rb.add_next("Storm's Eye")
    rb.add_next('Inner Release')
    rb.add_next('Inner Chaos')
    rb.add_next('Upheaval')
    rb.add_next('Onslaught')
    rb.add_next('Primal Rend')
    rb.add_next('Inner Chaos')
    rb.add_next('Onslaught')
    rb.add_next('Fell Cleave')
    rb.add_next('Onslaught')
    rb.add_next('Fell Cleave')
    rb.add_next('Fell Cleave')
    rb.add_next('Heavy Swing')
    rb.add_next('Maim')
    rb.add_next("Storm's Path")
    rb.add_next('Fell Cleave')
    rb.add_next('Inner Chaos')
    expected_damage = 358850.3
    expected_total_time = 32385.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_gnb_skills(self):
    stats = Stats(wd=126, weapon_delay=2.80, main_stat=2891, det_stat=1844, crit_stat=2377, dh_stat=1012, speed_stat=400, tenacity=751, job_class = 'GNB')
    skills_and_expected_damage = (('Auto', SkillModifier(), 2170.4),
                                  ('Keen Edge', SkillModifier(), 5202.9),
                                  ('Brutal Shell', SkillModifier(force_combo=True), 7818.0),
                                  ('Brutal Shell', SkillModifier(), 4160.9),
                                  ('Demon Slice', SkillModifier(), 2594.8),
                                  ('Lightning Shot', SkillModifier(), 3892.1),
                                  ('Solid Barrel', SkillModifier(force_combo=True), 9359.6),
                                  ('Solid Barrel', SkillModifier(), 3636.1),
                                  ('Burst Strike', SkillModifier(), 9880.3),
                                  ('Demon Slaughter', SkillModifier(force_combo=True), 4162.4),
                                  ('Demon Slaughter', SkillModifier(), 2601.2),
                                  ('Sonic Break', SkillModifier(), 23398.8),
                                  ('Rough Divide', SkillModifier(), 3899.6),
                                  ('Gnashing Fang', SkillModifier(), 9876.2),
                                  ('Savage Claw', SkillModifier(force_combo=True), 11950.9),
                                  ('Wicked Talon', SkillModifier(force_combo=True), 14031.2),
                                  ('Bow Shock', SkillModifier(), 11704.9),
                                  ('Jugular Rip', SkillModifier(), 5185.7),
                                  ('Abdomen Tear', SkillModifier(), 6238.4),
                                  ('Eye Gouge', SkillModifier(), 7284.4),
                                  ('Fated Circle', SkillModifier(), 7822.5),
                                  ('Blasting Zone', SkillModifier(), 18716.2),
                                  ('Double Down', SkillModifier(), 31283.2),
                                  ('Hypervelocity', SkillModifier(), 4683.7))
    return self.__test_skills(stats, skills_and_expected_damage)

  @TestClass.is_a_test
  def test_gnb_aggregate_rotation(self):
    stats = Stats(wd=126, weapon_delay=2.80, main_stat=2891, det_stat=1844, crit_stat=2377, dh_stat=1012, speed_stat=400, tenacity=751, job_class = 'GNB')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True)
    rb.add_next('Keen Edge')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Brutal Shell')
    rb.add_next('No Mercy')
    rb.add_next('Gnashing Fang')
    rb.add_next('Jugular Rip')
    rb.add_next('Sonic Break')
    rb.add_next('Blasting Zone')
    rb.add_next('Bow Shock')
    rb.add_next('Double Down')
    rb.add_next('Rough Divide')
    rb.add_next('Savage Claw')
    rb.add_next('Abdomen Tear')
    rb.add_next('Rough Divide')
    rb.add_next('Wicked Talon')
    rb.add_next('Eye Gouge')
    rb.add_next('Solid Barrel')
    rb.add_next('Burst Strike')
    rb.add_next('Hypervelocity')
    rb.add_next('Keen Edge')
    expected_damage = 279559.6
    expected_total_time = 34188.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_pld_skills(self):
    stats = Stats(wd=126, weapon_delay=2.24, main_stat=2891, det_stat=1844, crit_stat=2377, dh_stat=1012, speed_stat=400, tenacity=751, job_class = 'PLD')
    skills_and_expected_damage = (('Auto', SkillModifier(), 1741.2),
                                  ('Fast Blade', SkillModifier(), 5202.9),
                                  ('Riot Blade', SkillModifier(force_combo=True), 7792.7),
                                  ('Riot Blade', SkillModifier(), 3643.5),
                                  ('Total Eclipse', SkillModifier(), 2603.2),
                                  ('Shield Bash', SkillModifier(), 2592.1),
                                  ('Shield Lob', SkillModifier(), 2602.2),
                                  ('Prominence', SkillModifier(force_combo=True), 4417.4),
                                  ('Prominence', SkillModifier(), 2595.6),
                                  ('Circle of Scorn', SkillModifier(), 7530.2),
                                  ('Goring Blade', SkillModifier(), 18251.9),
                                  ('Royal Authority', SkillModifier(force_combo=True), 10425.1),
                                  ('Royal Authority', SkillModifier(), 3639.2),
                                  ('Holy Spirit', SkillModifier(), 9103.9),
                                  ('Holy Spirit', SkillModifier(with_condition='Divine Might'), 11707.1),
                                  ('Holy Spirit', SkillModifier(with_condition='Requiescat'), 16891.1),
                                  ('Holy Spirit', SkillModifier(with_condition='Divine Might, Requiescat'), 11714.4),
                                  ('Requiescat', SkillModifier(), 8321.4),
                                  ('Holy Circle', SkillModifier(), 2592.8),
                                  ('Holy Circle', SkillModifier(with_condition='Divine Might'), 5203.8),
                                  ('Holy Circle', SkillModifier(with_condition='Requiescat'), 7815.4),
                                  ('Holy Circle', SkillModifier(with_condition='Divine Might, Requiescat'), 5202.7),
                                  ('Intervene', SkillModifier(), 3900.0),
                                  ('Atonement', SkillModifier(), 10376.6),
                                  ('Confiteor', SkillModifier(), 10924.5),
                                  ('Confiteor', SkillModifier(with_condition='Requiescat'), 23904.3),
                                  ('Expiacion', SkillModifier(), 11718.3),
                                  ('Blade of Faith', SkillModifier(), 5719.8),
                                  ('Blade of Faith', SkillModifier(with_condition='Requiescat'), 18718.6),
                                  ('Blade of Truth', SkillModifier(), 8315.7),
                                  ('Blade of Truth', SkillModifier(with_condition='Requiescat'), 21320.3),
                                  ('Blade of Valor', SkillModifier(), 10916.9),
                                  ('Blade of Valor', SkillModifier(with_condition='Requiescat'), 23948.3))

    return self.__test_skills(stats, skills_and_expected_damage)

  @TestClass.is_a_test
  def test_pld_aggregate_rotation(self):
    stats = Stats(wd=126, weapon_delay=2.24, main_stat=2891, det_stat=1844, crit_stat=2377, dh_stat=1012, speed_stat=400, tenacity=751, job_class = 'PLD')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True)
    rb.add_next('Holy Spirit')
    rb.add_next('Fast Blade')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Riot Blade')
    rb.add_next('Royal Authority')
    rb.add_next('Fight or Flight')
    rb.add_next('Requiescat')
    rb.add_next('Goring Blade')
    rb.add_next('Circle of Scorn')
    rb.add_next('Expiacion')
    rb.add_next('Confiteor')
    rb.add_next('Intervene')
    rb.add_next('Blade of Faith')
    rb.add_next('Intervene')
    rb.add_next('Blade of Truth')
    rb.add_next('Blade of Valor')
    rb.add_next('Holy Spirit')
    rb.add_next('Atonement')
    rb.add_next('Atonement')
    rb.add_next('Atonement')
    expected_damage = 312325.9
    expected_total_time = 29035.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_drk_skills(self):
    stats = Stats(wd=126, weapon_delay=2.96, main_stat=2906, det_stat=1883, crit_stat=2352, dh_stat=868, speed_stat=650, tenacity=631, job_class = 'DRK')
    skills_and_expected_damage = (('Auto', SkillModifier(), 2322.9),
                                  ('Hard Slash', SkillModifier(), 4398.6),
                                  ('Syphon Strike', SkillModifier(force_combo=True), 6731.8),
                                  ('Syphon Strike', SkillModifier(), 3106.7),
                                  ('Unleash', SkillModifier(), 3105.4),
                                  ('Unmend', SkillModifier(), 3885.94),
                                  ('Souleater', SkillModifier(force_combo=True), 8805.3),
                                  ('Souleater', SkillModifier(), 3101.4),
                                  ('Flood of Shadow', SkillModifier(), 4140.5),
                                  ('Stalwart Soul', SkillModifier(force_combo=True), 3625.1),
                                  ('Stalwart Soul', SkillModifier(), 2589.5),
                                  ('Edge of Shadow', SkillModifier(), 11924.0),
                                  ('Salted Earth', SkillModifier(), 6576.1),
                                  ('Salt and Darkness', SkillModifier(), 12960.2),
                                  ('Plunge', SkillModifier(), 3885.7),
                                  ('Abyssal Drain', SkillModifier(), 6220.1),
                                  ('Carve and Spit', SkillModifier(), 13208.8),
                                  ('Bloodspiller', SkillModifier(), 12958.8),
                                  ('Quietus', SkillModifier(), 5186.4),
                                  ('Shadowbringer', SkillModifier(), 15534.5),
                                  ('Living Shadow', SkillModifier(), 67148.1))
    return self.__test_skills(stats, skills_and_expected_damage)

  @TestClass.is_a_test
  def test_drk_aggregate_rotation(self):
    stats = Stats(wd=126, weapon_delay=2.96, main_stat=2906, det_stat=1883, crit_stat=2352, dh_stat=868, speed_stat=650, tenacity=631, job_class = 'DRK')
    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True)

    rb.add_next('Hard Slash')
    rb.add_next('Edge of Shadow')
    rb.add_next('Syphon Strike')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Souleater')
    rb.add_next('Living Shadow')
    rb.add_next('Salted Earth')
    rb.add_next('Bloodspiller')
    rb.add_next('Shadowbringer')
    rb.add_next('Edge of Shadow')
    rb.add_next('Bloodspiller')
    rb.add_next('Carve and Spit')
    rb.add_next('Plunge')
    rb.add_next('Bloodspiller')
    rb.add_next('Edge of Shadow')
    rb.add_next('Salt and Darkness')
    rb.add_next('Hard Slash')
    rb.add_next('Plunge')
    rb.add_next('Edge of Shadow')
    rb.add_next('Syphon Strike')
    rb.add_next('Shadowbringer')
    rb.add_next('Edge of Shadow')
    rb.add_next('Souleater')
    rb.add_next('Hard Slash')
    rb.add_next('Syphon Strike')
    rb.add_next('Souleater')
    expected_damage = 370721.2
    expected_total_time = 26993.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_sch_skills(self):
    stats = Stats(wd=126, weapon_delay=3.12, main_stat=3366, det_stat=1948, crit_stat=2498, dh_stat=688, speed_stat=954, job_class = 'SCH', healer_or_caster_strength=351)
    skills_and_expected_damage = (('Auto', SkillModifier(), 185.2),
                                  ('Broil IV', SkillModifier(), 14462.0),
                                  ('Ruin II', SkillModifier(), 10786.7),
                                  ('Energy Drain', SkillModifier(), 4901.8),
                                  ('Art of War II', SkillModifier(), 8821.7),
                                  ('Biolysis', SkillModifier(), 35576.5))
    return self.__test_skills(stats, skills_and_expected_damage)

  @TestClass.is_a_test
  def test_sch_aggregate_rotation(self):
    stats = Stats(wd=126, weapon_delay=3.12, main_stat=3366, det_stat=1948, crit_stat=2498, dh_stat=688, speed_stat=954, job_class = 'SCH', healer_or_caster_strength=351)

    rb = RotationBuilder(stats, self.__skill_library)
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Broil IV')
    rb.add_next('Biolysis')
    rb.add_next('Broil IV')
    rb.add_next('Broil IV')
    rb.add_next('Chain Stratagem')
    rb.add_next('Broil IV')
    rb.add_next('Energy Drain')
    rb.add_next('Broil IV')
    rb.add_next('Energy Drain')
    rb.add_next('Broil IV')
    rb.add_next('Energy Drain')
    rb.add_next('Broil IV')
    rb.add_next('Broil IV')
    rb.add_next('Energy Drain')
    rb.add_next('Broil IV')
    rb.add_next('Energy Drain')
    rb.add_next('Broil IV')
    rb.add_next('Energy Drain')
    rb.add_next('Broil IV')
    rb.add_next('Broil IV')
    rb.add_next('Broil IV')
    expected_damage = 277595.4
    expected_total_time = 31200.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_whm_skills(self):
    stats = Stats(wd=132, weapon_delay=3.44, main_stat=3366, det_stat=2047, crit_stat=2502, dh_stat=616, speed_stat=1062, job_class = 'WHM', healer_or_caster_strength=214)
    skills_and_expected_damage = (('Auto', SkillModifier(), 37.2),
                                  ('Glare III', SkillModifier(), 15768.0),
                                  ('Assize', SkillModifier(), 20363.5),
                                  ('Dia', SkillModifier(), 37739.8),
                                  ('Afflatus Misery', SkillModifier(), 63205.7),
                                  ('Holy III', SkillModifier(), 7641.9))
    return self.__test_skills(stats, skills_and_expected_damage)

  @TestClass.is_a_test
  def test_whm_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.44, main_stat=3366, det_stat=2047, crit_stat=2502, dh_stat=616, speed_stat=1062, job_class = 'WHM', healer_or_caster_strength=214)

    rb = RotationBuilder(stats, self.__skill_library)
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Glare III')
    rb.add_next('Dia')
    rb.add_next('Glare III')
    rb.add_next('Glare III')
    rb.add_next('Presence of Mind')
    rb.add_next('Glare III')
    rb.add_next('Assize')
    rb.add_next('Glare III', num_times=10)
    expected_damage = 301604.8
    expected_total_time = 28560.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_sge_skills(self):
    stats = Stats(wd=132, weapon_delay=2.8, main_stat=3366, det_stat=2047, crit_stat=2502, dh_stat=1012, speed_stat=664, job_class = 'SGE', healer_or_caster_strength=214)
    skills_and_expected_damage = (('Auto', SkillModifier(), 30.9),
                                  ('Dosis III', SkillModifier(), 17275.3),
                                  ('Phlegma III', SkillModifier(), 31436.4),
                                  ('Toxikon II', SkillModifier(), 17284.2),
                                  ('Dykrasia II', SkillModifier(), 8901.3),
                                  ('Pneuma', SkillModifier(), 17264.3),
                                  ('Eukrasian Dosis III', SkillModifier(), 39979.0))
    return self.__test_skills(stats, skills_and_expected_damage)

  @TestClass.is_a_test
  def test_sge_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=2.8, main_stat=3366, det_stat=2047, crit_stat=2502, dh_stat=1012, speed_stat=664, job_class = 'SGE', healer_or_caster_strength=214)

    rb = RotationBuilder(stats, self.__skill_library)
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Dosis III')
    rb.add_next('Eukrasia')
    rb.add_next('Eukrasian Dosis III')
    rb.add_next('Dosis III')
    rb.add_next('Dosis III')
    rb.add_next('Phlegma III')
    rb.add_next('Phlegma III')
    rb.add_next('Dosis III', num_times=9)
    expected_damage = 329566.2
    expected_total_time = 36800.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_ast_skills(self):
    stats = Stats(wd=132, weapon_delay=3.2, main_stat=3366, det_stat=2047, crit_stat=2430, dh_stat=400, speed_stat=1350, job_class = 'AST', healer_or_caster_strength=214)
    skills_and_expected_damage = (('Auto', SkillModifier(), 33.0),
                                  ('Fall Malefic', SkillModifier(), 12456.6),
                                  ('Combust III', SkillModifier(), 28932.5),
                                  ('Earthly Star', SkillModifier(), 14885.5),
                                  ('Gravity II', SkillModifier(), 6443.0),
                                  ('Macrocosmos', SkillModifier(), 12470.8),
                                  ('Lord of Crowns', SkillModifier(), 12461.0))
    return self.__test_skills(stats, skills_and_expected_damage)


  @TestClass.is_a_test
  def test_ast_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.2, main_stat=3366, det_stat=2047, crit_stat=2430, dh_stat=400, speed_stat=1350, job_class = 'AST', healer_or_caster_strength=214)

    rb = RotationBuilder(stats, self.__skill_library)
    rb.add_next('Earthly Star')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Fall Malefic')
    rb.add_next('Lightspeed')
    rb.add_next('Combust III')
    # Just get the cards out
    rb.add_next('the Arrow')
    rb.add_next('the Balance')
    rb.add_next('Fall Malefic')
    rb.add_next('the Spire')
    rb.add_next('Fall Malefic')
    rb.add_next('Divination')
    rb.add_next('Astrodyne')
    rb.add_next('Lord of Crowns')
    rb.add_next('Fall Malefic', num_times=8)

    expected_damage = 222414.8
    expected_total_time = 27480.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_nin_rotation_damage_instances(self):
    stats = Stats(wd=132, weapon_delay=2.56, main_stat=3360, det_stat=1697, crit_stat=2554, dh_stat=1582, speed_stat=400, job_class = 'NIN')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True)
    rb.add(0, 'Kassatsu')
    rb.add(14, 'Hyosho Ranryu')
    rb.add(20, 'Kassatsu')
    rb.add(36, 'Hyosho Ranryu')

    rb.add(100, 'Bunshin')
    rb.add(102, 'Gust Slash')
    rb.add(104, 'Aeolian Edge')
    rb.add(106, 'Hakke Mujinsatsu')
    rb.add(108, 'Armor Crush')

    expected = (('Hyosho Ranryu', 68433.6),
                ('Hyosho Ranryu', 52765.4),
                ('_Bunshin_melee', 5985.3),
                ('Gust Slash', 6473.0),
                ('_Bunshin_melee', 5968.4),
                ('Aeolian Edge', 8111.4),
                ('_Bunshin_area', 2984.0),
                ('Hakke Mujinsatsu', 4054.4),
                ('_Bunshin_melee', 5970.8),
                ('Armor Crush', 8093.4))

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_nin_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=2.56, main_stat=3360, det_stat=1697, crit_stat=2554, dh_stat=1582, speed_stat=400, job_class = 'NIN')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Huton')
    rb.add_next('Hide')
    rb.add_next('Suiton')
    rb.add_next('Kassatsu')
    rb.add_next('Spinning Edge')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Gust Slash')
    rb.add_next('Mug')
    rb.add_next('Bunshin')
    rb.add_next('Phantom Kamaitachi')
    rb.add_next('Trick Attack')
    rb.add_next('Aeolian Edge')
    rb.add_next('Dream Within a Dream')
    rb.add_next('Ten')
    rb.add_next('Jin')
    rb.add_next('Hyosho Ranryu')
    rb.add_next('Ten')
    rb.add_next('Chi')
    rb.add_next('Raiton')
    rb.add_next('Ten Chi Jin')
    rb.add_next('Fuma Shuriken')
    rb.add_next('Raiton')
    rb.add_next('Suiton')
    rb.add_next('Meisui')
    rb.add_next('Forked Raiju')
    rb.add_next('Bhavacakra')
    rb.add_next('Forked Raiju')
    rb.add_next('Bhavacakra')
    rb.add_next('Ten')
    rb.add_next('Chi')
    rb.add_next('Raiton')
    rb.add_next('Forked Raiju')
    expected_damage = 566924.6
    expected_total_time = 24748.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_drg_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=2.8, main_stat=3379, det_stat=1818, crit_stat=2567, dh_stat=1818, speed_stat=400, job_class = 'DRG')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('True Thrust')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Disembowel')
    rb.add_next('Lance Charge')
    rb.add_next('Dragon Sight')
    rb.add_next('Chaotic Spring')
    rb.add_next('Battle Litany')
    rb.add_next('Wheeling Thrust')
    rb.add_next('Geirskogul')
    rb.add_next('Life Surge')
    rb.add_next('Fang and Claw')
    rb.add_next('High Jump')
    rb.add_next('Mirage Dive')
    rb.add_next('Raiden Thrust')
    rb.add_next('Dragonfire Dive')
    rb.add_next('Vorpal Thrust')
    rb.add_next('Spineshatter Dive')
    rb.add_next('Life Surge')
    rb.add_next("Heavens' Thrust")
    rb.add_next('Fang and Claw')
    rb.add_next('Wheeling Thrust')
    rb.add_next('Raiden Thrust')
    rb.add_next('Wyrmwind Thrust')
    rb.add_next('Disembowel')
    rb.add_next('Chaotic Spring')
    rb.add_next('Wheeling Thrust')

    expected_damage =  465784.9
    expected_total_time = 32410.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_drg_bonus_percent_e2e(self):
    stats = Stats(wd=132, weapon_delay=2.8, main_stat=3379, det_stat=1818, crit_stat=2567, dh_stat=1818, speed_stat=400, job_class = 'DRG')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True)
    rb.add_next('Fang and Claw')
    rb.add_next('Wheeling Thrust', skill_modifier=SkillModifier(bonus_percent=10))
    rb.add_next('Vorpal Thrust')
    rb.add_next('Fang and Claw', skill_modifier=SkillModifier(bonus_percent=13))
    rb.add_next('Fang and Claw', skill_modifier=SkillModifier(bonus_percent=0))

    expected = (('Fang and Claw', 12667.8),
                ('Wheeling Thrust', 16903.7),
                ('Vorpal Thrust', 5488.7),
                ('Fang and Claw', 12667.8),
                ('Fang and Claw', 10986.7))

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_drg_bonus_percent(self):
    test_passed = True
    err_msg = ''
    skill = self.__skill_library.get_skill('Wheeling Thrust', 'DRG')

    inputs = [SkillModifier(with_condition='', bonus_percent = 13),
              SkillModifier(with_condition='Fang and Claw', bonus_percent=10)]
    expected_outputs = (set([SimConsts.DEFAULT_CONDITION]),
                        set(['Fang and Claw']))

    for i in range(0, len(inputs)):
      init_skill_modifier = inputs[i]
      try:
        result = Utils.canonicalize_condition(Utils.get_positional_condition(skill, init_skill_modifier))
      except ValueError as v:
        result = init_skill_modifier.with_condition
        test_passed = False
        err_msg += str(v)
      if ",".join(result) != ",".join(expected_outputs[i]):
        print(",".join(init_skill_modifier.with_condition))
        test_passed = False
        err_msg += "Conditions did not match for example {}. Expected: '{}'. Actual: '{}'\n".format(i, ", ".join(expected_outputs[i]), ", ".join(result.with_condition))

    return test_passed, err_msg

  @TestClass.is_a_test
  def test_rdm_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.44, main_stat=3379, det_stat=1601, crit_stat=2514, dh_stat=1708, speed_stat=502, job_class = 'RDM', healer_or_caster_strength=214)

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Verthunder III')
    rb.add_next('Veraero III')
    rb.add_next('Swiftcast')
    rb.add_next('Acceleration')
    rb.add_next('Verthunder III')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Verthunder III')
    rb.add_next('Embolden')
    rb.add_next('Manafication')
    rb.add_next('Enchanted Riposte')
    rb.add_next('Fleche')
    rb.add_next('Enchanted Zwerchhau')
    rb.add_next('Contre Sixte')
    rb.add_next('Enchanted Redoublement')
    rb.add_next('Corps-a-corps')
    rb.add_next('Engagement')
    rb.add_next('Verholy')
    rb.add_next('Corps-a-corps')
    rb.add_next('Engagement')
    rb.add_next('Scorch')
    rb.add_next('Resolution')
    rb.add_next('Verfire')
    rb.add_next('Verthunder III')
    rb.add_next('Verstone')
    rb.add_next('Veraero III')
    rb.add_next('Jolt II')
    rb.add_next('Verthunder III')
    rb.add_next('Fleche')

    expected_damage = 519391.8
    expected_total_time = 34590.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_sam_combos(self):
    stats = Stats(wd=132, weapon_delay=2.64, main_stat=3367, det_stat=1736, crit_stat=2587, dh_stat=1494, speed_stat=508, job_class = 'SAM')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Meikyo Shisui')
    rb.add_next('Gekko')
    rb.add_next('Kasha')
    rb.add_next('Yukikaze')
    rb.add_next('Meikyo Shisui')
    rb.add_next('Jinpu')
    rb.add_next('Shifu')
    rb.add_next('Hakaze')
    rb.add_next('Meikyo Shisui')
    rb.add_next('Mangetsu')
    rb.add_next('Oka')
    rb.add_next('Fuko')

    expected_damage = 126529.1
    expected_total_time = 17860.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_sam_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=2.64, main_stat=3367, det_stat=1736, crit_stat=2587, dh_stat=1494, speed_stat=508, job_class = 'SAM')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Meikyo Shisui')
    rb.add_next('True North')
    rb.add_next('Gekko')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Kasha')
    rb.add_next('Yukikaze')
    rb.add_next('Midare Setsugekka')
    rb.add_next('Hissatsu: Senei')
    rb.add_next('Kaeshi: Setsugekka')
    rb.add_next('Meikyo Shisui')
    rb.add_next('Gekko')
    rb.add_next('Hissatsu: Shinten')
    rb.add_next('Higanbana')
    rb.add_next('Hissatsu: Shinten')
    rb.add_next('Ogi Namikiri')
    rb.add_next('Shoha')
    rb.add_next('Kaeshi: Namikiri')
    rb.add_next('Kasha')
    rb.add_next('Hissatsu: Shinten')
    rb.add_next('Gekko')
    rb.add_next('Hissatsu: Gyoten')
    rb.add_next('Hakaze')
    rb.add_next('Hissatsu: Shinten')
    rb.add_next('Yukikaze')
    rb.add_next('Midare Setsugekka')
    rb.add_next('Kaeshi: Setsugekka')

    expected_damage = 630124.6
    expected_total_time = 32120.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_rpr_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.2, main_stat=3379, det_stat=1764, crit_stat=2567, dh_stat=1558, speed_stat=436, job_class = 'RPR')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Harpe')
    rb.add_next('Shadow of Death')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Soul Slice')
    rb.add_next('Arcane Circle')
    rb.add_next('Gluttony')
    rb.add_next('Gibbet')
    rb.add_next('Gallows')
    rb.add_next('Plentiful Harvest')
    rb.add_next('Enshroud')
    rb.add_next('Void Reaping')
    rb.add_next('Cross Reaping')
    rb.add_next("Lemure's Slice")
    rb.add_next('Void Reaping')
    rb.add_next('Cross Reaping')
    rb.add_next("Lemure's Slice")
    rb.add_next('Communio')
    rb.add_next('Soul Slice')
    rb.add_next('Unveiled Gibbet')
    rb.add_next('Gibbet')

    expected_damage = 464185.7
    expected_total_time = 24200.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_mnk_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=2.56, main_stat=3356, det_stat=1453, crit_stat=2647, dh_stat=1453, speed_stat=771, job_class = 'MNK')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Form Shift')
    rb.add_next('Dragon Kick')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Twin Snakes')
    rb.add_next('Riddle of Fire')
    rb.add_next('Demolish')
    rb.add_next('The Forbidden Chakra')
    rb.add_next('Bootshine')
    rb.add_next('Brotherhood')
    rb.add_next('Perfect Balance')
    rb.add_next('Dragon Kick')
    rb.add_next('Riddle of Wind')
    rb.add_next('Bootshine')
    rb.add_next('Dragon Kick')
    rb.add_next('Elixir Field')
    rb.add_next('Bootshine')
    rb.add_next('Perfect Balance')
    rb.add_next('Twin Snakes')
    rb.add_next('Dragon Kick')
    rb.add_next('Demolish')
    rb.add_next('Rising Phoenix')

    expected_damage = 391365.1
    expected_total_time = 22770.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_brd_add_gauge(self):
    stats = Stats(wd=132, weapon_delay=3.04, main_stat=3379, det_stat=1885, crit_stat=2598, dh_stat=1344, speed_stat=479, job_class = 'BRD')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)

    rb.add(0, "Add Soul Voice")
    rb.add(3, "Add Soul Voice", skill_modifier=SkillModifier(with_condition='90'))
    rb.add(6, "Apex Arrow") #95 voice
    rb.add(9, "Add Soul Voice", skill_modifier=SkillModifier(with_condition='20'))
    rb.add(12, "Apex Arrow")
    rb.add(15, "Add Soul Voice", skill_modifier=SkillModifier(with_condition='100'))
    rb.add(18, "Apex Arrow")

    rb.add(20, "Add Repertoire")
    rb.add(26, "Pitch Perfect")
    rb.add(27, "Add Repertoire",)
    rb.add(28, "Add Repertoire", skill_modifier=SkillModifier(with_condition='2'))
    rb.add(30, "Pitch Perfect")
    rb.add(31, "Add Repertoire")
    rb.add(33, "Add Repertoire")
    rb.add(34, "Pitch Perfect")

    expected = (('Apex Arrow', 23485.1),
                ('Apex Arrow', 4948.9),
                ('Apex Arrow', 24763.2),
                ('Pitch Perfect', 4949.5),
                ('Pitch Perfect', 17820.9),
                ('Pitch Perfect', 10876.4))

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_brd_songs(self):
    stats = Stats(wd=132, weapon_delay=3.04, main_stat=3379, det_stat=1885, crit_stat=2598, dh_stat=1344, speed_stat=479, job_class = 'BRD')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add(0, "Sidewinder")

    rb.add(3, "The Wanderer's Minuet")
    rb.add(6, "Radiant Finale")
    rb.add(9, "Sidewinder")

    rb.add(12, "Army's Paeon")
    rb.add(15, "Mage's Ballad")
    rb.add(18, "Radiant Finale")
    rb.add(21, "Sidewinder")

    rb.add(24, "The Wanderer's Minuet")
    rb.add(27, "Army's Paeon")
    rb.add(30, "Mage's Ballad")
    rb.add(33, "Radiant Finale")
    rb.add(36, "Sidewinder")

    expected = (('Sidewinder', 15822.5),
                ("The Wanderer's Minuet", 4121.4),
                ('Sidewinder', 16352.2),
                ("Army's Paeon", 4246.9),
                ("Mage's Ballad", 4236.9),
                ('Sidewinder', 16621.7),
                ("The Wanderer's Minuet", 4332.8),
                ("Army's Paeon", 4337.2),
                ("Mage's Ballad", 4308.6),
                ('Sidewinder', 16932.4))

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_brd_rotation_damage_instances(self):
    stats = Stats(wd=132, weapon_delay=3.04, main_stat=3379, det_stat=1885, crit_stat=2598, dh_stat=1344, speed_stat=479, job_class = 'BRD')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next("The Wanderer's Minuet", SkillModifier(with_condition='Buff Only'))
    rb.add_next("Army's Paeon", SkillModifier(with_condition='Buff Only'))
    rb.add_next("Mage's Ballad", SkillModifier(with_condition='Buff Only'))
    rb.add_next("Sidewinder")
    rb.add_next('Radiant Finale')
    rb.add_next("Sidewinder")
    rb.add_next('Radiant Finale', SkillModifier(with_condition='2 Coda, Buff Only'))
    rb.add_next("Sidewinder")

    expected = (('Sidewinder', 15989.8),
                ('Sidewinder', 15996.7), #does not get buff yet. Application delay.
                ('Sidewinder', 16932.4)) #does not get overriden radiant finale buff yet. Application delay.

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_brd_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.04, main_stat=3379, det_stat=1885, crit_stat=2598, dh_stat=1344, speed_stat=479, job_class = 'BRD')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Stormbite')
    rb.add_next("The Wanderer's Minuet")
    rb.add_next("Raging Strikes")
    rb.add_next('Caustic Bite')
    rb.add_next('Empyreal Arrow')
    rb.add_next('Bloodletter')
    rb.add_next('Refulgent Arrow')
    rb.add_next('Radiant Finale')
    rb.add_next('Battle Voice')
    rb.add_next('Refulgent Arrow')
    rb.add_next('Sidewinder')
    rb.add_next('Refulgent Arrow')
    rb.add_next('Barrage')
    rb.add_next('Refulgent Arrow')
    rb.add_next('Burst Shot')
    rb.add_next('Refulgent Arrow')
    rb.add_next('Empyreal Arrow')
    rb.add_next('Iron Jaws')
    rb.add_next('Pitch Perfect')

    expected_damage = 299859.1
    expected_total_time = 19580.0

    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_drg_rotation_damage_instances(self):
    stats = Stats(wd=132, weapon_delay=2.8, main_stat=3379, det_stat=1818, crit_stat=2567, dh_stat=1818, speed_stat=400, job_class = 'DRG')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('True Thrust')
    rb.add_next('Vorpal Thrust')
    rb.add_next("Heavens' Thrust")
    rb.add_next('Fang and Claw')
    rb.add_next('Wheeling Thrust')

    # Not part of combo, and technically illegal, but we add this for testing.
    rb.add_next('True Thrust')
    rb.add_next('Wheeling Thrust')
    rb.add_next('Fang and Claw')

    rb.add_next('Wheeling Thrust')
    rb.add_next('True Thrust')
    rb.add_next('Fang and Claw')

    expected = (('True Thrust', 9713.7),
                ('Vorpal Thrust', 11867.5),
                ("Heavens' Thrust", 20274.8),
                ('Fang and Claw', 12678.4),
                ('Wheeling Thrust', 16900.6), #gets bonus
                #
                ('True Thrust', 9716.9),
                ('Wheeling Thrust', 12674.8),
                ('Fang and Claw', 16893.5),
                #
                ('Wheeling Thrust', 12674.8),
                ('True Thrust', 9713.7), # eat the Wheeling Thrust/Lance mastery buff, wasting it.
                ('Fang and Claw', 12674.8),)
    test_passed1, err_msg1 = self.__test_rotation_damage(rb, expected)

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Vorpal Thrust')
    rb.add_next("Heavens' Thrust")

    expected = (('Vorpal Thrust', 5488.0),
                ("Heavens' Thrust", 4231.9))

    test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
    return test_passed1 and test_passed2, ",".join([err_msg1, err_msg2])

  @TestClass.is_a_test
  def test_mch_rotation_damage_instances(self):
    stats = Stats(wd=132, weapon_delay=2.64, main_stat=3376, det_stat=2114, crit_stat=2557, dh_stat=1254, speed_stat=400, job_class = 'MCH')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Wildfire', skill_modifier=SkillModifier(with_condition='Manual'))
    rb.add_next('Detonator', skill_modifier=SkillModifier(with_condition='6 GCD'))
    rb.add_next('Detonator', skill_modifier=SkillModifier(with_condition='5 GCD'))
    rb.add_next('Detonator', skill_modifier=SkillModifier(with_condition='4 GCD'))
    rb.add_next('Detonator', skill_modifier=SkillModifier(with_condition='3 GCD'))
    rb.add_next('Detonator', skill_modifier=SkillModifier(with_condition='2 GCD'))
    rb.add_next('Detonator', skill_modifier=SkillModifier(with_condition='1 GCD'))
    rb.add_next('Detonator', skill_modifier=SkillModifier())

    expected = (('Detonator', 57463.6),
                ('Detonator', 47899.7),
                ('Detonator', 38321.5),
                ('Detonator', 28737.6),
                ('Detonator', 19157.3),
                ('Detonator', 9577.1),
                ('Detonator', 0.0))

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_mch_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=2.64, main_stat=3376, det_stat=2114, crit_stat=2557, dh_stat=1254, speed_stat=400, job_class = 'MCH')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Heated Split Shot')
    rb.add_next('Gauss Round')
    rb.add_next('Ricochet')
    rb.add_next('Drill')
    rb.add_next('Barrel Stabilizer')
    rb.add_next('Heated Slug Shot')
    rb.add_next('Ricochet')
    rb.add_next('Heated Clean Shot')
    rb.add_next('Reassemble')
    rb.add_next('Gauss Round')
    rb.add_next('Air Anchor')
    rb.add_next('Reassemble')
    rb.add_next('Wildfire')
    rb.add_next('Chain Saw')
    rb.add_next('Automaton Queen')
    rb.add_next('Hypercharge')
    rb.add_next('Heat Blast')
    rb.add_next('Ricochet')
    rb.add_next('Heat Blast')
    rb.add_next('Gauss Round')
    rb.add_next('Heat Blast')
    rb.add_next('Ricochet')
    rb.add_next('Heat Blast')
    rb.add_next('Gauss Round')
    rb.add_next('Heat Blast')
    rb.add_next('Ricochet')
    rb.add_next('Drill')
    rb.add_next('Ricochet')
    rb.add_next('Heated Split Shot')
    rb.add_next('Heated Slug Shot')
    rb.add_next('Heated Clean Shot')

    expected_damage = 562374.1
    expected_total_time = 30000.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_blm_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.28, main_stat=3375, det_stat=1764, crit_stat=545, dh_stat=1547, speed_stat=2469, job_class = 'BLM')

    rb = RotationBuilder(stats, self.__skill_library, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Sharpcast')
    rb.add_next('Fire III')
    rb.add_next('Thunder III')
    rb.add_next('Triplecast')
    rb.add_next('Fire IV')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Fire IV')
    rb.add_next('Amplifier')
    rb.add_next('Ley Lines')
    rb.add_next('Fire IV')
    rb.add_next('Swiftcast')
    rb.add_next('Fire IV')
    rb.add_next('Triplecast')
    rb.add_next('Despair')
    rb.add_next('Manafont')
    rb.add_next('Fire IV')
    rb.add_next('Sharpcast')
    rb.add_next('Despair')
    rb.add_next('Blizzard III')
    rb.add_next('Xenoglossy')
    rb.add_next('Paradox')
    rb.add_next('Blizzard IV')
    rb.add_next('Thunder III')

    expected_damage = 423107.9
    expected_total_time = 22880.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_dnc_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.12, main_stat=3379, det_stat=1952, crit_stat=2557, dh_stat=1380, speed_stat=436, job_class = 'DNC')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=True, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Double Standard Finish')
    rb.add_next('Technical Step')
    rb.add_next('Step Action')
    rb.add_next('Step Action')
    rb.add_next('Step Action')
    rb.add_next('Step Action')
    rb.add_next('Quadruple Technical Finish')
    rb.add_next('Devilment')
    rb.add_next('Starfall Dance')
    rb.add_next('Flourish')
    rb.add_next('Fan Dance III')
    rb.add_next('Fountainfall')
    rb.add_next('Fan Dance')
    rb.add_next('Fan Dance IV')
    rb.add_next('Tillana')
    rb.add_next('Fan Dance III')
    rb.add_next('Saber Dance')
    rb.add_next('Standard Step')
    rb.add_next('Step Action')
    rb.add_next('Step Action')
    rb.add_next('Double Standard Finish')
    rb.add_next('Saber Dance')
    rb.add_next('Reverse Cascade')
    rb.add_next('Saber Dance')
    expected_damage = 497533.9
    expected_total_time = 27360.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_smn_aggregate_rotation(self):
    stats = Stats(wd=132, weapon_delay=3.12, main_stat=3379, det_stat=1871, crit_stat=2514, dh_stat=1438, speed_stat=502, job_class = 'SMN')

    rb = RotationBuilder(stats, self.__skill_library, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Ruin III')
    rb.add_next('Summon Bahamut')
    rb.add_next('Searing Light')
    rb.add_next('Astral Impulse')
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Astral Impulse')
    rb.add_next('Astral Impulse')
    rb.add_next('Energy Drain')
    rb.add_next('Enkindle Bahamut')
    rb.add_next('Astral Impulse')
    rb.add_next('Deathflare')
    rb.add_next('Fester')
    rb.add_next('Astral Impulse')
    rb.add_next('Fester')
    rb.add_next('Astral Impulse')
    rb.add_next('Summon Garuda II')
    rb.add_next('Swiftcast')
    rb.add_next('Slipstream')
    rb.add_next('Emerald Rite')
    rb.add_next('Emerald Rite')
    rb.add_next('Emerald Rite')
    rb.add_next('Emerald Rite')
    rb.add_next('Summon Titan II')
    rb.add_next('Summon Phoenix') #idk just because, to test the subsequent autos

    expected_damage = 529126.8
    expected_total_time = 44440.0
    return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

  @TestClass.is_a_test
  def test_dnc_buff_expire(self):
    stats = Stats(wd=132, weapon_delay=3.12, main_stat=3379, det_stat=1952, crit_stat=2557, dh_stat=1380, speed_stat=436, job_class = 'DNC')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Cascade')
    rb.add_next('Quadruple Technical Finish', skill_modifier=SkillModifier(with_condition='Longest'))
    rb.add_next('Cascade')
    rb.add_next('Quadruple Technical Finish', skill_modifier=SkillModifier(with_condition='Remove Buff'))
    rb.add_next('Cascade')

    expected = (('Cascade', 10931.4),
                ('Quadruple Technical Finish', 59607.2),
                ('Cascade', 11449.4),
                ('Cascade', 10931.4))
    test_passed1, err_msg1 = self.__test_rotation_damage(rb, expected)

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Cascade')
    rb.add_next('Double Standard Finish')
    rb.add_next('Cascade')
    rb.add_next('Double Standard Finish', skill_modifier=SkillModifier(with_condition='Remove Buff'))
    rb.add_next('Cascade')

    expected = (('Cascade', 10931.4),
                ('Double Standard Finish', 35748.5),
                ('Cascade', 11449.4),
                ('Cascade', 10931.4))
    test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)

    return test_passed1 and test_passed2, ", ".join([err_msg1, err_msg2])

  @TestClass.is_a_test
  def test_sam_rotation_damage_instances(self):
    stats = Stats(wd=132, weapon_delay=2.64, main_stat=3367, det_stat=1736, crit_stat=2587, dh_stat=1494, speed_stat=508, job_class = 'SAM')

    rb = RotationBuilder(stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True, fight_start_time=0)
    rb.add(-7.045, 'Meikyo Shisui')
    rb.add(1.206, 'Kasha', skill_modifier=SkillModifier(bonus_percent=68))
    rb.add(5.806, 'Gekko')
    rb.add(7.995, 'Kasha', skill_modifier=SkillModifier(bonus_percent=68))
    rb.add(100.0, 'Enpi')
    rb.add(102.0, 'Hissatsu: Yaten')
    rb.add(104.0, 'Enpi')
    rb.add(106.0, 'Enpi')

    expected = (('Kasha', 15503.1),
                ('Gekko', 15503.1),
                ('Kasha', 17504.8),
                ('Enpi', 4081.2),
                ('Hissatsu: Yaten', 4077),
                ('Enpi', 10598.7),
                ('Enpi', 4081.2))

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_blm_rotation_damage_instances(self):
    stats = Stats(wd=132, weapon_delay=3.28, main_stat=3375, det_stat=1764, crit_stat=545, dh_stat=1547, speed_stat=2469, job_class = 'BLM')
    rb = RotationBuilder(stats, self.__skill_library, ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)

    rb.add(0, 'Fire III')
    rb.add(4.556, 'Fire IV')
    rb.add(7.012, 'Fire IV')
    rb.add(8.356, 'Fire IV')
    rb.add(10.411, 'Fire IV')
    rb.add(13.091, 'Transpose')
    rb.add(14.522, 'Paradox')
    rb.add(16.579, 'Xenoglossy')
    rb.add(18.099, 'Transpose')
    rb.add(18.769, 'Fire III')

    expected = (('Fire III', 12208.6),
                ('Fire IV', 32218.3),
                ('Fire IV', 32218.3),
                ('Fire IV', 32218.3),
                ('Fire IV', 32218.3),
                ('Paradox', 28865.3),
                ('Xenoglossy', 50834.4),
                ('Fire III', 21004.7))

    return self.__test_rotation_damage(rb, expected)

  @TestClass.is_a_test
  def test_ast_star(self):
    stats = Stats(wd=132, weapon_delay=3.2, main_stat=3366, det_stat=2047, crit_stat=2430, dh_stat=400, speed_stat=1350, job_class = 'AST', healer_or_caster_strength=214)

    rb = RotationBuilder(stats, self.__skill_library)
    rb.add(0, 'Earthly Star', skill_modifier=SkillModifier())

    rb.add(100, 'Earthly Star', skill_modifier=SkillModifier())
    rb.add(108, 'Stellar Detonation', skill_modifier=SkillModifier())

    rb.add(200, 'Earthly Star', skill_modifier=SkillModifier())
    rb.add(215, 'Stellar Detonation', skill_modifier=SkillModifier())

    expected = (('Stellar Detonation', 14899.6),
                ('Stellar Detonation', 9840.6),
                ('Stellar Detonation', 14899.6),)

    return self.__test_rotation_damage(rb, expected)

