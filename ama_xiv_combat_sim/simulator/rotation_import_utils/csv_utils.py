import ast
import pandas as pd  # i need to get rid of this...
import re

from collections import namedtuple
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier


class RotationCSV(
    namedtuple(
        "RotationCSV", ["t", "skill_name", "job_class", "skill_conditional", "targets"]
    )
):
    pass


class CSVUtils:

    @staticmethod
    def read_meta_fields(f):
        meta_fields = ["use_strict_skill_naming", "downtime_windows"]

        res = {}
        skiprows = 0
        with open(f, "r") as file:
            for line in file:
                line = line.lower()
                # Check if these are our rotation columns
                if "time" in line and "skill_name" in line:
                    break
                skiprows += 1
                line = line.replace(' ', '')
                for field in meta_fields:
                    val = re.search(rf"^#{field}=(.*?),*$", line)                    

                    if val is None:
                        continue
                    if field in res:
                        raise RuntimeError(f"Field defined multiple times: {field}")
                    res[field] = val.groups()[0]
        return res, skiprows

    @staticmethod
    def read_rotation_from_csv(filename, skiprows=None):
        res = []

        if skiprows is None:
            skiprows = 0
            with open(filename, "r") as file:
                for line in file:
                    # Print each line
                    if "time" in line and "skill_name" in line:
                        break
                    skiprows += 1
        try:
            df = pd.read_csv(filename, keep_default_na=False, skiprows=skiprows)

            # canonicalize column names
            df = df.rename(str.lower, axis="columns")
        except FileNotFoundError:
            print(f"File {filename} was not found.")
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
    def __def_process_metafields(rb, meta_fields):
        # process metafields
        if "use_strict_skill_naming" in meta_fields:
            if meta_fields["use_strict_skill_naming"] in ["True", "true"]:
                use_strict_skill_naming = True
            elif meta_fields["use_strict_skill_naming"] in ["False", "false"]:
                use_strict_skill_naming = False
            else:
                raise RuntimeError(
                    f"Bad value for use_strict_skill_naming: {meta_fields['use_strict_skill_naming']}"
                )            
            rb.set_use_strict_skill_naming(use_strict_skill_naming)
        if "downtime_windows" in meta_fields:
            downtime_windows = meta_fields["downtime_windows"].replace("\\", "")
            downtime_windows = tuple(ast.literal_eval(downtime_windows))
            rb.set_downtime_windows(downtime_windows)
        return rb

    @staticmethod
    def populate_rotation_from_csv(rb, filename):
        meta_fields, skiprows = CSVUtils.read_meta_fields(filename)
        rb = CSVUtils.__def_process_metafields(rb, meta_fields)

        all_skills = CSVUtils.read_rotation_from_csv(filename, skiprows)
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
                targets=sk.targets,
            )

        return rb, all_skills
