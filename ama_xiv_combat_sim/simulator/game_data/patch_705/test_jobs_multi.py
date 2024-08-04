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

GAME_VERSION="7.05"

class TestJobsMulti705(TestClass):
    def __init__(self):
        super().__init__()
        self.__skill_library = create_skill_library(GAME_VERSION)
        self.__relative_tol = 6e-3

    def __test_multi_target_skills(self, stats, skills_and_expected_damages):
        test_passed = True
        err_msg = ""

        for i, (
            sk,
            targets,
            skill_modifier,
            expected_damages,
        ) in enumerate(skills_and_expected_damages):
            assert isinstance(
                expected_damages, tuple
            ), "Expected damages must be tuples. Perhaps you forgot a comma?"

            rb = RotationBuilder(stats, self.__skill_library)
            rb.add_next(sk, skill_modifier=skill_modifier, targets=targets)

            db = DamageBuilder(stats, self.__skill_library)
            sim = DamageSimulator(
                rb.get_stats(), db.get_damage_instances(rb.get_skill_timing()), 75000
            )
            actual_per_skill_damage = sim.get_per_skill_damage()
            if len(expected_damages) != len(actual_per_skill_damage):
                test_passed = False
                err_msg += f"# skills return did not match. Expected: {len(expected_damages)}, Returned: {len(actual_per_skill_damage)}. Entry #: {i}.\n"
                return test_passed, err_msg

            for i, tmp in enumerate(zip(expected_damages, actual_per_skill_damage)):
                expected_damage, per_skill = tmp
                diff = abs(float(expected_damage - per_skill.expected_damage))
                if diff / expected_damage >= self.__relative_tol:
                    test_passed = False
                    err_msg += f"Did not get expected damage for {sk} / {skill_modifier}. Expected: {expected_damage} . Actual: {int(round(per_skill.expected_damage, 0))} at position {i}.\n"
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
                err_msg += f"Name did not match. Expected: {expected_skill_name}. Actual: {result_skill_name}\n"

            result_damage, expected_damage = (
                result[i][1],
                expected_damage_instances[i][1],
            )
            diff = abs(result_damage - expected_damage)
            if diff / max(1e-6, expected_damage) >= 0.005:
                test_passed = False
                err_msg += f"Did not get expected damage for damage instance {result_skill_name}. Expected: {expected_damage}. Actual: {int(round(result_damage, 0))} .\n"

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

        if expected_total_time is not None:
            actual_total_time = max(sim.get_damage_time()) - min(sim.get_damage_time())
            if abs(expected_total_time - actual_total_time) > 1e-3:
                test_passed = False
                err_msg += "Did not get expected total time for rotation. Expected: {} . Actual: {} .\n".format(
                    expected_total_time, int(round(actual_total_time, 0))
                )

        return test_passed, err_msg

    @TestClass.is_a_test
    def test_whm_aoe(self):
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
        holy_iii_base = 7574
        afflatus_misery_base = 66702
        glare_iv_base = 32290
        skills_and_expected_damages = (
            ("Holy III", "t1", SkillModifier(), (holy_iii_base,)),
            ("Holy III", "t1, t2", SkillModifier(), (holy_iii_base, holy_iii_base)),
            (
                "Afflatus Misery",
                "t1, t2, t3",
                SkillModifier(),
                (
                    afflatus_misery_base,
                    0.5 * afflatus_misery_base,
                    0.5 * afflatus_misery_base,
                ),
            ),
            (
                "Glare IV",
                "t1, t2, t3",
                SkillModifier(),
                (glare_iv_base, 0.6 * glare_iv_base, 0.6 * glare_iv_base),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_sch_aoe(self):
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
        baneful_base = 7000
        skills_and_expected_damages = (
            (
                "Baneful Impaction",
                "t1",
                SkillModifier(),
                tuple([baneful_base] * 5),
            ),
            (
                "Baneful Impaction",
                "t1, t2",
                SkillModifier(),
                tuple([baneful_base] * 10),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_sge_aoe(self):
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
        base_phlegma = 30885
        base_toxikon_ii = 18551
        base_pneuma = 18537
        base_psyche = 30895
        base_dyskii = 8734
        skills_and_expected_damages = (
            (
                "Phlegma III",
                "t1, t2, t3",
                SkillModifier(),
                (base_phlegma, 0.5 * base_phlegma, 0.5 * base_phlegma),
            ),
            (
                "Toxikon II",
                "t1, t2, t3",
                SkillModifier(),
                (base_toxikon_ii, 0.5 * base_toxikon_ii, 0.5 * base_toxikon_ii),
            ),
            (
                "Pneuma",
                "t1, t2, t3",
                SkillModifier(),
                (base_pneuma, 0.6 * base_pneuma, 0.6 * base_pneuma),
            ),
            (
                "Psyche",
                "t1, t2, t3",
                SkillModifier(),
                (base_psyche, 0.5 * base_psyche, 0.5 * base_psyche),
            ),
            (
                "Dyskrasia II",
                "t1, t2, t3",
                SkillModifier(),
                (base_dyskii, base_dyskii, base_dyskii),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_ast_aoe(self):
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
        base_marcocosmos = 13457
        base_lord_of_crowns = 19967.9
        skills_and_expected_damages = (
            (
                "Macrocosmos",
                "t1, t2, t3",
                SkillModifier(),
                (base_marcocosmos, 0.6 * base_marcocosmos, 0.6 * base_marcocosmos),
            ),
            (
                "Lord of Crowns",
                "t1, t2",
                SkillModifier(),
                (base_lord_of_crowns, base_lord_of_crowns),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_drk_aoe(self):
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
        base_quietus = 6163
        base_impalement = 8211
        base_disesteem = 25636
        base_salt_and_darkness = 12840
        skills_and_expected_damages = (
            (
                "Quietus",
                "t1, t2",
                SkillModifier(),
                (base_quietus, base_quietus),
            ),
            (
                "Impalement",
                "t1, t2",
                SkillModifier(),
                (base_impalement, base_impalement),
            ),
            (
                "Disesteem",
                "t1, t2, t3",
                SkillModifier(),
                (base_disesteem, 0.5 * base_disesteem, 0.5 * base_disesteem),
            ),
            (
                "Salt and Darkness",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_salt_and_darkness,
                    0.5 * base_salt_and_darkness,
                    0.5 * base_salt_and_darkness,
                ),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Stalwart Soul", skill_modifier=SkillModifier(), targets="t2")
        rb.add(3, "Unleash", skill_modifier=SkillModifier(), targets="t1")
        rb.add(6, "Stalwart Soul", skill_modifier=SkillModifier(), targets="t1, t2")

        rb.add(
            100, "Flood of Shadow", skill_modifier=SkillModifier(), targets="t1, t2"
        )
        rb.add(
            200, "Living Shadow", skill_modifier=SkillModifier(), targets="t1, t2"
        )

        expected = (
            ("Stalwart Soul", 3076),
            ("Unleash", 3077),
            ("Stalwart Soul", 4098),
            ("Stalwart Soul", 4098),
            ("Flood of Shadow", 4103),
            ("Flood of Shadow", 4103),
            # living shadow. only 2 of these cleave.
            ("Abyssal Drain (pet)", 12298),
            ("Shadowbringer (pet)", 16690),
            ("Shadowbringer (pet)", 16690),
            ("Edge of Shadow (pet)", 12297),
            ("Bloodspiller (pet)", 12302),
            ("Disesteem (pet)", 18151),
            ("Disesteem (pet)", 18151),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_gnb_aoe(self):
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
        base_double_down = 30611
        base_reign = 20406
        base_noble_blood = 25539
        base_lion_heart = 30603
        skills_and_expected_damages = (
            (
                "Double Down",
                "t1, t2, t3",
                SkillModifier(),
                (base_double_down, 0.85 * base_double_down, 0.85 * base_double_down),
            ),
            (
                "Reign of Beasts",
                "t1, t2, t3",
                SkillModifier(),
                (base_reign, 0.4 * base_reign, 0.4 * base_reign),
            ),
            (
                "Noble Blood",
                "t1, t2, t3",
                SkillModifier(),
                (base_noble_blood, 0.4 * base_noble_blood, 0.4 * base_noble_blood),
            ),
            (
                "Lion Heart",
                "t1, t2, t3",
                SkillModifier(),
                (base_lion_heart, 0.4 * base_lion_heart, 0.4 * base_lion_heart),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Demon Slaughter", skill_modifier=SkillModifier(), targets="t2")
        rb.add(3, "Demon Slice", skill_modifier=SkillModifier(), targets="t1")
        rb.add(
            6, "Demon Slaughter", skill_modifier=SkillModifier(), targets="t1, t2"
        )

        expected = (
            ("Demon Slaughter", 2550),
            ("Demon Slice", 2545),
            ("Demon Slaughter", 4080),
            ("Demon Slaughter", 4080),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_pld_aoe(self):
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
        base_expiacion = 11487
        base_holy_circle = 5096
        skills_and_expected_damages = (
            (
                "Expiacion",
                "t1, t2, t3",
                SkillModifier(),
                (base_expiacion, 0.4 * base_expiacion, 0.4 * base_expiacion),
            ),
            (
                "Holy Circle",
                "t1, t2",
                SkillModifier(with_condition="Divine Might"),
                (base_holy_circle, base_holy_circle),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Prominence", skill_modifier=SkillModifier(), targets="t2")
        rb.add(3, "Total Eclipse", skill_modifier=SkillModifier(), targets="t1")
        rb.add(6, "Prominence", skill_modifier=SkillModifier(), targets="t1, t2")

        rb.add(100, "Requiescat")
        rb.add(103, "Confiteor", targets="t1, t2")
        rb.add(106, "Confiteor", targets="t1, t2")
        rb.add(109, "Confiteor", targets="t1")
        rb.add(112, "Confiteor", targets="t1")
        # this one should be weaker now
        rb.add(115, "Confiteor", targets="t1")
                
        expected = (
            ("Prominence", 2550),
            ("Total Eclipse", 2546),
            ("Prominence", 4337),
            ("Prominence", 4337),
            ("Requiescat", 8155),
            ("Confiteor", 25500),
            ("Confiteor", 12747),  # non-primary target
            ("Confiteor", 25500),
            ("Confiteor", 12747),  # non-primary target
            ("Confiteor", 25500),
            ("Confiteor", 25500),
            # only this one should be weaker
            ("Confiteor", 12762),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_war_aoe(self):
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
        base_chaotic_cyclone = 13530
        base_orogeny = 3867.3
        base_primal_rend = 31575
        base_primal_wrath = 18032
        base_primal_ruination = 35066

        skills_and_expected_damages = (
            (
                "Chaotic Cyclone",
                "t1, t2",
                SkillModifier(),
                (base_chaotic_cyclone, base_chaotic_cyclone),
            ),
            (
                "Orogeny",
                "t1, t2",
                SkillModifier(),
                (base_orogeny, base_orogeny),
            ),
            (
                "Primal Rend",
                "t1, t2, t3",
                SkillModifier(),
                (base_primal_rend, 0.3 * base_primal_rend, 0.3 * base_primal_rend),
            ),
            (
                "Primal Wrath",
                "t1, t2, t3",
                SkillModifier(),
                (base_primal_wrath, 0.3 * base_primal_wrath, 0.3 * base_primal_wrath),
            ),
            (
                "Primal Ruination",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_primal_ruination,
                    0.3 * base_primal_ruination,
                    0.3 * base_primal_ruination,
                ),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)

        rb.add(0, "Heavy Swing", skill_modifier=SkillModifier(), targets="t2")
        rb.add(3, "Mythril Tempest", skill_modifier=SkillModifier(), targets="t2")
        rb.add(6, "Overpower", skill_modifier=SkillModifier(), targets="t1")
        rb.add(
            9, "Mythril Tempest", skill_modifier=SkillModifier(), targets="t1, t2"
        )
        rb.add(23, "Heavy Swing", skill_modifier=SkillModifier(), targets="t1")
        rb.add(43, "Heavy Swing", skill_modifier=SkillModifier(), targets="t2")

        expected = (
            ("Heavy Swing", 5674),
            ("Mythril Tempest", 2576),
            ("Overpower", 2834),
            ("Mythril Tempest", 3608),
            ("Mythril Tempest", 3608),
            ("Heavy Swing", 6238),
            # Surging tempest should've worn off by now
            ("Heavy Swing", 5670),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_dnc_aoe(self):
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
        base_fan_dance_iv = 20385

        skills_and_expected_damages = (
            (
                "Fan Dance IV",
                "t1, t2, t3",
                SkillModifier(),
                (base_fan_dance_iv, 0.5 * base_fan_dance_iv, 0.5 * base_fan_dance_iv),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)

        rb.add(0, "Cascade", skill_modifier=SkillModifier(), targets="t2")
        rb.add(
            3,
            "Double Standard Finish",
            skill_modifier=SkillModifier(),
            targets="t2, t1",
        )
        rb.add(6, "Cascade", skill_modifier=SkillModifier(), targets="t2")

        rb.add(100, "Cascade", skill_modifier=SkillModifier(), targets="t2")
        rb.add(
            103, "Standard Finish", skill_modifier=SkillModifier(), targets="t2, t1"
        )
        rb.add(106, "Cascade", skill_modifier=SkillModifier(), targets="t2")

        rb.add(200, "Cascade", skill_modifier=SkillModifier(), targets="t2")
        rb.add(
            203,
            "Quadruple Technical Finish",
            skill_modifier=SkillModifier(),
            targets="t2, t1",
        )
        rb.add(206, "Cascade", skill_modifier=SkillModifier(), targets="t2")

        rb.add(300, "Cascade", skill_modifier=SkillModifier(), targets="t2")
        rb.add(
            303,
            "Quadruple Technical Finish",
            skill_modifier=SkillModifier(),
            targets="t2, t1",
        )
        rb.add(306, "Cascade", skill_modifier=SkillModifier(), targets="t2")

        expected = (
            ("Cascade", 10671),
            ("Double Standard Finish", 41240),
            ("Double Standard Finish", 41240),
            ("Cascade", 11195),
            #
            ("Cascade", 10671),
            ("Double Standard Finish", 41240),
            ("Double Standard Finish", 41240),
            ("Cascade", 11195),
            #
            ("Cascade", 10678),
            ("Quadruple Technical Finish", 63075),
            ("Quadruple Technical Finish", 63075),
            ("Cascade", 11220),
            #
            ("Cascade", 10670),
            ("Quadruple Technical Finish", 63118),
            ("Quadruple Technical Finish", 63118),
            ("Cascade", 11200),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_mch_aoe(self):
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
        base_bioblaster = 2428
        base_bioblaster_dot = 2421

        skills_and_expected_damages = (
            (
                "Bioblaster",
                "t1, t2",
                SkillModifier(),
                (
                    base_bioblaster,
                    base_bioblaster,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                    base_bioblaster_dot,
                ),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)

        rb.add(0, "Heat Blast", skill_modifier=SkillModifier(), targets="t1")
        rb.add(3, "Reassemble", skill_modifier=SkillModifier(), targets="t1")
        rb.add(6, "Auto Crossbow", skill_modifier=SkillModifier(), targets="t2, t1")
        rb.add(9, "Heat Blast", skill_modifier=SkillModifier(), targets="t1")

        expected = (
            ("Heat Blast", 9710),
            # both get the bonus- this is how it's coded to behave for now...
            ("Auto Crossbow", 13516),
            ("Auto Crossbow", 13516),
            ("Heat Blast", 9716),  # make sure bonus is gone
        )
        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)

        expected_damage_rb2_rb3 = 143450
        rb2 = RotationBuilder(stats, self.__skill_library)
        rb2.add_next("Automaton Queen", SkillModifier(with_condition="50 Battery"))
        rb2.add_next("Heated Clean Shot")
        rb2.add_next("Chain Saw", targets="t1, t2")
        rb2.add_next("Chain Saw", targets="t1, t2")
        test_passed3, err_msg3 = self.__test_aggregate_rotation(
            rb2, expected_damage_rb2_rb3, None
        )

        rb3 = RotationBuilder(stats, self.__skill_library)
        rb3.add_next("Heated Clean Shot")
        rb3.add_next("Chain Saw", targets="t1, t2")
        rb3.add_next("Chain Saw", targets="t1, t2")
        rb3.add_next("Automaton Queen")
        test_passed4, err_msg4 = self.__test_aggregate_rotation(
            rb3, expected_damage_rb2_rb3, None
        )

        return (
            test_passed1 and test_passed2 and test_passed3 and test_passed4,
            err_msg1 + "\n" + err_msg2 + "\n" + err_msg3 + "\n" + err_msg4,
        )

    @TestClass.is_a_test
    def test_brd_aoe(self):
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
        pitch_perfect_base = 17407
        apex_arrow_base = 29003

        skills_and_expected_damages = (
            (
                "Pitch Perfect",
                "t1, t2, t3",
                SkillModifier(),
                (
                    pitch_perfect_base,
                    0.5 * pitch_perfect_base,
                    0.5 * pitch_perfect_base,
                ),
            ),
            (
                "Apex Arrow",
                "t1, t2, t3",
                SkillModifier(),
                (apex_arrow_base, apex_arrow_base, apex_arrow_base),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)

        rb.add(
            0,
            "Radiant Encore",
            skill_modifier=SkillModifier(with_condition="2 Encore"),
            targets="t1, t2",
        )
        rb.add(3, "Mage's Ballad", skill_modifier=SkillModifier(), targets="t1")
        rb.add(
            6, "The Wanderer's Minuet", skill_modifier=SkillModifier(), targets="t2"
        )
        rb.add(9, "Radiant Finale", skill_modifier=SkillModifier(), targets="t2")
        rb.add(
            20, "Radiant Encore", skill_modifier=SkillModifier(), targets="t1, t2"
        )

        expected = (
            ("Radiant Encore", 29040),
            ("Radiant Encore", 14491),
            # still affected by RF, but if we delay any longer we lose our
            # job resources. So a bit more damage.
            ("Radiant Encore", 30467),
            ("Radiant Encore", 15217),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_smn_aoe(self):
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
        base_summon_ifrit_ii = 32798
        base_ruin_iv = 25688
        skills_and_expected_damages = (
            (
                "Summon Ifrit II",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_summon_ifrit_ii,
                    0.4 * base_summon_ifrit_ii,
                    0.4 * base_summon_ifrit_ii,
                ),
            ),
            (
                "Ruin IV",
                "t1, t2",
                SkillModifier(),
                (base_ruin_iv, 0.4 * base_ruin_iv),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_rdm_aoe(self):
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
        base_grand_impact = 31439
        skills_and_expected_damages = (
            (
                "Grand Impact",
                "t1, t2, t3",
                SkillModifier(),
                (base_grand_impact, 0.4 * base_grand_impact, 0.4 * base_grand_impact),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_blm_aoe(self):
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
        base_flare = 11556
        base_flare_star = 19299
        base_thunder_iv_dot = 1830
        base_thunder_iv = 3845

        # initial hit is not a dot
        base_thunder_iv_tmp = [base_thunder_iv_dot] * 16
        # because of application delay. should really just compare a set
        base_thunder_iv_tmp[2] = base_thunder_iv
        base_thunder_iv_tmp[3] = base_thunder_iv

        skills_and_expected_damages = (
            (
                "Flare",
                "t1, t2, t3",
                SkillModifier(),
                (base_flare, 0.7 * base_flare, 0.7 * base_flare),
            ),
            (
                "Flare Star",
                "t1, t2, t3",
                SkillModifier(),
                (base_flare_star, 0.35 * base_flare_star, 0.35 * base_flare_star),
            ),
            (
                "Thunder IV",
                "t1, t2",
                SkillModifier(),
                tuple(base_thunder_iv_tmp),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_drg_aoe(self):
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
        base_geirskogul = 11503
        base_sonic_thrust = 4098

        skills_and_expected_damages = (
            (
                "Geirskogul",
                "t1, t2, t3",
                SkillModifier(),
                (base_geirskogul, 0.5 * base_geirskogul, 0.5 * base_geirskogul),
            ),
            (
                "Sonic Thrust",
                "t1, t2, t3",
                SkillModifier(),
                (base_sonic_thrust, base_sonic_thrust, base_sonic_thrust),
            ),
        )
        return self.__test_multi_target_skills(stats, skills_and_expected_damages)

    @TestClass.is_a_test
    def test_nin_aoe(self):
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
        base_phantom = 21794

        skills_and_expected_damages = (
            (
                "Phantom Kamaitachi",
                "t1, t2, t3",
                SkillModifier(),
                (base_phantom, 0.5 * base_phantom, 0.5 * base_phantom),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Bunshin")
        rb.add(3, "Death Blossom", targets="t1, t2")
        rb.add(6, "Death Blossom", targets="t1")
        rb.add(9, "Death Blossom", targets="t1")
        rb.add(12, "Death Blossom", targets="t1")
        rb.add(15, "Hakke Mujinsatsu", targets="t1, t2")
        rb.add(18, "Death Blossom", targets="t1")
        rb.add(100, "Kunai's Bane", targets="t1, t2")
        rb.add(103, "Spinning Edge", targets="t1")
        rb.add(106, "Spinning Edge", targets="t2")
        rb.add(109, "Spinning Edge", targets="t3")
        
        
        expected = (
            ("Death Blossom (pet)", 2898),
            ("Death Blossom (pet)", 2898),
            ("Death Blossom", 3967),
            ("Death Blossom", 3967),            
            #
            ("Death Blossom (pet)", 2898),
            ("Death Blossom", 3967),            
            #
            ("Death Blossom (pet)", 2898),
            ("Death Blossom", 3967),            
            #
            ("Death Blossom (pet)", 2898),
            ("Death Blossom", 3967),            
            #
            ("Hakke Mujinsatsu (pet)", 2898),
            ("Hakke Mujinsatsu (pet)", 2898),
            ("Hakke Mujinsatsu", 5150),
            ("Hakke Mujinsatsu", 5150),
            #
            ("Death Blossom", 3967),
            #
            ("Kunai's Bane", 23820),
            ("Kunai's Bane", 23820),
            ("Spinning Edge", 13076),
            ("Spinning Edge", 13076),
            ("Spinning Edge", 11906),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_sam_aoe(self):
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
        base_mangetsu = 3990        

        skills_and_expected_damages = (
            (
                "Mangetsu",
                "t1, t2",
                SkillModifier(),
                (base_mangetsu, base_mangetsu),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Mangetsu", targets="t1")
        rb.add(3, "Fuko", targets="t1, t2")
        rb.add(6, "Mangetsu", targets="t1, t2")
        
        expected = (
            ("Mangetsu", 3984),
            ("Fuko", 3988),
            ("Fuko", 3988),
            ("Mangetsu", 4792),
            ("Mangetsu", 4792),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2
    
    @TestClass.is_a_test
    def test_rpr_aoe(self):
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
        base_plentiful = 40401        

        skills_and_expected_damages = (
            (
                "Plentiful Harvest",
                "t1, t2",
                SkillModifier(),
                (base_plentiful, 0.4*base_plentiful),
            ),
        )
        test_passed1, err_msg1 = self.__test_multi_target_skills(
            stats, skills_and_expected_damages
        )
        
        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Spinning Scythe", targets="t1, t2")
        rb.add(3, "Whorl of Death", targets="t1, t2")
        rb.add(6, "Spinning Scythe", targets="t1, t2, t3")
        rb.add(40, "Spinning Scythe", targets="t1, t2")
        
        expected = (
            ("Spinning Scythe", 6463),
            ("Spinning Scythe", 6463),
            ("Whorl of Death", 4043),
            ("Whorl of Death", 4043),
            ("Spinning Scythe", 7115),
            ("Spinning Scythe", 7115),
            ("Spinning Scythe", 6463), # target 3, no debuff
            ("Spinning Scythe", 6463), # death's design dropped off
            ("Spinning Scythe", 6463),
        )

        test_passed2, err_msg2 = self.__test_rotation_damage(rb, expected)
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2
    
    @TestClass.is_a_test
    def test_vpr_aoe(self):
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

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(0, "Uncoiled Twinfang", targets="t1")
        rb.add(3, "Uncoiled Fury", targets="t1, t2")
        rb.add(6, "Uncoiled Twinfang", targets="t1, t2")
        
        expected = (
            ("Uncoiled Twinfang", 4766),
            ("Uncoiled Fury", 27027),
            ("Uncoiled Fury", 27027),
            ("Uncoiled Twinfang", 6748),
            ("Uncoiled Twinfang", 3370),            
        )
        return self.__test_rotation_damage(rb, expected)        