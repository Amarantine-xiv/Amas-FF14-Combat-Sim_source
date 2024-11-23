from ama_xiv_combat_sim.simulator.game_data.job_class_tester_util import (
    JobClassTesterUtil,
)
from ama_xiv_combat_sim.simulator.skills.create_skill_library import (
    create_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


class TestJobsMultiUnified71(TestClass):
    def __init__(self):
        super().__init__()

        self.__version = "7.1"
        self.__level = 100
        self.__skill_library = create_skill_library(
            version=self.__version, level=self.__level
        )
        self.__job_class_tester = JobClassTesterUtil(self.__skill_library)
        
    @TestClass.is_a_test
    def test_nin_dokumori_damage(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.56,
            main_stat=3360,
            det_stat=1697,
            crit_stat=2554,
            dh_stat=1582,
            speed_stat=400,
            job_class="NIN",
            version=self.__version,
            level=self.__level
        )
        base_dokumori = 11899
        skills_and_expected_damages = (
            (
                "Dokumori",
                "t1, t2, t3",
                SkillModifier(),
                (base_dokumori, 0.75 * base_dokumori, 0.75 * base_dokumori),
            ),
        )
        return self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )
        
    @TestClass.is_a_test
    def test_nin_dokumori_damage_with_debuff(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.56,
            main_stat=3360,
            det_stat=1697,
            crit_stat=2554,
            dh_stat=1582,
            speed_stat=400,
            job_class="NIN",
            version=self.__version,
            level=self.__level
        )
        
        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Death Blossom", targets="t1, t2, t3")
        rb.add(5, "Dokumori", targets="t1, t2")
        rb.add(10, "Death Blossom", targets="t1, t2, t3")        
        
        expected = (
            ("Death Blossom", 3966),
            ("Death Blossom", 3966),
            ("Death Blossom", 3966),
            ("Dokumori", 11899),
            ("Dokumori", 8921),
            ("Death Blossom", 4164),
            ("Death Blossom", 4164),
            ("Death Blossom", 3966) #did not get dokumori'ed
        )
        
        return self.__job_class_tester.test_rotation_damage(
            rb, expected
        )