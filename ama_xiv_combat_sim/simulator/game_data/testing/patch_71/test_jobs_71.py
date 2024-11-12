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


class TestJobsUnified71(TestClass):
    def __init__(self):
        super().__init__()
        self.__version = "7.1"
        self.__level = 100
        self.__skill_library = create_skill_library(
            version=self.__version, level=self.__level
        )
        self.__job_class_tester = JobClassTesterUtil(self.__skill_library)
        
    @TestClass.is_a_test
    def test_drg_enhanced_piercing_talon(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.8,
            main_stat=3379,
            det_stat=1818,
            crit_stat=2567,
            dh_stat=1818,
            speed_stat=400,
            job_class="DRG",
            version=self.__version,
            level=self.__level,
        )
        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Piercing Talon")
        rb.add_next("Elusive Jump")
        rb.add_next("Piercing Talon")
        expected = (            
            ("Piercing Talon", 8205),
            ("Piercing Talon", 14363),
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)
    
    @TestClass.is_a_test
    def test_flare_cast_time(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.28,
            main_stat=3375,
            det_stat=1764,
            crit_stat=545,
            dh_stat=1547,
            speed_stat=2469,
            job_class="BLM",
            version="7.1",
            level=100,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        
        rb.add_next("Fire III")
        rb.add_next("Flare")
        rb.add_next("Fire III")
        expected_damage = 72994
        expected_total_time = 6070
        
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )