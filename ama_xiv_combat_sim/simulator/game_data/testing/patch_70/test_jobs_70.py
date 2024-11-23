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


class TestJobsUnified70(TestClass):
    def __init__(self):
        super().__init__()
        self.__version = "7.0"
        self.__level = 100
        self.__skill_library = create_skill_library(
            version=self.__version, level=self.__level
        )
        self.__job_class_tester = JobClassTesterUtil(self.__skill_library)

    @TestClass.is_a_test
    def test_war_skills(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 2610),
            ("Heavy Swing", SkillModifier(), 5674),
            ("Maim", SkillModifier(force_combo=True), 8758),
            ("Maim", SkillModifier(), 4890),
            ("Storm's Path", SkillModifier(force_combo=True), 12358),
            ("Storm's Path", SkillModifier(), 5147),
            ("Storm's Eye", SkillModifier(force_combo=True), 12358),
            ("Storm's Eye", SkillModifier(), 5161),
            ("Upheaval", SkillModifier(), 10312),
            ("Onslaught", SkillModifier(), 3865),
            ("Fell Cleave", SkillModifier(), 14956),
            ("Primal Rend", SkillModifier(), 31574),
            ("Inner Chaos", SkillModifier(), 29773),
            ("Tomahawk", SkillModifier(), 3863),
            ("Overpower", SkillModifier(), 2836),
            ("Mythril Tempest", SkillModifier(force_combo=True), 3613),
            ("Mythril Tempest", SkillModifier(), 2576),
            ("Orogeny", SkillModifier(), 3868),
            ("Decimate", SkillModifier(), 4647),
            ("Damnation", SkillModifier(with_condition="Retaliation"), 1412),
            ("Primal Wrath", SkillModifier(), 18037),
            ("Primal Ruination", SkillModifier(), 33374),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_war_aggregate_rotation(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(stats, self.__skill_library, enable_autos=True)
        rb.add_next("Heavy Swing")
        rb.add_next("Maim")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Storm's Eye")
        rb.add_next("Inner Release")
        rb.add_next("Inner Chaos")
        rb.add_next("Upheaval")
        rb.add_next("Onslaught")
        rb.add_next("Primal Rend")
        rb.add_next("Inner Chaos")
        rb.add_next("Onslaught")
        rb.add_next("Fell Cleave")
        rb.add_next("Onslaught")
        rb.add_next("Fell Cleave")
        rb.add_next("Fell Cleave")
        rb.add_next("Heavy Swing")
        rb.add_next("Maim")
        rb.add_next("Storm's Path")
        rb.add_next("Fell Cleave")
        rb.add_next("Inner Chaos")
        expected_damage = 376198.2
        expected_total_time = 32645

        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_gnb_skills(self):
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
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 2129),
            ("Keen Edge", SkillModifier(), 7637),
            ("Brutal Shell", SkillModifier(force_combo=True), 9691),
            ("Brutal Shell", SkillModifier(), 6122),
            ("Demon Slice", SkillModifier(), 2546),
            ("Lightning Shot", SkillModifier(), 3823),
            ("Solid Barrel", SkillModifier(force_combo=True), 11739),
            ("Solid Barrel", SkillModifier(), 6118),
            ("Burst Strike", SkillModifier(), 11735),
            ("Demon Slaughter", SkillModifier(force_combo=True), 4082),
            ("Demon Slaughter", SkillModifier(), 2547),
            ("Sonic Break", SkillModifier(), 22916),
            ("Gnashing Fang", SkillModifier(), 12755),
            ("Savage Claw", SkillModifier(force_combo=True), 14293),
            ("Wicked Talon", SkillModifier(force_combo=True), 15817),
            ("Bow Shock", SkillModifier(), 11462),
            ("Jugular Rip", SkillModifier(), 6114),
            ("Abdomen Tear", SkillModifier(), 7137),
            ("Eye Gouge", SkillModifier(), 8166),
            ("Fated Circle", SkillModifier(), 7650),
            ("Blasting Zone", SkillModifier(), 20397),
            ("Double Down", SkillModifier(), 30636),
            ("Hypervelocity", SkillModifier(), 5613),
            ("Fated Brand", SkillModifier(), 3060),
            ("Reign of Beasts", SkillModifier(), 20396),
            ("Lion Heart", SkillModifier(), 30567),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_pld_skills(self):
        stats = Stats(
            wd=126,
            weapon_delay=2.24,
            main_stat=2891,
            det_stat=1844,
            crit_stat=2377,
            dh_stat=1012,
            speed_stat=400,
            tenacity=751,
            job_class="PLD",
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 1699),
            ("Fast Blade", SkillModifier(), 5618),
            ("Riot Blade", SkillModifier(force_combo=True), 8406),
            ("Riot Blade", SkillModifier(), 4332),
            ("Total Eclipse", SkillModifier(), 2547),
            ("Shield Bash", SkillModifier(), 2547),
            ("Shield Lob", SkillModifier(), 2547),
            ("Prominence", SkillModifier(force_combo=True), 4331),
            ("Prominence", SkillModifier(), 2547),
            ("Circle of Scorn", SkillModifier(), 7372),
            ("Goring Blade", SkillModifier(), 17849),
            ("Royal Authority", SkillModifier(force_combo=True), 11197),
            ("Royal Authority", SkillModifier(), 4588),
            ("Holy Spirit", SkillModifier(), 9443),
            ("Holy Spirit", SkillModifier(with_condition="Divine Might"), 11982),
            ("Holy Spirit", SkillModifier(with_condition="Requiescat"), 17103),
            (
                "Holy Spirit",
                SkillModifier(with_condition="Divine Might, Requiescat"),
                11983,
            ),            
            ("Holy Circle", SkillModifier(), 2548),
            ("Holy Circle", SkillModifier(with_condition="Divine Might"), 5100),
            ("Holy Circle", SkillModifier(with_condition="Requiescat"), 7651),
            (
                "Holy Circle",
                SkillModifier(with_condition="Divine Might, Requiescat"),
                5099,
            ),
            ("Intervene", SkillModifier(), 3824),
            ("Atonement", SkillModifier(), 11220),
            ("Sepulchre", SkillModifier(), 12251),
            ("Supplication", SkillModifier(), 11732),
            ("Confiteor", SkillModifier(), 11223),
            ("Confiteor", SkillModifier(with_condition="Requiescat"), 23984),
            ("Expiacion", SkillModifier(), 11470),
            ("Blade of Faith", SkillModifier(), 6112),
            ("Blade of Faith", SkillModifier(with_condition="Requiescat"), 18868),
            ("Blade of Truth", SkillModifier(), 8667),
            ("Blade of Truth", SkillModifier(with_condition="Requiescat"), 21448),
            ("Blade of Valor", SkillModifier(), 11216),
            ("Blade of Valor", SkillModifier(with_condition="Requiescat"), 23957),
            ("Blade of Honor", SkillModifier(), 25532),
            ("Imperator", SkillModifier(), 14798),
        )

        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_pld_req_stacks(self):
        stats = Stats(
            wd=126,
            weapon_delay=2.24,
            main_stat=2891,
            det_stat=1844,
            crit_stat=2377,
            dh_stat=1012,
            speed_stat=400,
            tenacity=751,
            job_class="PLD",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True
        )
        rb.add_next("Imperator")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        rb.add_next("Imperator")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        # last one should be weaker, since we should only have 4 charges from early imperator
        rb.add_next("Confiteor")

        expected = (            
            ("Confiteor", 23990),
            ("Imperator", 14794),
            ("Confiteor", 23990),
            ("Imperator", 14802),
            ("Confiteor", 23990),
            ("Confiteor", 23990),
            ("Confiteor", 23990),
            ("Confiteor", 23990),
            ("Confiteor", 11212),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

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
            ("Glare III", SkillModifier(), 16632),
            ("Glare IV", SkillModifier(), 32312),
            ("Assize", SkillModifier(), 20172),
            ("Dia", SkillModifier(), 39813),
            ("Afflatus Misery", SkillModifier(), 66760),
            ("Holy III", SkillModifier(), 7573),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_sge_skills(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.8,
            main_stat=3366,
            det_stat=2047,
            crit_stat=2502,
            dh_stat=1012,
            speed_stat=664,
            job_class="SGE",
            healer_or_caster_strength=214,
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Dosis III", SkillModifier(), 18529),
            ("Phlegma III", SkillModifier(), 30903),
            ("Toxikon II", SkillModifier(), 18558),
            ("Dyskrasia II", SkillModifier(), 8744),
            ("Pneuma", SkillModifier(), 18535),
            ("Eukrasian Dosis III", SkillModifier(), 38905),
            ("Eukrasian Dyskrasia", SkillModifier(), 20585),
            ("Psyche", SkillModifier(), 30874),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_sch_skills(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.12,
            main_stat=3366,
            det_stat=1948,
            crit_stat=2498,
            dh_stat=688,
            speed_stat=954,
            job_class="SCH",
            healer_or_caster_strength=351,
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Broil IV", SkillModifier(), 15103),
            ("Ruin II", SkillModifier(), 10716),
            ("Energy Drain", SkillModifier(), 4875),
            ("Art of War II", SkillModifier(), 8762),
            ("Biolysis", SkillModifier(), 37475),
            ("Baneful Impaction", SkillModifier(), 34940),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_sch_aggregate_rotation(self):
        stats = Stats(
            wd=126,
            weapon_delay=3.12,
            main_stat=3366,
            det_stat=1948,
            crit_stat=2498,
            dh_stat=688,
            speed_stat=954,
            job_class="SCH",
            healer_or_caster_strength=351,
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Broil IV")
        rb.add_next("Biolysis")
        rb.add_next("Broil IV")
        rb.add_next("Broil IV")
        rb.add_next("Chain Stratagem")
        rb.add_next("Broil IV")
        rb.add_next("Energy Drain")
        rb.add_next("Broil IV")
        rb.add_next("Energy Drain")
        rb.add_next("Broil IV")
        rb.add_next("Energy Drain")
        rb.add_next("Broil IV")
        rb.add_next("Broil IV")
        rb.add_next("Energy Drain")
        rb.add_next("Broil IV")
        rb.add_next("Energy Drain")
        rb.add_next("Broil IV")
        rb.add_next("Energy Drain")
        rb.add_next("Broil IV")
        rb.add_next("Broil IV")
        rb.add_next("Broil IV")
        expected_damage = 290862
        expected_total_time = 31720
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_ast_skills(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.2,
            main_stat=3366,
            det_stat=2047,
            crit_stat=2430,
            dh_stat=400,
            speed_stat=1350,
            job_class="AST",
            healer_or_caster_strength=214,
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Fall Malefic", SkillModifier(), 13453),
            ("Combust III", SkillModifier(), 36297),
            ("Earthly Star", SkillModifier(), 14814),
            ("Gravity II", SkillModifier(), 6476),
            ("Macrocosmos", SkillModifier(), 12486),
            ("Oracle", SkillModifier(), 42942),
            ("Lord of Crowns", SkillModifier(), 19957),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    #   This might be wrong because it was 6.55 before?
    def test_ast_star(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.2,
            main_stat=3366,
            det_stat=2047,
            crit_stat=2430,
            dh_stat=400,
            speed_stat=1350,
            job_class="AST",
            healer_or_caster_strength=214,
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Earthly Star", skill_modifier=SkillModifier())

        rb.add(100, "Earthly Star", skill_modifier=SkillModifier())
        rb.add(108, "Stellar Detonation", skill_modifier=SkillModifier())

        rb.add(200, "Earthly Star", skill_modifier=SkillModifier())
        rb.add(215, "Stellar Detonation", skill_modifier=SkillModifier())

        expected = (
            ("Stellar Explosion (pet)", 14814),
            ("Stellar Explosion (pet)", 9788),
            ("Stellar Explosion (pet)", 14814),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_drk_skills(self):
        stats = Stats(
            wd=126,
            weapon_delay=2.96,
            main_stat=2906,
            det_stat=1883,
            crit_stat=2352,
            dh_stat=868,
            speed_stat=650,
            tenacity=631,
            job_class="DRK",
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 2289),
            ("Hard Slash", SkillModifier(), 6660),
            ("Syphon Strike", SkillModifier(force_combo=True), 9236),
            ("Syphon Strike", SkillModifier(), 5638),
            ("Unleash", SkillModifier(), 3081),
            ("Unmend", SkillModifier(), 3842),
            ("Souleater", SkillModifier(force_combo=True), 11796),
            ("Souleater", SkillModifier(), 6153),
            ("Flood of Shadow", SkillModifier(), 4106),
            ("Stalwart Soul", SkillModifier(force_combo=True), 4102),
            ("Stalwart Soul", SkillModifier(), 3076),
            ("Edge of Shadow", SkillModifier(), 11797),
            ("Salted Earth", SkillModifier(), 6456),
            ("Salt and Darkness", SkillModifier(), 12836),
            ("Abyssal Drain", SkillModifier(), 6158),
            ("Carve and Spit", SkillModifier(), 13093),
            ("Bloodspiller", SkillModifier(), 14913),
            ("Quietus", SkillModifier(), 6149),
            ("Shadowbringer", SkillModifier(), 15394),
            ("Living Shadow", SkillModifier(), 71725),
            ("Scarlet Delirium", SkillModifier(), 15393),
            ("Comeuppance", SkillModifier(), 17973),
            ("Torcleaver", SkillModifier(), 20548),
            ("Impalement", SkillModifier(), 8202),
            ("Disesteem", SkillModifier(), 20531),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_drk_aggregate_rotation(self):
        #   This might be wrong because it was 6.55 before?
        stats = Stats(
            wd=126,
            weapon_delay=2.96,
            main_stat=2906,
            det_stat=1883,
            crit_stat=2352,
            dh_stat=868,
            speed_stat=650,
            tenacity=631,
            job_class="DRK",
            version=self.__version,
            level=self.__level,
        )
        rb = RotationBuilder(stats, self.__skill_library, enable_autos=True)

        rb.add_next("Hard Slash")
        rb.add_next("Edge of Shadow")
        rb.add_next("Syphon Strike")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Souleater")
        rb.add_next("Living Shadow")
        rb.add_next("Salted Earth")
        rb.add_next("Bloodspiller")
        rb.add_next("Shadowbringer")
        rb.add_next("Edge of Shadow")
        rb.add_next("Bloodspiller")
        rb.add_next("Carve and Spit")
        rb.add_next("Bloodspiller")
        rb.add_next("Edge of Shadow")
        rb.add_next("Salt and Darkness")
        rb.add_next("Hard Slash")
        rb.add_next("Edge of Shadow")
        rb.add_next("Syphon Strike")
        rb.add_next("Shadowbringer")
        rb.add_next("Edge of Shadow")
        rb.add_next("Souleater")
        rb.add_next("Hard Slash")
        rb.add_next("Syphon Strike")
        rb.add_next("Souleater")
        expected_damage = 403557
        expected_total_time = 27213.0

        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_dnc_buff_expire(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1952,
            crit_stat=2557,
            dh_stat=1380,
            speed_stat=436,
            job_class="DNC",
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
        rb.add_next("Cascade")
        rb.add_next(
            "Quadruple Technical Finish",
            skill_modifier=SkillModifier(with_condition="Longest"),
        )
        rb.add_next("Cascade")
        rb.add_next(
            "Quadruple Technical Finish",
            skill_modifier=SkillModifier(with_condition="Remove Buff"),
        )
        rb.add_next("Cascade")

        expected = (
            ("Cascade", 10676),
            ("Quadruple Technical Finish", 62994),
            ("Cascade", 11198),
            ("Cascade", 10675),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb, expected
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Cascade")
        rb.add_next("Double Standard Finish")
        rb.add_next("Cascade")
        rb.add_next(
            "Double Standard Finish",
            skill_modifier=SkillModifier(with_condition="Remove Buff"),
        )
        rb.add_next("Cascade")

        expected = (
            ("Cascade", 10676),
            ("Double Standard Finish", 41262),
            ("Cascade", 11200),
            ("Cascade", 10677),
        )
        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb, expected
        )

        return test_passed1 and test_passed2, ", ".join([err_msg1, err_msg2])

    @TestClass.is_a_test
    def test_dnc_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1952,
            crit_stat=2557,
            dh_stat=1380,
            speed_stat=436,
            job_class="DNC",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Double Standard Finish")
        rb.add_next("Technical Step")
        rb.add_next("Step Action")
        rb.add_next("Step Action")
        rb.add_next("Step Action")
        rb.add_next("Step Action")
        rb.add_next("Quadruple Technical Finish")
        rb.add_next("Devilment")
        rb.add_next("Starfall Dance")
        rb.add_next("Flourish")
        rb.add_next("Fan Dance III")
        rb.add_next("Fountainfall")
        rb.add_next("Fan Dance")
        rb.add_next("Fan Dance IV")
        rb.add_next("Tillana")
        rb.add_next("Fan Dance III")
        rb.add_next("Saber Dance")
        rb.add_next("Standard Step")
        rb.add_next("Step Action")
        rb.add_next("Step Action")
        rb.add_next("Double Standard Finish")
        rb.add_next("Saber Dance")
        rb.add_next("Reverse Cascade")
        rb.add_next("Saber Dance")
        expected_damage = 530208
        expected_total_time = 27410
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_dnc_skills(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1952,
            crit_stat=2557,
            dh_stat=1380,
            speed_stat=436,
            job_class="DNC",
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 3775),
            ("Cascade", SkillModifier(), 10682),
            ("Fountain", SkillModifier(), 5816),
            ("Fountain", SkillModifier(force_combo=True), 13572),
            ("Windmill", SkillModifier(), 4851),
            ("Double Standard Finish", SkillModifier(), 41218),
            ("Single Standard Finish", SkillModifier(), 26198),
            ("Standard Finish", SkillModifier(), 41250),
            ("Standard Finish", SkillModifier(with_condition="Log"), 17453),
            ("Reverse Cascade", SkillModifier(), 13577),
            ("Bladeshower", SkillModifier(), 4851),
            ("Bladeshower", SkillModifier(force_combo=True), 6789),
            ("Fan Dance", SkillModifier(), 7278),
            ("Rising Windmill", SkillModifier(), 6791),
            ("Fountainfall", SkillModifier(), 16515),
            ("Bloodshower", SkillModifier(), 8728),
            ("Fan Dance II", SkillModifier(), 4853),
            ("Fan Dance III", SkillModifier(), 9696),
            ("Quadruple Technical Finish", SkillModifier(), 63089),
            ("Triple Technical Finish", SkillModifier(), 43693),
            ("Double Technical Finish", SkillModifier(), 34943),
            ("Single Technical Finish", SkillModifier(), 26233),
            ("Saber Dance", SkillModifier(), 25229),
            ("Tillana", SkillModifier(), 29158),
            ("Finishing Move", SkillModifier(), 41253),
            ("Fan Dance IV", SkillModifier(), 14525),
            ("Starfall Dance", SkillModifier(), 50684),
            ("Last Dance", SkillModifier(), 25233),
            ("Dance of the Dawn", SkillModifier(), 48512),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_mch_rotation_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.64,
            main_stat=3376,
            det_stat=2114,
            crit_stat=2557,
            dh_stat=1254,
            speed_stat=400,
            job_class="MCH",
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
        rb.add_next("Wildfire", skill_modifier=SkillModifier(with_condition="Manual"))
        rb.add_next("Detonator", skill_modifier=SkillModifier(with_condition="6 GCD"))
        rb.add_next("Detonator", skill_modifier=SkillModifier(with_condition="5 GCD"))
        rb.add_next("Detonator", skill_modifier=SkillModifier(with_condition="4 GCD"))
        rb.add_next("Detonator", skill_modifier=SkillModifier(with_condition="3 GCD"))
        rb.add_next("Detonator", skill_modifier=SkillModifier(with_condition="2 GCD"))
        rb.add_next("Detonator", skill_modifier=SkillModifier(with_condition="1 GCD"))
        rb.add_next("Detonator", skill_modifier=SkillModifier())

        expected = (
            ("Detonator", 60374),
            ("Detonator", 50316),
            ("Detonator", 40242),
            ("Detonator", 30186),
            ("Detonator", 20123),
            ("Detonator", 10060),
            ("Detonator", 0),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_mch_skills(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.64,
            main_stat=3376,
            det_stat=2114,
            crit_stat=2557,
            dh_stat=1254,
            speed_stat=400,
            job_class="MCH",
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Shot", SkillModifier(), 2837),
            ("Gauss Round", SkillModifier(), 6305),
            ("Heat Blast", SkillModifier(), 9697),
            ("Heat Blast", SkillModifier(with_condition="Reassemble"), 16905),
            ("Heat Blast", SkillModifier(with_condition="Overheated"), 10678),
            (
                "Heat Blast",
                SkillModifier(with_condition="Overheated, Reassemble"),
                18592,
            ),
            ("Ricochet", SkillModifier(), 6315),
            ("Auto Crossbow", SkillModifier(), 7775),
            ("Auto Crossbow", SkillModifier(with_condition="Reassemble"), 13515),
            ("Auto Crossbow", SkillModifier(with_condition="Overheated"), 8732),
            ("Heated Split Shot", SkillModifier(), 10677),
            ("Heated Split Shot", SkillModifier(with_condition="Reassemble"), 18592),
            ("Heated Split Shot", SkillModifier(with_condition="Overheated"), 11656),
            ("Drill", SkillModifier(), 29128),
            ("Drill", SkillModifier(with_condition="Reassemble"), 50722),
            ("Drill", SkillModifier(with_condition="Overheated"), 30148),
            ("Heated Slug Shot", SkillModifier(), 6796),
            ("Heated Slug Shot", SkillModifier(force_combo=True), 15524),
            ("Heated Slug Shot", SkillModifier(with_condition="Reassemble"), 11830),
            ("Heated Slug Shot", SkillModifier(with_condition="Overheated"), 7770),
            ("Air Anchor", SkillModifier(), 29144),
            ("Scattergun", SkillModifier(), 7775),
            # overheated should do nothing
            ("Scattergun", SkillModifier(with_condition="Overheated"), 7759),
            ("Chain Saw", SkillModifier(), 29111),
            ("Double Check", SkillModifier(), 7766),
            ("Excavator", SkillModifier(), 29129),
            ("Full Metal Field", SkillModifier(), 59187),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_brd_rotation_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.04,
            main_stat=3379,
            det_stat=1885,
            crit_stat=2598,
            dh_stat=1344,
            speed_stat=479,
            job_class="BRD",
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

        rb.add_next("The Wanderer's Minuet")
        rb.add_next("Army's Paeon")
        rb.add_next("Mage's Ballad")
        rb.add_next("Sidewinder")
        rb.add_next("Radiant Finale")
        rb.add_next("Sidewinder")
        rb.add_next("Radiant Encore")  # should be 3 coda
        rb.add_next(
            "Radiant Finale",
            SkillModifier(with_condition="1 Mage's Coda, 1 Army's Coda"),
        )
        rb.add_next("Sidewinder")
        rb.add_next("Radiant Encore")  # should be 2 coda
        rb.add_next("Army's Paeon")
        rb.add_next("Wait 2.00s")
        rb.add_next("Radiant Finale")
        rb.add_next("Wait 2.00s")
        rb.add_next("Radiant Encore")  # should be 1 coda

        expected = (
            ("Sidewinder", 19547),
            ("Sidewinder", 20719),
            (
                "Sidewinder",
                20316,
            ),
            ("Radiant Encore", 46662),
            ("Radiant Encore", 30510),
            ("Radiant Encore", 24841),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_brd_songs(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.04,
            main_stat=3379,
            det_stat=1885,
            crit_stat=2598,
            dh_stat=1344,
            speed_stat=479,
            job_class="BRD",
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

        expected = (
            ("Sidewinder", 19368),
            ("Sidewinder", 19946),
            ("Sidewinder", 20364),
            ("Sidewinder", 20747),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_brd_add_gauge(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.04,
            main_stat=3379,
            det_stat=1885,
            crit_stat=2598,
            dh_stat=1344,
            speed_stat=479,
            job_class="BRD",
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

        rb.add(0, "Add Soul Voice")
        rb.add(3, "Add Soul Voice", skill_modifier=SkillModifier(with_condition="90"))
        rb.add(6, "Apex Arrow")  # 95 voice
        rb.add(9, "Add Soul Voice", skill_modifier=SkillModifier(with_condition="20"))
        rb.add(12, "Apex Arrow")
        rb.add(15, "Add Soul Voice", skill_modifier=SkillModifier(with_condition="100"))
        rb.add(18, "Apex Arrow")

        rb.add(20, "Add Repertoire")
        rb.add(26, "Pitch Perfect")
        rb.add(
            27,
            "Add Repertoire",
        )
        rb.add(28, "Add Repertoire", skill_modifier=SkillModifier(with_condition="2"))
        rb.add(30, "Pitch Perfect")
        rb.add(31, "Add Repertoire")
        rb.add(33, "Add Repertoire")
        rb.add(34, "Pitch Perfect")

        expected = (
            ("Apex Arrow", 27548),
            ("Apex Arrow", 5803),
            ("Apex Arrow", 29020),
            ("Pitch Perfect", 4838),
            ("Pitch Perfect", 17390),
            ("Pitch Perfect", 10633),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_mnk_skills(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.56,
            main_stat=3356,
            det_stat=1453,
            crit_stat=2647,
            dh_stat=1453,
            speed_stat=771,
            job_class="MNK",
            version=self.__version,
            level=self.__level,
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 3036),
            ("Twin Snakes", SkillModifier(), 14867),
            ("Demolish", SkillModifier(), 15636),
            ("Rockbreaker", SkillModifier(), 5086),
            ("Four-point Fury", SkillModifier(), 4689),
            ("Dragon Kick", SkillModifier(), 12494),
            ("The Forbidden Chakra", SkillModifier(), 15634),
            ("Elixir Field", SkillModifier(), 31322),
            ("Celestial Revolution", SkillModifier(), 17622),
            ("Enlightenment", SkillModifier(), 6652),
            ("Six-sided Star", SkillModifier(with_condition="5 Chakra"), 46075),
            ("Six-sided Star", SkillModifier(with_condition="0 Chakra"), 30495),
            ("Leaping Opo", SkillModifier(), 10157),
            ("Leaping Opo", SkillModifier(with_condition="Opo-opo's Fury"), 17986),
            ("Rising Raptor", SkillModifier(), 12916),
            ("Rising Raptor", SkillModifier(with_condition="Raptor's Fury"), 18771),
            ("Pouncing Coeurl", SkillModifier(), 15650),
            ("Pouncing Coeurl", SkillModifier(with_condition="Coeurl's Fury"), 19562),
            ("Wind's Reply", SkillModifier(), 31313),
            ("Fire's Reply", SkillModifier(), 43002),
        )
        return self.__job_class_tester.test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_mnk_seqs(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.56,
            main_stat=3356,
            det_stat=1453,
            crit_stat=2647,
            dh_stat=1453,
            speed_stat=771,
            job_class="MNK",
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
        #
        rb.add_next("Wait 5.00s")
        rb.add_next("Rising Raptor")
        rb.add_next("Twin Snakes")
        rb.add_next("Rising Raptor")
        rb.add_next("Rising Raptor")
        rb.add_next("Rising Raptor")
        #
        rb.add_next("Wait 5.00s")
        rb.add_next("Pouncing Coeurl")
        rb.add_next("Demolish")
        rb.add_next("Pouncing Coeurl")
        rb.add_next("Pouncing Coeurl")
        rb.add_next("Pouncing Coeurl")
        rb.add_next("Pouncing Coeurl")

        # test formless fist pattern
        for _ in range(0, 5):
            rb.add_next("Wait 5.00s")
        rb.add_next("Leaping Opo")
        rb.add_next("Elixir Burst")
        rb.add_next("Leaping Opo")

        expected = (
            ("Rising Raptor", 12903),
            ("Twin Snakes", 14881),
            ("Rising Raptor", 18782),
            ("Rising Raptor", 18782),
            ("Rising Raptor", 12891),
            #
            ("Pouncing Coeurl", 15642),
            ("Demolish", 15642),
            ("Pouncing Coeurl", 19576),
            ("Pouncing Coeurl", 19576),
            ("Pouncing Coeurl", 19576),
            ("Pouncing Coeurl", 15639),
            #
            ("Leaping Opo", 14184),
            ("Elixir Burst", 35218),
            ("Leaping Opo", 14184),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_drg_rotation_damage_instances(self):
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
        rb.add_next("True Thrust")
        rb.add_next("Piercing Talon")
        rb.add_next("Dragonfire Dive")
        rb.add_next("Fang and Claw")
        rb.add_next("Rise of the Dragon")
        rb.add_next("Spiral Blow")

        expected = (
            ("True Thrust", 9437),
            ("Piercing Talon", 6149),
            ("Dragonfire Dive", 20501),
            ("Fang and Claw", 7391),
            ("Rise of the Dragon", 22577),
            ("Spiral Blow", 5733),
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_drg_combos(self):
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
        rb.add_next("True Thrust")
        rb.add_next("Lance Barrage")
        rb.add_next("Heavens' Thrust")
        rb.add_next("Fang and Claw")
        rb.add_next("Fang and Claw")
        rb.add_next("Heavens' Thrust")
        rb.add_next("Lance Barrage")

        rb.add_next("True Thrust")
        rb.add_next("Lance Barrage")
        rb.add_next("Lance Barrage")
        rb.add_next("Heavens' Thrust")

        expected = (
            ("True Thrust", 9437),
            ("Lance Barrage", 13927),
            ("Heavens' Thrust", 18047),
            ("Fang and Claw", 13958),
            ("Fang and Claw", 7379),
            ("Heavens' Thrust", 5747),  # no combo bonus
            ("Lance Barrage", 5332),  # no combo bonus
            ("True Thrust", 9436),
            ("Lance Barrage", 13947),
            ("Lance Barrage", 5329),
            ("Heavens' Thrust", 5733),  # no combo bonus
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_nin_hyosho_regression(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.56,
            main_stat=3360,
            dh_stat=1582,
            crit_stat=2554,
            # det_stat=1679,
            det_stat=1679,
            speed_stat=400,
            job_class="NIN",
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
        rb.add(1, "Kassatsu")
        rb.add(3, "Hyosho Ranryu")

        rb.add(423.369, "Spinning Edge")  ##
        rb.add(425.947, "Kassatsu")

        rb.add(427.369, "Gust Slash")
        rb.add(429.506, "Armor Crush")
        rb.add(430.798, "Bhavacakra")
        rb.add(431.642, "Ten")
        rb.add(432.132, "Jin")
        rb.add(432.622, "Hyosho Ranryu")

        expected = (
            ("Hyosho Ranryu", 67050),
            ("Spinning Edge", 11880),
            ("Gust Slash", 15051),
            ("Armor Crush", 18986),
            ("Bhavacakra", 15062),
            ("Hyosho Ranryu", 66992),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_nin_damage_instances(self):
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
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Aeolian Edge")
        rb.add_next(
            "Aeolian Edge", skill_modifier=SkillModifier(with_condition="Kazematoi")
        )

        # armor crush tests
        rb.add_next("Armor Crush")
        rb.add_next("Aeolian Edge")
        rb.add_next("Aeolian Edge")
        rb.add_next("Aeolian Edge")
        # 4 charges
        rb.add_next("Armor Crush")
        rb.add_next("Armor Crush")
        rb.add_next("Aeolian Edge")
        rb.add_next("Aeolian Edge")
        rb.add_next("Aeolian Edge")
        rb.add_next("Aeolian Edge")
        rb.add_next("Aeolian Edge")
        # doku
        rb.add_next("Aeolian Edge")
        rb.add_next("Dokumori")
        rb.add_next("Wait 3.00s")
        rb.add_next("Aeolian Edge")
        for _ in range(0, 5):
            rb.add_next("Wait 9.00s")
        rb.add_next("Aeolian Edge")
        rb.add_next("Kunai's Bane")
        rb.add_next("Aeolian Edge")
        # meisui
        for _ in range(0, 5):
            rb.add_next("Wait 9.00s")
        rb.add_next("Zesho Meppo")
        rb.add_next("Bhavacakra")
        rb.add_next("Meisui")
        rb.add_next("Zesho Meppo")
        rb.add_next("Bhavacakra")

        expected = (
            ("Aeolian Edge", 10309),
            ("Aeolian Edge", 14290),
            #
            ("Armor Crush", 11118),
            ("Aeolian Edge", 14285),
            ("Aeolian Edge", 14285),
            ("Aeolian Edge", 10305),
            #
            ("Armor Crush", 11097),
            ("Armor Crush", 11097),
            ("Aeolian Edge", 14266),
            ("Aeolian Edge", 14266),
            ("Aeolian Edge", 14266),
            ("Aeolian Edge", 14266),
            ("Aeolian Edge", 10303),
            # doku
            ("Aeolian Edge", 10303),
            ("Dokumori", 11892),
            ("Aeolian Edge", 10812),
            # Kunai
            ("Aeolian Edge", 10319),
            ("Kunai's Bane", 23791),
            ("Aeolian Edge", 11353),
            # meisui
            ("Zesho Meppo", 21788),
            ("Bhavacakra", 15089),
            ("Zesho Meppo", 27753),
            ("Bhavacakra", 15089),
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_nin_rotation_damage_instances(self):
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
            stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True
        )
        rb.add(0, "Kassatsu")
        rb.add(14, "Hyosho Ranryu")
        rb.add(20, "Kassatsu")
        rb.add(36, "Hyosho Ranryu")

        rb.add(100, "Bunshin")
        rb.add(102, "Gust Slash")
        rb.add(104, "Aeolian Edge")
        rb.add(106, "Hakke Mujinsatsu")
        rb.add(108, "Armor Crush")

        expected = (
            ("Hyosho Ranryu", 67006),
            ("Hyosho Ranryu", 51565),
            ("Gust Slash (pet)", 5801),
            ("Gust Slash", 8722),
            ("Aeolian Edge (pet)", 5799),
            ("Aeolian Edge", 10317),
            ("Hakke Mujinsatsu (pet)", 2902),
            ("Hakke Mujinsatsu", 3963),
            ("Armor Crush (pet)", 5802),
            ("Armor Crush", 11091),
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_nin_aggregate_rotation(self):
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
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Huton")
        rb.add_next("Hide")
        rb.add_next("Suiton")
        rb.add_next("Kassatsu")
        rb.add_next("Spinning Edge")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Gust Slash")
        rb.add_next("Dokumori")
        rb.add_next("Bunshin")
        rb.add_next("Phantom Kamaitachi")
        rb.add_next("Kunai's Bane")
        rb.add_next("Aeolian Edge")
        rb.add_next("Dream Within a Dream")
        rb.add_next("Ten")
        rb.add_next("Jin")
        rb.add_next("Hyosho Ranryu")
        rb.add_next("Ten")
        rb.add_next("Chi")
        rb.add_next("Raiton")
        rb.add_next("Ten Chi Jin")
        rb.add_next("Fuma Shuriken")
        rb.add_next("Raiton")
        rb.add_next("Suiton")
        rb.add_next("Meisui")
        rb.add_next("Forked Raiju")
        rb.add_next("Bhavacakra")
        rb.add_next("Forked Raiju")
        rb.add_next("Bhavacakra")
        rb.add_next("Ten")
        rb.add_next("Chi")
        rb.add_next("Raiton")
        rb.add_next("Forked Raiju")
        expected_damage = 625945
        expected_total_time = 27228.0

        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_sam_combos(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.64,
            main_stat=3367,
            det_stat=1736,
            crit_stat=2587,
            dh_stat=1494,
            speed_stat=508,
            job_class="SAM",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Meikyo Shisui")
        rb.add_next("Gekko")
        rb.add_next("Kasha")
        rb.add_next("Yukikaze")
        rb.add_next("Meikyo Shisui")
        rb.add_next("Jinpu")
        rb.add_next("Shifu")
        rb.add_next("Gyofu")
        rb.add_next("Meikyo Shisui")
        rb.add_next("Mangetsu")
        rb.add_next("Oka")
        rb.add_next("Fuko")

        expected_damage = 137348
        expected_total_time = 17940
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_sam_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.64,
            main_stat=3367,
            det_stat=1736,
            crit_stat=2587,
            dh_stat=1494,
            speed_stat=508,
            job_class="SAM",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Meikyo Shisui")
        rb.add_next("True North")
        rb.add_next("Gekko")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Kasha")
        rb.add_next("Yukikaze")
        rb.add_next("Midare Setsugekka")
        rb.add_next("Hissatsu: Senei")
        rb.add_next("Kaeshi: Setsugekka")
        rb.add_next("Meikyo Shisui")
        rb.add_next("Gekko")
        rb.add_next("Hissatsu: Shinten")
        rb.add_next("Higanbana")
        rb.add_next("Hissatsu: Shinten")
        rb.add_next("Ogi Namikiri")
        rb.add_next("Shoha")
        rb.add_next("Kaeshi: Namikiri")
        rb.add_next("Kasha")
        rb.add_next("Hissatsu: Shinten")
        rb.add_next("Gekko")
        rb.add_next("Hissatsu: Gyoten")
        rb.add_next("Gyofu")
        rb.add_next("Hissatsu: Shinten")
        rb.add_next("Yukikaze")
        rb.add_next("Midare Setsugekka")
        rb.add_next("Kaeshi: Setsugekka")

        expected_damage = 666727
        expected_total_time = 32220
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_sam_rotation_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.64,
            main_stat=3367,
            det_stat=1736,
            crit_stat=2587,
            dh_stat=1494,
            speed_stat=508,
            job_class="SAM",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            fight_start_time=0,
        )
        rb.add(-7.045, "Meikyo Shisui")
        rb.add(1.206, "Kasha", skill_modifier=SkillModifier(bonus_percent=59))
        rb.add(5.806, "Gekko")
        rb.add(7.995, "Kasha", skill_modifier=SkillModifier(bonus_percent=59))
        rb.add(100.0, "Enpi")
        rb.add(102.0, "Hissatsu: Yaten")
        rb.add(104.0, "Enpi")
        rb.add(106.0, "Enpi")

        expected = (
            ("Kasha", 17568),
            ("Gekko", 17581),
            ("Kasha", 19859),
            ("Enpi", 3991),
            ("Hissatsu: Yaten", 3991),
            ("Enpi", 10379),
            ("Enpi", 3998),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_rpr_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.2,
            main_stat=3379,
            det_stat=1764,
            crit_stat=2567,
            dh_stat=1558,
            speed_stat=436,
            job_class="RPR",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Harpe")
        rb.add_next("Shadow of Death")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Soul Slice")
        rb.add_next("Arcane Circle")
        rb.add_next("Gluttony")
        rb.add_next("Gibbet")
        rb.add_next("Gallows")
        rb.add_next("Plentiful Harvest")
        rb.add_next("Enshroud")
        rb.add_next("Void Reaping")
        rb.add_next("Cross Reaping")
        rb.add_next("Lemure's Slice")
        rb.add_next("Void Reaping")
        rb.add_next("Cross Reaping")
        rb.add_next("Lemure's Slice")
        rb.add_next("Communio")
        rb.add_next("Soul Slice")
        rb.add_next("Unveiled Gibbet")
        rb.add_next("Gibbet")

        expected_damage = 482862
        expected_total_time = 24800
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_rpr_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.2,
            main_stat=3379,
            det_stat=1764,
            crit_stat=2567,
            dh_stat=1558,
            speed_stat=436,
            job_class="RPR",
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
        rb.add_next("Executioner's Gibbet")
        rb.add_next("Gallows")
        rb.add_next("Executioner's Gibbet")
        rb.add_next("Executioner's Gibbet")
        #
        rb.add_next("Executioner's Gallows")
        rb.add_next("Gibbet")
        rb.add_next("Executioner's Gallows")
        rb.add_next("Executioner's Gallows")
        #
        rb.add_next("Gallows")
        rb.add_next("Gibbet")
        rb.add_next("Executioner's Gibbet")
        expected = (
            ("Executioner's Gibbet", 30760),
            ("Gallows", 25088),
            ("Executioner's Gibbet", 33178),
            ("Executioner's Gibbet", 30727),
            #
            ("Executioner's Gallows", 33178),
            ("Gibbet", 25056),
            ("Executioner's Gallows", 33126),
            ("Executioner's Gallows", 30684),
            #
            ("Gallows", 22613),
            ("Gibbet", 25106),
            ("Executioner's Gibbet", 30721),
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_smn_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1871,
            crit_stat=2514,
            dh_stat=1438,
            speed_stat=502,
            job_class="SMN",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Ruin III")
        rb.add_next("Summon Bahamut")
        rb.add_next("Searing Light")
        rb.add_next("Astral Impulse")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Astral Impulse")
        rb.add_next("Astral Impulse")
        rb.add_next("Energy Drain")
        rb.add_next("Enkindle Bahamut")
        rb.add_next("Astral Impulse")
        rb.add_next("Deathflare")
        rb.add_next("Necrotize")
        rb.add_next("Astral Impulse")
        rb.add_next("Necrotize")
        rb.add_next("Astral Impulse")
        rb.add_next("Summon Garuda II")
        rb.add_next("Swiftcast")
        rb.add_next("Slipstream")
        rb.add_next("Emerald Rite")
        rb.add_next("Emerald Rite")
        rb.add_next("Emerald Rite")
        rb.add_next("Emerald Rite")
        rb.add_next("Summon Titan II")
        rb.add_next("Summon Phoenix")  # idk just because, to test the subsequent autos
        #
        rb.add_next("Summon Solar Bahamut")
        rb.add_next("Umbral Impulse")
        rb.add_next("Umbral Flare")
        rb.add_next("Enkindle Solar Bahamut")

        expected_damage = 690759
        expected_total_time = 47580
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_smn_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1871,
            crit_stat=2514,
            dh_stat=1438,
            speed_stat=502,
            job_class="SMN",
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
        rb.add_next("Ruin III")
        rb.add_next("Aethercharge")
        rb.add_next("Ruin III")
        rb.add_next("Ruin III")

        expected = (
            ("Ruin III", 18849),
            ("Ruin III", 21488),
            ("Ruin III", 18847),
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_rdm_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.44,
            main_stat=3379,
            det_stat=1601,
            crit_stat=2514,
            dh_stat=1708,
            speed_stat=502,
            job_class="RDM",
            healer_or_caster_strength=214,
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        rb.add_next("Verthunder III")
        rb.add_next("Veraero III")
        rb.add_next("Swiftcast")
        rb.add_next("Acceleration")
        rb.add_next("Verthunder III")
        rb.add_next("Grade 8 Tincture")
        rb.add_next("Verthunder III")
        rb.add_next("Embolden")
        rb.add_next("Manafication")
        rb.add_next("Enchanted Riposte")
        rb.add_next("Fleche")
        rb.add_next("Enchanted Zwerchhau")
        rb.add_next("Contre Sixte")
        rb.add_next("Enchanted Redoublement")
        rb.add_next("Corps-a-corps")
        rb.add_next("Engagement")
        rb.add_next("Verholy")
        rb.add_next("Corps-a-corps")
        rb.add_next("Engagement")
        rb.add_next("Scorch")
        rb.add_next("Resolution")
        rb.add_next("Verfire")
        rb.add_next("Verthunder III")
        rb.add_next("Verstone")
        rb.add_next("Veraero III")
        rb.add_next("Jolt II")
        rb.add_next("Verthunder III")
        rb.add_next("Fleche")

        expected_damage = 540413
        expected_total_time = 33710
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_rdm_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.44,
            main_stat=3379,
            det_stat=1601,
            crit_stat=2514,
            dh_stat=1708,
            speed_stat=502,
            job_class="RDM",
            healer_or_caster_strength=214,
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
        rb.add_next("Jolt III")
        rb.add_next("Grand Impact")
        rb.add_next("Manafication")
        rb.add_next("Grand Impact")
        rb.add_next("Jolt III")
        #
        expected = (
            ("Jolt III", 18792),
            ("Grand Impact", 31435),
            ("Grand Impact", 32915),
            ("Jolt III", 19742),
        )
        return self.__job_class_tester.test_rotation_damage(rb, expected)

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

        expected_damage = 456625
        expected_total_time = 26620
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_blm_rotation_damage_instances(self):
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
            fight_start_time=0,
        )

        rb.add_next("Flare Star")
        rb.add_next("Fire III")
        rb.add_next("Flare Star")
        rb.add_next("Fire IV")
        rb.add_next("Flare Star")
        rb.add_next("Fire IV")
        rb.add_next("Transpose")
        rb.add_next("Paradox")
        rb.add_next("Xenoglossy")
        rb.add_next("Transpose")
        rb.add_next("Fire III")
        rb.add_next("Blizzard III")
        rb.add_next("Flare Star")
        rb.add_next("Manafont")
        rb.add_next("Flare Star")

        expected = (
            ("Flare Star", 19289),
            ("Fire III", 13489),
            ("Flare Star", 45094),
            ("Fire IV", 34968),
            ("Flare Star", 45158),
            ("Fire IV", 34996),
            ("Paradox", 31356),
            ("Xenoglossy", 55127),
            ("Fire III", 24544),
            ("Blizzard III", 12258),
            ("Flare Star", 17523),
            ("Flare Star", 45134),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

    @TestClass.is_a_test
    def test_vpr_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.64,
            main_stat=3367,
            det_stat=1736,
            crit_stat=2587,
            dh_stat=1494,
            speed_stat=508,
            job_class="VPR",
            version=self.__version,
            level=self.__level,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        skill_seq = (
            "Dreadwinder",
            "Serpent's Ire",
            "Grade 8 Tincture",
            "Hunter's Coil",
            "Twinfang Bite",
            "Twinblood Bite",
            "Swiftskin's Coil",
            "Twinblood Bite",
            "Twinfang Bite",
            "Reawaken",
            "First Generation",
            "First Legacy",
            "Second Generation",
            "Second Legacy",
            "Third Generation",
            "Third Legacy",
            "Fourth Generation",
            "Fourth Legacy",
            "Ouroboros",
            "Dreadwinder",
            "Swiftskin's Coil",
            "Twinblood Bite",
            "Twinfang Bite",
            "Hunter's Coil",
            "Twinfang Bite",
            "Twinblood Bite",
            "Uncoiled Fury",
            "Uncoiled Twinfang",
            "Uncoiled Twinblood",
        )
        for e in skill_seq:
            rb.add_next(e)

        expected_damage = 583522
        expected_total_time = 29380
        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_vpr_rotation_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=2.64,
            main_stat=3367,
            det_stat=1736,
            crit_stat=2587,
            dh_stat=1494,
            speed_stat=508,
            job_class="VPR",
            version=self.__version,
            level=self.__level,
        )
        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )

        rot_and_expected = (
            ("Hindsting Strike", 14272),
            ("Flanksbane Fang", 18265),
            ("Hindsbane Fang", 18265),
            ("Flanksting Strike", 18289),
            ("Flanksting Strike", 14291),
            ("Hindsting Strike", 18289),
            ("Hindsting Strike", 14291),
            #
            ("Flanksbane Fang", 18265),
            ("Hindsbane Fang", 18265),
        )
        for e in rot_and_expected:
            rb.add_next(e[0])

        return self.__job_class_tester.test_rotation_damage(rb, rot_and_expected)

    @TestClass.is_a_test
    def test_pct_rotation_damage_instances(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1871,
            crit_stat=2514,
            dh_stat=1438,
            speed_stat=502,
            job_class="PCT",
            version=self.__version,
            level=self.__level,
        )
        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )

        # TODO: fill these out. For now, just do the e2e. I am tired.
        rot_and_expected = (
            ("Fire in Red", 23012),
            ("Rainbow Drip", 52434),
        )
        for e in rot_and_expected:
            rb.add_next(e[0])

        return self.__job_class_tester.test_rotation_damage(rb, rot_and_expected)

    @TestClass.is_a_test
    def test_pct_aggregate_rotation(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.12,
            main_stat=3379,
            det_stat=1871,
            crit_stat=2514,
            dh_stat=1438,
            speed_stat=502,
            job_class="PCT",
            version=self.__version,
            level=self.__level,
        )
        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )

        skill_seq = (
            ("Rainbow Drip"),
            ("Grade 8 Tincture"),
            ("Holy in White"),
            ("Pom Muse"),
            ("Swiftcast"),
            ("Wing Motif"),
            ("Striking Muse"),
            ("Fire in Red"),
            ("Starry Muse"),
            ("Star Prism"),
            ("Hammer Stamp"),
            ("Winged Muse"),
            ("Hammer Brush"),
            ("Mog of the Ages"),
            ("Polishing Hammer"),
            ("Subtractive Palette"),
            ("Stone in Yellow"),
            ("Thunder in Magenta"),
            ("Comet in Black"),
            ("Claw Motif"),
            ("Clawed Muse"),
            ("Holy in White"),
            ("Rainbow Drip"),
            ("Blizzard in Cyan"),
            ("Aero in Green"),
            ("Water in Blue"),
            ("Fire in Red"),
            ("Maw Motif"),
            ("Aero in Green"),
            ("Fanged Muse"),
            ("Water in Blue"),
        )

        for e in skill_seq:
            rb.add_next(e)

        expected_damage = 1113818
        expected_total_time = 54450

        return self.__job_class_tester.test_aggregate_rotation(
            rb, expected_damage, expected_total_time
        )

    @TestClass.is_a_test
    def test_nin_dokumori_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "Dokumori", job_class="NIN")
        rb1.add(5, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5953),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        stats2 = Stats(
            wd=132,
            weapon_delay=2.56,
            main_stat=3360,
            dh_stat=1582,
            crit_stat=2554,
            # det_stat=1679,
            det_stat=1679,
            speed_stat=400,
            job_class="NIN",
            version=self.__version,
            level=self.__level,
        )

        rb2 = RotationBuilder(
            stats2,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb2.add(0.0, "Spinning Edge")
        rb2.add(1, "Dokumori", job_class="NIN")
        rb2.add(5, "Spinning Edge")

        expected = (
            ("Spinning Edge", 11885),
            ("Dokumori", 11885),
            ("Spinning Edge", 12479),
        )
        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb2, expected
        )

        return test_passed1 and test_passed2, ", ".join([err_msg1, err_msg2])

    @TestClass.is_a_test
    def test_pct_starry_muse_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "Starry Muse", job_class="PCT")
        rb1.add(5, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5953),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        return test_passed1, err_msg1

    @TestClass.is_a_test
    def test_brd_mages_ballad_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "Mage's Ballad", job_class="BRD")
        rb1.add(5, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5726),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        stats2 = Stats(
            wd=132,
            weapon_delay=3.04,
            main_stat=3379,
            det_stat=1885,
            crit_stat=2598,
            dh_stat=1344,
            speed_stat=479,
            job_class="BRD",
            version=self.__version,
            level=self.__level,
        )

        rb2 = RotationBuilder(
            stats2,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb2.add(0.0, "Burst Shot")
        rb2.add(1, "Mage's Ballad")
        rb2.add(5, "Burst Shot")

        expected = (
            ("Burst Shot", 10635),
            ("Burst Shot", 10741),
        )
        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb2, expected
        )

        return test_passed1 and test_passed2, ", ".join([err_msg1, err_msg2])

    @TestClass.is_a_test
    def test_brd_wanderers_minuet_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "The Wanderer's Minuet", job_class="BRD")
        rb1.add(5, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5726),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        stats2 = Stats(
            wd=132,
            weapon_delay=3.04,
            main_stat=3379,
            det_stat=1885,
            crit_stat=2598,
            dh_stat=1344,
            speed_stat=479,
            job_class="BRD",
            version=self.__version,
            level=self.__level,
        )

        rb2 = RotationBuilder(
            stats2,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb2.add(0.0, "Burst Shot")
        rb2.add(1, "The Wanderer's Minuet")
        rb2.add(5, "Burst Shot")

        expected = (
            ("Burst Shot", 10635),
            ("Burst Shot", 10741),
        )
        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb2, expected
        )

        return test_passed1 and test_passed2, ", ".join([err_msg1, err_msg2])

    @TestClass.is_a_test
    def test_brd_armys_paeon_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "Army's Paeon", job_class="BRD")
        rb1.add(5, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5726),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        stats2 = Stats(
            wd=132,
            weapon_delay=3.04,
            main_stat=3379,
            det_stat=1885,
            crit_stat=2598,
            dh_stat=1344,
            speed_stat=479,
            job_class="BRD",
            version=self.__version,
            level=self.__level,
        )

        rb2 = RotationBuilder(
            stats2,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb2.add(0.0, "Burst Shot")
        rb2.add(1, "Army's Paeon")
        rb2.add(5, "Burst Shot")

        expected = (
            ("Burst Shot", 10635),
            ("Burst Shot", 10741),
        )
        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb2, expected
        )

        return test_passed1 and test_passed2, ", ".join([err_msg1, err_msg2])

    @TestClass.is_a_test
    def test_brd_radiant_finale_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(
            1,
            "Radiant Finale",
            job_class="BRD",
            skill_modifier=SkillModifier(with_condition="2 Coda"),
        )
        rb1.add(5, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5897),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        return test_passed1, err_msg1

    @TestClass.is_a_test
    def test_dnc_tech_finish_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "Quadruple Technical Finish", job_class="DNC")
        rb1.add(5, "Heavy Swing")
        rb1.add(100, "Double Technical Finish", job_class="DNC")
        rb1.add(105, "Heavy Swing")
        rb1.add(201, "Technical Finish", job_class="DNC")
        rb1.add(205, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5953),
            ("Heavy Swing", 5783),
            ("Heavy Swing", 5953),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        return test_passed1, err_msg1

    @TestClass.is_a_test
    def test_dnc_standard_finish_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "Double Standard Finish", job_class="DNC")
        rb1.add(5, "Heavy Swing")
        rb1.add(100, "Single Technical Finish", job_class="DNC")
        rb1.add(105, "Heavy Swing")
        rb1.add(200, "Standard Finish", job_class="DNC")
        rb1.add(205, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 5953),
            ("Heavy Swing", 5726),
            ("Heavy Swing", 5953),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        return test_passed1, err_msg1

    @TestClass.is_a_test
    def test_ast_off_class_default_condition(self):
        stats1 = Stats(
            wd=126,
            weapon_delay=3.36,
            main_stat=2910,
            det_stat=1980,
            crit_stat=2313,
            dh_stat=868,
            speed_stat=592,
            tenacity=631,
            job_class="WAR",
            version=self.__version,
            level=self.__level,
        )

        rb1 = RotationBuilder(
            stats1,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )
        rb1.add(0.0, "Heavy Swing")
        rb1.add(1, "The Spear", job_class="AST")
        rb1.add(5, "Heavy Swing")
        rb1.add(
            100,
            "The Spear",
            job_class="AST",
            skill_modifier=SkillModifier(with_condition="Small"),
        )
        rb1.add(105, "Heavy Swing")
        rb1.add(200, "Card", job_class="AST")
        rb1.add(205, "Heavy Swing")

        expected = (
            ("Heavy Swing", 5670),
            ("Heavy Swing", 6010),
            ("Heavy Swing", 5840),
            ("Heavy Swing", 6010),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_rotation_damage(
            rb1, expected
        )

        return test_passed1, err_msg1
