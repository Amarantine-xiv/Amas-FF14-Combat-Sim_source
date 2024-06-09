import numpy as np

from simulator.damage_simulator import DamageSimulator
from simulator.skills.create_skill_library import create_skill_library
from simulator.skills.skill_modifier import SkillModifier
from simulator.stats import Stats
from simulator.testing.test_class import TestClass
from simulator.timeline_builders.damage_builder import DamageBuilder
from simulator.timeline_builders.rotation_builder import RotationBuilder


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
            ("Glare IV", SkillModifier(), 28982.0),
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
            ("Toxikon II", SkillModifier(), 17284.2),
            ("Dykrasia II", SkillModifier(), 8901.3),
            ("Pneuma", SkillModifier(), 17264.3),
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
            ("Ruin II", SkillModifier(), 10786.7),
            ("Energy Drain", SkillModifier(), 4901.8),
            ("Art of War II", SkillModifier(), 8821.7),
            ("Biolysis", SkillModifier(), 37945.5),
            ("Baneful Impaction", SkillModifier(), 35576.5),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            ("Oracle", SkillModifier(), 29889.0),
            ("Lord of Crowns", SkillModifier(), 19933.8),
        )
        return self.__test_skills(stats, skills_and_expected_damage)

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
            ("Storm's Path", SkillModifier(force_combo=True), 11970.2),
            ("Storm's Path", SkillModifier(), 4676.8),
            ("Storm's Eye", SkillModifier(force_combo=True), 11968.8),
            ("Storm's Eye", SkillModifier(), 4680.4),
            ("Upheaval", SkillModifier(), 10418.6),
            ("Onslaught", SkillModifier(), 3900.5),
            ("Fell Cleave", SkillModifier(), 14035.7),
            ("Primal Rend", SkillModifier(), 31574.8),
            ("Inner Chaos", SkillModifier(), 29773.5),
            ("Tomahawk", SkillModifier(), 3898.4),
            ("Overpower", SkillModifier(), 2859.7),
            ("Mythril Tempest", SkillModifier(force_combo=True), 3639.6),
            ("Mythril Tempest", SkillModifier(), 2602.5),
            ("Orogeny", SkillModifier(), 3903.3),
            ("Decimate", SkillModifier(), 4677.1),
            ("Damnation", SkillModifier(with_condition="Retaliation"), 1424.1),
            ("Primal Wrath", SkillModifier(), 15611.6),
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
        expected_damage = 367328.8
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
            ("Keen Edge", SkillModifier(), 7269.3),
            ("Brutal Shell", SkillModifier(force_combo=True), 9897.2),
            ("Brutal Shell", SkillModifier(), 6235.2),
            ("Demon Slice", SkillModifier(), 2594.8),
            ("Lightning Shot", SkillModifier(), 3892.1),
            ("Solid Barrel", SkillModifier(force_combo=True), 11444.1),
            ("Solid Barrel", SkillModifier(), 5713.8),
            ("Burst Strike", SkillModifier(), 11446.3),
            ("Demon Slaughter", SkillModifier(force_combo=True), 4162.4),
            ("Demon Slaughter", SkillModifier(), 2601.2),
            ("Sonic Break", SkillModifier(), 23398.8),
            ("Gnashing Fang", SkillModifier(), 11967.3),
            ("Savage Claw", SkillModifier(force_combo=True), 14044.1),
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
            ("Sepulcher", SkillModifier(), 12457.3),
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
            ("Blade of Honor", SkillModifier(), 19258.4),
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
            ("Hard Slash", SkillModifier(), 6211.8),
            ("Syphon Strike", SkillModifier(force_combo=True), 8802.9),
            ("Syphon Strike", SkillModifier(), 5176.9),
            ("Unleash", SkillModifier(), 3105.4),
            ("Unmend", SkillModifier(), 3885.94),
            ("Souleater", SkillModifier(force_combo=True), 10865.9),
            ("Souleater", SkillModifier(), 5182.6),
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
            ("Cascade", SkillModifier(), 13897.6),
            ("Fountain", SkillModifier(), 7934.8),
            ("Fountain", SkillModifier(force_combo=True), 16878.3),
            ("Windmill", SkillModifier(), 4960.8),
            ("Double Standard Finish", SkillModifier(), 35716.8),
            ("Single Standard Finish", SkillModifier(), 26814.9),
            ("Standard Finish", SkillModifier(), 17881.2),
            ("Reverse Cascade", SkillModifier(), 13881.5),
            ("Bladeshower", SkillModifier(), 4958.4),
            ("Bladeshower", SkillModifier(force_combo=True), 6946.2),
            ("Fan Dance", SkillModifier(), 8927.1),
            ("Rising Windmill", SkillModifier(), 6960.2),
            ("Fountainfall", SkillModifier(), 19840.9),
            ("Bloodshower", SkillModifier(), 8931.5),
            ("Fan Dance II", SkillModifier(), 4959.1),
            ("Fan Dance III", SkillModifier(), 10913.2),
            ("Quadruple Technical Finish", SkillModifier(), 59531.4),
            ("Triple Technical Finish", SkillModifier(), 44704.6),
            ("Double Technical Finish", SkillModifier(), 35715.3),
            ("Single Technical Finish", SkillModifier(), 26831.2),
            ("Saber Dance", SkillModifier(), 26816.4),
            ("Tillana", SkillModifier(), 21849.6),
            ("Finishing Move", SkillModifier(), 21823.6),
            ("Fan Dance IV", SkillModifier(), 16873.1),
            ("Starfall Dance", SkillModifier(), 51329.6),
            ("Last Dance", SkillModifier(), 20875.5),
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
            ("Sidewinder", 15989.8),
            ("Sidewinder", 15996.7),  # does not get buff yet. Application delay.
            ("Radiant Encore", 37056.9),
            (
                "Sidewinder",
                16932.4,
            ),  # does not get overriden radiant finale buff yet. Application delay.
            ("Radiant Encore", 25948.72),
            ("Radiant Encore", 20333.96),
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
            ("Sidewinder", 15822.5),
            ("Sidewinder", 16352.2),
            ("Sidewinder", 16621.7),
            ("Sidewinder", 16932.4),
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
            ("Apex Arrow", 23485.1),
            ("Apex Arrow", 4948.9),
            ("Apex Arrow", 24763.2),
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
            ("Bootshine", SkillModifier(), 11947.4),
            ("Bootshine", SkillModifier(with_condition="Opo-opo Form"), 16497.9),
            ("Snap Punch", SkillModifier(), 13512.7),
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
            ("Leaping Opo", SkillModifier(), 14286.1),
            ("Leaping Opo", SkillModifier(with_condition="Opo-opo's Fury"), 18279.3),
            ("Rising Raptor", SkillModifier(), 15089.2),
            ("Rising Raptor", SkillModifier(with_condition="Raptor's Fury"), 19062.8),
            ("Pouncing Coeurl", SkillModifier(), 15887.2),
            ("Pouncing Coeurl", SkillModifier(with_condition="Coeurl's Fury"), 19886.2),
            ("Wind's Reply", SkillModifier(), 35717.6),
            ("Fire's Reply", SkillModifier(), 51731.4),
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
            ("Bootshine", 11930.5),
            ("Snap Punch", 13511.2),
            ("Bootshine", 16493.4),
            #
            ("Rising Raptor", 15096.6),
            ("Twin Snakes", 15112.2),
            ("Rising Raptor", 19062.7),
            ("Rising Raptor", 19062.8),
            ("Rising Raptor", 15096.3),
            #
            ("Pouncing Coeurl", 15887.2),
            ("Demolish", 15885.6),
            ("Pouncing Coeurl", 19886.1),
            ("Pouncing Coeurl", 19886.2),
            ("Pouncing Coeurl", 19886.3),
            ("Pouncing Coeurl", 15887.2),
            #
            ("Bootshine", 11947.4),
            ("Elixir Burst", 35727.8),
            ("Bootshine", 16497.2),
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
            ("Aeolian Edge", 9725.6),
            ("Aeolian Edge", 12157.7),
            #
            ("Armor Crush", 9704.3),
            ("Aeolian Edge", 12157.7),
            ("Aeolian Edge", 12157.7),
            ("Aeolian Edge", 9725.6),
            #
            ("Armor Crush", 9704.3),
            ("Armor Crush", 9704.3),
            ("Aeolian Edge", 12157.7),
            ("Aeolian Edge", 12157.7),
            ("Aeolian Edge", 12157.7),
            ("Aeolian Edge", 12157.7),
            ("Aeolian Edge", 9725.6),
            # doku
            ("Aeolian Edge", 9725.6),
            ("Dokumori", 12163.7),
            ("Aeolian Edge", 10201.0),
            # Kunai
            ("Aeolian Edge", 9725.6),
            ("Kunai's Bane", 24314.3),
            ("Aeolian Edge", 10702.7),
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
            ("_Bunshin_melee", 5984.8),
            ("Gust Slash", 8115.2),
            ("_Bunshin_melee", 5968.4),
            ("Aeolian Edge", 9723.2),
            ("_Bunshin_area", 2984.0),
            ("Hakke Mujinsatsu", 4054.4),
            ("_Bunshin_melee", 5970.8),
            ("Armor Crush", 9727.0),
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
        expected_damage = 620771.8
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

        expected_damage = 676189.0
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
        expected_total_time = 24200.0
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

        expected_damage = 742475.8
        expected_total_time = 46920.0
        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)

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

        expected_damage = 542672.9
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
            ("Grand Impact", 28827.0),
            ("Grand Impact", 30327.5),
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

        expected_damage = 442172.1
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
            ("Flare Star", 16435.5),
            ("Fire III", 13116.0),
            ("Flare Star", 38411.7),
            ("Fire IV", 34029.0),
            ("Flare Star", 38426.4),
            ("Paradox", 30526.3),
            ("Fire IV", 34068.2),
            ("Xenoglossy", 53659.7),
            ("Fire III", 23889.8),
            ("Blizzard III", 11927.9),
            ("Flare Star", 14882.7),
            ("Flare Star", 38413.0),
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

        expected_damage = 608896.2
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
            ("Hindsting Strike", 14205.2),
            ("Flanksbane Fang", 18245.3),
            ("Hindsbane Fang", 18245.3),
            ("Flanksting Strike", 18245.3),
            ("Flanksting Strike", 14205.2),
            ("Hindsting Strike", 18232.7),
            ("Hindsting Strike", 14205.2),
            #
            ("Flanksbane Fang", 18239.9),
            ("Hindsbane Fang", 18239.9),
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
            ("Fire in Red", 21411.3),
            ("Rainbow Drip", 48173.9),
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
            
        expected_damage = 1030746.5
        expected_total_time = 54470.0

        return self.__test_aggregate_rotation(rb, expected_damage, expected_total_time)
