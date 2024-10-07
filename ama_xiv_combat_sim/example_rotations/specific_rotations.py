from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts
from ama_xiv_combat_sim.simulator.stats import Stats


class SpecificRotations:
    def __init__(self):
        self.rotations = {}
        self.version = None
        self.level = -1

    def set_version(self, version):
        self.version = version

    def set_level(self, level):
        self.level = level

    def add_rotation_data(self, rotation_key, vals):
        assert (
            rotation_key not in self.rotations
        ), f"Rotation already exists: {rotation_key}"
        self.rotations[rotation_key] = vals

    def get_rotation_data(self, rotation_key, param_name):
        assert (
            rotation_key in self.rotations
        ), f"Rotation does not exist: {rotation_key}"        

        if self.level not in self.rotations[rotation_key]:
            return None
        return self.rotations[rotation_key][self.level].get(param_name, None)

    def rotation_is_valid(self, rotation_key):
        start_version = self.get_rotation_data(rotation_key, "start_version")
        end_version = self.get_rotation_data(rotation_key, "end_version")

        if self.level not in self.rotations[rotation_key]:            
            return False
        if self.version < start_version or (
            end_version is not None and self.version > end_version
        ):            
            return False
        return True

    def get_stats(self, rotation_key):
        stats_dict = self.get_rotation_data(rotation_key, "stats")        
        job_class = stats_dict["job_class"]

        stats = Stats(
            wd=stats_dict["wd"],
            weapon_delay=stats_dict.get(
                "weapon_delay", GameConsts.WEAPON_DELAYS[job_class]
            ),
            main_stat=stats_dict["main_stat"],
            det_stat=stats_dict["det_stat"],
            crit_stat=stats_dict["crit_stat"],
            dh_stat=stats_dict["dh_stat"],
            speed_stat=stats_dict["speed_stat"],
            tenacity=stats_dict.get("tenacity", None),
            healer_or_caster_strength=stats_dict.get(
                "healer_or_caster_strength",
                GameConsts.HEALER_CASTER_STRENGTH.get(job_class, None),
            ),
            job_class=job_class,
            version=self.version,
        )
        return stats

    def get_skills(self, rotation_key):
        return self.get_rotation_data(rotation_key, "skills")

    def get_party_skills(self, rotation_key):
        res = self.get_rotation_data(rotation_key, "party_skills")
        if res is None:
            return tuple()
        return res
