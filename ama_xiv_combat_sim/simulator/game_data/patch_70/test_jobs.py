import numpy as np

from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.skills.create_skill_library import create_skill_library
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


class TestJobs(TestClass):
    def __init__(self):
        super().__init__()
        self.__skill_library = create_skill_library("7.0")
        self.__relative_tol = 5e-3

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
                    sk, skill_modifier, expected_damage, round(actual_damage, 1)
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
                    result_skill_name, expected_damage, round(result_damage, 1)
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
                expected_damage, round(actual_damage, 1)
            )

        actual_total_time = max(sim.get_damage_time()) - min(sim.get_damage_time())
        if abs(expected_total_time - actual_total_time) > 1e-3:
            test_passed = False
            err_msg += "Did not get expected total time for rotation. Expected: {} . Actual: {} .\n".format(
                expected_total_time, round(actual_total_time, 1)
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 37.2),
            ("Glare III", SkillModifier(), 16774.59),
            ("Glare IV", SkillModifier(), 32588.4),
            ("Assize", SkillModifier(), 20363.5),
            ("Dia", SkillModifier(), 40727.1),
            ("Afflatus Misery", SkillModifier(), 67102.7),
            ("Holy III", SkillModifier(), 7641.9),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 30.9),
            ("Dosis III", SkillModifier(), 18823.3),
            ("Phlegma III", SkillModifier(), 31436.4),
            ("Toxikon II", SkillModifier(), 18829.7),
            ("Dyskrasia II", SkillModifier(), 8901.3),
            ("Pneuma", SkillModifier(), 18835.1),
            ("Eukrasian Dosis III", SkillModifier(), 39979.0),
            ("Eukrasian Dyskrasia", SkillModifier(), 21179.5),
            ("Psyche", SkillModifier(), 31368.2),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 185.2),
            ("Broil IV", SkillModifier(), 15190.6),
            ("Ruin II", SkillModifier(), 10779.9),
            ("Energy Drain", SkillModifier(), 4901.8),
            ("Art of War II", SkillModifier(), 8821.7),
            ("Biolysis", SkillModifier(), 37945.5),
            ("Baneful Impaction", SkillModifier(), 35576.5),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 33.0),
            ("Fall Malefic", SkillModifier(), 13456.7),
            ("Combust III", SkillModifier(), 37091.7),
            ("Earthly Star", SkillModifier(), 14885.5),
            ("Gravity II", SkillModifier(), 6443.0),
            ("Macrocosmos", SkillModifier(), 12470.8),
            ("Oracle", SkillModifier(), 42848.3),
            ("Lord of Crowns", SkillModifier(), 19933.8),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 2641.6),
            ("Heavy Swing", SkillModifier(), 5716.0),
            ("Maim", SkillModifier(force_combo=True), 8833.2),
            ("Maim", SkillModifier(), 4945.0),
            ("Storm's Path", SkillModifier(force_combo=True), 12490.1),
            ("Storm's Path", SkillModifier(), 5201.3),
            ("Storm's Eye", SkillModifier(force_combo=True), 12494.9),
            ("Storm's Eye", SkillModifier(), 5204.7),
            ("Upheaval", SkillModifier(), 10418.6),
            ("Onslaught", SkillModifier(), 3900.5),
            ("Fell Cleave", SkillModifier(), 15100.2),
            ("Primal Rend", SkillModifier(), 31574.8),
            ("Inner Chaos", SkillModifier(), 29773.5),
            ("Tomahawk", SkillModifier(), 3898.4),
            ("Overpower", SkillModifier(), 2859.7),
            ("Mythril Tempest", SkillModifier(force_combo=True), 3639.6),
            ("Mythril Tempest", SkillModifier(), 2602.5),
            ("Orogeny", SkillModifier(), 3903.3),
            ("Decimate", SkillModifier(), 4677.1),
            ("Damnation", SkillModifier(with_condition="Retaliation"), 1424.1),
            ("Primal Wrath", SkillModifier(), 18221.4),
            ("Primal Ruination", SkillModifier(), 33374.8),
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
            version="7.0",
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
        expected_total_time = 32385.0

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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 2170.4),
            ("Keen Edge", SkillModifier(), 7789.2),
            ("Brutal Shell", SkillModifier(force_combo=True), 9897.2),
            ("Brutal Shell", SkillModifier(), 6235.2),
            ("Demon Slice", SkillModifier(), 2594.8),
            ("Lightning Shot", SkillModifier(), 3892.1),
            ("Solid Barrel", SkillModifier(force_combo=True), 11962.1),
            ("Solid Barrel", SkillModifier(), 6244.5),
            ("Burst Strike", SkillModifier(), 11967.1),
            ("Demon Slaughter", SkillModifier(force_combo=True), 4162.4),
            ("Demon Slaughter", SkillModifier(), 2601.2),
            ("Sonic Break", SkillModifier(), 23398.8),
            ("Gnashing Fang", SkillModifier(), 13024.5),
            ("Savage Claw", SkillModifier(force_combo=True), 14574.3),
            ("Wicked Talon", SkillModifier(force_combo=True), 16104.3),
            ("Bow Shock", SkillModifier(), 11704.9),
            ("Jugular Rip", SkillModifier(), 6243.4),
            ("Abdomen Tear", SkillModifier(), 7278.1),
            ("Eye Gouge", SkillModifier(), 8322.0),
            ("Fated Circle", SkillModifier(), 7822.5),
            ("Blasting Zone", SkillModifier(), 20798.5),
            ("Double Down", SkillModifier(), 31283.2),
            ("Hypervelocity", SkillModifier(), 5716.1),
            ("Fated Brand", SkillModifier(), 3117.4),
            ("Reign of Beasts", SkillModifier(), 20827.0),
            ("Lion Heart", SkillModifier(), 31160.3),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 1741.2),
            ("Fast Blade", SkillModifier(), 5726.3),
            ("Riot Blade", SkillModifier(force_combo=True), 8570.2),
            ("Riot Blade", SkillModifier(), 4418.5),
            ("Total Eclipse", SkillModifier(), 2603.2),
            ("Shield Bash", SkillModifier(), 2592.1),
            ("Shield Lob", SkillModifier(), 2602.2),
            ("Prominence", SkillModifier(force_combo=True), 4417.4),
            ("Prominence", SkillModifier(), 2595.6),
            ("Circle of Scorn", SkillModifier(), 7530.2),
            ("Goring Blade", SkillModifier(), 18251.9),
            ("Royal Authority", SkillModifier(force_combo=True), 11446.0),
            ("Royal Authority", SkillModifier(), 4680.2),
            ("Holy Spirit", SkillModifier(), 9616.7),
            ("Holy Spirit", SkillModifier(with_condition="Divine Might"), 12241.2),
            ("Holy Spirit", SkillModifier(with_condition="Requiescat"), 17416.6),
            (
                "Holy Spirit",
                SkillModifier(with_condition="Divine Might, Requiescat"),
                12217.0,
            ),
            ("Requiescat", SkillModifier(), 8321.4),
            ("Holy Circle", SkillModifier(), 2592.8),
            ("Holy Circle", SkillModifier(with_condition="Divine Might"), 5203.8),
            ("Holy Circle", SkillModifier(with_condition="Requiescat"), 7815.4),
            (
                "Holy Circle",
                SkillModifier(with_condition="Divine Might, Requiescat"),
                5202.7,
            ),
            ("Intervene", SkillModifier(), 3900.0),
            ("Atonement", SkillModifier(), 11453.9),
            ("Sepulchre", SkillModifier(), 12457.3),
            ("Supplication", SkillModifier(), 11964.4),
            ("Confiteor", SkillModifier(), 11453.0),
            ("Confiteor", SkillModifier(with_condition="Requiescat"), 24421.0),
            ("Expiacion", SkillModifier(), 11718.3),
            ("Blade of Faith", SkillModifier(), 6235.1),
            ("Blade of Faith", SkillModifier(with_condition="Requiescat"), 19259.1),
            ("Blade of Truth", SkillModifier(), 8829.0),
            ("Blade of Truth", SkillModifier(with_condition="Requiescat"), 21896.4),
            ("Blade of Valor", SkillModifier(), 11439.3),
            ("Blade of Valor", SkillModifier(with_condition="Requiescat"), 24417.9),
            ("Blade of Honor", SkillModifier(), 26022.5),
            ("Imperator", SkillModifier(), 15078.2),
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
            version="7.0",
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

        expected = (
            ("Requiescat", 8321.4),
            ("Confiteor", 24421.4),
            ("Confiteor", 24421.4),
            ("Imperator", 15078.2),
            ("Confiteor", 24421.4),
            ("Confiteor", 24421.0),
            ("Confiteor", 24421.4),
            ("Confiteor", 24421.4),
            ("Confiteor", 11453.0),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 2322.9),
            ("Hard Slash", SkillModifier(), 6736.0),
            ("Syphon Strike", SkillModifier(force_combo=True), 9323.0),
            ("Syphon Strike", SkillModifier(), 5701.8),
            ("Unleash", SkillModifier(), 3105.4),
            ("Unmend", SkillModifier(), 3885.94),
            ("Souleater", SkillModifier(force_combo=True), 11904.7),
            ("Souleater", SkillModifier(), 6210.8),
            ("Flood of Shadow", SkillModifier(), 4140.5),
            ("Stalwart Soul", SkillModifier(force_combo=True), 4142.5),
            ("Stalwart Soul", SkillModifier(), 3102.1),
            ("Edge of Shadow", SkillModifier(), 11924.0),
            ("Salted Earth", SkillModifier(), 6576.1),
            ("Salt and Darkness", SkillModifier(), 12960.2),
            ("Abyssal Drain", SkillModifier(), 6220.1),
            ("Carve and Spit", SkillModifier(), 13208.8),
            ("Bloodspiller", SkillModifier(), 14994.5),
            ("Quietus", SkillModifier(), 6223.6),
            ("Shadowbringer", SkillModifier(), 15534.5),
            ("Living Shadow", SkillModifier(), 85506.7),
            ("Scarlet Delirium", SkillModifier(), 15531.8),
            ("Comeuppance", SkillModifier(), 18128.8),
            ("Torcleaver", SkillModifier(), 20740.6),
            ("Impalement", SkillModifier(), 8285.2),
            ("Disesteem", SkillModifier(), 20705.0),
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
        expected_damage = 417250.7
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
            version="7.0",
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
            ("Cascade", 10928.0),
            ("Quadruple Technical Finish", 64527.1),
            ("Cascade", 11470.0),
            ("Cascade", 10928.1),
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
            ("Cascade", 10932.2),
            ("Double Standard Finish", 42119.5),
            ("Cascade", 11459.8),
            ("Cascade", 10912.8),
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
            version="7.0",
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
        expected_damage = 543925.2
        expected_total_time = 27360.0
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 3874.0),
            ("Cascade", SkillModifier(), 10926.3),
            ("Fountain", SkillModifier(), 5961.0),
            ("Fountain", SkillModifier(force_combo=True), 13915.5),
            ("Windmill", SkillModifier(), 4960.8),
            ("Double Standard Finish", SkillModifier(), 42185.6),
            ("Single Standard Finish", SkillModifier(), 26814.9),
            ("Standard Finish", SkillModifier(), 42153.2),
            ("Standard Finish", SkillModifier(with_condition="Log"), 17881.2),
            ("Reverse Cascade", SkillModifier(), 13881.5),
            ("Bladeshower", SkillModifier(), 4958.4),
            ("Bladeshower", SkillModifier(force_combo=True), 6946.2),
            ("Fan Dance", SkillModifier(), 7439.8),
            ("Rising Windmill", SkillModifier(), 6960.2),
            ("Fountainfall", SkillModifier(), 16909.7),
            ("Bloodshower", SkillModifier(), 8931.5),
            ("Fan Dance II", SkillModifier(), 4959.1),
            ("Fan Dance III", SkillModifier(), 9927.4),
            ("Quadruple Technical Finish", SkillModifier(), 64524.2),
            ("Triple Technical Finish", SkillModifier(), 44704.6),
            ("Double Technical Finish", SkillModifier(), 35715.3),
            ("Single Technical Finish", SkillModifier(), 26831.2),
            ("Saber Dance", SkillModifier(), 25811.8),
            ("Tillana", SkillModifier(), 29797.7),
            ("Finishing Move", SkillModifier(), 42226.1),
            ("Fan Dance IV", SkillModifier(), 14902.1),
            ("Starfall Dance", SkillModifier(), 51329.6),
            ("Last Dance", SkillModifier(), 25823.5),
            ("Dance of the Dawn", SkillModifier(), 49558.4),
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
            version="7.0",
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
            ("Detonator", 57463.6),
            ("Detonator", 47899.7),
            ("Detonator", 38321.5),
            ("Detonator", 28737.6),
            ("Detonator", 19157.3),
            ("Detonator", 9577.1),
            ("Detonator", 0.0),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Shot", SkillModifier(), 2899.8),
            ("Gauss Round", SkillModifier(), 6460.1),
            ("Heat Blast", SkillModifier(), 9929.0),
            ("Heat Blast", SkillModifier(with_condition="Reassemble"), 17122.5),
            ("Heat Blast", SkillModifier(with_condition="Overheated"), 10948.2),
            (
                "Heat Blast",
                SkillModifier(with_condition="Overheated, Reassemble"),
                18840.8,
            ),
            ("Ricochet", SkillModifier(), 6459.0),
            ("Auto Crossbow", SkillModifier(), 7955.0),
            ("Auto Crossbow", SkillModifier(with_condition="Reassemble"), 13697.6),
            ("Auto Crossbow", SkillModifier(with_condition="Overheated"), 8940.2),
            ("Heated Split Shot", SkillModifier(), 10947.1),
            ("Heated Split Shot", SkillModifier(with_condition="Reassemble"), 18836.8),
            ("Heated Split Shot", SkillModifier(with_condition="Overheated"), 11908.8),
            ("Drill", SkillModifier(), 29890.8),
            ("Drill", SkillModifier(with_condition="Reassemble"), 51380.2),
            ("Drill", SkillModifier(with_condition="Overheated"), 30840.5),
            ("Heated Slug Shot", SkillModifier(), 6966.0),
            ("Heated Slug Shot", SkillModifier(force_combo=True), 15896.1),
            ("Heated Slug Shot", SkillModifier(with_condition="Reassemble"), 11981.3),
            ("Heated Slug Shot", SkillModifier(with_condition="Overheated"), 7954.6),
            ("Air Anchor", SkillModifier(), 29832.8),
            ("Scattergun", SkillModifier(), 7960.1),
            # overheated should do nothing
            ("Scattergun", SkillModifier(with_condition="Overheated"), 7960.1),
            ("Chain Saw", SkillModifier(), 29857.3),
            ("Double Check", SkillModifier(), 7958.9),
            ("Excavator", SkillModifier(), 29822.8),
            ("Full Metal Field", SkillModifier(), 59950.8),
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
            version="7.0",
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
            ("Sidewinder", 19994.3),
            ("Sidewinder", 19989.9),  # does not get buff yet. Application delay.
            ("Radiant Encore", 47658.1),
            (
                "Sidewinder",
                21164.0,
            ),  # does not get overriden radiant finale buff yet. Application delay.
            ("Radiant Encore", 31176.6),
            ("Radiant Encore", 25418.7),
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
            version="7.0",
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
            ("Sidewinder", 19784.8),
            ("Sidewinder", 20373.3),
            ("Sidewinder", 20742.7),
            ("Sidewinder", 21154.8),
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
            version="7.0",
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
            ("Apex Arrow", 28162.4),
            ("Apex Arrow", 5929.0),
            ("Apex Arrow", 29664.9),
            ("Pitch Perfect", 4949.5),
            ("Pitch Perfect", 17820.9),
            ("Pitch Perfect", 10876.4),
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
            version="7.0",
        )
        skills_and_expected_damage = (
            ("Auto", SkillModifier(), 3113.1),
            ("Bootshine", SkillModifier(), 8735.4),
            ("Bootshine", SkillModifier(with_condition="Opo-opo Form"), 12096.6),
            ("Snap Punch", SkillModifier(), 14277.8),
            ("Twin Snakes", SkillModifier(), 15072.6),
            ("Demolish", SkillModifier(), 15878.9),
            ("Rockbreaker", SkillModifier(), 5170.4),
            ("Four-point Fury", SkillModifier(), 4757.3),
            ("Dragon Kick", SkillModifier(), 12719.4),
            ("The Forbidden Chakra", SkillModifier(), 15870.9),
            ("Elixir Field", SkillModifier(), 31833.3),
            ("Celestial Revolution", SkillModifier(), 17874.0),
            ("Enlightenment", SkillModifier(), 6757.2),
            ("Six-sided Star", SkillModifier(with_condition="5 Chakra"), 46834.1),
            ("Six-sided Star", SkillModifier(with_condition="0 Chakra"), 31007.0),
            ("Leaping Opo", SkillModifier(), 10318.2),
            ("Leaping Opo", SkillModifier(with_condition="Opo-opo's Fury"), 18279.3),
            ("Rising Raptor", SkillModifier(), 13084.2),
            ("Rising Raptor", SkillModifier(with_condition="Raptor's Fury"), 19062.8),
            ("Pouncing Coeurl", SkillModifier(), 15887.2),
            ("Pouncing Coeurl", SkillModifier(with_condition="Coeurl's Fury"), 19886.2),
            ("Wind's Reply", SkillModifier(), 31798.2),
            ("Fire's Reply", SkillModifier(), 43637.0),
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
            version="7.0",
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
        rb.add_next("Bootshine")
        rb.add_next("Elixir Burst")
        rb.add_next("Bootshine")

        expected = (
            ("Bootshine", 8727.6),
            ("Snap Punch", 14300.5),
            ("Bootshine", 12096.3),
            #
            ("Rising Raptor", 13098.8),
            ("Twin Snakes", 15112.2),
            ("Rising Raptor", 19062.7),
            ("Rising Raptor", 19062.8),
            ("Rising Raptor", 13118.0),
            #
            ("Pouncing Coeurl", 15887.2),
            ("Demolish", 15885.6),
            ("Pouncing Coeurl", 19886.1),
            ("Pouncing Coeurl", 19886.2),
            ("Pouncing Coeurl", 19886.3),
            ("Pouncing Coeurl", 15887.2),
            #
            ("Bootshine", 12089.1),
            ("Elixir Burst", 35727.8),
            ("Bootshine", 12089.1),
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
            version="7.0",
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
            ("True Thrust", 9713.7),
            ("Piercing Talon", 6340.6),
            ("Dragonfire Dive", 21071.5),
            ("Fang and Claw", 7608.8),
            ("Rise of the Dragon", 23247.5),
            ("Spiral Blow", 5917.1),
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
            version="7.0",
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
            ("True Thrust", 9703.4),
            ("Lance Barrage", 14354.6),
            ("Heavens' Thrust", 18582.8),
            ("Fang and Claw", 14335.6),
            ("Fang and Claw", 7601.4),
            ("Heavens' Thrust", 5914.7),  # no combo bonus
            ("Lance Barrage", 5494.3),  # no combo bonus
            ("True Thrust", 9703.4),
            ("Lance Barrage", 14354.6),
            ("Lance Barrage", 5490.1),
            ("Heavens' Thrust", 5914.7),  # no combo bonus
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
            version="7.0",
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
            
        rb.add(423.369, "Spinning Edge") ##
        rb.add(425.947, "Kassatsu")
        
        rb.add(427.369, "Gust Slash")
        rb.add(429.506, "Armor Crush")
        rb.add(430.798, "Bhavacakra")
        rb.add(431.642, "Ten")
        rb.add(432.132, "Jin")
        rb.add(432.622, "Hyosho Ranryu")
        
        expected = (
            ("Hyosho Ranryu", 68225.1),
            ("Spinning Edge", 12132.1),
            ("Gust Slash", 15376.3),
            ("Armor Crush", 19416.3),
            ("Bhavacakra", 15372.9),
            ("Hyosho Ranryu", 68306.8),
            
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
            version="7.0",
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
            ("Aeolian Edge", 10527.2),
            ("Aeolian Edge", 14597.0),
            #
            ("Armor Crush", 11341.4),
            ("Aeolian Edge", 14573.7),
            ("Aeolian Edge", 14580.4),
            ("Aeolian Edge", 10538.1),
            #
            ("Armor Crush", 11335.1),
            ("Armor Crush", 11335.1),
            ("Aeolian Edge", 14566.2),
            ("Aeolian Edge", 14566.2),
            ("Aeolian Edge", 14566.2),
            ("Aeolian Edge", 14566.2),
            ("Aeolian Edge", 10545.0),
            # doku
            ("Aeolian Edge", 10545.0),
            ("Dokumori", 12163.7),
            ("Aeolian Edge", 11056.0),
            # Kunai
            ("Aeolian Edge", 10526.6),
            ("Kunai's Bane", 24314.3),
            ("Aeolian Edge", 11586.8),
            # meisui
            ("Zesho Meppo", 22275.9),
            ("Bhavacakra", 15392.6),
            ("Zesho Meppo", 28371.5),
            ("Bhavacakra", 15392.6),
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
            version="7.0",
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
            ("Hyosho Ranryu", 68433.6),
            ("Hyosho Ranryu", 52765.4),
            ("Gust Slash (pet)", 5984.8),
            ("Gust Slash", 8913.4),
            ("Aeolian Edge (pet)", 5968.4),
            ("Aeolian Edge", 10554.2),
            ("Hakke Mujinsatsu (pet)", 2984.0),
            ("Hakke Mujinsatsu", 4054.4),
            ("Armor Crush (pet)", 5970.8),
            ("Armor Crush", 11355.8),
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
            version="7.0",
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
        expected_damage = 638909.4
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
            version="7.0",
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

        expected_damage = 140551.9
        expected_total_time = 17860.0
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
            version="7.0",
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

        expected_damage = 678638.5
        expected_total_time = 32120.0
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
            version="7.0",
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
            ("Kasha", 17952.2),
            ("Gekko", 17942.0),
            ("Kasha", 20247.1),
            ("Enpi", 4081.2),
            ("Hissatsu: Yaten", 4077),
            ("Enpi", 10598.7),
            ("Enpi", 4081.2),
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
            version="7.0",
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

        expected_damage = 493500.6
        expected_total_time = 24240.0
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
            version="7.0",
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
            ("Executioner's Gibbet", 31448.6),
            ("Gallows", 25660.0),
            ("Executioner's Gibbet", 33950.4),
            ("Executioner's Gibbet", 31448.6),
            #
            ("Executioner's Gallows", 33916.7),
            ("Gibbet", 25660.0),
            ("Executioner's Gallows", 33950.4),
            ("Executioner's Gallows", 31448.6),
            #
            ("Gallows", 23152.1),
            ("Gibbet", 25671.4),
            ("Executioner's Gibbet", 31434.5),
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
            version="7.0",
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

        expected_damage = 720311.3
        expected_total_time = 46920.0
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
            version="7.0",
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
            ("Ruin III", 19237.4),
            ("Ruin III", 21928.8),
            ("Ruin III", 19237.4),
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
            version="7.0",
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

        expected_damage = 549948.4
        expected_total_time = 34590.0
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
            version="7.0",
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
            ("Jolt III", 19238.6),
            ("Grand Impact", 32052.8),
            ("Grand Impact", 33710.7),
            ("Jolt III", 20177.3),
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
            version="7.0",
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

        expected_damage = 444172.1
        expected_total_time = 24660.0
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
            version="7.0",
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
            ("Flare Star", 18770.2),
            ("Fire III", 13116.0),
            ("Flare Star", 43924.3),
            ("Fire IV", 34029.0),
            ("Flare Star", 43934.5),
            ("Paradox", 30526.3),
            ("Fire IV", 34068.2),
            ("Xenoglossy", 53659.7),
            ("Fire III", 23889.8),
            ("Blizzard III", 11927.9),
            ("Flare Star", 17063.6),
            ("Flare Star", 43917.0),
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
            version="7.0",
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

        expected_damage = 595855.6
        expected_total_time = 28860.0

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
            version="7.0",
        )
        rb = RotationBuilder(
            stats,
            self.__skill_library,
            ignore_trailing_dots=True,
            snap_dots_to_server_tick_starting_at=0,
            fight_start_time=0,
        )

        rot_and_expected = (
            ("Hindsting Strike", 14592.2),
            ("Flanksbane Fang", 18685.5),
            ("Hindsbane Fang", 18659.3),
            ("Flanksting Strike", 18674.2),
            ("Flanksting Strike", 14596.1),
            ("Hindsting Strike", 18659.5),
            ("Hindsting Strike", 14624.3),
            #
            ("Flanksbane Fang", 18641.5),
            ("Hindsbane Fang", 18658.1),
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
            version="7.0",
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
            ("Fire in Red", 23540.1),
            ("Rainbow Drip", 53499.0),
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
            version="7.0",
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
            
        expected_damage = 1133183.8
        expected_total_time = 54470.0

        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)
