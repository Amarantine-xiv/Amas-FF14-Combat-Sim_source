from simulator.testing.create_test_skill_library import create_test_skill_library
from simulator.testing.test_class import TestClass

class TestSkills(TestClass):
  def __init__(self):
    self.__skill_library = create_test_skill_library()

  @TestClass.is_a_test
  def test_has_status_effect(self):
    test_passed = True
    err_msg = ""

    #skill name, has_buff, has_debuff
    skill_names_and_expected = [('test_simple_buff_gcd', True, False),
                                ('test_simple_debuff_gcd', False, True),
                                ('test_gcd', False, False),
                                ('test_magical_dot_instant_gcd', False, False),
                                ('test_simple_buff_gcd_2', True, False),
                                ('test_buff_with_cond', True, False),
                                ('test_skill_with_follow_up_buff1', True, False),
                                ('test_follow_up', False, False)]
    for skill_name, expected_buff, expected_debuff in skill_names_and_expected:
      result_buff = self.__skill_library.get_skill(skill_name, job_class='test_job').has_buff
      result_debuff = self.__skill_library.get_skill(skill_name, job_class='test_job').has_debuff
      if (result_buff != expected_buff) or (result_debuff != expected_debuff):
        test_passed = False
        err_msg += 'Verification failed on: {}. Expected buff: {}. Actual buff: {}. Expected debuff: {}. Actual debuff: {}\n'.format(skill_name, expected_buff, result_buff, expected_debuff, result_debuff)

    return test_passed, err_msg

  @TestClass.is_a_test
  def test_has_party_status_effect(self):
    test_passed = True
    err_msg = ""

    #skill name, has_party_buff, has_party_debuff
    skill_names_and_expected = [('test_simple_buff_gcd', True, False),
                                ('test_simple_debuff_gcd', False, True),
                                ('test_gcd', False, False),
                                ('test_magical_dot_instant_gcd', False, False),
                                ('test_simple_buff_gcd_2', False, False), # it has a buff, but not a party buff
                                ('test_buff_with_cond', True, False),
                                ('test_skill_with_follow_up_buff1', True, False),
                                ('test_follow_up', False, False)]

    for skill_name, expected_buff, expected_debuff in skill_names_and_expected:
      result_buff = self.__skill_library.get_skill(skill_name, job_class='test_job').has_party_buff
      result_debuff = self.__skill_library.get_skill(skill_name, job_class='test_job').has_party_debuff
      if (result_buff != expected_buff) or (result_debuff != expected_debuff):
        test_passed = False
        err_msg += 'Verification failed on: {}. Expected buff: {}. Actual buff: {}. Expected debuff: {}. Actual debuff: {}\n'.format(skill_name, expected_buff, result_buff, expected_debuff, result_debuff)

    return test_passed, err_msg