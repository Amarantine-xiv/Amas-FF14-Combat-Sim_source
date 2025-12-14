from ama_xiv_combat_sim.simulator.sim_consts import SimConsts


def radiant_finale_processing(brd_rotation):
    curr_songs = set()
    res = []
    for _, skill, skill_condition, _, _ in brd_rotation.get_timed_skills():
        skill_name = skill.name
        if (
            skill_name in ["Army's Paeon", "Mage's Ballad", "The Wanderer's Minuet"]
            and skill_name not in curr_songs
        ):
            curr_songs.add(skill_name)
        if skill_name in [
            "Radiant Finale",
        ]:
            conditional_to_use = f"{len(curr_songs)} Coda"
            res.append(conditional_to_use)
            curr_songs = set()
    return res
