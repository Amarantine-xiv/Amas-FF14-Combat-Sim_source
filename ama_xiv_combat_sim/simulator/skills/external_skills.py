from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

kPlayer = None


def populate_abilities(abilities):
    # abilities is a tuple
    # abilities[i] = (source name, name of skill, Skill)
    res = {}
    for tmp in abilities:
        if tmp[0] not in res:
            res[tmp[0]] = {}
        res[tmp[0]][tmp[1]] = tmp[2]
    return res


base_timing_spec = TimingSpec(
    base_cast_time=0,
    animation_lock=0,
    application_delay=0,
    affected_by_speed_stat=False,
    affected_by_haste_buffs=False,
)


def create_fru_map():
    abilities = (
        (
            "ice veil",
            "Vulnerability Down",
            Skill(
                name="Vulnerability Down",
                debuff_spec=StatusEffectSpec(
                    duration=9999000, damage_mult=0.5, is_party_effect=True
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                buff_spec=StatusEffectSpec(
                    duration=180 * 1000, damage_mult=0.1, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
        (
            kPlayer,
            "Mark of Mortality",
            Skill(
                name="Mark of Mortality",
                buff_spec=StatusEffectSpec(
                    duration=180 * 1000, damage_mult=0.1, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_valigarmanda_map():
    abilities = (
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                buff_spec=StatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.75, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_m1s_map():
    abilities = (
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                buff_spec=StatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.75, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_m2s_map():
    abilities = (
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                buff_spec=StatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.74, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_m3s_map():
    abilities = (
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                buff_spec=StatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.62, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_m4s_map():
    abilities = (
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                buff_spec=StatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.75, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_external_skill_library(encounter_id):
    encounterid_to_external = {
        1079: create_fru_map,
        1071: create_valigarmanda_map,
        93: create_m1s_map,
        94: create_m2s_map,
        95: create_m3s_map,
        96: create_m4s_map,
    }
    map_creator = encounterid_to_external.get(encounter_id, None)

    if map_creator is not None:
        return map_creator()
    return None
