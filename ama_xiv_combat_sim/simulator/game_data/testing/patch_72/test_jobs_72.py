from ama_xiv_combat_sim.simulator.game_data.job_class_tester_util import (
    JobClassTesterUtil,
)
from ama_xiv_combat_sim.simulator.skills.create_skill_library import (
    create_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import OffensiveStatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)


class TestJobsUnified72(TestClass):
    def __init__(self):
        super().__init__()
        self.__version = "7.2"
        self.__level = 100
        self.__skill_library = create_skill_library(
            version=self.__version, level=self.__level
        )
        self.__job_class_tester = JobClassTesterUtil(self.__skill_library)

    @TestClass.is_a_test
    def test_whm_skills(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.44,
            main_stat=3366,
            det_stat=2047,
            crit_stat=2502,
            dh_stat=616,
            speed_stat=1062,
            job_class="WHM",
            healer_or_caster_strength=214,
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Dia", SkillModifier(), 45472),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)
    
    @TestClass.is_a_test
    def test_blm_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.28,
            main_stat=3375,
            det_stat=1764,
            crit_stat=545,
            dh_stat=1547,
            speed_stat=2469,
            job_class="BLM",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Fire III")
        rb.add_next("Thunder III")
        rb.add_next("Triplecast")
        rb.add_next("Fire IV")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Fire IV")
        rb.add_next("Amplifier")
        rb.add_next("Ley Lines")
        rb.add_next("Fire IV")
        rb.add_next("Swiftcast")
        rb.add_next("Fire IV")
        rb.add_next("Triplecast")
        rb.add_next("Despair")
        rb.add_next("Manafont")
        rb.add_next("Fire IV")
        rb.add_next("Despair")
        rb.add_next("Blizzard III")
        rb.add_next("Xenoglossy")
        rb.add_next("Paradox")
        rb.add_next("Blizzard IV")
        rb.add_next("Thunder III")

        expected_damage = 443135
        expected_total_time = 26020
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )
        
    @TestClass.is_a_test
    def test_blm_infinite_enochian(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.28,
            main_stat=3375,
            det_stat=1764,
            crit_stat=545,
            dh_stat=1547,
            speed_stat=2469,
            job_class="BLM",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        
        rb.add(0, "Fire")
        rb.add(3, "Fire")
        rb.add(6, "Fire")
        rb.add(100, "Fire")
        rb.add(1000, "Fire")
        
        expected = (
            ("Fire", 8665),
            ("Fire", 15407),
            ("Fire", 17608),
            ("Fire", 19810),
            ("Fire", 19810),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)
    
    @TestClass.is_a_test
    def test_gnb_fight_or_flight_app_same_timestamp(self):
        stats = Stats(
            wd=126,
            weapon_delay=2.80,
            main_stat=2891,
            det_stat=1844,
            crit_stat=2377,
            dh_stat=1012,
            speed_stat=400,
            tenacity=751,
            job_class="GNB",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        
        rb.add(0, "Hypervelocity")
        rb.add(123.87, "No Mercy")
        rb.add(124.49, "Hypervelocity")
        
        expected = (
            ("Hypervelocity", 5098),
            ("Hypervelocity", 6117),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)
    
    @TestClass.is_a_test
    def test_nin_hollow_nozuchi(self):
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
            level=self.__level,
        )
        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        
        #rapid fire because i dont want to minimize dealing with doton dots
        rb.add(0, "Doton")
        rb.add(1, "Katon")
        rb.add(2, "Goka Mekkyaku")
        rb.add(3, "Phantom Kamaitachi")
        rb.add(5, "Death Blossom")
        rb.add(6, "Hakke Mujinsatsu")
        rb.add(7, "Hakke Mujinsatsu")
        
        #after doton
        rb.add(101, "Katon")
        rb.add(102, "Goka Mekkyaku")
        rb.add(103, "Phantom Kamaitachi")
        rb.add(105, "Death Blossom")
        rb.add(106, "Hakke Mujinsatsu")
        rb.add(107, "Hakke Mujinsatsu")
        
        expected = (
            ("Doton", 3167),
            ("Katon", 13880),
            ("Hollow Nozuchi", 1979),
            ("Goka Mekkyaku", 23799),
            ("Doton (dot)", 3167),
            ("Hollow Nozuchi", 1979),
            ("Phantom Kamaitachi (pet)", 21765),            
            ("Death Blossom", 3966),            
            ("Doton (dot)", 3167),
            ("Hollow Nozuchi", 1979),
            ("Hakke Mujinsatsu", 4757),
            ("Hollow Nozuchi", 1979),
            ("Hakke Mujinsatsu", 3966),
            ("Doton (dot)", 3167),
            ("Doton (dot)", 3167),
            ("Doton (dot)", 3167),
            ("Doton (dot)", 3167),
            # after doton, so no dotons or hollow nozuchis
            ("Katon", 13880),
            ("Goka Mekkyaku", 23799),
            ("Phantom Kamaitachi (pet)", 21765),            
            ("Death Blossom", 3966),      
            ("Hakke Mujinsatsu", 4757),
            ("Hakke Mujinsatsu", 3966)
            
        )
        
        return self.__job_class_tester.test_rotation_damage(rb, expected)