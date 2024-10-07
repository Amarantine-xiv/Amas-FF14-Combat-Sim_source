from ama_xiv_combat_sim.simulator.game_data.job_class_fns_data import (
    ALL_DATA as ALL_DATA,
)
from ama_xiv_combat_sim.simulator.utils import Utils


class JobClassFns:

    # See https://www.akhmorning.com/allagan-studies/modifiers/ . Each class' class num is its main attribute #.
    JOB_MODS = {
        "SCH": 115,
        "SGE": 115,
        "WHM": 115,
        "AST": 115,
        "WAR": 105,
        "DRK": 105,
        "PLD": 100,
        "GNB": 100,
        "SAM": 112,
        "DRG": 115,
        "RPR": 115,
        "MNK": 110,
        "NIN": 110,
        "VPR": 110,
        "DNC": 115,
        "MCH": 115,
        "BRD": 115,
        "RDM": 115,
        "SMN": 115,
        "BLM": 115,
        "PCT": 115,
    }

    USES_SKS = [
        "WAR",
        "DRK",
        "PLD",
        "GNB",
        "SAM",
        "DRG",
        "RPR",
        "MNK",
        "NIN",
        "VPR",
        "DNC",
        "MCH",
        "BRD",
    ]

    @staticmethod
    def compute_trait_damage_mult(job_class, version, level=100):
        job_to_trait_damage_mult = {
            "SCH": 1.30,
            "SGE": 1.30,
            "WHM": 1.30,
            "AST": 1.30,
            "RDM": 1.30,
            "SMN": 1.30,
            "BLM": 1.30,
            "PCT": 1.30,
            "DNC": 1.20,
            "BRD": 1.20,
            "MCH": 1.20,
        }
        if job_class in job_to_trait_damage_mult:
            return job_to_trait_damage_mult[job_class]
        return 1

    @staticmethod
    def compute_trait_haste_time_reduction(job_class, version, level=100):
        job_to_trait_haste_time_reduction = (
            Utils.get_greatest_dict_key_val_less_than_query(
                ALL_DATA["haste_time_reduction"][level], version
            )
        )        
        if (
            job_to_trait_haste_time_reduction is not None
            and job_class in job_to_trait_haste_time_reduction
        ):
            return job_to_trait_haste_time_reduction[job_class]
        return 0

    @staticmethod
    def compute_trait_auto_attack_delay_reduction(job_class, version, level=100):
        job_to_trait_auto_attack_delay_reduction = (
            Utils.get_greatest_dict_key_val_less_than_query(
                ALL_DATA["auto_attack_delay_reduction"][level], version
            )
        )

        if (
            job_to_trait_auto_attack_delay_reduction is not None
            and job_class in job_to_trait_auto_attack_delay_reduction
        ):
            return job_to_trait_auto_attack_delay_reduction[job_class]
        return 0

    @staticmethod
    def isTank(job_class):
        return job_class in ["GNB", "WAR", "PLD", "DRK"]

    @staticmethod
    def isHealer(job_class):
        return job_class in ["SCH", "WHM", "AST", "SGE"]

    @staticmethod
    def isMelee(job_class):
        return job_class in ["MNK", "DRG", "SAM", "NIN", "RPR", "VPR"]

    @staticmethod
    def isCaster(job_class):
        return job_class in ["RDM", "BLM", "SMN", "PCT"]

    @staticmethod
    def isPhysRanged(job_class):
        return job_class in ["DNC", "BRD", "MCH"]
