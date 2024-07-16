from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.patch_655.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec


def add_mnk_skills(skill_library):
    auto_timing = get_auto_timing()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class("MNK")

    _disciplined_fist_follow_up = FollowUp(
        skill=Skill(
            name="_Disciplined Fist buff",
            is_GCD=False,
            buff_spec=StatusEffectSpec(damage_mult=1.15, duration=int(14.97 * 1000)),
        ),
        delay_after_parent_application=0,
    )
    demolish_dot = Skill(
        name="Demolish (dot)",
        is_GCD=False,
        damage_spec=DamageSpec(potency=70, damage_class=DamageClass.PHYSICAL_DOT),
    )
    demolish_follow_up = FollowUp(
        skill=demolish_dot,
        delay_after_parent_application=0,
        dot_duration=18 * 1000,
        snapshot_buffs_with_parent=True,
        snapshot_debuffs_with_parent=True,
    )

    leaden_fist_skill = Skill(
        name="Leaden Fist",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            duration=30 * 1000,
            skill_allowlist=("Bootshine",),
        ),
    )
    leaden_fist_follow_up = FollowUp(
        skill=leaden_fist_skill, delay_after_parent_application=0
    )
    opo_opo_form_skill = Skill(
        name="Opo-opo Form",
        is_GCD=False,
        buff_spec=StatusEffectSpec(
            add_to_skill_modifier_condition=True,
            num_uses=1,
            max_num_uses=3,
            duration=30 * 1000,
            skill_allowlist=(
                "Bootshine",
                "Dragon Kick",
                "Shadow of the Destroyer",
            ),
        ),
    )
    opo_opo_form_follow_up = FollowUp(
        skill=opo_opo_form_skill, delay_after_parent_application=0
    )

    skill_library.add_skill(
        Skill(
            name="Formless Fist",
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=(
                    "Bootshine",
                    "Dragon Kick",
                    "Shadow of the Destroyer",
                    "True Strike",
                    "Snap Punch",
                    "Twin Snakes",
                    "Demolish",
                    "Rockbreaker",
                    "Four-point Fury",
                ),
            ),
        )
    )

    formless_fist_follow_up = FollowUp(
        skill=Skill(
            name="Formless Fist",
            is_GCD=False,
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=(
                    "Bootshine",
                    "Dragon Kick",
                    "Shadow of the Destroyer",
                    "True Strike",
                    "Snap Punch",
                    "Twin Snakes",
                    "Demolish",
                    "Rockbreaker",
                    "Four-point Fury",
                ),
            ),
        ),
        delay_after_parent_application=0,
        primary_target_only=True
    )

    skill_library.add_skill(
        Skill(
            name="Auto",
            is_GCD=False,
            timing_spec=auto_timing,
            damage_spec=DamageSpec(
                potency=90,
                damage_class=DamageClass.AUTO,
                trait_damage_mult_override=1,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Bootshine",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=210),
                "Leaden Fist": DamageSpec(potency=310),
                "Opo-opo Form": DamageSpec(
                    potency=210, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Leaden Fist, Opo-opo Form": DamageSpec(
                    potency=310, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist": DamageSpec(
                    potency=210, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Leaden Fist": DamageSpec(
                    potency=310, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Opo-opo Form": DamageSpec(
                    potency=210, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Leaden Fist, Opo-opo Form": DamageSpec(
                    potency=310, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1110
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="True Strike",
            is_GCD=True,
            damage_spec=DamageSpec(potency=300),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Snap Punch",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=310),
                "No Positional": DamageSpec(potency=250),
                "Formless Fist": DamageSpec(potency=310),
                "Formless Fist, No Positional": DamageSpec(potency=250),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            follow_up_skills=(opo_opo_form_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Twin Snakes",
            is_GCD=True,
            damage_spec=DamageSpec(potency=280),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=840
            ),
            follow_up_skills=(_disciplined_fist_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Demolish",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=130),
                "No Positional": DamageSpec(potency=70),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1600
            ),
            follow_up_skills=(demolish_follow_up, opo_opo_form_follow_up),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rockbreaker",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=940
            ),
            follow_up_skills=(opo_opo_form_follow_up,),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Four-point Fury",
            is_GCD=True,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=970
            ),
            follow_up_skills=(_disciplined_fist_follow_up,),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Dragon Kick",
            is_GCD=True,
            damage_spec=DamageSpec(potency=320),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Opo-opo Form": (leaden_fist_follow_up,),
                "Formless Fist": (leaden_fist_follow_up,),
                "Formless Fist, Opo-opo Form": (leaden_fist_follow_up,),
            },
        )
    )
    skill_library.add_skill(
        Skill(
            name="The Forbidden Chakra",
            is_GCD=False,
            damage_spec=DamageSpec(potency=340),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1480
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Elixir Field",
            is_GCD=True,
            damage_spec=DamageSpec(potency=600),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070
            ),
            follow_up_skills=(formless_fist_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.7
        )
    )
    skill_library.add_skill(
        Skill(
            name="Celestial Revolution",
            is_GCD=True,
            damage_spec=DamageSpec(potency=450),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890
            ),
            follow_up_skills=(formless_fist_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Riddle of Fire",
            is_GCD=False,
            timing_spec=instant_timing_spec,  # Does apply instantly it seems.
            # Riddle of fire seems to last ~0.7-0.8s longer than advertised
            buff_spec=StatusEffectSpec(damage_mult=1.15, duration=int(20.72 * 1000)),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Brotherhood",
            is_GCD=False,
            # Self is about 800ms after, following is 133-134 in order
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            buff_spec=StatusEffectSpec(
                damage_mult=1.05, duration=int(14.95 * 1000), is_party_effect=True
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Riddle of Wind",
            is_GCD=False,
            timing_spec=instant_timing_spec,  # Does apply instantly it seems.
            # Riddle of wind seems to last ~0.8s longer than advertised
            buff_spec=StatusEffectSpec(
                auto_attack_delay_reduction=0.50, duration=int(15.78 * 1000)
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Enlightenment",
            is_GCD=True,
            damage_spec=DamageSpec(potency=170),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Six-sided Star",
            is_GCD=True,
            damage_spec=DamageSpec(potency=550),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Shadow of the Destroyer",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=110),
                "Opo-opo Form": DamageSpec(
                    potency=110, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist": DamageSpec(
                    potency=110, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Opo-opo Form": DamageSpec(
                    potency=110, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=400
            ),
            has_aoe=True
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rising Phoenix",
            is_GCD=True,
            damage_spec=DamageSpec(potency=700),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            follow_up_skills=(formless_fist_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.7
        )
    )
    skill_library.add_skill(
        Skill(
            name="Phantom Rush",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1150),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=400
            ),
            follow_up_skills=(formless_fist_follow_up,),
            has_aoe=True,
            aoe_dropoff=0.5
        )
    )
    skill_library.add_skill(
        Skill(
            name="Perfect Balance",
            is_GCD=False,
            timing_spec=instant_timing_spec,  # Does apply instantly it seems.
            follow_up_skills=(
                opo_opo_form_follow_up,
                opo_opo_form_follow_up,
                opo_opo_form_follow_up,
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Form Shift",
            is_GCD=False,
            timing_spec=instant_timing_spec,
            follow_up_skills=(formless_fist_follow_up,),
        )
    )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
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
