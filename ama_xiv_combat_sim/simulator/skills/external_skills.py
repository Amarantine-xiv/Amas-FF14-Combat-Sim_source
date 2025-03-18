from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def create_fru_map():
    res = {}
    abilities = (
        (
            "ice veil",
            "Vulnerability Down",
            Skill(
                name="Vulnerability Down",
                debuff_spec=StatusEffectSpec(
                    duration=9999000, damage_mult=0.5, is_party_effect=True
                ),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=0,
                    application_delay=0,
                    affected_by_speed_stat=False,
                    affected_by_haste_buffs=False,
                ),
                is_GCD=False,
            ),
        ),
    )

    for tmp in abilities:
        if tmp[0] not in res:
            res[tmp[0]] = {}
        res[tmp[0]][tmp[1]] = tmp[2]
    return res


def create_external_skill_library(encounter_id):
    encounterid_to_external = {1079: create_fru_map}
    map_creator = encounterid_to_external.get(encounter_id, None)

    if map_creator is not None:
        return map_creator()
    return None
