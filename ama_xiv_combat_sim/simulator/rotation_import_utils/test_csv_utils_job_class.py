import os
from ama_xiv_combat_sim.simulator.rotation_import_utils.csv_utils import CSVUtils
from ama_xiv_combat_sim.simulator.skills.create_skill_library import (
    create_skill_library,
)
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import (
    RotationBuilder,
)

class TestCSVUtilsJobClass(TestClass):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.realpath(__file__))
        self.__skill_library = create_skill_library(version="7.3", level=100)

        self.__default_job_rb = RotationBuilder(
            None,
            self.__skill_library,
            ignore_trailing_dots=True,
            enable_autos=False,
            fight_start_time=0,
        )
        self.__test_bulk_job_filenames = {}
        for job, filename in {
            "SAM1": "test_sam1.csv",
            "SCH1": "test_sch1.csv",
            "DRG1": "test_drg1.csv",
            # tanks
            "WAR_buffs": "test_war_buffs.csv",
            "GNB_buffs": "test_gnb_buffs.csv",
            "PLD_buffs": "test_pld_buffs.csv",
            "DRK_buffs": "test_drk_buffs.csv",
            # healers
            "AST_buffs": "test_ast_buffs.csv",
            "SCH_buffs": "test_sch_buffs.csv",
            "WHM_buffs": "test_whm_buffs.csv",
            # melees
            "DRG_buffs": "test_drg_buffs.csv",
            "SAM_buffs": "test_sam_buffs.csv",
            "VPR_buffs": "test_vpr_buffs.csv",
            "RPR_buffs": "test_rpr_buffs.csv",
            "MNK_buffs": "test_mnk_buffs.csv",
            "NIN_buffs": "test_nin_buffs.csv",
            # caster
            "SMN_buffs": "test_smn_buffs.csv",
            "RDM_buffs": "test_rdm_buffs.csv",
            "PCT_buffs": "test_pct_buffs.csv",
            "BLM_buffs": "test_blm_buffs.csv",
            # ranged
            "MCH_buffs": "test_mch_buffs.csv",
            "DNC_buffs": "test_dnc_buffs.csv",
            "BRD_buffs": "test_brd_buffs.csv",
            "BRD_buffs2": "test_brd_buffs2.csv",
        }.items():
            self.__test_bulk_job_filenames[job] = os.path.join(
                base_dir, "test_class_csvs", filename
            )

    @staticmethod
    def __test_csv_job_class_helper(expected, actual_rbs, use_actual_rbs_strict=True):
        test_passed = True
        err_msg = ""

        if use_actual_rbs_strict and expected.keys() != actual_rbs.keys():
            test_passed = False
            err_msg = f"Did not get expected keys for rotations. Expected: {expected.keys()} vs. Acual: {actual_rbs.keys()}"

        results = {}
        for player_name, rb in actual_rbs.items():
            # just grab the fields we need for simplicty of testing
            results[player_name] = [x[0:3] for x in rb.get_timed_skills()]

        for player_name, expected_result in expected.items():
            is_passed, this_err_msg = TestCSVUtilsJobClass._compare_sequential(
                results[player_name], expected_result
            )
            test_passed &= is_passed
            err_msg += this_err_msg

        return test_passed, err_msg

    @TestClass.is_a_test
    def test_csv_sch(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "SCH1": self.__test_bulk_job_filenames["SCH_buffs"],
                "SAM1": self.__test_bulk_job_filenames["SAM1"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "SAM1": (
                (
                    0,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
                (
                    1200,
                    skill_library_to_use.get_skill("Chain Stratagem", "SCH"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
            ),
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    1200,
                    skill_library_to_use.get_skill("Chain Stratagem", "SCH"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
            "SCH1": (
                (
                    0,
                    skill_library_to_use.get_skill("Broil IV", "SCH"),
                    SkillModifier(),
                ),
                (
                    1200,
                    skill_library_to_use.get_skill("Chain Stratagem", "SCH"),
                    SkillModifier(),
                ),
            ),
        }
        return TestCSVUtilsJobClass.__test_csv_job_class_helper(expected, result_rbs)

    @TestClass.is_a_test
    def test_csv_ast(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "AST1": self.__test_bulk_job_filenames["AST_buffs"],
                "SAM1": self.__test_bulk_job_filenames["SAM1"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "SAM1": (
                (
                    0,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
                (
                    1200,
                    skill_library_to_use.get_skill("Divination", "AST"),
                    SkillModifier(),
                ),
                (
                    1500,
                    skill_library_to_use.get_skill("The Spear", "AST"),
                    SkillModifier(with_condition="Big"),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
            ),
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    1200,
                    skill_library_to_use.get_skill("Divination", "AST"),
                    SkillModifier(),
                ),
                (
                    1650,
                    skill_library_to_use.get_skill("The Balance", "AST"),
                    SkillModifier(with_condition="Small"),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
            "AST1": (
                (
                    0,
                    skill_library_to_use.get_skill("Fall Malefic", "AST"),
                    SkillModifier(),
                ),
                (
                    1200,
                    skill_library_to_use.get_skill("Divination", "AST"),
                    SkillModifier(),
                ),
                (
                    1500,
                    skill_library_to_use.get_skill("The Spear", "AST"),
                    SkillModifier(),
                ),
                (
                    1650,
                    skill_library_to_use.get_skill("The Balance", "AST"),
                    SkillModifier(),
                ),
            ),
        }
        return TestCSVUtilsJobClass.__test_csv_job_class_helper(expected, result_rbs)

    @TestClass.is_a_test
    def test_csv_drg(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "SCH1": self.__test_bulk_job_filenames["SCH1"],
                "SAM1": self.__test_bulk_job_filenames["SAM1"],
                "DRG1": self.__test_bulk_job_filenames["DRG_buffs"],
            },
        )

        expected = {
            "SAM1": (
                (
                    0,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
                (
                    1600,
                    skill_library_to_use.get_skill("Battle Litany", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
            ),
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    1000,
                    skill_library_to_use.get_skill("Life Surge", "DRG"),
                    SkillModifier(),
                ),
                (
                    1500,
                    skill_library_to_use.get_skill("Lance Charge", "DRG"),
                    SkillModifier(),
                ),
                (
                    1600,
                    skill_library_to_use.get_skill("Battle Litany", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
            "SCH1": (
                (
                    1600,
                    skill_library_to_use.get_skill("Battle Litany", "DRG"),
                    SkillModifier(),
                ),
                (
                    3000,
                    skill_library_to_use.get_skill("Broil IV", "SCH"),
                    SkillModifier(),
                ),
            ),
        }
        return TestCSVUtilsJobClass.__test_csv_job_class_helper(expected, result_rbs)

    @TestClass.is_a_test
    def test_csv_sam(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "SAM1": self.__test_bulk_job_filenames["SAM_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        # just make sure DRG1 does not have sam buffs
        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }
        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_vpr(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "VPR1": self.__test_bulk_job_filenames["VPR_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        # just make sure DRG1 does not have vpr buffs
        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }
        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_rpr(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "RPR1": self.__test_bulk_job_filenames["RPR_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        # make sure DRG gets RPR arcane circle buff
        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2500,
                    skill_library_to_use.get_skill("Arcane Circle", "RPR"),
                    SkillModifier(),
                ),
            ),
        }
        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_mnk(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "MNK1": self.__test_bulk_job_filenames["MNK_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2200,
                    skill_library_to_use.get_skill("Brotherhood", "MNK"),
                    SkillModifier(),
                ),
            ),
        }
        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_nin(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "NIN1": self.__test_bulk_job_filenames["NIN_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2200,
                    skill_library_to_use.get_skill("Dokumori", "NIN"),
                    SkillModifier(with_condition="Debuff Only"),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_smn(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "SMN1": self.__test_bulk_job_filenames["SMN_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2200,
                    skill_library_to_use.get_skill("Searing Light", "SMN"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_rdm(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "RDM1": self.__test_bulk_job_filenames["RDM_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2200,
                    skill_library_to_use.get_skill("Embolden", "RDM"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_blm(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "BLM": self.__test_bulk_job_filenames["BLM_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_pct(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "PCT1": self.__test_bulk_job_filenames["PCT_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2200,
                    skill_library_to_use.get_skill("Starry Muse", "PCT"),
                    SkillModifier(with_condition="Buff Only"),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_whm(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "WHM": self.__test_bulk_job_filenames["WHM_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_war(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "WAR": self.__test_bulk_job_filenames["WAR_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_gnb(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "GNB": self.__test_bulk_job_filenames["GNB_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_pld(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "PLD": self.__test_bulk_job_filenames["PLD_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_drk(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "DRK": self.__test_bulk_job_filenames["DRK_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_mch(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "MCH": self.__test_bulk_job_filenames["MCH_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_dnc(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "DNC": self.__test_bulk_job_filenames["DNC_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
                "SAM1": self.__test_bulk_job_filenames["SAM1"],
            },
        )

        expected = {
            "SAM1": (
                (
                    0,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("Gyofu", "SAM"),
                    SkillModifier(),
                ),
                (
                    2200,
                    skill_library_to_use.get_skill("Standard Finish", "DNC"),
                    SkillModifier("Buff Only"),
                ),
                (
                    3000,
                    skill_library_to_use.get_skill("Technical Finish", "DNC"),
                    SkillModifier("Buff Only"),
                ),
                (
                    3500,
                    skill_library_to_use.get_skill("Devilment", "DNC"),
                    SkillModifier(),
                ),
                (
                    4000,
                    skill_library_to_use.get_skill("Finishing Move", "DNC"),
                    SkillModifier("Buff Only"),
                ),
            ),
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    3000,
                    skill_library_to_use.get_skill("Technical Finish", "DNC"),
                    SkillModifier("Buff Only"),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_brd(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "BRD": self.__test_bulk_job_filenames["BRD_buffs"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2200,
                    skill_library_to_use.get_skill("Mage's Ballad", "BRD"),
                    SkillModifier("Buff Only"),
                ),
                (
                    2300,
                    skill_library_to_use.get_skill("Radiant Finale", "BRD"),
                    SkillModifier("1 Coda"),
                ),
                (
                    2500,
                    skill_library_to_use.get_skill("Army's Paeon", "BRD"),
                    SkillModifier("Buff Only"),
                ),
                (
                    3000,
                    skill_library_to_use.get_skill("Battle Voice", "BRD"),
                    SkillModifier(),
                ),
                (
                    3500,
                    skill_library_to_use.get_skill("The Wanderer's Minuet", "BRD"),
                    SkillModifier("Buff Only"),
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )

    @TestClass.is_a_test
    def test_csv_brd2(self):
        skill_library_to_use = self.__skill_library
        result_rbs, _ = CSVUtils.get_bulk_rotations_from_csv(
            self.__default_job_rb,
            {
                "BRD": self.__test_bulk_job_filenames["BRD_buffs2"],
                "DRG1": self.__test_bulk_job_filenames["DRG1"],
            },
        )

        expected = {
            "DRG1": (
                (
                    0,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2000,
                    skill_library_to_use.get_skill("True Thrust", "DRG"),
                    SkillModifier(),
                ),
                (
                    2300,
                    skill_library_to_use.get_skill("Radiant Finale", "BRD"),
                    SkillModifier("3 Coda"),  # hard override
                ),
                (
                    3000,
                    skill_library_to_use.get_skill("Battle Voice", "BRD"),
                    SkillModifier(),
                ),
                (
                    3800,
                    skill_library_to_use.get_skill("Radiant Finale", "BRD"),
                    SkillModifier("2 Coda"),  # computed
                ),
                (
                    4200,
                    skill_library_to_use.get_skill("Mage's Ballad", "BRD"),
                    SkillModifier("Buff Only"),
                ),
                (
                    4500,
                    skill_library_to_use.get_skill("Radiant Finale", "BRD"),
                    SkillModifier("1 Coda"),  # computed
                ),
            ),
        }

        return TestCSVUtilsJobClass.__test_csv_job_class_helper(
            expected, result_rbs, use_actual_rbs_strict=False
        )
