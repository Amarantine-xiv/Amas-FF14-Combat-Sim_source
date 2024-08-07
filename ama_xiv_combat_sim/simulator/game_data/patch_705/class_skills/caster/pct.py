import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
    get_auto_timing,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def add_pct_skills(skill_library):
    auto_timing = get_auto_timing()

    pct_caster_tax_ms = 100
    base_animation_lock = 600
    instant_timing_spec = TimingSpec(
        base_cast_time=0, animation_lock=base_animation_lock
    )
    skill_library.set_current_job_class("PCT")

    rainbow_bright_follow_up = FollowUp(
        skill=Skill(
            name="Rainbow Bright",
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                flat_gcd_recast_time_reduction=3500,
                skill_allowlist=("Rainbow Drip",),
            ),
        ),
        delay_after_parent_application=0,
    )

    aetherhue_skills = (
        "Starry Muse",
        "Fire in Red",
        "Aero in Green",
        "Water in Blue",
        "Fire II in Red",
        "Aero II in Green",
        "Water II in Blue",
        "Blizzard in Cyan",
        "Blizzard II in Cyan",
        "Stone in Yellow",
        "Stone II in Yellow",
        "Thunder in Magenta",
        "Thunder II in Magenta",
        "Holy in White",
        "Comet in Black",
        "Star Prism",
    )

    inspiration_follow_up = FollowUp(
        skill=Skill(
            name="Inspiration",
            buff_spec=StatusEffectSpec(
                duration=30 * 1000,
                num_uses=5,
                haste_time_reduction=0.25,
                skill_allowlist=aetherhue_skills,
            ),
        ),
        delay_after_parent_application=0,
    )

    skill_library.add_resource(
        name="Hyperphantasia",
        job_resource_settings=JobResourceSettings(
            max_value=5, skill_allowlist=aetherhue_skills
        ),
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
            name="Fire in Red",
            is_GCD=True,
            damage_spec=DamageSpec(potency=440),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=pct_caster_tax_ms,
                application_delay=840,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Aero in Green",
            is_GCD=True,
            damage_spec=DamageSpec(potency=480),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=pct_caster_tax_ms,
                application_delay=890,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Water in Blue",
            is_GCD=True,
            damage_spec=DamageSpec(potency=520),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=pct_caster_tax_ms,
                application_delay=980,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
        )
    )

    skill_library.add_skill(
        Skill(
            name="Fire II in Red",
            is_GCD=True,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=pct_caster_tax_ms,
                application_delay=840,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Mog of the Ages",
            is_GCD=False,
            damage_spec=DamageSpec(potency=1300),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1150,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Pom Muse",
            is_GCD=False,
            damage_spec=DamageSpec(potency=1100),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=620,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Winged Muse",
            is_GCD=False,
            damage_spec=DamageSpec(potency=1100),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=980,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Aero II in Green",
            is_GCD=True,
            damage_spec=DamageSpec(potency=140),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=pct_caster_tax_ms,
                application_delay=890,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Water II in Blue",
            is_GCD=True,
            damage_spec=DamageSpec(potency=160),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=pct_caster_tax_ms,
                application_delay=980,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hammer Stamp",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=560,
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1380,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blizzard in Cyan",
            is_GCD=True,
            damage_spec=DamageSpec(potency=800),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=pct_caster_tax_ms,
                application_delay=750,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Blizzard II in Cyan",
            is_GCD=True,
            damage_spec=DamageSpec(potency=240),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=pct_caster_tax_ms,
                application_delay=750,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Stone in Yellow",
            is_GCD=True,
            damage_spec=DamageSpec(potency=840),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=pct_caster_tax_ms,
                application_delay=800,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Thunder in Magenta",
            is_GCD=True,
            damage_spec=DamageSpec(potency=880),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=pct_caster_tax_ms,
                application_delay=850,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Stone II in Yellow",
            is_GCD=True,
            damage_spec=DamageSpec(potency=260),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=pct_caster_tax_ms,
                application_delay=800,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Thunder II in Magenta",
            is_GCD=True,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=pct_caster_tax_ms,
                application_delay=850,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
        )
    )

    skill_library.add_skill(
        Skill(
            name="Starry Muse",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=620,
            ),
            buff_spec={
                SimConsts.DEFAULT_CONDITION: StatusEffectSpec(
                    damage_mult=1.05, duration=int(20.35 * 1000), is_party_effect=True
                ),
                "Longest": StatusEffectSpec(
                    damage_mult=1.05, duration=int(21.5 * 1000), is_party_effect=True
                ),
            },
            job_resource_spec={
                SimConsts.DEFAULT_CONDITION: (
                    JobResourceSpec(name="Hyperphantasia", change=5),
                ),
                "Buff Only": tuple(),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (inspiration_follow_up,),
                "Buff Only": tuple(),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="Holy in White",
            is_GCD=True,
            damage_spec=DamageSpec(potency=520),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1340,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hammer Brush",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=620,
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1250,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Polishing Hammer",
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=680,
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=2100,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Comet in Black",
            is_GCD=True,
            damage_spec=DamageSpec(potency=880),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1870,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rainbow Drip",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1000),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=4000,
                    animation_lock=pct_caster_tax_ms,
                    application_delay=1240,
                    gcd_base_recast_time=6000,
                ),
                "Rainbow Bright": TimingSpec(
                    base_cast_time=0,
                    animation_lock=base_animation_lock,
                    application_delay=1240,
                    gcd_base_recast_time=6000
                ),
            },
            has_aoe=True,
            aoe_dropoff=0.85,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Clawed Muse",
            is_GCD=False,
            damage_spec=DamageSpec(potency=1100),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=980,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fanged Muse",
            is_GCD=False,
            damage_spec=DamageSpec(potency=1100),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1160,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Retribution of the Madeen",
            is_GCD=False,
            damage_spec=DamageSpec(potency=1400),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1300,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )
    skill_library.add_skill(
        Skill(
            name="Star Prism",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1400),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=1250,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (rainbow_bright_follow_up,),
            },
            has_aoe=True,
            aoe_dropoff=0.6,
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

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
                    "Fire in Red",
                    "Aero in Green",
                    "Water in Blue",
                    "Fire II in Red",
                    "Creature Motif",
                    "Aero II in Green",
                    "Water II in Blue",
                    "Weapon Motif",
                    "Blizzard in Cyan",
                    "Blizzard II in Cyan",
                    "Stone in Yellow",
                    "Thunder in Magenta",
                    "Stone II in Yellow",
                    "Thunder II in Magenta",
                    "Landscape Motif",
                    "Wing Motif",
                    "Pom Motif",
                    "Claw Motif",
                    "Hammer Motif",
                    "Starry Sky Motif",
                    "Maw Motif",
                    "Rainbow Drip",  # will be consumed under Rainbowbright...bug.
                ),
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Tempera Coat",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Smudge",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Creature Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Living Muse",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Pom Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Wing Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Weapon Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Steel Muse",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Hammer Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Striking Muse",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Subtractive Palette",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )

    skill_library.add_skill(
        Skill(
            name="Landscape Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Scenic Muse",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Starry Sky Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Tempera Grassa",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=base_animation_lock,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Claw Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Maw Motif",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
    )
