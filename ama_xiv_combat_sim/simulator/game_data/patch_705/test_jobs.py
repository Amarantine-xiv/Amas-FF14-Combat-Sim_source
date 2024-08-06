import numpy as np

from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.skills.create_skill_library import (
    create_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)

GAME_VERSION = "7.05"


class TestJobs705(TestClass):
    def __init__(self):
        super().__init__()
        self.__skill_library = create_skill_library(GAME_VERSION)
        self.__relative_tol = 6e-3

    def __test_skills(self, stats, skills_and_expected_damage):
        test_passed = True
        err_msg = ""

        for sk, skill_modifier, expected_damage in skills_and_expected_damage:
            rb = RotationBuilder(stats, self.__skill_library)
            rb.add_next(sk, skill_modifier=skill_modifier)

            db = DamageBuilder(stats, self.__skill_library)
            sim = DamageSimulator(
                rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
            )
            actual_damage = np.mean(sim.get_raw_damage())
            diff = abs(float(expected_damage - actual_damage))
            if diff / expected_damage >= self.__relative_tol:
                test_passed = False
                err_msg += "Did not get expected damage for {} / {}. Expected: {} . Actual: {} .\n".format(
                    sk, skill_modifier, expected_damage, int(round(actual_damage, 0))
                )
        return test_passed, err_msg

    def __test_rotation_damage(self, rb, expected_damage_instances):
        test_passed = True
        err_msg = ""

        db = DamageBuilder(rb.get_stats(), self.__skill_library)
        sim = DamageSimulator(
            rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
        )
        result = [(x.skill_name, x.expected_damage) for x in sim.get_per_skill_damage()]

        if len(result) != len(expected_damage_instances):
            test_passed = False
            err_msg += "Expected {} skills returned. Instead got {}.\n".format(
                len(expected_damage_instances), len(result)
            )
            return test_passed, err_msg
        for i in range(0, len(result)):
            result_skill_name, expected_skill_name = (
                result[i][0],
                expected_damage_instances[i][0],
            )
            if result_skill_name != expected_skill_name:
                test_passed = False
                err_msg += "Name did not match. Expected: {}. Actual: {}\n".format(
                    expected_skill_name, result_skill_name
                )

            result_damage, expected_damage = (
                result[i][1],
                expected_damage_instances[i][1],
            )
            diff = abs(result_damage - expected_damage)
            if diff / max(1e-6, expected_damage) >= 0.005:
                test_passed = False
                err_msg += "Did not get expected damage for damage instance {}. Expected: {}. Actual: {} .\n".format(
                    result_skill_name, expected_damage, int(round(result_damage, 0))
                )
        return test_passed, err_msg

    def __test_aggregate_rotation(self, rb, expected_damage, expected_total_time):
        test_passed = True
        err_msg = ""

        db = DamageBuilder(rb.get_stats(), self.__skill_library)
        sim = DamageSimulator(
            rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
        )
        actual_damage = np.mean(sim.get_raw_damage())
        damage_diff = abs(float(expected_damage - actual_damage))
        if damage_diff / expected_damage >= self.__relative_tol:
            test_passed = False
            err_msg += "Did not get expected damage for rotation. Expected: {} . Actual: {} .\n".format(
                expected_damage, int(round(actual_damage, 0))
            )

        actual_total_time = max(sim.get_damage_time()) - min(sim.get_damage_time())
        if abs(expected_total_time - actual_total_time) > 1e-3:
            test_passed = False
            err_msg += "Did not get expected total time for rotation. Expected: {} . Actual: {} .\n".format(
                expected_total_time, int(round(actual_total_time, 0))
            )

        return test_passed, err_msg

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
            version=GAME_VERSION,
        )
        skills_and_expected_damage = (
            ("Glare III", SkillModifier(), 16632),
            ("Glare IV", SkillModifier(), 32312),
            ("Assize", SkillModifier(), 20172),
            ("Dia", SkillModifier(), 42644),
            ("Afflatus Misery", SkillModifier(), 66760),
            ("Holy III", SkillModifier(), 7573),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
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
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
        )
        skills_and_expected_damage = (
            ("Broil IV", SkillModifier(), 15103),
            ("Ruin II", SkillModifier(), 10716),
            ("Energy Drain", SkillModifier(), 4875),
            ("Art of War II", SkillModifier(), 8762),
            ("Biolysis", SkillModifier(), 37475),
            ("Baneful Impaction", SkillModifier(), 34940),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version="6.55",
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
        expected_damage = 292932.5
        expected_total_time = 31200.0
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
        )
        skills_and_expected_damage = (
            ("Fall Malefic", SkillModifier(), 13453),
            ("Combust III", SkillModifier(), 36297),
            ("Earthly Star", SkillModifier(), 14814),
            ("Gravity II", SkillModifier(), 6476),
            ("Macrocosmos", SkillModifier(), 13453),
            ("Oracle", SkillModifier(), 42942),
            ("Lord of Crowns", SkillModifier(), 19957),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
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
            version="6.55",
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Earthly Star", skill_modifier=SkillModifier())

        rb.add(100, "Earthly Star", skill_modifier=SkillModifier())
        rb.add(108, "Stellar Detonation", skill_modifier=SkillModifier())

        rb.add(200, "Earthly Star", skill_modifier=SkillModifier())
        rb.add(215, "Stellar Detonation", skill_modifier=SkillModifier())

        expected = (
            ("Stellar Explosion (pet)", 14899.6),
            ("Stellar Explosion (pet)", 9840.6),
            ("Stellar Explosion (pet)", 14899.6),
        )

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
            ("Primal Ruination", SkillModifier(), 35067),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
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

        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
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
            ("Royal Authority", SkillModifier(force_combo=True), 11727),
            ("Royal Authority", SkillModifier(), 5100),
            ("Holy Spirit", SkillModifier(), 10194),
            ("Holy Spirit", SkillModifier(with_condition="Divine Might"), 12732),
            ("Holy Spirit", SkillModifier(with_condition="Requiescat"), 17837),
            (
                "Holy Spirit",
                SkillModifier(with_condition="Divine Might, Requiescat"),
                12752,
            ),
            ("Requiescat", SkillModifier(), 8167),
            ("Holy Circle", SkillModifier(), 2548),
            ("Holy Circle", SkillModifier(with_condition="Divine Might"), 5100),
            ("Holy Circle", SkillModifier(with_condition="Requiescat"), 7651),
            (
                "Holy Circle",
                SkillModifier(with_condition="Divine Might, Requiescat"),
                5099,
            ),
            ("Intervene", SkillModifier(), 3824),
            ("Atonement", SkillModifier(), 11725),
            ("Sepulchre", SkillModifier(), 13800),
            ("Supplication", SkillModifier(), 12750),
            ("Confiteor", SkillModifier(), 12754),
            ("Confiteor", SkillModifier(with_condition="Requiescat"), 25485),
            ("Expiacion", SkillModifier(), 11470),
            ("Blade of Faith", SkillModifier(), 6638),
            ("Blade of Faith", SkillModifier(with_condition="Requiescat"), 19395),
            ("Blade of Truth", SkillModifier(), 9681),
            ("Blade of Truth", SkillModifier(with_condition="Requiescat"), 22452),
            ("Blade of Valor", SkillModifier(), 12755),
            ("Blade of Valor", SkillModifier(with_condition="Requiescat"), 25512),
            ("Blade of Honor", SkillModifier(), 25532),
            ("Imperator", SkillModifier(), 14798),
        )

        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
        )

        rb = RotationBuilder(
            stats, self.__skill_library, enable_autos=False, ignore_trailing_dots=True
        )
        rb.add_next("Requiescat")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        rb.add_next("Imperator")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        rb.add_next("Confiteor")
        # last one should be weaker, since we should only have 4 charges from early imperator
        rb.add_next("Confiteor")

        confiteor_damage_big = 25528
        confiteor_damage_small = 12748
        expected = (
            ("Requiescat", 8157),
            ("Confiteor", confiteor_damage_big),
            ("Confiteor", confiteor_damage_big),
            ("Imperator", 14802),
            ("Confiteor", confiteor_damage_big),
            ("Confiteor", confiteor_damage_big),
            ("Confiteor", confiteor_damage_big),
            ("Confiteor", confiteor_damage_big),
            ("Confiteor", confiteor_damage_small),
        )

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 2289),
            ("Hard Slash", SkillModifier(), 7693),
            ("Syphon Strike", SkillModifier(force_combo=True), 9751),
            ("Syphon Strike", SkillModifier(), 6158),
            ("Unleash", SkillModifier(), 3081),
            ("Unmend", SkillModifier(), 3842),
            ("Souleater", SkillModifier(force_combo=True), 12296),
            ("Souleater", SkillModifier(), 6666),
            ("Flood of Shadow", SkillModifier(), 4106),
            ("Stalwart Soul", SkillModifier(force_combo=True), 4102),
            ("Stalwart Soul", SkillModifier(), 3076),
            ("Edge of Shadow", SkillModifier(), 11797),
            ("Salted Earth", SkillModifier(), 6456),
            ("Salt and Darkness", SkillModifier(), 12836),
            ("Abyssal Drain", SkillModifier(), 6158),
            ("Carve and Spit", SkillModifier(), 13848),
            ("Bloodspiller", SkillModifier(), 14913),
            ("Quietus", SkillModifier(), 6149),
            ("Shadowbringer", SkillModifier(), 15394),
            ("Living Shadow", SkillModifier(), 71725),
            ("Scarlet Delirium", SkillModifier(), 15393),
            ("Comeuppance", SkillModifier(), 17973),
            ("Torcleaver", SkillModifier(), 20548),
            ("Impalement", SkillModifier(), 8202),
            ("Disesteem", SkillModifier(), 25679),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

    @TestClass.is_a_test
    def test_drk_aggregate_rotation(self):
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
            version="6.55",
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
        expected_damage = 411509
        expected_total_time = 26993.0

        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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
        test_passed1, err_msg1 = self.__test_rotation_damage(rb, expected)

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
        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
        expected_damage = 534419
        expected_total_time = 27410
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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
            ("Fan Dance IV", SkillModifier(), 20385),
            ("Starfall Dance", SkillModifier(), 50684),
            ("Last Dance", SkillModifier(), 25233),
            ("Dance of the Dawn", SkillModifier(), 48512),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
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

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
            ("Full Metal Field", SkillModifier(), 76076),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
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
        rb.add_next("Radiant Finale", SkillModifier(with_condition="2 Coda, Buff Only"))
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

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 3036),
            ("Bootshine", SkillModifier(), 8617),
            ("Bootshine", SkillModifier("Opo-opo's Fury"), 16423),
            ("Bootshine", SkillModifier(with_condition="Opo-opo Form"), 12013),
            ("Snap Punch", SkillModifier(), 12900),
            ("Snap Punch", SkillModifier("Coeurl's Fury"), 18771),
            ("Twin Snakes", SkillModifier(), 16409),
            ("Demolish", SkillModifier(), 16424),
            ("Rockbreaker", SkillModifier(), 5869),
            ("Four-point Fury", SkillModifier(), 5478),
            ("Dragon Kick", SkillModifier(), 12494),
            ("The Forbidden Chakra", SkillModifier(), 15634),
            ("Elixir Field", SkillModifier(), 31322),
            ("Celestial Revolution", SkillModifier(), 23489),
            ("Enlightenment", SkillModifier(), 7828),
            ("Six-sided Star", SkillModifier(with_condition="5 Chakra"), 46075),
            ("Six-sided Star", SkillModifier(with_condition="0 Chakra"), 30495),
            ("Leaping Opo", SkillModifier(), 10157),
            ("Leaping Opo", SkillModifier(with_condition="Opo-opo's Fury"), 17986),
            ("Rising Raptor", SkillModifier(), 13308),
            ("Rising Raptor", SkillModifier(with_condition="Raptor's Fury"), 21099),
            ("Pouncing Coeurl", SkillModifier(), 14463),
            ("Pouncing Coeurl", SkillModifier(with_condition="Coeurl's Fury"), 20343),
            ("Wind's Reply", SkillModifier(), 35226),
            ("Fire's Reply", SkillModifier(), 46931),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            version=GAME_VERSION,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        # test opo-opo automatic bonus
        rb.add_next("Bootshine")
        rb.add_next("Snap Punch")
        rb.add_next("Bootshine")
        #
        rb.add_next("Wait 5.00s")
        rb.add_next("Rising Raptor")
        rb.add_next("Twin Snakes")
        rb.add_next("Rising Raptor")
        rb.add_next("Rising Raptor")
        #
        rb.add_next("Wait 5.00s")
        rb.add_next("Pouncing Coeurl")
        rb.add_next("Demolish")
        rb.add_next("Pouncing Coeurl")
        rb.add_next("Pouncing Coeurl")
        rb.add_next("Pouncing Coeurl")

        # test formless fist pattern
        for _ in range(0, 5):
            rb.add_next("Wait 5.00s")
        rb.add_next("Bootshine")
        rb.add_next("Elixir Burst")
        rb.add_next("Bootshine")

        # formless on dragon kick
        for _ in range(0, 10):
            rb.add_next("Wait 5.00s")
        rb.add_next("Leaping Opo")
        rb.add_next("Dragon Kick")
        rb.add_next("Leaping Opo")
        rb.add_next("Formless Fist")
        rb.add_next("Dragon Kick")
        rb.add_next("Leaping Opo")

        expected = (
            ("Bootshine", 8599),
            ("Snap Punch", 12910),
            ("Bootshine", 12009),
            #
            ("Rising Raptor", 13280),
            ("Twin Snakes", 16417),
            ("Rising Raptor", 21134),
            ("Rising Raptor", 13293),
            #
            ("Pouncing Coeurl", 14484),
            ("Demolish", 16433),
            ("Pouncing Coeurl", 20334),
            ("Pouncing Coeurl", 20334),
            ("Pouncing Coeurl", 14472),
            #
            ("Bootshine", 12007),
            ("Elixir Burst", 35218),
            ("Bootshine", 12003),
            #
            ("Leaping Opo", 10180),
            ("Dragon Kick", 12525),
            ("Leaping Opo", 10162),
            ("Dragon Kick", 12525),
            ("Leaping Opo", 18014),
        )

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
            ("Gust Slash", 15838),
            ("Armor Crush", 18986),
            ("Bhavacakra", 15062),
            ("Hyosho Ranryu", 66992),
        )

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
            ("Zesho Meppo", 27744),
            ("Bhavacakra", 15089),
            ("Zesho Meppo", 33713),
            ("Bhavacakra", 15089),
        )
        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
            ("Gust Slash", 9526),
            ("Aeolian Edge (pet)", 5799),
            ("Aeolian Edge", 10317),
            ("Hakke Mujinsatsu (pet)", 2902),
            ("Hakke Mujinsatsu", 3963),
            ("Armor Crush (pet)", 5802),
            ("Armor Crush", 11091),
        )

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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
        expected_damage = 635900
        expected_total_time = 27228.0

        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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

        expected_damage = 132529
        expected_total_time = 17940
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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

        expected_damage = 640625
        expected_total_time = 32220
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=False,
            ignore_trailing_dots=True,
            fight_start_time=0,
        )
        rb.add(-7.045, "Meikyo Shisui")
        rb.add(1.206, "Kasha", skill_modifier=SkillModifier(bonus_percent=61))
        rb.add(5.806, "Gekko")
        rb.add(7.995, "Kasha", skill_modifier=SkillModifier(bonus_percent=61))
        rb.add(100.0, "Enpi")
        rb.add(102.0, "Hissatsu: Yaten")
        rb.add(104.0, "Enpi")
        rb.add(106.0, "Enpi")

        expected = (
            ("Kasha", 16772),
            ("Gekko", 16774),
            ("Kasha", 18973),
            ("Enpi", 3991),
            ("Hissatsu: Yaten", 3991),
            ("Enpi", 10379),
            ("Enpi", 3998),
        )

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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

        expected_damage = 489597
        expected_total_time = 24300
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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
        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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

        expected_damage = 703667
        expected_total_time = 47080
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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
        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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

        expected_damage = 549027
        expected_total_time = 33710
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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
        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
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

        expected_damage = 475338
        expected_total_time = 26620
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
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
            ("Flare Star", 46164),
            ("Fire IV", 36921),
            ("Flare Star", 46247),
            ("Fire IV", 36903),
            ("Paradox", 33338),
            ("Xenoglossy", 56409),
            ("Fire III", 25093),
            ("Blizzard III", 12560),
            ("Flare Star", 17967),
            ("Flare Star", 46187),
        )

        return self.__test_rotation_damage(rb, expected)

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
            version=GAME_VERSION,
        )

        rb = RotationBuilder(
            stats,
            self.__skill_library,
            enable_autos=True,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
        )
        skill_seq = (
            "Vicewinder",
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
            "Vicewinder",
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

        expected_damage = 591148
        expected_total_time = 29380
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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
            version=GAME_VERSION,
        )
        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )

        rot_and_expected = (
            ("Hindsting Strike", 15878),
            ("Flanksbane Fang", 19870),
            ("Hindsbane Fang", 19870),
            ("Flanksting Strike", 19831),
            ("Flanksting Strike", 15889),
            ("Hindsting Strike", 19840),
            ("Hindsting Strike", 15898),
            #
            ("Flanksbane Fang", 19878),
            ("Hindsbane Fang", 19878),
        )
        for e in rot_and_expected:
            rb.add_next(e[0])

        return self.__test_rotation_damage(rb, rot_and_expected)

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
            version=GAME_VERSION,
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

        return self.__test_rotation_damage(rb, rot_and_expected)

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
            version=GAME_VERSION,
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

        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)
