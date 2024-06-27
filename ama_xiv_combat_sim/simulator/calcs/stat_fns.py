import numpy as np
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts


class StatFns:
    @staticmethod
    def get_time_using_speed_stat(t_ms, speed_stat, version, level=90):
        level_sub = GameConsts.get_level_sub(version, level)
        level_div = GameConsts.get_level_div(version, level)

        tmp = np.ceil(130 * (level_sub - speed_stat) / level_div)
        tmp2 = t_ms * (1000 + tmp) / 10000
        tmp3 = np.floor(tmp2) / 100
        return int(1000 * tmp3)

    @staticmethod
    def get_crit_stats(crit_stat, version, level=90):
        level_sub = GameConsts.get_level_sub(version, level)
        level_div = GameConsts.get_level_div(version, level)

        crit_rate = (np.floor(200 * (crit_stat - level_sub) / level_div) + 50) / 1000
        crit_bonus = (np.floor(200 * (crit_stat - level_sub) / level_div) + 400) / 1000
        return crit_rate, crit_bonus

    @staticmethod
    def get_dh_rate(dh_stat, version, level=90):
        level_sub = GameConsts.get_level_sub(version, level)
        level_div = GameConsts.get_level_div(version, level)
        return np.floor(550 * (dh_stat - level_sub) / level_div) / 1000

    @staticmethod
    # from Hint's repo, https://github.com/hintxiv/reassemble
    def fWD(wd, job_mod, version, level=90):
        level_main = GameConsts.get_level_main(version, level)
        return np.floor(level_main * job_mod / 1000 + wd)

    @staticmethod
    # from Hint's repo, https://github.com/hintxiv/reassemble
    def fSpd(speed_stat, version, level=90):
        level_sub = GameConsts.get_level_sub(version, level)
        level_div = GameConsts.get_level_div(version, level)
        return np.floor(130 * (speed_stat - level_sub) / level_div + 1000)

    @staticmethod
    def fTnc(tenacity, version, level=90):
        level_sub = GameConsts.get_level_sub(version, level)
        level_div = GameConsts.get_level_div(version, level)
        return np.floor(100 * (tenacity - level_sub) / level_div) + 1000

    @staticmethod
    # from Hint's repo, https://github.com/hintxiv/reassemble
    def fAP(main_stat, is_tank, version, level=90):
        level_main = GameConsts.get_level_main(version, level)
        if is_tank:
            return (
                np.floor(
                    GameConsts.get_fAP_tank(version, level)
                    * (main_stat - level_main)
                    / level_main
                )
                + 100
            )
        return (
            np.floor(
                GameConsts.get_fAP(version, level)
                * (main_stat - level_main)
                / level_main
            )
            + 100
        )

    @staticmethod
    # from Hint's repo, https://github.com/hintxiv/reassemble
    def fDet(det_stat, version, level=90):
        level_main = GameConsts.get_level_main(version, level)
        level_div = GameConsts.get_level_div(version, level)

        return np.floor(140 * (det_stat - level_main) / level_div) + 1000

    # Used for auto dh
    @staticmethod
    def fDetDH(det_stat, dh_stat, version, level=90):
        level_sub = GameConsts.get_level_sub(version, level)
        level_div = GameConsts.get_level_div(version, level)
        return StatFns.fDet(det_stat, version, level) + np.floor(
            140 * (dh_stat - level_sub) / level_div
        )

    @staticmethod
    def fAuto(wd, weapon_delay, job_mod, version, level=90):
        level_main = GameConsts.get_level_main(version, level)
        return np.floor(np.floor(level_main * job_mod / 1000 + wd) * (weapon_delay / 3))
