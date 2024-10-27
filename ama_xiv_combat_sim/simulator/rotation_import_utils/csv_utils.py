import pandas as pd  # i need to get rid of this...

from collections import namedtuple
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier


class RotationCSV(
    namedtuple("RotationCSV", ["t", "skill_name", "job_class", "skill_conditional", "targets"])
):
    pass


class CSVUtils:
    @staticmethod
    def read_rotation_from_csv(filename):
        res = []

        try:
            df = pd.read_csv(filename, keep_default_na=False)
            
            #canonicalize column names
            df=df.rename(str.lower, axis='columns')
        except FileNotFoundError:
            print(
                f"File {filename} was not found."
            )
            return res

        for i in range(0, len(df)):
            t = df["time"][i]
            skill_name = df["skill_name"][i]
            job_class = None if df["job_class"][i] == "" else df["job_class"][i]
            skill_conditional = df["skill_conditional"][i]
            targets = (
                None
                if "targets" not in df or df["targets"][i] == ""
                else df["targets"][i]
            )

            res.append(
                RotationCSV(t, skill_name, job_class, skill_conditional, targets)
            )
        return res

    @staticmethod
    def populate_rotation_from_csv(rb, filename):
        all_skills = CSVUtils.read_rotation_from_csv(filename)
        for sk in all_skills:
            if sk.skill_conditional is None or sk.skill_conditional == "":
                skill_modifier = None
            else:
                skill_modifier = SkillModifier(with_condition=sk.skill_conditional)
            rb.add(
                sk.t,
                sk.skill_name,
                skill_modifier=skill_modifier,
                job_class=sk.job_class,
                targets=sk.targets
            )
        return rb, all_skills
