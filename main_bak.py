import copy
import matplotlib.pyplot as plt
import numpy as np
import time
import ama_xiv_combat_sim

from ama_xiv_combat_sim.example_rotations.get_example_rotations import (
    get_example_rotations,
)
from ama_xiv_combat_sim.kill_time_estimator.kill_time_estimator import KillTimeEstimator
from ama_xiv_combat_sim.simulator.skills import create_skill_library, SkillModifier
from ama_xiv_combat_sim.simulator.damage_simulator import DamageSimulator
from ama_xiv_combat_sim.simulator.timeline_builders.damage_builder import DamageBuilder
from ama_xiv_combat_sim.rotation_analysis.rotation_analysis_utils import (
    RotationAnalysisUtils,
)


class DisplayUtils:
    PERCENTILES_TO_USE = [1, 5, 25, 50, 75, 95, 99]
    COLOURS_TO_USE = [
        "black",
        "dimgray",
        "g",
        "b",
        (0.36, 0.28, 0.55),
        (1, 0.5, 0),
        (1, 0.0, 0.5),
    ]

    @staticmethod
    def print_button_press_timings(rb):
        print("---Times (in ms) when skills get used:---")
        for tmp in rb.get_button_press_timing():
            print("{:>8}: {:>22}".format(tmp[0], tmp[1]))
        print("\n")

    @staticmethod
    def print_damage_applications(per_skill_damage):
        print("---Times (in ms) when damage lands:---")
        for sk in per_skill_damage:
            print(
                "time: {:>8}, name: {:>22}, expected_damage: {:9.2f}, potency: {:4n}, skill modifier: {:>22}, damage variance: {:6.2f}".format(
                    sk.application_time,
                    sk.skill_name,
                    sk.expected_damage,
                    sk.potency,
                    ", ".join(sk.skill_modifier_condition),
                    sk.standard_deviation,
                )
            )

    @staticmethod
    def print_damage_details(
        per_skill_damage, damage_ranges, status_effect_names_only=True
    ):
        print("---Damage ranges and expectation:---")
        for i in range(0, len(damage_ranges)):
            sk = per_skill_damage[i]
            print(
                '{:5n}: {:<22}, Potency: {:4n}, Modifier: "{}". '.format(
                    sk.application_time,
                    damage_ranges[i][0],
                    sk.potency,
                    ", ".join(sk.skill_modifier_condition),
                )
            )
            buffs, debuffs = sk.status_effects[0], sk.status_effects[1]
            if status_effect_names_only:
                print("  Buffs: ||{}||".format(", ".join(buffs.status_effects)))
                print("  DeBuffs: ||{}||".format(", ".join(debuffs.status_effects)))
            else:
                print(
                    "  Buffs: ||{:>22}||  crit: {:3.2f}, dh: {:3.2f}, damage_mult: {:3.2f}, guaranteed crit/dh: {}/{}:".format(
                        ", ".join(buffs.status_effects),
                        buffs.crit_rate_add,
                        buffs.dh_rate_add,
                        buffs.damage_mult,
                        buffs.guaranteed_crit,
                        buffs.guaranteed_dh,
                    )
                )
                print(
                    "  Debuffs: ||{:>22}||  crit: {:3.2f}, dh: {:3.2f}, damage_mult: {:3.2f}, guaranteed crit/dh: {}/{}:".format(
                        ", ".join(debuffs.status_effects),
                        debuffs.crit_rate_add,
                        debuffs.dh_rate_add,
                        debuffs.damage_mult,
                        debuffs.guaranteed_crit,
                        debuffs.guaranteed_dh,
                    )
                )
            for tmp in damage_ranges[i][1:]:
                print(
                    "   {:>14} ({:5.1f}%). expected_damage: {:9.2f},   [low, high]: [{}, {}]".format(
                        tmp[0], 100 * tmp[3], (tmp[1] + tmp[2]) / 2, tmp[1], tmp[2]
                    )
                )

    @staticmethod
    def print_results(total_damage, title="Average Damage"):
        percs = np.percentile(total_damage, DisplayUtils.PERCENTILES_TO_USE)
        print("{}: {mean:.2f}".format(title, mean=np.mean(total_damage)))
        for i in range(0, len(DisplayUtils.PERCENTILES_TO_USE)):
            print(
                "Percentile {}: {percs:.2f}".format(
                    DisplayUtils.PERCENTILES_TO_USE[i], percs=percs[i]
                )
            )
        print()

    @staticmethod
    def display_results(
        total_damage, xlabel="DPS", title=None, display_cumulative=True
    ):
        percs = np.percentile(total_damage, DisplayUtils.PERCENTILES_TO_USE)

        try:
            count, bins_count = np.histogram(total_damage, bins=500)
        except ValueError:
            return

        plt.figure()
        pdf = count / sum(count)
        plt.plot(bins_count[1:], pdf)
        for i in range(len(percs)):
            plt.plot(
                [percs[i], percs[i]],
                [0, max(pdf)],
                color=DisplayUtils.COLOURS_TO_USE[i],
            )
        plt.ylabel("Probability")
        plt.xlabel(xlabel)
        if title is not None:
            plt.title(title)
        plt.show(block=False)

        if display_cumulative:
            plt.figure()
            plt.plot(bins_count[1:], np.cumsum(pdf))
            plt.ylabel("Cumulative Probability")
            plt.xlabel("{} <= Value".format(xlabel))
            if title is not None:
                plt.title(title)
            plt.show(block=False)

    @staticmethod
    def display_damage_over_time(damage, t, window_length, title_prefix="Damage done"):
        RESOLUTION = 10
        x = np.asarray(range(int(min(t)), int(max(t)), RESOLUTION))
        res = np.zeros((len(x), 1))
        t = np.asarray(t)
        damage = np.asarray(damage)

        for i in range(0, len(x)):
            time_to_use = x[i]
            idx = np.argwhere(
                (t >= time_to_use) & (t <= time_to_use + window_length * 1000)
            )[:, 0]
            res[i] = np.sum(damage[idx])

        plt.figure()
        plt.plot(x / 1000, res)
        plt.title("{} in a time window of {}s".format(title_prefix, window_length))
        plt.xlabel("Starting Time of Window")
        plt.ylabel("Average damage in time window")
        plt.show(block=False)
        return res

    @staticmethod
    def display_damage_snapshots_in_time_window(per_skill_damage, window_length):
        DisplayUtils.display_damage_over_time(
            [float(x.expected_damage) for x in per_skill_damage],
            [float(x.snapshot_time) for x in per_skill_damage],
            window_length,
            title_prefix="Snapshotted Damage Done",
        )

    @staticmethod
    def display_kill_time_estimates(kill_times):
        num_examples = len(kill_times)
        kill_time_success = list(filter(lambda x: x is not None, kill_times))
        num_kill_succeeded = len(kill_time_success)
        print("Num success: {}. Total: {}".format(num_kill_succeeded, num_examples))

        if num_kill_succeeded == 0:
            print("Boss cannot be killed with given rotations")
            return

        count, bins_count = np.histogram(kill_time_success, bins=500)
        plt.figure()
        pdf = (num_kill_succeeded / num_examples) * count / sum(count)
        plt.plot(bins_count[1:], pdf)
        plt.title("Kill time")
        plt.ylabel("Probability")
        plt.xlabel("Time")

        plt.figure()
        plt.plot(bins_count[1:], np.cumsum(pdf))
        plt.title("Probability of killing boss at time <= T")
        plt.xlabel("Time=T")
        plt.ylabel("Probability")


# @title Set up the simulation environment


# @title execute_rotation
def execute_rotation(rb, skill_library, num_samples=200000):
    stats = rb.get_stats()
    db = DamageBuilder(stats, skill_library)
    start = time.time()
    sim = DamageSimulator(
        stats, db.get_damage_instances(rb.get_skill_timing()), num_samples
    )
    end = time.time()
    print("Time taken: {}".format(end - start))
    dps = sim.get_dps()
    damage = sim.get_raw_damage()
    per_skill_damage = sim.get_per_skill_damage(rb)
    damage_ranges = sim.get_damage_ranges()
    t = sim.get_damage_time()
    return dps, damage, per_skill_damage, damage_ranges, t


SKILL_LIBRARY = create_skill_library()
ROTATION_LIBRARY = get_example_rotations(SKILL_LIBRARY)

# @title Example of executing a pre-set rotation
rotation_name = "WAR 6.55"
rotation_to_use = ROTATION_LIBRARY[rotation_name]
dps, damage, per_skill_damage, damage_ranges, t = execute_rotation(
    rotation_to_use, SKILL_LIBRARY, num_samples=100000
)

print("Results: ")

DisplayUtils.print_button_press_timings(rotation_to_use)
DisplayUtils.print_damage_applications(per_skill_damage)
DisplayUtils.print_damage_details(
    per_skill_damage, damage_ranges, status_effect_names_only=True
)

if len(per_skill_damage) > 0:
    DisplayUtils.display_damage_snapshots_in_time_window(
        per_skill_damage, window_length=15
    )
    DisplayUtils.display_results(
        dps,
        title="DPS over {} s".format(per_skill_damage[-1].application_time / 1000),
        display_cumulative=False,
    )

DisplayUtils.print_results(dps, title="Average DPS")
DisplayUtils.print_results(damage, title="Average Damage")

print("---Expected max damage over N runs---")
for num_runs in [1, 5, 10, 20, 50, 100]:
    print(
        "{} Runs: {:.2f}".format(
            num_runs,
            RotationAnalysisUtils.get_expected_max_in_k_runs(
                dps, num_runs, num_trials=10000
            ),
        )
    )

# @title Example of estimating kill time
boss_hp = 3700000
kte = KillTimeEstimator(boss_hp=boss_hp)
kte.add_rotation(ROTATION_LIBRARY["WAR 6.55 Party Buffs"])
kte.add_rotation(ROTATION_LIBRARY["DRK 6.55"])
kte.add_rotation(ROTATION_LIBRARY["SCH 6.55"])
kte.add_rotation(ROTATION_LIBRARY["WHM 6.55"])
kte.add_rotation(ROTATION_LIBRARY["RPR 6.55, Early Gluttony"])
kte.add_rotation(ROTATION_LIBRARY["SMN 6.55 Fast Garuda"])
kte.add_rotation(ROTATION_LIBRARY["MCH 6.55 Delayed Tools (Extended)"])

# Copy the rotation because we're about to change it (you don't need to do
# this if you're building the rotation specifically for this kill time
# estimation).
sam_rotation = copy.deepcopy(ROTATION_LIBRARY["SAM 6.55, 2.15 gcd"])
sam_rotation.add(
    25, "LB 3", skill_modifier=SkillModifier(with_condition="Mean Damage: 10000")
)
# Times are close, just for the sake of example of how to specify LB damage and type.
sam_rotation.add(
    26, "LB 1", skill_modifier=SkillModifier(with_condition="Exact Damage: 5000")
)
kte.add_rotation(sam_rotation)

kill_times, cumsum_damage, all_t = kte.estimate_kill_time(num_samples=100000)
DisplayUtils.display_kill_time_estimates(kill_times)
