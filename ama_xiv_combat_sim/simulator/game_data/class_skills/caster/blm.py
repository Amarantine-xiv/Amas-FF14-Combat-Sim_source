import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
)
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.blm_data import (
    all_blm_skills,
)


def add_blm_skills(skill_library):
    version = skill_library.get_version()
    all_blm_skills.set_version(version)

    level = skill_library.get_level()
    all_blm_skills.set_level(level)

    auto_timing = get_auto_timing()
    blm_caster_tax_ms = 100
    base_animation_lock = 600
    instant_timing_spec = TimingSpec(
        base_cast_time=0, animation_lock=base_animation_lock
    )
    skill_library.set_current_job_class("BLM")

    skill_library.set_status_effect_priority(("Swiftcast", "Triplecast"))

    name = "Astral Fire"
    af_skill_allowlist = all_blm_skills.get_skill_data(name, "allowlist")

    name = "Astral Fire"
    skill_library.add_resource(
        name=name,
        job_resource_settings=JobResourceSettings(
            max_value=3,
            expiry_from_last_gain=15 * 1000,
            skill_allowlist=af_skill_allowlist,
        ),
    )

    name = "Umbral Ice"
    ui_skill_allowlist = all_blm_skills.get_skill_data(name, "allowlist")
    skill_library.add_resource(
        name=name,
        job_resource_settings=JobResourceSettings(
            max_value=3,
            expiry_from_last_gain=15 * 1000,
            skill_allowlist=ui_skill_allowlist,
        ),
    )

    clear_umbral_ice = JobResourceSpec(
        name="Umbral Ice", change=-math.inf, refreshes_duration_of_last_gained=True
    )
    clear_astral_fire = JobResourceSpec(
        name="Astral Fire", change=-math.inf, refreshes_duration_of_last_gained=True
    )

    def get_enochian_damage_spec_cross(base_potency, is_fire_spell):
        res = {}
        elem_strs = [
            "1 Astral Fire",
            "2 Astral Fire",
            "3 Astral Fire",
            "1 Umbral Ice",
            "2 Umbral Ice",
            "3 Umbral Ice",
        ]
        fire_potency_modifiers = {
            "1 Astral Fire": 1.4,
            "2 Astral Fire": 1.6,
            "3 Astral Fire": 1.8,
            "1 Umbral Ice": 0.9,
            "2 Umbral Ice": 0.8,
            "3 Umbral Ice": 0.7,
        }
        ice_potency_modifiers = {
            "1 Astral Fire": 0.9,
            "2 Astral Fire": 0.8,
            "3 Astral Fire": 0.7,
            "1 Umbral Ice": 1,
            "2 Umbral Ice": 1,
            "3 Umbral Ice": 1,
        }

        res[SimConsts.DEFAULT_CONDITION] = DamageSpec(
            potency=base_potency
        )  # no astral/umbral fire
        for elem_str in elem_strs:
            potency_modifier = (
                fire_potency_modifiers[elem_str]
                if is_fire_spell
                else ice_potency_modifiers[elem_str]
            )
            res[elem_str] = DamageSpec(
                potency=base_potency, single_damage_mult=potency_modifier
            )
        return res

    def get_enochian_timing_spec_cross(
        base_cast_time, is_fire_spell, application_delay=0
    ):
        res = {}
        elem_strs = [
            "1 Astral Fire",
            "2 Astral Fire",
            "3 Astral Fire",
            "1 Umbral Ice",
            "2 Umbral Ice",
            "3 Umbral Ice",
        ]
        fire_cast_time_modifiers = {
            "1 Astral Fire": 1,
            "2 Astral Fire": 1,
            "3 Astral Fire": 1,
            "1 Umbral Ice": 1,
            "2 Umbral Ice": 1,
            "3 Umbral Ice": 0.5,
        }
        ice_cast_time_modifiers = {
            "1 Astral Fire": 1,
            "2 Astral Fire": 1,
            "3 Astral Fire": 0.5,
            "1 Umbral Ice": 1,
            "2 Umbral Ice": 1,
            "3 Umbral Ice": 1,
        }
        animation_lock_overflow = max(
            0,
            base_animation_lock
            - min(base_cast_time, GameConsts.DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES),
        )
        res[SimConsts.DEFAULT_CONDITION] = TimingSpec(
            base_cast_time=base_cast_time,
            animation_lock=animation_lock_overflow,
            application_delay=application_delay,
        )
        for elem_str in elem_strs:
            cast_modifier = (
                fire_cast_time_modifiers[elem_str]
                if is_fire_spell
                else ice_cast_time_modifiers[elem_str]
            )
            animation_lock_overflow = max(
                0,
                base_animation_lock
                - min(
                    int(cast_modifier * base_cast_time),
                    GameConsts.DAMAGE_SNAPSHOT_TIME_BEFORE_CAST_FINISHES,
                ),
            )
            res[elem_str] = TimingSpec(
                base_cast_time=int(cast_modifier * base_cast_time),
                animation_lock=animation_lock_overflow,
                application_delay=application_delay,
            )
        return res

    name = "Enochian"
    enochian_buff = Skill(
        name=name,
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            damage_mult=all_blm_skills.get_skill_data(name, "damage_mult"),
            duration=15 * 1000,
        ),
    )
    enochian_buff_follow_up = FollowUp(
        skill=enochian_buff, delay_after_parent_application=0, primary_target_only=True
    )

    name = "Auto"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )

    thunderiii_dot = Skill(
        name="Thunder (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_blm_skills.get_potency("Thunder III (dot)"),
            damage_class=DamageClass.MAGICAL_DOT,
        ),
    )
    thunderiii_follow_up = FollowUp(
        skill=thunderiii_dot,
        delay_after_parent_application=0,
        dot_duration=all_blm_skills.get_skill_data("Thunder III (dot)", "duration"),
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    thunderiv_dot = Skill(
        name="Thunder (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_blm_skills.get_potency("Thunder IV (dot)"),
            damage_class=DamageClass.MAGICAL_DOT,
        ),
    )
    thunderiv_follow_up = FollowUp(
        skill=thunderiv_dot,
        delay_after_parent_application=0,
        dot_duration=all_blm_skills.get_skill_data("Thunder IV (dot)", "duration"),
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
        primary_target_only=False,
    )

    if level in [100]:
        high_thunder_dot = Skill(
            name="Thunder (dot)",
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=all_blm_skills.get_potency("High Thunder (dot)"),
                damage_class=DamageClass.MAGICAL_DOT,
            ),
        )

    if level in [100]:
        high_thunder_follow_up = FollowUp(
            skill=high_thunder_dot,
            delay_after_parent_application=0,
            dot_duration=all_blm_skills.get_skill_data(
                "High Thunder (dot)", "duration"
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
        )
        high_thunder_ii_follow_up = FollowUp(
            skill=Skill(
                name="Thunder (dot)",
                is_GCD=False,
                damage_spec=DamageSpec(
                    potency=all_blm_skills.get_potency("High Thunder II (dot)"),
                    damage_class=DamageClass.MAGICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=all_blm_skills.get_skill_data(
                "High Thunder II (dot)", "duration"
            ),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
            primary_target_only=False,
        )

    name = "Blizzard"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=2500, is_fire_spell=False, application_delay=840
            ),
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Umbral Ice", change=+1),
                ),
                "1 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=-math.inf,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=-math.inf,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=-math.inf,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "1 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
            },
            follow_up_skills=(enochian_buff_follow_up,),
        )
    )

    name = "Firestarter"
    firestarter_buff = Skill(
        name=name,
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=30 * 1000,
            skill_allowlist=all_blm_skills.get_skill_data(name, "allowlist"),
        ),
    )
    firestarter_follow_up = FollowUp(
        skill=firestarter_buff, delay_after_parent_application=10
    )

    name = "Firestarter"
    # For automated/proc management convenience
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=all_blm_skills.get_skill_data(name, "allowlist"),
            ),
        )
    )

    if level in [90]:
        name = "Thundercloud"
        thundercloud_buff = Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=40 * 1000,
                skill_allowlist=("Thunder III", "Thunder IV"),
            ),
        )
        thundercloud_follow_up = FollowUp(
            skill=thundercloud_buff, delay_after_parent_application=10
        )
    if level in [90]:
        # For automated/proc management convenience
        name = "Thundercloud"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=0, application_delay=0
                ),
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=40 * 1000,
                    skill_allowlist=("Thunder III", "Thunder IV"),
                ),
            )
        )

    if level in [90]:
        name = "Enhanced"
        enhanced_flare_follow_up = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    # this is incorrect, since it expires with astral fire.
                    duration=math.inf,
                    skill_allowlist=("Flare",),
                ),
            ),
            delay_after_parent_application=10,
        )

    fire_job_resource_spec = {
        SimConsts.DEFAULT_CONDITION: (JobResourceSpec(name="Astral Fire", change=+1),),
        "1 Astral Fire": (
            JobResourceSpec(
                name="Astral Fire", change=+1, refreshes_duration_of_last_gained=True
            ),
        ),
        "2 Astral Fire": (
            JobResourceSpec(
                name="Astral Fire", change=+1, refreshes_duration_of_last_gained=True
            ),
        ),
        "3 Astral Fire": (
            JobResourceSpec(
                name="Astral Fire", change=+1, refreshes_duration_of_last_gained=True
            ),
        ),
        "1 Umbral Ice": (
            JobResourceSpec(
                name="Umbral Ice",
                change=-math.inf,
                refreshes_duration_of_last_gained=True,
            ),
        ),
        "2 Umbral Ice": (
            JobResourceSpec(
                name="Umbral Ice",
                change=-math.inf,
                refreshes_duration_of_last_gained=True,
            ),
        ),
        "3 Umbral Ice": (
            JobResourceSpec(
                name="Umbral Ice",
                change=-math.inf,
                refreshes_duration_of_last_gained=True,
            ),
        ),
    }
    name = "Fire"
    fire_damage_spec = get_enochian_damage_spec_cross(
        base_potency=all_blm_skills.get_potency(name), is_fire_spell=True
    )
    fire_timing_spec = get_enochian_timing_spec_cross(
        base_cast_time=2500, is_fire_spell=True, application_delay=1030
    )

    if level in [90]:
        fire_keys = tuple(fire_damage_spec.keys())
        for k in fire_keys:
            assembled_str = (
                "Sharpcast" if k == SimConsts.DEFAULT_CONDITION else "{k}, Sharpcast"
            )
            fire_damage_spec[assembled_str] = fire_damage_spec[k]
            fire_timing_spec[assembled_str] = fire_timing_spec[k]
            fire_job_resource_spec[assembled_str] = fire_job_resource_spec[k]

    name = "Fire"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=fire_damage_spec,
            timing_spec=fire_timing_spec,
            job_resource_spec=fire_job_resource_spec,
            follow_up_skills=(
                {
                    SimConsts.DEFAULT_CONDITION: (enochian_buff_follow_up,),
                    "Sharpcast": (firestarter_follow_up, enochian_buff_follow_up),
                }
                if level in [90]
                else {
                    SimConsts.DEFAULT_CONDITION: (enochian_buff_follow_up,),
                    "Firestarter": (
                        enochian_buff_follow_up,
                        firestarter_follow_up,
                    ),
                }
            ),
        )
    )

    name = "Scathe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_blm_skills.get_potency(name)
                    ),
                    "2x": DamageSpec(potency=2 * all_blm_skills.get_potency(name)),
                    "Sharpcast": DamageSpec(
                        potency=2 * all_blm_skills.get_potency(name)
                    ),
                }
                if level in [90]
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_blm_skills.get_potency(name)
                    ),
                    "2x": DamageSpec(potency=2 * all_blm_skills.get_potency(name)),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=670,
            ),
        )
    )

    name = "Fire III"
    fire_iii_damage_spec = get_enochian_damage_spec_cross(
        base_potency=all_blm_skills.get_potency(name), is_fire_spell=True
    )
    fire_iii_timing_spec = get_enochian_timing_spec_cross(
        base_cast_time=3500, is_fire_spell=True, application_delay=1290
    )
    fire_iii_keys = tuple(fire_iii_damage_spec.keys())
    for k in fire_iii_keys:
        assembled_str = (
            "Firestarter" if k == SimConsts.DEFAULT_CONDITION else f"{k}, Firestarter"
        )
        fire_iii_damage_spec[assembled_str] = fire_iii_damage_spec[k]
        fire_iii_timing_spec[assembled_str] = TimingSpec(
            base_cast_time=0, animation_lock=base_animation_lock, application_delay=1290
        )
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=fire_iii_damage_spec,
            timing_spec=fire_iii_timing_spec,
            job_resource_spec=(
                clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=(enochian_buff_follow_up,),
        )
    )

    name = "Blizzard III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=3500, is_fire_spell=False, application_delay=840
            ),
            buff_spec=StatusEffectSpec(expires_status_effects=("Enhanced",)),
            job_resource_spec=(
                clear_astral_fire,
                JobResourceSpec(
                    name="Umbral Ice", change=+3, refreshes_duration_of_last_gained=True
                ),
            ),
            follow_up_skills=(enochian_buff_follow_up,),
        )
    )

    name = "Freeze"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=2800, is_fire_spell=False, application_delay=620
            ),
            has_aoe=True,
        )
    )

    name = "Thunder III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_blm_skills.get_potency(name)
                    ),
                    "Thundercloud": DamageSpec(
                        potency=all_blm_skills.get_skill_data(
                            name, "potency_thundercloud"
                        )
                    ),
                }
                if level in [90]
                else DamageSpec(potency=all_blm_skills.get_potency(name))
            ),
            timing_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=2500,
                        animation_lock=blm_caster_tax_ms,
                        application_delay=1030,
                    ),
                    "Thundercloud": TimingSpec(
                        base_cast_time=0,
                        animation_lock=base_animation_lock,
                        application_delay=1030,
                    ),
                }
                if level in [90]
                else TimingSpec(
                    base_cast_time=2500,
                    animation_lock=blm_caster_tax_ms,
                    application_delay=1030,
                )
            ),
            follow_up_skills=(
                {
                    SimConsts.DEFAULT_CONDITION: (thunderiii_follow_up,),
                    "Thundercloud": (thunderiii_follow_up,),
                    "Sharpcast": (thunderiii_follow_up, thundercloud_follow_up),
                    "Sharpcast, Thundercloud": (
                        (
                            thunderiii_follow_up,
                            thundercloud_follow_up,
                        )
                    ),
                }
                if level in [90]
                else (thunderiii_follow_up,)
            ),
        )
    )

    flare_elem_mults = {
        "1 Astral Fire": 1.4,
        "2 Astral Fire": 1.6,
        "3 Astral Fire": 1.8,
        "1 Umbral Ice": 0.9,
        "2 Umbral Ice": 0.8,
        "3 Umbral Ice": 0.7,
    }
    name = "Flare"
    flare_damage_spec = get_enochian_damage_spec_cross(
        base_potency=all_blm_skills.get_potency(name), is_fire_spell=True
    )
    if level in [90]:
        enhanced_flare_potency = all_blm_skills.get_skill_data(name, "potency_enhanced")
        flare_damage_spec["Enhanced"] = DamageSpec(potency=enhanced_flare_potency)
        flare_damage_spec["Enhanced, Triplecast"] = DamageSpec(
            potency=enhanced_flare_potency
        )
        for k, potency_modifier in flare_elem_mults.items():
            assemebled_str = f"{k}, Enhanced"
            flare_damage_spec[assemebled_str] = DamageSpec(
                potency=int(potency_modifier * enhanced_flare_potency)
            )
            assemebled_str = f"{k}, Enhanced, Triplecast"
            flare_damage_spec[assemebled_str] = DamageSpec(
                potency=int(potency_modifier * enhanced_flare_potency)
            )
    flare_timing_spec = get_enochian_timing_spec_cross(
        base_cast_time=all_blm_skills.get_skill_data(name, "cast time"),
        is_fire_spell=True,
        application_delay=1160,
    )
    flare_timing_keys = tuple(flare_timing_spec.keys())
    for k in flare_timing_keys:
        assembled_str = f"{k}, Enhanced"
        flare_timing_spec[assembled_str] = flare_timing_spec[k]
        
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=flare_damage_spec,
            timing_spec=flare_timing_spec,
            job_resource_spec=(
                clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=(enochian_buff_follow_up,),
            has_aoe=True,
            aoe_dropoff=all_blm_skills.get_skill_data(name, "aoe_dropoff"),
        )
    )

    name = "Ley Lines"
    skill_library.add_skill(
        Skill(
            name="Ley Lines",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                haste_time_reduction=0.15,
                auto_attack_delay_reduction=0.15,
                duration=30 * 1000,
            ),
        )
    )

    name = "Blizzard IV"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=2500, is_fire_spell=False, application_delay=1160
            ),
        )
    )

    name = "Fire IV"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=True
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=2800, is_fire_spell=True, application_delay=1160
            ),
        )
    )

    name = "Thunder IV"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_blm_skills.get_potency(name)
                    ),
                    "Thundercloud": DamageSpec(
                        potency=all_blm_skills.get_skill_data(
                            name, "potency_thundercloud"
                        )
                    ),
                }
                if level in [90]
                else DamageSpec(potency=all_blm_skills.get_potency(name))
            ),
            timing_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: TimingSpec(
                        base_cast_time=2500,
                        animation_lock=blm_caster_tax_ms,
                        application_delay=1160,
                    ),
                    "Thundercloud": TimingSpec(
                        base_cast_time=0,
                        animation_lock=blm_caster_tax_ms,
                        application_delay=1160,
                    ),
                }
                if level in [90]
                else TimingSpec(
                    base_cast_time=2500,
                    animation_lock=blm_caster_tax_ms,
                    application_delay=1160,
                )
            ),
            follow_up_skills=(
                {
                    SimConsts.DEFAULT_CONDITION: (thunderiv_follow_up,),
                    "Thundercloud": (thunderiv_follow_up,),
                    "Sharpcast": (thunderiv_follow_up, thundercloud_follow_up),
                    "Sharpcast, Thundercloud": (
                        thunderiv_follow_up,
                        thundercloud_follow_up,
                    ),
                }
                if level in [90]
                else (thunderiv_follow_up,)
            ),
            has_aoe=True,
        )
    )

    name = "Foul"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_blm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1160,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Despair"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=True
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=all_blm_skills.get_skill_data(name, "cast time"),
                is_fire_spell=True,
                application_delay=490,
                # may need to change the animation lock for when it's instant cast?
            ),
            job_resource_spec=(
                clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=(enochian_buff_follow_up,),
        )
    )

    name = "Xenoglossy"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_blm_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=620,
            ),
        )
    )

    name = "High Fire II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=True
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=3000, is_fire_spell=True, application_delay=1160
            ),
            job_resource_spec=(
                clear_umbral_ice,
                JobResourceSpec(
                    name="Astral Fire",
                    change=+3,
                    refreshes_duration_of_last_gained=True,
                ),
            ),
            follow_up_skills=(
                (enhanced_flare_follow_up, enochian_buff_follow_up)
                if level in [90]
                else (enochian_buff_follow_up,)
            ),
            has_aoe=True,
        )
    )

    name = "High Blizzard II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=all_blm_skills.get_potency(name), is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=3000, is_fire_spell=False, application_delay=1160
            ),
            buff_spec=StatusEffectSpec(expires_status_effects=("Enhanced",)),
            job_resource_spec=(
                clear_astral_fire,
                JobResourceSpec(
                    name="Umbral Ice", change=+3, refreshes_duration_of_last_gained=True
                ),
            ),
            follow_up_skills=(enochian_buff_follow_up,),
            has_aoe=True,
        )
    )

    if level in [90]:
        paradox_base_timing_spec = TimingSpec(
            base_cast_time=2500, animation_lock=blm_caster_tax_ms, application_delay=670
        )
        paradox_umbral_timing_spec = TimingSpec(
            base_cast_time=0, animation_lock=base_animation_lock, application_delay=670
        )
    name = "Paradox"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_blm_skills.get_potency(name)),
            timing_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: paradox_base_timing_spec,
                    "1 Astral Fire": paradox_base_timing_spec,
                    "2 Astral Fire": paradox_base_timing_spec,
                    "3 Astral Fire": paradox_base_timing_spec,
                    "1 Umbral Ice": paradox_umbral_timing_spec,
                    "2 Umbral Ice": paradox_umbral_timing_spec,
                    "3 Umbral Ice": paradox_umbral_timing_spec,
                }
                if level in [90]
                else TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=670,
                )
            ),
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Astral Fire": (
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "1 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Umbral Ice": (
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
            },
            follow_up_skills=(
                {
                    SimConsts.DEFAULT_CONDITION: (enochian_buff_follow_up,),
                    "Sharpcast": (
                        firestarter_follow_up,
                        enochian_buff_follow_up,
                    ),
                }
                if level in [90]
                else {
                    SimConsts.DEFAULT_CONDITION: (enochian_buff_follow_up,),
                    "1 Astral Fire": (enochian_buff_follow_up, firestarter_follow_up),
                    "2 Astral Fire": (enochian_buff_follow_up, firestarter_follow_up),
                    "3 Astral Fire": (enochian_buff_follow_up, firestarter_follow_up),
                }
            ),
        )
    )

    if level in [100]:
        name = "High Thunder"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_blm_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=2500,
                    animation_lock=blm_caster_tax_ms,
                    application_delay=760,
                ),
                follow_up_skills=(high_thunder_follow_up,),
            )
        )

    if level in [100]:
        name = "High Thunder II"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_blm_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=2500,
                    animation_lock=blm_caster_tax_ms,
                    application_delay=760,
                ),
                follow_up_skills=(high_thunder_ii_follow_up,),
                has_aoe=True,
            )
        )

    if level in [100]:
        name = "Flare Star"
        flare_star_damage_spec = get_enochian_damage_spec_cross(
            base_potency=all_blm_skills.get_potency(name), is_fire_spell=True
        )
        flare_star_timing_spec = get_enochian_timing_spec_cross(
            base_cast_time=3000, is_fire_spell=True, application_delay=620
        )
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=flare_star_damage_spec,
                timing_spec=flare_star_timing_spec,
                has_aoe=True,
                aoe_dropoff=0.65,
            ),
        )

    name = "Swiftcast"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=1,
                skill_allowlist=(
                    (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                    if version in ["7.1"]
                    else (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Despair",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                ),
            ),
        )
    )

    name = "Triplecast"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=3,
                skill_allowlist=(
                    (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                    if version in ["7.1"]
                    else (
                        "Thunder III",
                        "Thunder IV",
                        "Blizzard",
                        "High Blizzard II",
                        "Blizzard III",
                        "Blizzard IV",
                        "Freeze",
                        "Fire",
                        "High Fire II",
                        "Fire III",
                        "Fire IV",
                        "Despair",
                        "Flare",
                        "Paradox",
                        "Flare Star",
                    )
                ),
            ),
        )
    )

    name = "Transpose"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: None,
                    "1 Umbral Ice": StatusEffectSpec(
                        expires_status_effects=("Enhanced",)
                    ),
                    "2 Umbral Ice": StatusEffectSpec(
                        expires_status_effects=("Enhanced",)
                    ),
                    "3 Umbral Ice": StatusEffectSpec(
                        expires_status_effects=("Enhanced",)
                    ),
                }
                if level in [90]
                else None
            ),
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Astral Fire": (
                    clear_astral_fire,
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Astral Fire": (
                    clear_astral_fire,
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Astral Fire": (
                    clear_astral_fire,
                    JobResourceSpec(
                        name="Umbral Ice",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "1 Umbral Ice": (
                    clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "2 Umbral Ice": (
                    clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
                "3 Umbral Ice": (
                    clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+1,
                        refreshes_duration_of_last_gained=True,
                    ),
                ),
            },
            follow_up_skills=(enochian_buff_follow_up,),
        )
    )

    if level in [90]:
        name = "Sharpcast"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=instant_timing_spec,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30 * 1000,
                    skill_allowlist=(
                        "Scathe",
                        "Fire",
                        "Paradox",
                        "Thunder III",
                        "Thunder IV",
                    ),
                ),
            )
        )

    # # These skills do not damage, but grants resources/affects future skills.
    # # Since we do not model resources YET, we just record their usage/timings but
    # # not their effect.
    name = "Manafont"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            job_resource_spec=(
                tuple()
                if level in [90]
                else (
                    clear_umbral_ice,
                    JobResourceSpec(
                        name="Astral Fire",
                        change=+3,
                        refreshes_duration_of_last_gained=True,
                    ),
                )
            ),
        )
    )
    skill_library.add_skill(
        Skill(name="Umbral Soul", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Amplifier", is_GCD=False, timing_spec=instant_timing_spec)
    )

    return skill_library
