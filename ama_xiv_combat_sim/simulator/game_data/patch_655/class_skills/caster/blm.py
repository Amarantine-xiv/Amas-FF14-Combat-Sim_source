import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_655.convenience_timings import (
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


def add_blm_skills(skill_library):
    auto_timing = get_auto_timing()
    blm_caster_tax_ms = 100
    base_animation_lock = 600
    instant_timing_spec = TimingSpec(base_cast_time=0, animation_lock=base_animation_lock)
    skill_library.set_current_job_class("BLM")

    skill_library.set_status_effect_priority(("Swiftcast", "Triplecast"))
    skill_library.add_resource(
        name="Astral Fire",
        job_resource_settings=JobResourceSettings(
            max_value=3,
            expiry_from_last_gain=15 * 1000,
            skill_allowlist=(
                "Blizzard",
                "Transpose",
                "Fire",
                "Fire III",
                "Fire IV",
                "Blizzard IV",
                "Blizzard III",
                "Flare",
                "Despair",
                "High Fire II",
                "High Blizzard II",
                "Paradox",
            ),
        ),
    )
    skill_library.add_resource(
        name="Umbral Ice",
        job_resource_settings=JobResourceSettings(
            max_value=3,
            expiry_from_last_gain=15 * 1000,
            skill_allowlist=(
                "Blizzard",
                "Transpose",
                "Fire",
                "Fire III",
                "Fire IV",
                "Blizzard IV",
                "Blizzard III",
                "Flare",
                "Despair",
                "High Fire II",
                "High Blizzard II",
                "Paradox",
            ),
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
            res[elem_str] = DamageSpec(potency=int(potency_modifier * base_potency))
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

    enochian_buff = Skill(
        name="Enochian",
        is_GCD=False,
        buff_spec=StatusEffectSpec(damage_mult=1.23, duration=15 * 1000),
    )
    enochian_buff_follow_up = FollowUp(
        skill=enochian_buff, delay_after_parent_application=0,
        primary_target_only=True
    )

    thunderiii_dot = Skill(
        name="Thunder (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=35, damage_class=DamageClass.MAGICAL_DOT),
    )
    thunderiii_follow_up = FollowUp(
        skill=thunderiii_dot,
        delay_after_parent_application=0,
        dot_duration=30 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )
    thunderiv_dot = Skill(
        name="Thunder (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=20, damage_class=DamageClass.MAGICAL_DOT),
    )
    thunderiv_follow_up = FollowUp(
        skill=thunderiv_dot,
        delay_after_parent_application=0,
        dot_duration=18 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Auto",
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blizzard",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=180, is_fire_spell=False
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
    firestarter_buff = Skill(
        name="Firestarter",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=30 * 1000,
            skill_allowlist=("Fire",),
        ),
    )
    firestarter_follow_up = FollowUp(
        skill=firestarter_buff, delay_after_parent_application=10
    )
    # For automated/proc management convenience
    skill_library.add_skill(
        Skill(
            name="Firestarter",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=("Fire",),
            ),
        )
    )
    thundercloud_buff = Skill(
        name="Thundercloud",
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
    # For automated/proc management convenience
    skill_library.add_skill(
        Skill(
            name="Thundercloud",
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

    enhanced_flare_buff = Skill(
        name="Enhanced",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            # this is incorrect, since it expires with astral fire.
            duration=math.inf,
            skill_allowlist=("Flare",),
        ),
    )
    enhanced_flare_follow_up = FollowUp(
        skill=enhanced_flare_buff, delay_after_parent_application=10
    )

    fire_damage_spec = get_enochian_damage_spec_cross(
        base_potency=180, is_fire_spell=True
    )
    fire_timing_spec = get_enochian_timing_spec_cross(
        base_cast_time=2500, is_fire_spell=True, application_delay=1030
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
    fire_keys = tuple(fire_damage_spec.keys())
    for k in fire_keys:
        assembled_str = (
            "Sharpcast"
            if k == SimConsts.DEFAULT_CONDITION
            else "{}, Sharpcast".format(k)
        )
        fire_damage_spec[assembled_str] = fire_damage_spec[k]
        fire_timing_spec[assembled_str] = fire_timing_spec[k]
        fire_job_resource_spec[assembled_str] = fire_job_resource_spec[k]
    skill_library.add_skill(
        Skill(
            name="Fire",
            is_GCD=True,
            damage_spec=fire_damage_spec,
            timing_spec=fire_timing_spec,
            job_resource_spec=fire_job_resource_spec,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (enochian_buff_follow_up,),
                "Sharpcast": (firestarter_follow_up, enochian_buff_follow_up),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Scathe",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=100),
                "2x": DamageSpec(potency=200),
                "Sharpcast": DamageSpec(potency=200),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=670,
            ),
        )
    )

    fire_iii_damage_spec = get_enochian_damage_spec_cross(
        base_potency=260, is_fire_spell=True
    )
    fire_iii_timing_spec = get_enochian_timing_spec_cross(
        base_cast_time=3500, is_fire_spell=True, application_delay=1290
    )
    fire_iii_keys = tuple(fire_iii_damage_spec.keys())
    for k in fire_iii_keys:
        assembled_str = (
            "Firestarter"
            if k == SimConsts.DEFAULT_CONDITION
            else "{}, Firestarter".format(k)
        )
        fire_iii_damage_spec[assembled_str] = fire_iii_damage_spec[k]
        fire_iii_timing_spec[assembled_str] = TimingSpec(
            base_cast_time=0, animation_lock=base_animation_lock, application_delay=1290
        )
    skill_library.add_skill(
        Skill(
            name="Fire III",
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
    skill_library.add_skill(
        Skill(
            name="Blizzard III",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=260, is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=3500, is_fire_spell=False, application_delay=890
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
    skill_library.add_skill(
        Skill(
            name="Freeze",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=120, is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=2800, is_fire_spell=False, application_delay=620
            ),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Thunder III",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=50),
                "Thundercloud": DamageSpec(potency=50 + 35 * 10),
            },
            timing_spec={
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
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (thunderiii_follow_up,),
                "Thundercloud": (thunderiii_follow_up,),
                "Sharpcast": (thunderiii_follow_up, thundercloud_follow_up),
                "Sharpcast, Thundercloud": (
                    thunderiii_follow_up,
                    thundercloud_follow_up,
                ),
            },
        )
    )

    enhanced_flare_potency = 280
    flare_damage_spec = get_enochian_damage_spec_cross(
        base_potency=220, is_fire_spell=True
    )
    flare_elem_mults = {
        "1 Astral Fire": 1.4,
        "2 Astral Fire": 1.6,
        "3 Astral Fire": 1.8,
        "1 Umbral Ice": 0.9,
        "2 Umbral Ice": 0.8,
        "3 Umbral Ice": 0.7,
    }
    flare_damage_spec["Enhanced"] = DamageSpec(potency=enhanced_flare_potency)
    flare_damage_spec["Enhanced, Triplecast"] = DamageSpec(
        potency=enhanced_flare_potency
    )
    for k, potency_modifier in flare_elem_mults.items():
        assemebled_str = "{}, Enhanced".format(k)
        flare_damage_spec[assemebled_str] = DamageSpec(
            potency=int(potency_modifier * enhanced_flare_potency)
        )
        assemebled_str = "{}, Enhanced, Triplecast".format(k)
        flare_damage_spec[assemebled_str] = DamageSpec(
            potency=int(potency_modifier * enhanced_flare_potency)
        )
    flare_timing_spec = get_enochian_timing_spec_cross(
        base_cast_time=4000, is_fire_spell=True, application_delay=1160
    )
    flare_timing_keys = tuple(flare_timing_spec.keys())
    for k in flare_timing_keys:
        assembled_str = "{}, Enhanced".format(k)
        flare_timing_spec[assembled_str] = flare_timing_spec[k]
    skill_library.add_skill(
        Skill(
            name="Flare",
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
            aoe_dropoff=0.4
        )
    )

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
    skill_library.add_skill(
        Skill(
            name="Blizzard IV",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=310, is_fire_spell=False
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=2500, is_fire_spell=False, application_delay=1160
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fire IV",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=310, is_fire_spell=True
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=2800, is_fire_spell=True, application_delay=1160
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Thunder IV",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=50),
                "Thundercloud": DamageSpec(potency=50 + 20 * 6),
            },
            timing_spec={
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
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (thunderiv_follow_up,),
                "Thundercloud": (thunderiv_follow_up,),
                "Sharpcast": (thunderiv_follow_up, thundercloud_follow_up),
                "Sharpcast, Thundercloud": (
                    thunderiv_follow_up,
                    thundercloud_follow_up,
                ),
            },
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Foul",
            is_GCD=True,
            damage_spec=DamageSpec(potency=600),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1160,
            ),
            has_aoe=True,
            aoe_dropoff=0.6
        )
    )
    skill_library.add_skill(
        Skill(
            name="Despair",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=340, is_fire_spell=True
            ),
            timing_spec=get_enochian_timing_spec_cross(
                base_cast_time=3000, is_fire_spell=True, application_delay=490
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
    skill_library.add_skill(
        Skill(
            name="Xenoglossy",
            is_GCD=True,
            damage_spec=DamageSpec(potency=880),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=620,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="High Fire II",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=140, is_fire_spell=True
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
            follow_up_skills=(enhanced_flare_follow_up, enochian_buff_follow_up),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="High Blizzard II",
            is_GCD=True,
            damage_spec=get_enochian_damage_spec_cross(
                base_potency=140, is_fire_spell=False
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
            has_aoe=True
        )
    )

    paradox_base_timing_spec = TimingSpec(
        base_cast_time=2500, animation_lock=blm_caster_tax_ms, application_delay=670
    )
    paradox_umbral_timing_spec = TimingSpec(
        base_cast_time=0, animation_lock=base_animation_lock, application_delay=670
    )
    skill_library.add_skill(
        Skill(
            name="Paradox",
            is_GCD=True,
            damage_spec=DamageSpec(potency=500),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: paradox_base_timing_spec,
                "1 Astral Fire": paradox_base_timing_spec,
                "2 Astral Fire": paradox_base_timing_spec,
                "3 Astral Fire": paradox_base_timing_spec,
                "1 Umbral Ice": paradox_umbral_timing_spec,
                "2 Umbral Ice": paradox_umbral_timing_spec,
                "3 Umbral Ice": paradox_umbral_timing_spec,
            },
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
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (enochian_buff_follow_up,),
                "Sharpcast": (
                    firestarter_follow_up,
                    enochian_buff_follow_up,
                ),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Swiftcast",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=1,
                skill_allowlist=(
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
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Triplecast",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=3,
                skill_allowlist=(
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
                ),
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Transpose",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "1 Umbral Ice": StatusEffectSpec(expires_status_effects=("Enhanced",)),
                "2 Umbral Ice": StatusEffectSpec(expires_status_effects=("Enhanced",)),
                "3 Umbral Ice": StatusEffectSpec(expires_status_effects=("Enhanced",)),
            },
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

    skill_library.add_skill(
        Skill(
            name="Sharpcast",
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

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Manafont", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Umbral Soul", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Amplifier", is_GCD=False, timing_spec=instant_timing_spec)
    )
    return skill_library
