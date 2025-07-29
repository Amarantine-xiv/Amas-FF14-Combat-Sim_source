import copy
import numpy as np
import math

from ama_xiv_combat_sim.simulator.sim_consts import SimConsts


class Utils:

    @staticmethod
    def get_greatest_val_less_than_query(vals, query_val):
        # Linear scan- we can change to BST later with some refactoring,
        # but vals really should only be a handful (<20) values so it
        # won't really matter.
        st = tuple(k for k in vals if k <= query_val)
        if len(st) == 0:
            raise ValueError(f"No values found for query val: {query_val}")
        return max(st)

    @staticmethod
    def get_greatest_dict_key_val_less_than_query(ex_dict, query_val):
        try:
            key_to_use = Utils.get_greatest_val_less_than_query(
                ex_dict.keys(), query_val
            )
        except ValueError:
            return None
        return ex_dict[key_to_use]

    @staticmethod
    def transform_time_to_prio(t):
        return int(1000 * t)

    @staticmethod
    def truncate_to_digit(x, digit_to_round_to):
        modifier = math.pow(10, digit_to_round_to - 1)
        return int(modifier * np.floor(x / modifier))

    @staticmethod
    def canonicalize_condition(condition):
        if len(condition) == 0:
            return set()
        tmp = [x.strip() for x in condition.split(",")]
        return set(tmp)

    @staticmethod
    def get_best_key(keys, with_condition):
        max_match = -1
        best_keys = []
        for key in keys:
            if len(key) < max_match:
                continue
            if key.issubset(with_condition):
                if max_match < len(with_condition):
                    max_match = len(key)
                    best_keys = [
                        key,
                    ]
                else:
                    best_keys.append(key)
        if len(best_keys) == 0:
            return frozenset([SimConsts.DEFAULT_CONDITION])

        assert (
            len(best_keys) == 1
        ), "Did not find exactly one match. matches:{}, Keys: {}, with_condition {}".format(
            best_keys, keys, with_condition
        )
        return best_keys[0]

    @staticmethod
    def get_positional_condition(skill, init_skill_modifier):
        damage_spec_to_use = None
        if isinstance(skill.damage_spec, dict):
            damage_spec_to_use = skill.damage_spec
        if damage_spec_to_use is None:
            if isinstance(skill.follow_up_skills, dict):
                follow_up_fakes_skill = {}
                for key, all_follow_ups in skill.follow_up_skills.items():
                    for follow_up in all_follow_ups:
                        if follow_up.skill.damage_spec is not None:
                            follow_up_fakes_skill[key] = follow_up.skill.damage_spec
                            break
                if len(follow_up_fakes_skill) > 0:
                    damage_spec_to_use = follow_up_fakes_skill
        if damage_spec_to_use is None:
            return ""

        # check if the damage spec even references a positional
        missed_positional_damage_spec = {
            condition: conditional_damage_spec
            for condition, conditional_damage_spec in damage_spec_to_use.items()
            if "No Positional" in condition
        }

        # If this ended up empty, just return
        if (
            not missed_positional_damage_spec
            or init_skill_modifier.bonus_percent is None
        ):
            return ",".join(init_skill_modifier.with_condition)

        skill_modifier = copy.deepcopy(init_skill_modifier)
        for condition_to_ignore in skill.ignored_conditions_for_bonus_potency:
            skill_modifier.remove_from_condition(condition_to_ignore)

        # We know the skill contains a positional now, so if we don't have a bonus percent
        # We know it's a missed positional
        if skill_modifier.bonus_percent == 0.0:
            new_condition = {*init_skill_modifier.with_condition, "No Positional"}
            # Return confirmed condition mixed in with the original, adding back ignored ones.
            return ",".join(new_condition)

        # assumes lowest potency is No Combo, No Positional. But we can search over the min key instead if this is untrue.
        skill_modifier_no_combo_no_pos = copy.deepcopy(skill_modifier).add_to_condition(
            "No Combo, No Positional"
        )
        min_potency_key = Utils.get_best_key(
            damage_spec_to_use.keys(), skill_modifier_no_combo_no_pos.with_condition
        )
        min_potency = damage_spec_to_use[min_potency_key].potency

        skill_modifier_no_combo_no_pos = copy.deepcopy(skill_modifier).add_to_condition(
            "No Combo, No Positional"
        )
        skill_modifier_no_combo = copy.deepcopy(skill_modifier).add_to_condition(
            "No Combo"
        )
        skill_modifier_no_pos = copy.deepcopy(skill_modifier).add_to_condition(
            "No Positional"
        )

        for to_try in [
            skill_modifier,
            skill_modifier_no_pos,
            skill_modifier_no_combo,
            skill_modifier_no_combo_no_pos,
        ]:
            potency_key = Utils.get_best_key(
                damage_spec_to_use.keys(), to_try.with_condition
            )
            potency = damage_spec_to_use[potency_key].potency
            if damage_spec_to_use[potency_key].use_min_potency:
                min_potency_to_use = damage_spec_to_use[potency_key].use_min_potency
            else:
                min_potency_to_use = min_potency
            potential_bonus_potency = int(
                100 * (potency - min_potency_to_use) / potency
            )
            if potential_bonus_potency == init_skill_modifier.bonus_percent:
                to_try.add_to_condition(",".join(init_skill_modifier.with_condition))
                return ", ".join(to_try.with_condition)

        print(f"Could not find match for skill {skill.name} with bonusPercent {init_skill_modifier.bonus_percent} and condition {init_skill_modifier.with_condition}. Please contact a dev.\n")
        return ", ".join(skill_modifier.with_condition)
        # raise ValueError(
        #     f"Could not find match for skill {skill.name} with bonusPercent {init_skill_modifier.bonus_percent} and condition {init_skill_modifier.with_condition}. Please contact a dev.\n"
        # )
