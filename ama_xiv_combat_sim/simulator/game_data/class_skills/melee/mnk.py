import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.mnk_data import (
    all_mnk_skills,
)


def add_mnk_skills(skill_library):
    version = skill_library.get_version()
    level = skill_library.get_level()

    all_mnk_skills.set_version(version)
    level = skill_library.get_level()
    all_mnk_skills.set_level(level)

    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("MNK")

    if level in [90]:
        name = "_Disciplined Fist buff"
        _disciplined_fist_follow_up = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.15, duration=int(14.97 * 1000)
                ),
            ),
            delay_after_parent_application=0,
        )

    if level in [90]:
        name = "Leaden Fist"
        leaden_fist_follow_up = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30 * 1000,
                    skill_allowlist=("Bootshine",),
                ),
            ),
            delay_after_parent_application=0,
        )

    if level in [100]:
        name = "Raptor's Fury"
        raptor_fury_follow_up = FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    num_uses=all_mnk_skills.get_skill_data(name, "num_uses"),
                    duration=math.inf,
                    add_to_skill_modifier_condition=True,
                    skill_allowlist=all_mnk_skills.get_skill_data(name, "allowlist"),
                ),
            ),
            delay_after_parent_application=0,
        )

    if level in [100]:
        name = "Coeurl's Fury"
        coeurl_fury_follow_up = FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    num_uses=all_mnk_skills.get_skill_data(name, "num_uses"),
                    duration=math.inf,
                    add_to_skill_modifier_condition=True,
                    skill_allowlist=all_mnk_skills.get_skill_data(name, "allowlist"),
                ),
            ),
            delay_after_parent_application=0,
        )

    if level in [100]:
        name = "Opo-opo's Fury"
        opo_opo_fury_follow_up = FollowUp(
            skill=Skill(
                name=name,
                buff_spec=StatusEffectSpec(
                    num_uses=all_mnk_skills.get_skill_data(name, "num_uses"),
                    duration=math.inf,
                    add_to_skill_modifier_condition=True,
                    skill_allowlist=all_mnk_skills.get_skill_data(name, "allowlist"),
                ),
            ),
            delay_after_parent_application=0,
        )

    name = "Opo-opo Form"
    opo_opo_form_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                max_num_uses=3,
                duration=30 * 1000,
                skill_allowlist=all_mnk_skills.get_skill_data(name, "allowlist"),
            ),
        ),
        delay_after_parent_application=0,
    )

    name = "Formless Fist"
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
                skill_allowlist=all_mnk_skills.get_skill_data(name, "allowlist"),
            ),
        )
    )

    name = "Formless Fist"
    formless_fist_follow_up = FollowUp(
        skill=Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=all_mnk_skills.get_skill_data(name, "allowlist"),
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True,
    )

    name = "Auto"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90,
                damage_class=DamageClass.AUTO,
                trait_damage_mult_override=1,
            ),
        )
    )

    if level in [90]:
        name = "Bootshine"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_mnk_skills.get_potency(name)
                    ),
                    "Leaden Fist": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(
                            name, "potency_leaden_fist"
                        )
                    ),
                    "Opo-opo Form": DamageSpec(
                        potency=all_mnk_skills.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Leaden Fist, Opo-opo Form": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(
                            name, "potency_leaden_fist"
                        ),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist": DamageSpec(
                        potency=all_mnk_skills.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Leaden Fist": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(
                            name, "potency_leaden_fist"
                        ),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Opo-opo Form": DamageSpec(
                        potency=all_mnk_skills.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Leaden Fist, Opo-opo Form": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(
                            name, "potency_leaden_fist"
                        ),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=1110,
                    gcd_base_recast_time=2000,
                ),
            )
        )
    if level in [90]:
        name = "True Strike"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=800,
                    gcd_base_recast_time=2000,
                ),
            )
        )

    if level in [90]:
        name = "Snap Punch"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_mnk_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_mnk_skills.get_potency_no_positional(name)
                    ),
                    "Formless Fist": DamageSpec(
                        potency=all_mnk_skills.get_potency(name)
                    ),
                    "Formless Fist, No Positional": DamageSpec(
                        potency=all_mnk_skills.get_potency_no_positional(name)
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=760,
                    gcd_base_recast_time=2000,
                ),
                follow_up_skills=(opo_opo_form_follow_up,),
            )
        )

    name = "Twin Snakes"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=840,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(
                (_disciplined_fist_follow_up,)
                if level in [90]
                else (raptor_fury_follow_up,)
            ),
        )
    )

    if level in [90]:
        name = "Demolish (dot)"
        demolish_follow_up = FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(
                    potency=all_mnk_skills.get_potency(name),
                    damage_class=DamageClass.PHYSICAL_DOT,
                ),
            ),
            delay_after_parent_application=0,
            dot_duration=18 * 1000,
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=True,
        )

    if level in [100]:
        name = "Demolish"
        demolish_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_mnk_skills.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=all_mnk_skills.get_potency_no_positional(name)
                    ),
                },
            ),
            delay_after_parent_application=1600,
        )

    name = "Demolish"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=all_mnk_skills.get_skill_data(name, "damage_spec"),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=all_mnk_skills.get_skill_data(
                    name, "primary_application_delay"
                ),
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(
                (demolish_follow_up, opo_opo_form_follow_up)
                if level in [90]
                else (
                    demolish_damage_follow_up,
                    opo_opo_form_follow_up,
                    coeurl_fury_follow_up,
                )
            ),
        )
    )

    name = "Rockbreaker"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=940,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(opo_opo_form_follow_up,),
            has_aoe=True,
        )
    )

    name = "Four-point Fury"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=970,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(
                (_disciplined_fist_follow_up,) if level in [90] else tuple()
            ),
            has_aoe=True,
        )
    )

    name = "Dragon Kick"
    if level in [90]:
        dragon_follow_up = {
            SimConsts.DEFAULT_CONDITION: tuple(),
            "Opo-opo Form": (leaden_fist_follow_up,),
            "Formless Fist": (leaden_fist_follow_up,),
            "Formless Fist, Opo-opo Form": (leaden_fist_follow_up,),
        }
    else:
        if version in [7.0]:
            dragon_follow_up = (opo_opo_fury_follow_up,)
        else:
            dragon_follow_up = {
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Opo-opo Form": (opo_opo_fury_follow_up,),
                "Formless Fist": (opo_opo_fury_follow_up,),
                "Formless Fist, Opo-opo Form": (opo_opo_fury_follow_up,),
            }

    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1290,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=dragon_follow_up,
        )
    )

    name = "The Forbidden Chakra"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1420
            ),
        )
    )

    name = "Elixir Field"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1070,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(formless_fist_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.7,
        )
    )

    name = "Celestial Revolution"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=890,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(formless_fist_follow_up,),
        )
    )

    name = "Riddle of Fire"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,  # Does apply instantly it seems.
            # Riddle of fire seems to last ~0.7-0.8s longer than advertised
            buff_spec=StatusEffectSpec(
                damage_mult=all_mnk_skills.get_skill_data(name, "damage_mult"),
                duration=all_mnk_skills.get_skill_data(name, "duration"),
            ),
        )
    )

    name = "Brotherhood"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            # Self is about 800ms after, following is 133-134 in order
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            buff_spec=StatusEffectSpec(
                damage_mult=all_mnk_skills.get_skill_data(name, "damage_mult"),
                duration=all_mnk_skills.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
        )
    )

    name = "Riddle of Wind"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,  # Does apply instantly it seems.
            # Riddle of wind seems to last ~0.8s longer than advertised
            buff_spec=StatusEffectSpec(
                auto_attack_delay_reduction=0.50,
                duration=all_mnk_skills.get_skill_data(name, "duration"),
            ),
        )
    )

    name = "Enlightenment"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
        )
    )

    name = "Six-sided Star"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=all_mnk_skills.get_skill_data(name, "damage_spec"),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=4000,
            ),
        )
    )

    name = "Shadow of the Destroyer"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=all_mnk_skills.get_potency(name)
                ),
                "Opo-opo Form": DamageSpec(
                    potency=all_mnk_skills.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist": DamageSpec(
                    potency=all_mnk_skills.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist, Opo-opo Form": DamageSpec(
                    potency=all_mnk_skills.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=400,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
        )
    )

    name = "Rising Phoenix"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=760,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(formless_fist_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.7,
        )
    )

    name = "Phantom Rush"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=400,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(formless_fist_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.5,
        )
    )

    if level in [100]:
        name = "Leaping Opo"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_mnk_skills.get_potency(name)
                    ),
                    "Opo-opo Form": DamageSpec(
                        potency=all_mnk_skills.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist": DamageSpec(
                        potency=all_mnk_skills.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Opo-opo Form": DamageSpec(
                        potency=all_mnk_skills.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    # Add in opo
                    "Opo-opo's Fury": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(name, "potency_fury")
                    ),
                    "Opo-opo's Fury, Opo-opo Form": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(name, "potency_fury"),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Opo-opo's Fury": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(name, "potency_fury"),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Opo-opo Form, Opo-opo's Fury": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(name, "potency_fury"),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=620,
                    gcd_base_recast_time=2000,
                ),
            )
        )

    if level in [100]:
        name = "Rising Raptor"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_mnk_skills.get_potency(name)
                    ),
                    "Raptor's Fury": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(name, "potency_fury")
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=890,
                    gcd_base_recast_time=2000,
                ),
            )
        )

    if level in [100]:
        name = "Pouncing Coeurl"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=all_mnk_skills.get_potency(name),
                        use_min_potency=all_mnk_skills.get_skill_data(
                            name, "min_potency"
                        ),
                    ),
                    "Coeurl's Fury": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(name, "potency_fury"),
                        use_min_potency=all_mnk_skills.get_skill_data(
                            name, "min_potency_fury"
                        ),
                    ),
                    "No Positional": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(name, "potency_no_pos"),
                        use_min_potency=all_mnk_skills.get_skill_data(
                            name, "min_potency"
                        ),
                    ),
                    "Coeurl's Fury, No Positional": DamageSpec(
                        potency=all_mnk_skills.get_skill_data(
                            name, "potency_no_pos_fury"
                        ),
                        use_min_potency=all_mnk_skills.get_skill_data(
                            name, "min_potency_fury"
                        ),
                    ),
                },
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=1020,
                    gcd_base_recast_time=2000,
                ),
                follow_up_skills=(opo_opo_form_follow_up,),
            )
        )

    if level in [100]:
        name = "Elixir Burst"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=1420,
                    gcd_base_recast_time=2000,
                ),
                follow_up_skills=(formless_fist_follow_up,),
                has_aoe=True,
                aoe_dropoff=0.7,
            )
        )

    if level in [100]:
        name = "Wind's Reply"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=1200,
                    gcd_base_recast_time=2000,
                ),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    if level in [100]:
        name = "Fire's Reply"
        skill_library.add_skill(
            Skill(
                name=name,
                is_GCD=True,
                damage_spec=DamageSpec(potency=all_mnk_skills.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0,
                    animation_lock=650,
                    application_delay=1420,
                    gcd_base_recast_time=2000,
                ),
                follow_up_skills=(formless_fist_follow_up,),
                has_aoe=True,
                aoe_dropoff=0.5,
            )
        )

    name = "Perfect Balance"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=instant_timing_spec,  # Does apply instantly it seems.
            follow_up_skills=(
                opo_opo_form_follow_up,
                opo_opo_form_follow_up,
                opo_opo_form_follow_up,
            ),
        )
    )

    name = "Form Shift"
    skill_library.add_skill(
        Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, gcd_base_recast_time=2000),
            follow_up_skills=(formless_fist_follow_up,),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(
        Skill(name="Steeled Meditation", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(
            name="Inspirited Meditation", is_GCD=False, timing_spec=instant_timing_spec
        )
    )
    skill_library.add_skill(
        Skill(
            name="Forbidden Meditation", is_GCD=False, timing_spec=instant_timing_spec
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enlightened Meditation", is_GCD=False, timing_spec=instant_timing_spec
        )
    )

    skill_library.add_skill(
        Skill(name="True North", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Meditation", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Thunderclap", is_GCD=False, timing_spec=instant_timing_spec)
    )

    return skill_library
