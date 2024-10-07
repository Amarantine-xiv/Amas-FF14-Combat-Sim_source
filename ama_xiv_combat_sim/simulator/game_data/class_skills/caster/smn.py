import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.smn_data import (
    all_smn_skills,
)


def add_smn_skills(skill_library):
    all_smn_skills.set_version(skill_library.get_version())

    level = skill_library.get_level()
    all_smn_skills.set_level(level)

    auto_timing = get_auto_timing()

    smn_caster_tax_ms = 100
    base_animation_lock = 600
    instant_timing_spec = TimingSpec(
        base_cast_time=0, animation_lock=base_animation_lock
    )
    skill_library.set_current_job_class("SMN")

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
    if level in [90]:
        name = "Fester"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=930,
                ),
            )
        )

    name = "Energy Drain"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock + smn_caster_tax_ms,
                application_delay=1070,
            ),
        )
    )

    name = "Painflare"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock + smn_caster_tax_ms,
                application_delay=440,
            ),
            has_aoe=True,
        )
    )

    name = "Energy Siphon"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1020,
            ),
            has_aoe=True,
        )
    )

    aethercharge_bonus = 50
    name = "Ruin III"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_smn_skills.get_potency(name)),
                "Aethercharge": DamageSpec(potency=all_smn_skills.get_potency(name)+aethercharge_bonus),
            },
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=smn_caster_tax_ms,
                application_delay=800,
            ),
        )
    )

    name = "Astral Impulse"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=670,
            ),
        )
    )

    name = "Astral Flare"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=540,
            ),
            has_aoe=True,
        )
    )

    name = "Deathflare"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Ruin IV"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    name = "Searing Light"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=all_smn_skills.get_skill_data(name, "damage_mult"),
                duration=all_smn_skills.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
            timing_spec=instant_timing_spec,
        )
    )

    name = "Akh Morn (pet)"
    akh_morn_for_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                    pet_scalar=0.88,
                )
            },
            has_aoe=True,
            aoe_dropoff=0.6,
        ),
        delay_after_parent_application=0,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
        primary_target_only=False,
    )

    name = "Enkindle Bahamut"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(akh_morn_for_follow_up,),
        )
    )

    name = "Akh Morn"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(akh_morn_for_follow_up,),
        )
    )

    name = "Ruby Rite"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2800,
                gcd_base_recast_time=3000,
                animation_lock=smn_caster_tax_ms,
                application_delay=620,
            ),
        )
    )

    name = "Topaz Rite"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                animation_lock=base_animation_lock,
                application_delay=620,
            ),
        )
    )

    # # Recast really isn't affected by sps for some reason. You can check this in-game.
    name = "Emerald Rite"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=base_animation_lock,
                application_delay=620,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )
    )

    name = "Tri-disaster"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=base_animation_lock,
            ),
            has_aoe=True,
        )
    )

    name = "Fountain of Fire"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1070,
            ),
        )
    )

    name = "Brand of Purgatory"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
        )
    )

    name = "Revelation (pet)"
    revelation_follow_up = FollowUp(
        Skill(
            name=name,
            is_GCD=False,
            status_effect_denylist=("Dragon Sight",),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                    pet_scalar=0.88,
                )
            },
            timing_spec=instant_timing_spec,
            has_aoe=True,
            aoe_dropoff=0.6,
        ),
        delay_after_parent_application=0,
        snapshot_buffs_with_parent=0,
        snapshot_debuffs_with_parent=0,
        primary_target_only=False,
    )

    name = "Enkindle Phoenix"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(revelation_follow_up,),
        )
    )

    name = "Revelation"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(revelation_follow_up,),
        )
    )

    name = "Ruby Catastrophe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2800,
                gcd_base_recast_time=3000,
                animation_lock=smn_caster_tax_ms,
                application_delay=535,
            ),
            has_aoe=True,
        )
    )

    name = "Topaz Catastrophe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                animation_lock=base_animation_lock,
                application_delay=535,
            ),
            has_aoe=True,
        )
    )

    # # Recast really isn't affected by sps for some reason. You can check this in-game.
    name = "Emerald Catastrophe"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=base_animation_lock,
                application_delay=535,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
            has_aoe=True,
        )
    )

    name = "Crimson Cyclone"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )

    name = "Crimson Strike"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=760,
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )

    name = "Mountain Buster"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=760,
            ),
            has_aoe=True,
            aoe_dropoff=0.7,
        )
    )

    name = "Slipstream (dot)"
    slipstream_dot = Skill(
        name=name,
        is_GCD=False,
        damage_spec=DamageSpec(
            potency=all_smn_skills.get_potency(name),
            damage_class=DamageClass.MAGICAL_DOT,
        ),
        has_aoe=True,
    )
    slipstream_follow_up = FollowUp(
        skill=slipstream_dot,
        delay_after_parent_application=0,
        dot_duration=15 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=False,
        primary_target_only=False,
    )

    name = "Slipstream"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_smn_skills.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=3000,
                gcd_base_recast_time=3500,
                animation_lock=smn_caster_tax_ms,
                application_delay=1020,
            ),
            follow_up_skills=(slipstream_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )

    name = "Inferno (pet)"
    inferno = Skill(
        name=name,
        is_GCD=True,
        status_effect_denylist=("Dragon Sight",),
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(
                potency=all_smn_skills.get_potency(name),
                damage_class=DamageClass.PET,
                pet_job_mod_override=100,
                pet_scalar=0.88,
            )
        },
        has_aoe=True,
        aoe_dropoff=0.6,
    )
    # Model the 2.1s snap with this hack. Damage will not come out correctly though.
    inferno_follow_up = FollowUp(
        skill=inferno,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
        delay_after_parent_application=2100,
        primary_target_only=False,
    )

    name = "Summon Ifrit II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills=(inferno_follow_up,),
        )
    )

    name = "Earthen Fury (pet)"
    earthen_fury_blast = Skill(
        name=name,
        is_GCD=True,
        status_effect_denylist=("Dragon Sight",),
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(
                potency=all_smn_skills.get_potency(name),
                damage_class=DamageClass.PET,
                pet_job_mod_override=100,
                pet_scalar=0.88,
            )
        },
        has_aoe=True,
        aoe_dropoff=0.6,
    )
    # Model the 2.1s snap with this hack. Damage will not come out correctly though.
    earthen_fury_follow_up = FollowUp(
        skill=earthen_fury_blast,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
        delay_after_parent_application=2100,
        primary_target_only=False,
    )

    name = "Summon Titan II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills=(earthen_fury_follow_up,),
        )
    )

    name = "Aerial Blast (pet)"
    aerial_blast = Skill(
        name=name,
        is_GCD=True,
        status_effect_denylist=("Dragon Sight",),
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(
                potency=all_smn_skills.get_potency(name),
                damage_class=DamageClass.PET,
                pet_job_mod_override=100,
                pet_scalar=0.88,
            )
        },
        has_aoe=True,
        aoe_dropoff=0.6,
    )
    # Model the 2.1s snap with this hack. Damage will not come out correctly though.
    aerial_blast_follow_up = FollowUp(
        skill=aerial_blast,
        snapshot_buffs_with_parent=False,
        snapshot_debuffs_with_parent=False,
        delay_after_parent_application=2100,
        primary_target_only=False,
    )

    if level in [100]:
        name="Necrotize"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=710,
                ),
            )
        )
    
    if level in [100]:
        name="Searing Flash"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=800,
                ),
                has_aoe=True,
            )
        )

    name = "Summon Garuda II"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills=(aerial_blast_follow_up,),
        )
    )

    name = "Scarlet Flame (pet)"
    scarlet_flame_skill_for_follow_up = Skill(
        name=name,
        is_GCD=False,
        status_effect_denylist=("Dragon Sight",),
        damage_spec=DamageSpec(
            potency=all_smn_skills.get_potency(name),
            damage_class=DamageClass.PET,
            pet_job_mod_override=100,
            pet_scalar=0.88,
        ),
    )

    name = "Scarlet Flame"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            status_effect_denylist=("Dragon Sight",),
            timing_spec=auto_timing,
            follow_up_skills=(
                FollowUp(
                    skill=scarlet_flame_skill_for_follow_up,
                    delay_after_parent_application=0,
                    snapshot_buffs_with_parent=False,
                    snapshot_debuffs_with_parent=False,
                ),
            ),
        )
    )

    name = "Summon Phoenix"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    FollowUp(
                        skill=scarlet_flame_skill_for_follow_up,
                        delay_after_parent_application=3650,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                    FollowUp(
                        skill=scarlet_flame_skill_for_follow_up,
                        delay_after_parent_application=6250,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                    FollowUp(
                        skill=scarlet_flame_skill_for_follow_up,
                        delay_after_parent_application=10850,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                    FollowUp(
                        skill=scarlet_flame_skill_for_follow_up,
                        delay_after_parent_application=12500,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                ),
                "Manual": tuple(),
            },
        )
    )

    name = "Wyrmwave (pet)"
    wyrmwave_skill_for_follow_up = Skill(
        name=name,
        is_GCD=False,
        status_effect_denylist=("Dragon Sight",),
        damage_spec=DamageSpec(
            potency=all_smn_skills.get_potency(name),
            damage_class=DamageClass.PET,
            pet_job_mod_override=100,
            pet_scalar=0.88,
        ),
    )

    name = "Wyrmwave"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=auto_timing,
            follow_up_skills=(
                FollowUp(
                    skill=wyrmwave_skill_for_follow_up,
                    delay_after_parent_application=0,
                    snapshot_buffs_with_parent=False,
                    snapshot_debuffs_with_parent=False,
                ),
            ),
        ),
    )

    name = "Summon Bahamut"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    FollowUp(
                        skill=wyrmwave_skill_for_follow_up,
                        delay_after_parent_application=3200,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                    FollowUp(
                        skill=wyrmwave_skill_for_follow_up,
                        delay_after_parent_application=6350,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                    FollowUp(
                        skill=wyrmwave_skill_for_follow_up,
                        delay_after_parent_application=10950,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                    FollowUp(
                        skill=wyrmwave_skill_for_follow_up,
                        delay_after_parent_application=12500,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                ),
                "Manual": tuple(),
            },
        )
    )

    if level in [100]:
        name="Luxwave"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(
                    potency=all_smn_skills.get_potency(name),
                    damage_class=DamageClass.PET,
                    pet_job_mod_override=100,
                    pet_scalar=0.88,
                ),
                timing_spec=auto_timing,
            )
        )
        
        name="Luxwave"
        luxwave_skill_for_follow_up = Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=all_smn_skills.get_potency(name),
                damage_class=DamageClass.PET,
                pet_job_mod_override=100,
                pet_scalar=0.88,
            ),
        )
        name="Summon Solar Bahamut"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                timing_spec=instant_timing_spec,
                follow_up_skills={
                    SimConsts.DEFAULT_CONDITION: (
                        FollowUp(
                            skill=luxwave_skill_for_follow_up,
                            delay_after_parent_application=3200,
                            snapshot_buffs_with_parent=False,
                            snapshot_debuffs_with_parent=False,
                        ),
                        FollowUp(
                            skill=luxwave_skill_for_follow_up,
                            delay_after_parent_application=6350,
                            snapshot_buffs_with_parent=False,
                            snapshot_debuffs_with_parent=False,
                        ),
                        FollowUp(
                            skill=luxwave_skill_for_follow_up,
                            delay_after_parent_application=10950,
                            snapshot_buffs_with_parent=False,
                            snapshot_debuffs_with_parent=False,
                        ),
                        FollowUp(
                            skill=luxwave_skill_for_follow_up,
                            delay_after_parent_application=12500,
                            snapshot_buffs_with_parent=False,
                            snapshot_debuffs_with_parent=False,
                        ),
                    ),
                    "Manual": tuple(),
                },
            )
        )

    if level in [100]:
        name="Umbral Impulse"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=800,
                ),
            )
        )
    
    if level in [100]:
        name="Umbral Flare"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_smn_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=530,
                ),
                has_aoe=True,
            )
        )

    if level in [100]:
        name="Sunflare"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=all_smn_skills.get_potency(name))},
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=800,
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        )
        
    if level in [100]:
        name="Exodus (Pet)"
        exodus_follow_up = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_smn_skills.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                        pet_scalar=0.88,
                    )
                },
                timing_spec=instant_timing_spec,
                has_aoe=True,
                aoe_dropoff=0.6,
            ),
            delay_after_parent_application=0,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

        name="Exodus"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=instant_timing_spec,
                follow_up_skills=(exodus_follow_up,),
            )
        )
        name="Enkindle Solar Bahamut"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=False,
                timing_spec=instant_timing_spec,
                follow_up_skills=(exodus_follow_up,),
            )
        )
    
    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    skill_library.add_skill(
        Skill(
            name="Aethercharge",
            is_GCD=True,
            timing_spec=instant_timing_spec,
            buff_spec=StatusEffectSpec(
                duration=15 * 1000,
                num_uses=1,
                add_to_skill_modifier_condition=True,
                skill_allowlist=("Ruin III",),
            ),
        )
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
                    "Ruin III",
                    "Ruby Rite",
                    "Tri-disaster",
                    "Ruby Catastrophe",
                    "Slipstream",
                ),
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Summon Carbuncle",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=smn_caster_tax_ms,
            ),
        )
    )
    skill_library.add_skill(
        Skill(name="Summon Ifrit", is_GCD=True, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Summon Titan", is_GCD=True, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Summon Garuda", is_GCD=True, timing_spec=instant_timing_spec)
    )

    skill_library.add_skill(
        Skill(name="Astral Flow", is_GCD=True, timing_spec=instant_timing_spec)
    )

    return skill_library
