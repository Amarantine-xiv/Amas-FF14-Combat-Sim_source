import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.patch_655.convenience_timings import (
    get_auto_timing,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def add_smn_skills(skill_library):
    auto_timing = get_auto_timing()

    smn_caster_tax_ms = 100
    base_animation_lock = 600
    instant_timing_spec = TimingSpec(
        base_cast_time=0, animation_lock=base_animation_lock
    )
    skill_library.set_current_job_class("SMN")

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
            name="Fester",
            is_GCD=False,
            damage_spec=DamageSpec(potency=340),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=930,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Energy Drain",
            is_GCD=False,
            damage_spec=DamageSpec(potency=200),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1070,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Painflare",
            is_GCD=False,
            damage_spec=DamageSpec(potency=150),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=440,
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Energy Siphon",
            is_GCD=False,
            damage_spec=DamageSpec(potency=100),
            timing_spec=instant_timing_spec,
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ruin III",
            is_GCD=True,
            damage_spec=DamageSpec(potency=310),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock= smn_caster_tax_ms,
                application_delay=800,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Astral Impulse",
            is_GCD=True,
            damage_spec=DamageSpec(potency=440),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=670,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Astral Flare",
            is_GCD=True,
            damage_spec=DamageSpec(potency=180),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=540,
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Deathflare",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=500)},
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ruin IV",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=430)},
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Searing Light",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                damage_mult=1.03, duration=30 * 1000, is_party_effect=True
            ),
            timing_spec=instant_timing_spec,
        )
    )

    akh_morn_for_follow_up = FollowUp(
        skill=Skill(
            name="Akh Morn (pet)",
            is_GCD=False,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=1300,
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
        primary_target_only=False
    )

    skill_library.add_skill(
        Skill(
            name="Enkindle Bahamut",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(akh_morn_for_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Akh Morn",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(akh_morn_for_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ruby Rite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=510),
            timing_spec=TimingSpec(
                base_cast_time=2800,
                gcd_base_recast_time=3000,
                animation_lock= smn_caster_tax_ms,
                application_delay=620,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Topaz Rite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=330),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                animation_lock=base_animation_lock,
                application_delay=620,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Emerald Rite",
            is_GCD=True,
            damage_spec=DamageSpec(potency=230),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=base_animation_lock,
                application_delay=620,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tri-disaster",
            is_GCD=True,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock= smn_caster_tax_ms,
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fountain of Fire",
            is_GCD=True,
            damage_spec=DamageSpec(potency=540),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1070,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Brand of Purgatory",
            is_GCD=True,
            damage_spec=DamageSpec(potency=240),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
        )
    )
    revelation_follow_up = FollowUp(
        Skill(
            name="Revelation (pet)",
            is_GCD=False,
            status_effect_denylist=("Dragon Sight",),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=1300,
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
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Enkindle Phoenix",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(revelation_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Revelation",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(revelation_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Ruby Catastrophe",
            is_GCD=True,
            damage_spec=DamageSpec(potency=210),
            timing_spec=TimingSpec(
                base_cast_time=2800,
                gcd_base_recast_time=3000,
                animation_lock= smn_caster_tax_ms,
                application_delay=535,
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Topaz Catastrophe",
            is_GCD=True,
            damage_spec=DamageSpec(potency=140),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                animation_lock= base_animation_lock,
                application_delay=535,
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Emerald Catastrophe",
            is_GCD=True,
            damage_spec=DamageSpec(potency=100),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=base_animation_lock,
                application_delay=535,
            ),
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Crimson Cyclone",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=430)},
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Crimson Strike",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=430)},
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=760,
            ),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Mountain Buster",
            is_GCD=False,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=150)},
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=760,
            ),
            has_aoe=True,
            aoe_dropoff=0.7,
        )
    )

    slipstream_dot = Skill(
        name="Slipstream (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=30, damage_class=DamageClass.MAGICAL_DOT),
        has_aoe=True,
    )
    slipstream_follow_up = FollowUp(
        skill=slipstream_dot,
        delay_after_parent_application=0,
        dot_duration=15 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=False,
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Slipstream",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=430)},
            timing_spec=TimingSpec(
                base_cast_time=3000,
                gcd_base_recast_time=3500,
                animation_lock= smn_caster_tax_ms,
                application_delay=1020,
            ),
            follow_up_skills=(slipstream_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.65,
        )
    )
    inferno = Skill(
        name="Inferno (pet)",
        is_GCD=True,
        status_effect_denylist=("Dragon Sight",),
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(
                potency=750,
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
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Summon Ifrit II",
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills=(inferno_follow_up,),
        )
    )
    earthen_fury_blast = Skill(
        name="Earthen Fury (pet)",
        is_GCD=True,
        status_effect_denylist=("Dragon Sight",),
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(
                potency=750,
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
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Summon Titan II",
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills=(earthen_fury_follow_up,),
        )
    )
    aerial_blast = Skill(
        name="Aerial Blast (pet)",
        is_GCD=True,
        status_effect_denylist=("Dragon Sight",),
        damage_spec={
            SimConsts.DEFAULT_CONDITION: DamageSpec(
                potency=750,
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
        primary_target_only=False
    )
    skill_library.add_skill(
        Skill(
            name="Summon Garuda II",
            is_GCD=True,
            timing_spec=instant_timing_spec,
            follow_up_skills=(aerial_blast_follow_up,),
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
                    "Ruin III",
                    "Ruby Rite",
                    "Tri-disaster",
                    "Ruby Catastrophe",
                    "Slipstream",
                ),
            ),
        )
    )
    scarlet_flame_skill_for_follow_up = Skill(
        name="Scarlet Flame (pet)",
        is_GCD=False,
        status_effect_denylist=("Dragon Sight",),
        damage_spec=DamageSpec(
            potency=150,
            damage_class=DamageClass.PET,
            pet_job_mod_override=100,
            pet_scalar=0.88,
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Scarlet Flame",
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
    skill_library.add_skill(
        Skill(
            name="Summon Phoenix",
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
    wyrmwave_skill_for_follow_up = Skill(
        name="Wyrmwave (pet)",
        is_GCD=False,
        status_effect_denylist=("Dragon Sight",),
        damage_spec=DamageSpec(
            potency=150,
            damage_class=DamageClass.PET,
            pet_job_mod_override=100,
            pet_scalar=0.88,
        ),
    )
    skill_library.add_skill(
        Skill(
            name="Wyrmwave",
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

    skill_library.add_skill(
        Skill(
            name="Summon Bahamut",
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

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(
            name="Summon Carbuncle",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock= smn_caster_tax_ms,
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
