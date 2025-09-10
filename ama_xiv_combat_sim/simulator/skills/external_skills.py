from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import OffensiveStatusEffectSpec
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
                offensive_debuff_spec=OffensiveStatusEffectSpec(
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
                offensive_buff_spec=OffensiveStatusEffectSpec(
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
                offensive_buff_spec=OffensiveStatusEffectSpec(
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
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.75, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_car_map():
    abilities = (
        (
            "Cloud of Darkness",
            "Arcane Design",
            Skill(
                name="Arcane Design",
                offensive_debuff_spec=OffensiveStatusEffectSpec(
                    duration=145 * 1000, damage_mult=1.2, is_party_effect=False
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
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.75, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def get_dd_ability(duration, dd_value):
    abilities = (
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    duration=duration, damage_mult=1 - dd_value, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_m5s_map():
    abilities = (
        (
            kPlayer,
            "Damage Down",
            Skill(
                name="Damage Down",
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    duration=30 * 1000, damage_mult=0.75, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
        (
            kPlayer,
            "Perfect Groove",
            Skill(
                name="Perfect Groove",
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    duration=20 * 1000, damage_mult=1.03, is_party_effect=False
                ),
                timing_spec=base_timing_spec,
                is_GCD=False,
            ),
        ),
    )
    return populate_abilities(abilities)


def create_external_skill_library(encounter_id):
    encounterid_to_external = {
        2061: create_car_map(),
        1079: create_fru_map(),
        1071: create_valigarmanda_map(),
        93: get_dd_ability(30 * 1000, 0.25),  # m1s
        94: get_dd_ability(30 * 1000, 0.26),  # m2s
        95: get_dd_ability(30 * 1000, 0.38),  # m3s
        96: get_dd_ability(30 * 1000, 0.25),  # m4s
        97: create_m5s_map(),
        98: get_dd_ability(30 * 1000, 0.30),  # m6s
        99: get_dd_ability(30 * 1000, 0.35),  # m7s
        100: get_dd_ability(30 * 1000, 0.50),  # m8s
        1065: get_dd_ability(180 * 1000, 0.50),  # DSR
        1068: get_dd_ability(180 * 1000, 0.90),  # TOP
    }
    map_creator = encounterid_to_external.get(encounter_id, None)

    if map_creator is not None:
        return map_creator
    return None
