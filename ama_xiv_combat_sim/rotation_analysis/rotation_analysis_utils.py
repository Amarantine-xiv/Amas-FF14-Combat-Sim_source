import numpy as np


class RotationAnalysisUtils:
    @staticmethod
    def get_expected_max_in_k_runs(x, k, num_trials=10000):
        res = np.zeros((num_trials, 1))
        for i in range(0, num_trials):
            res[i] = np.max(np.random.choice(x, k))
        return np.mean(res)

    @staticmethod
    def get_all_damage_snapshots_before_timestamp(per_skill_damage, timestamp_in_s):
        timestamp = 1000 * timestamp_in_s
        res = 0
        for sk in per_skill_damage:
            if sk.snapshot_time <= timestamp:
                res += sk.expected_damage
        return res

    @staticmethod
    def get_dps_at_intervals(per_skill_damage, interval_in_s):
        max_t = -1
        for sk in per_skill_damage:
            if sk.snapshot_time > max_t:
                max_t = sk.snapshot_time

        res = {'snapshot_time': [],     
               'total_snapshotted_damage': []}
        timestamps = list(range(interval_in_s, int(np.ceil(max_t / 1000)), interval_in_s))
        timestamps.append(max_t/1000)
        for t in timestamps:
            tot_damage = (
                RotationAnalysisUtils.get_all_damage_snapshots_before_timestamp(
                    per_skill_damage, t
                )
            )
            res['snapshot_time'].append(t)            
            res['total_snapshotted_damage'].append(round(tot_damage,2))
        return res
