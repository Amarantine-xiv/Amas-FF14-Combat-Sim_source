import copy
import math
import numpy as np
import time

from collections import namedtuple
from ama_xiv_combat_sim.simulator.calcs.compute_damage_utils import ComputeDamageUtils
from ama_xiv_combat_sim.simulator.trackers.damage_tracker import DamageTracker


class PerInstanceDamage(
    namedtuple(
        "PerInstanceDamage",
        [
            "application_time",
            "snapshot_time",
            "skill_name",
            "potency",
            "skill_modifier_condition",
            "status_effects",
            "expected_damage",
            "standard_deviation",
            "event_id",
            "target",
            "damage_class",
        ],
    )
):
    pass


class DamageSimulator:
    def __init__(
        self, stats, dmg_instances, num_samples, verbose=False, save_damage_matrix=False, save_crit_dh_status = False,
    ):
        self.__dmg_instances = copy.deepcopy(dmg_instances)
        # defensively sort
        self.__dmg_instances.sort(key=lambda x: x[0])
        self.__stats = stats
        self.__damage_tracker = DamageTracker()
        start_time = time.time()
        self.__damage_matrix = None

        self.__compile_damage(num_samples, save_damage_matrix, save_crit_dh_status)
        end_time = time.time()
        if verbose:
            print(f"Simulation time took: {end_time - start_time}")

    # dmg_instances is a list in format: # (current_time, skill, (buffs, debuffs), event_id)
    def __compile_damage(self, num_samples, save_damage_matrix=False, save_crit_dh_status=False):
        self.__target = [0] * len(self.__dmg_instances)
        i = 0
        for (
            t,
            skill,
            skill_modifier,
            status_effects,
            _,
            target,
        ) in self.__dmg_instances:
            base_damage = ComputeDamageUtils.get_base_damage(
                skill, skill_modifier, self.__stats, status_effects
            )
            assert base_damage is not None, "base_damage should not be None."

            (dh_rate, crit_rate, crit_bonus) = (
                ComputeDamageUtils.compute_crit_rates_and_bonuses(
                    self.__stats, skill, skill_modifier, status_effects
                )
            )
            damage_mult = ComputeDamageUtils.compute_damage_mult(status_effects)

            damage_spec = skill.get_damage_spec(skill_modifier)
            single_damage_mult = damage_spec.single_damage_mult #things like AF/UI
            damage_class = damage_spec.damage_class
            trait_damage_mult = (
                self.__stats.processed_stats.trait_damage_mult
                if damage_spec.trait_damage_mult_override is None
                else damage_spec.trait_damage_mult_override
            )

            self.__damage_tracker.add_damage(
                base_damage,
                crit_rate,
                crit_bonus,
                dh_rate,
                trait_damage_mult,
                single_damage_mult,
                damage_mult,
                t,
                damage_spec.potency,
                skill_modifier,
                (status_effects[0], status_effects[1]),
                damage_class,
            )
            self.__target[i] = target
            i += 1

        self.__damage_tracker.finalize()

        if len(self.__dmg_instances) == 0:
            fight_time = 0
        else:
            fight_time = (
                self.__dmg_instances[-1][0] - self.__dmg_instances[0][0]
            ) / 1000  # convert to s
        self.__event_ids = tuple(x[4] for x in self.__dmg_instances)

        expected_mean, expected_variance = self.__get_expected_damage_and_variance_per_damage_instance()
        self.__per_skill_damage_mean = expected_mean
        self.__per_skill_damage_std = list(np.sqrt(expected_variance))
        
        if save_crit_dh_status:
            damage_matrix, crit_status, dh_status = self.__damage_tracker.compute_damage(num_samples)        
            self.__crit_status = crit_status
            self.__dh_status = dh_status
        else:
            damage_matrix, _, _ = self.__damage_tracker.compute_damage(num_samples)        
        
        if save_damage_matrix:
            self.__damage_matrix = damage_matrix
        
        self.__sampled_damage = np.sum(damage_matrix, axis=0)
        self.__sampled_dps = (
            self.__sampled_damage / fight_time
            if fight_time > 0
            else np.full(self.__sampled_damage.shape, math.inf)
        )

    @staticmethod
    def __add_damage_snapshots(per_skill_damage, rb):
        rot = rb.get_skill_timing().get_q()
        event_id_to_snapshot_time = {}
        for x in rot:
            event_id, snapshot_time, skill_name = (
                x.event_id,
                x.event_times.primary,
                x.skill.name,
            )
            event_id_to_snapshot_time[event_id] = (snapshot_time, skill_name)

        for i, curr_per_skill_damage in enumerate(per_skill_damage):            
            event_id = curr_per_skill_damage.event_id
            skill_name = curr_per_skill_damage.skill_name
            assert (
                event_id in event_id_to_snapshot_time.keys()
            ), f"Unknown event_id found: {event_id}"
            assert (
                skill_name == event_id_to_snapshot_time[event_id][1]
            ), f"Skill names did not match on event id: {event_id}. rotation name: {event_id_to_snapshot_time[event_id][1]}, per_skill_damage name: {skill_name}"
            per_skill_damage[i] = curr_per_skill_damage._replace(
                snapshot_time=event_id_to_snapshot_time[event_id][0]
            )
        return per_skill_damage

    def get_event_ids(self):
        return self.__event_ids

    def get_crit_and_dh_rates(self):
        return self.__damage_tracker.get_crit_and_dh_rates()

    def get_trait_damage_mult(self):
        return self.__damage_tracker.get_trait_damage_mult()

    def get_raw_damage(self):
        return self.__sampled_damage

    def get_dps(self):
        return self.__sampled_dps

    def get_damage_time(self):
        return self.__damage_tracker.time

    def get_damage_matrix(self):
        return self.__damage_matrix
    
    def get_crit_status(self):
        return self.__crit_status

    def get_dh_status(self):
        return self.__dh_status

    def get_damage_ranges(self):
        skill_names = [x[1].name for x in self.__dmg_instances]
        damage_ranges = self.__damage_tracker.get_damage_ranges_and_probabilities()
        res = [
            (
                skill_names[i],
                damage_ranges[i][0],
                damage_ranges[i][1],
                damage_ranges[i][2],
                damage_ranges[i][3],
            )
            for i in range(0, len(skill_names))
        ]
        return res

    def __get_expected_damage_and_variance_per_damage_instance(self):
        def get_all_probs(x):
            return list(x[i][3] for i in range(0, len(x)))
        def get_all_sums(x):
            return list(x[i][1] + x[i][2] for i in range(0, len(x)))
        def get_all_diffs(x):
            return list(x[i][2] - x[i][1] for i in range(0, len(x)))  
        
        #damage_ranges[i]: (string to identify crit/dh status, low damage, high damage, probability)
        damage_ranges = self.__damage_tracker.get_damage_ranges_and_probabilities()

        all_probs = np.asarray(
            list(get_all_probs(damage_ranges[i]) for i in range(0, len(damage_ranges)))
        )
        all_means = np.asarray(
            list(get_all_sums(damage_ranges[i]) for i in range(0, len(damage_ranges)))
        )/2
        all_diffs = np.asarray(
            list(get_all_diffs(damage_ranges[i]) for i in range(0, len(damage_ranges)))
        )
        
        expected_damage = np.sum(all_probs * all_means, axis=1)
        
        # See: law of total variance, variance of a uniform
        unexplained_variances = np.sum(all_probs * np.power(all_diffs, 2), axis=1)/12
        explained_variances = np.sum(all_probs*np.power(all_means, 2), axis=1) - np.power(np.sum(all_probs*all_means,axis=1), 2)
        variances = unexplained_variances + explained_variances
    
        return list(expected_damage), list(variances)

    def get_expected_damage_per_damage_instance(self):        
        return self.__per_skill_damage_mean

    def get_variance_per_damage_instance(self):
        return np.power(self.__per_skill_damage_std, 2)

    def get_expected_damage(self):        
        return np.sum(self.get_expected_damage_per_damage_instance())
        
    def get_damage_variance(self):        
        return np.sum(self.get_variance_per_damage_instance())

    def get_per_skill_damage(self, rb=None):
        t = self.__damage_tracker.time
        potencies = self.__damage_tracker.potency
        status_effects = self.__damage_tracker.status_effects
        skill_modifier_condition = self.__damage_tracker.skill_modifier_condition
        skill_names = [x[1].name for x in self.__dmg_instances]
        damage_classes = [x for x in self.__damage_tracker.damage_classes]
        res = [
            PerInstanceDamage(
                t[i],
                None,  # Snapshot time- not known yet. Sus implementation.
                skill_names[i],
                potencies[i],
                skill_modifier_condition[i],
                status_effects[i],
                self.__per_skill_damage_mean[i],
                self.__per_skill_damage_std[i],
                self.__event_ids[i],
                self.__target[i],
                damage_classes[i],
            )
            for i in range(
                0,
                len(t),
            )
        ]
        if rb is not None:
            res = self.__add_damage_snapshots(res, rb)
        return res
