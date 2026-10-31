from ama_xiv_combat_sim.simulator.game_data.job_class_tester_util import (
    JobClassTesterUtil,
)
from ama_xiv_combat_sim.simulator.skills.create_skill_library import (
    create_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass


class TestSMN(TestClass):
    def __init__(self):
        super().__init__()
        self.__version = "7.5"
        self.__skill_library = {
            70: create_skill_library(version=self.__version, level=70),
            100: create_skill_library(version=self.__version, level=100),
        }

    @TestClass.is_a_test
    def test_smn_skills_70(self):
        level_to_use = 70
        skill_library_to_use = self.__skill_library[level_to_use]
        job_class_tester_to_use = JobClassTesterUtil(skill_library_to_use)
        stats = Stats(
            wd=132,
            main_stat=3366,
            det_stat=2047,
            crit_stat=2502,
            dh_stat=616,
            speed_stat=1062,
            job_class="SMN",
            version=self.__version,
            level=level_to_use,
        )
        skills_and_expected_damage = (
            ("Outburst", SkillModifier(), 6148),
            ("Ruby Ruin III", SkillModifier(), 25195),
            ("Topaz Ruin III", SkillModifier(), 18449),
            ("Emerald Ruin III", SkillModifier(), 11069),
            ("Ruby Outburst", SkillModifier(), 9838),
            ("Topaz Outburst", SkillModifier(), 6744),
            ("Emerald Outburst", SkillModifier(), 4283),
            ("Summon Ifrit", SkillModifier(), 29701),
            ("Summon Garuda", SkillModifier(), 29701),
            ("Summon Titan", SkillModifier(), 29701),
        )

        return job_class_tester_to_use.test_skills(stats, skills_and_expected_damage)
