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


class TestJobsMultiUnified72(TestClass):
    def __init__(self):
        super().__init__()

        self.__version = "7.2"
        self.__level = 100
        self.__skill_library = create_skill_library(
            version=self.__version, level=self.__level
        )
        self.__job_class_tester = JobClassTesterUtil(self.__skill_library)

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
            version=self.__version,
            level=self.__level,
        )
        base_oracle = 42847
        skills_and_expected_damages = (
            (
                "Oracle",
                "t1, t2, t3",
                SkillModifier(),
                (base_oracle, 0.5 * base_oracle, 0.5 * base_oracle),
            ),
        )
        return self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )

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
            version=self.__version,
            level=self.__level,
        )
        base_confiteor = 12753
        base_blade_of_faith = 6631
        base_blade_of_truth = 9692
        base_blade_of_valor = 12753
        base_blade_of_honor = 25510
        base_imperator = 14794
        skills_and_expected_damages = (
            (
                "Confiteor",
                "t1, t2, t3",
                SkillModifier(),
                (base_confiteor, 0.4 * base_confiteor, 0.4 * base_confiteor),
            ),
            (
                "Blade of Faith",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_blade_of_faith,
                    0.4 * base_blade_of_faith,
                    0.4 * base_blade_of_faith,
                ),
            ),
            (
                "Blade of Truth",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_blade_of_truth,
                    0.4 * base_blade_of_truth,
                    0.4 * base_blade_of_truth,
                ),
            ),
            (
                "Blade of Valor",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_blade_of_valor,
                    0.4 * base_blade_of_valor,
                    0.4 * base_blade_of_valor,
                ),
            ),
            (
                "Blade of Honor",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_blade_of_honor,
                    0.4 * base_blade_of_honor,
                    0.4 * base_blade_of_honor,
                ),
            ),
            (
                "Imperator",
                "t1, t2, t3",
                SkillModifier(),
                (base_imperator, 0.4 * base_imperator, 0.4 * base_imperator),
            ),
        )

        return self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )

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
            version=self.__version,
            level=self.__level,
        )

        base_disesteem = 25636
        base_salt_and_darkness = 12840
        skills_and_expected_damages = (
            (
                "Disesteem",
                "t1, t2, t3",
                SkillModifier(),
                (base_disesteem, 0.75 * base_disesteem, 0.75 * base_disesteem),
            ),
            (
                "Salt and Darkness",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_salt_and_darkness,
                    0.75 * base_salt_and_darkness,
                    0.75 * base_salt_and_darkness,
                ),
            ),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)
        rb.add(200, "Living Shadow", skill_modifier=SkillModifier(), targets="t1, t2")

        expected = (
            # living shadow. only 2 of these cleave.
            ("Abyssal Drain (pet)", 12298),
            ("Shadowbringer (pet)", 16690),
            ("Shadowbringer (pet)", 12509),
            ("Edge of Shadow (pet)", 12297),
            ("Bloodspiller (pet)", 12302),
            ("Disesteem (pet)", 18151),
            ("Disesteem (pet)", 13608),
        )

        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb, expected
        )
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
            version=self.__version,
            level=self.__level,
        )
        base_primal_rend = 31575
        base_primal_wrath = 18032
        base_primal_ruination = 35064

        skills_and_expected_damages = (
            (
                "Primal Rend",
                "t1, t2, t3",
                SkillModifier(),
                (base_primal_rend, 0.5 * base_primal_rend, 0.5 * base_primal_rend),
            ),
            (
                "Primal Wrath",
                "t1, t2, t3",
                SkillModifier(),
                (base_primal_wrath, 0.5 * base_primal_wrath, 0.5 * base_primal_wrath),
            ),
            (
                "Primal Ruination",
                "t1, t2, t3",
                SkillModifier(),
                (
                    base_primal_ruination,
                    0.5 * base_primal_ruination,
                    0.5 * base_primal_ruination,
                ),
            ),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )

        rb = RotationBuilder(stats, self.__skill_library)

        rb.add(0, "Heavy Swing", skill_modifier=SkillModifier(), targets="t2")
        rb.add(3, "Mythril Tempest", skill_modifier=SkillModifier(), targets="t2")
        rb.add(6, "Overpower", skill_modifier=SkillModifier(), targets="t1")
        rb.add(9, "Mythril Tempest", skill_modifier=SkillModifier(), targets="t1, t2")
        rb.add(23, "Heavy Swing", skill_modifier=SkillModifier(), targets="t1")
        rb.add(43, "Heavy Swing", skill_modifier=SkillModifier(), targets="t2")

        expected = (
            ("Heavy Swing", 6186),
            ("Mythril Tempest", 2576),
            ("Overpower", 2834),
            ("Mythril Tempest", 3608),
            ("Mythril Tempest", 3608),
            ("Heavy Swing", 6805),
            # Surging tempest should've worn off by now
            ("Heavy Swing", 6186),
        )

        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb, expected
        )
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

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
            version=self.__version,
            level=self.__level,
        )
        pitch_perfect_base = 17408
        resonant_arrow_base = 29018

        skills_and_expected_damages = (
            (
                "Pitch Perfect",
                "t1, t2, t3",
                SkillModifier(),
                (
                    pitch_perfect_base,
                    0.45 * pitch_perfect_base,
                    0.45 * pitch_perfect_base,
                ),
            ),
            (
                "Resonant Arrow",
                "t1, t2, t3",
                SkillModifier(),
                (
                    resonant_arrow_base,
                    0.45 * resonant_arrow_base,
                    0.45 * resonant_arrow_base,
                ),
            ),
        )
        return self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )

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
            version=self.__version,
            level=self.__level,
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
        rb.add(103, "Standard Finish", skill_modifier=SkillModifier(), targets="t2, t1")
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
            ("Double Standard Finish", 16498),
            ("Cascade", 11195),
            #
            ("Cascade", 10671),
            ("Double Standard Finish", 41240),
            ("Double Standard Finish", 16498),
            ("Cascade", 11195),
            #
            ("Cascade", 10678),
            ("Quadruple Technical Finish", 63075),
            ("Quadruple Technical Finish", 25231),
            ("Cascade", 11220),
            #
            ("Cascade", 10670),
            ("Quadruple Technical Finish", 63075),
            ("Quadruple Technical Finish", 25231),
            ("Cascade", 11200),
        )

        return self.__job_class_tester.test_rotation_damage(rb, expected)

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
            version=self.__version,
            level=self.__level,
        )
        base_phantom = 21794

        skills_and_expected_damages = (
            (
                "Phantom Kamaitachi",
                "t1, t2, t3",
                SkillModifier(),
                (base_phantom, 0.75 * base_phantom, 0.75 * base_phantom),
            ),
        )
        test_passed1, err_msg1 = self.__job_class_tester.test_multi_target_skills(
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
            ("Hakke Mujinsatsu", 4757),
            ("Hakke Mujinsatsu", 4757),
            #
            ("Death Blossom", 3967),
            #
            ("Kunai's Bane", 23820),
            ("Kunai's Bane", 0.75 * 23820),
            ("Spinning Edge", 13076),
            ("Spinning Edge", 13076),
            ("Spinning Edge", 11906),
        )

        test_passed2, err_msg2 = self.__job_class_tester.test_rotation_damage(
            rb, expected
        )
        return test_passed1 and test_passed2, err_msg1 + "\n" + err_msg2

    @TestClass.is_a_test
    def test_pct_aoe(self):
        stats = Stats(
            wd=132,
            weapon_delay=3.44,
            main_stat=3379,
            det_stat=1601,
            crit_stat=2514,
            dh_stat=1708,
            speed_stat=502,
            job_class="PCT",
            healer_or_caster_strength=214,
            version=self.__version,
            level=self.__level,
        )
        mog_of_the_ages_base = 52368
        pom_muse_base = 41895
        winged_muse_base = 41895
        holy_in_white_base = 31420
        hammer_brush_base = 47388
        polishing_hammer_base = 51046
        comet_in_black_base = 51303
        clawed_muse_base = 41895
        fanged_muse_base = 41895
        madeen_base = 57604
        star_prism_base = 57604

        skills_and_expected_damages = (
            (
                "Mog of the Ages",
                "t1, t2, t3",
                SkillModifier(),
                (
                    mog_of_the_ages_base,
                    0.3 * mog_of_the_ages_base,
                    0.3 * mog_of_the_ages_base,
                ),
            ),
            (
                "Pom Muse",
                "t1, t2, t3",
                SkillModifier(),
                (pom_muse_base, 0.3 * pom_muse_base, 0.3 * pom_muse_base),
            ),
            (
                "Winged Muse",
                "t1, t2, t3",
                SkillModifier(),
                (winged_muse_base, 0.3 * winged_muse_base, 0.3 * winged_muse_base),
            ),
            (
                "Holy in White",
                "t1, t2, t3",
                SkillModifier(),
                (
                    holy_in_white_base,
                    0.35 * holy_in_white_base,
                    0.35 * holy_in_white_base,
                ),
            ),
            (
                "Hammer Brush",
                "t1, t2, t3",
                SkillModifier(),
                (hammer_brush_base, 0.3 * hammer_brush_base, 0.3 * hammer_brush_base),
            ),
            (
                "Polishing Hammer",
                "t1, t2, t3",
                SkillModifier(),
                (
                    polishing_hammer_base,
                    0.3 * polishing_hammer_base,
                    0.3 * polishing_hammer_base,
                ),
            ),
            (
                "Comet in Black",
                "t1, t2, t3",
                SkillModifier(),
                (
                    comet_in_black_base,
                    0.35 * comet_in_black_base,
                    0.35 * comet_in_black_base,
                ),
            ),
            (
                "Clawed Muse",
                "t1, t2, t3",
                SkillModifier(),
                (clawed_muse_base, 0.3 * clawed_muse_base, 0.3 * clawed_muse_base),
            ),
            (
                "Fanged Muse",
                "t1, t2, t3",
                SkillModifier(),
                (fanged_muse_base, 0.3 * fanged_muse_base, 0.3 * fanged_muse_base),
            ),
            (
                "Retribution of the Madeen",
                "t1, t2, t3",
                SkillModifier(),
                (madeen_base, 0.3 * madeen_base, 0.3 * madeen_base),
            ),
            (
                "Star Prism",
                "t1, t2, t3",
                SkillModifier(),
                (star_prism_base, 0.3 * star_prism_base, 0.3 * star_prism_base),
            ),
        )
        return self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )

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
            version=self.__version,
            level=self.__level,
        )
        base_harvest_moon = 32350
        base_plentiful = 40401
        base_communio = 44481
        base_sacrificum = 24262
        base_perfectio = 52570

        skills_and_expected_damages = (
            (
                "Harvest Moon",
                "t1, t2",
                SkillModifier(),
                (base_harvest_moon, 0.6 * base_harvest_moon),
            ),
            (
                "Plentiful Harvest",
                "t1, t2",
                SkillModifier(),
                (base_plentiful, 0.6 * base_plentiful),
            ),
            (
                "Communio",
                "t1, t2",
                SkillModifier(),
                (base_communio, 0.6 * base_communio),
            ),
            (
                "Sacrificium",
                "t1, t2",
                SkillModifier(),
                (base_sacrificum, 0.6 * base_sacrificum),
            ),
            (
                "Perfectio",
                "t1, t2",
                SkillModifier(),
                (base_perfectio, 0.6 * base_perfectio),
            ),
        )
        return self.__job_class_tester.test_multi_target_skills(
            stats, skills_and_expected_damages
        )
