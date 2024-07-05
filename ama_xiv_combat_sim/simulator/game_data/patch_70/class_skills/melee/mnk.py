import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.patch_70.convenience_timings import (
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

    raptor_fury_follow_up = FollowUp(
        skill=Skill(
            name="Raptor's Fury",
            buff_spec=StatusEffectSpec(
                num_uses=2,
                duration=math.inf,
                add_to_skill_modifier_condition=True,
                skill_allowlist=("Rising Raptor",),
            ),
        ),
        delay_after_parent_application=0,
    )
    coeurl_fury_follow_up = FollowUp(
        skill=Skill(
            name="Coeurl's Fury",
            buff_spec=StatusEffectSpec(
                num_uses=3,
                duration=math.inf,
                add_to_skill_modifier_condition=True,
                skill_allowlist=("Pouncing Coeurl",),
            ),
        ),
        delay_after_parent_application=0,
    )
    opo_opo_fury_follow_up = FollowUp(
        skill=Skill(
            name="Opo-opo's Fury",
            buff_spec=StatusEffectSpec(
                num_uses=1,
                duration=math.inf,
                add_to_skill_modifier_condition=True,
                skill_allowlist=("Leaping Opo",),
            ),
        ),
        delay_after_parent_application=0,
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
                'Leaping Opo'
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
                    "Leaping Opo",
                    "Rising Raptor",
                    "Pouncing Coeurl",
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
                    "True Strike",
                    "Snap Punch",
                    "Dragon Kick",
                    "Shadow of the Destroyer",                    
                    "Twin Snakes",
                    "Demolish",
                    "Rockbreaker",
                    "Four-point Fury",
                    "Elixir Burst",
                    "Fire's Reply",
                    "Leaping Opo"
                ),
            ),
        ),
        delay_after_parent_application=0,
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
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=220),
                "Opo-opo Form": DamageSpec(
                    potency=220, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist": DamageSpec(
                    potency=220, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Opo-opo Form": DamageSpec(
                    potency=220, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1110, gcd_base_recast_time=2000
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="True Strike",
            is_GCD=True,
            damage_spec=DamageSpec(potency=290),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800, gcd_base_recast_time=2000
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Snap Punch",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=360),
                "No Positional": DamageSpec(potency=300),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760, gcd_base_recast_time=2000
            ),
            follow_up_skills=(opo_opo_form_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Twin Snakes",
            is_GCD=True,
            damage_spec=DamageSpec(potency=380),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=840, gcd_base_recast_time=2000
            ),
            follow_up_skills=(raptor_fury_follow_up,),
        )
    )
    demolish_damage_follow_up = FollowUp(
        skill=Skill(
            name="Demolish",
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=400),
                "No Positional": DamageSpec(potency=340),
            },
        ),
        delay_after_parent_application=1600,
    )

    skill_library.add_skill(
        Skill(
            name="Demolish",
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0, gcd_base_recast_time=2000
            ),
            follow_up_skills=(demolish_damage_follow_up, opo_opo_form_follow_up, coeurl_fury_follow_up),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rockbreaker",
            is_GCD=True,
            damage_spec=DamageSpec(potency=130),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=940, gcd_base_recast_time=2000
            ),
            follow_up_skills=(opo_opo_form_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Four-point Fury",
            is_GCD=True,
            damage_spec=DamageSpec(potency=120),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=970, gcd_base_recast_time=2000
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Dragon Kick",
            is_GCD=True,
            damage_spec=DamageSpec(potency=320),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290, gcd_base_recast_time=2000
            ),
            follow_up_skills=(opo_opo_fury_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="The Forbidden Chakra",
            is_GCD=False,
            damage_spec=DamageSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1480
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Elixir Field",
            is_GCD=True,
            damage_spec=DamageSpec(potency=800),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1070, gcd_base_recast_time=2000
            ),
            follow_up_skills=(formless_fist_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Celestial Revolution",
            is_GCD=True,
            damage_spec=DamageSpec(potency=450),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=890, gcd_base_recast_time=2000
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
                damage_mult=1.05, duration=int(19.95 * 1000), is_party_effect=True
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
        )
    )
    skill_library.add_skill(
        Skill(
            name="Six-sided Star",
            is_GCD=True,
            # can just construct dictionary in a loop, but i am lazy
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=780+5*80),
                         '10 Chakra': DamageSpec(potency=780+10*80),
                         '9 Chakra': DamageSpec(potency=780+9*80),
                         '8 Chakra': DamageSpec(potency=780+8*80),
                         '7 Chakra': DamageSpec(potency=780+7*80),
                         '6 Chakra': DamageSpec(potency=780+6*80),
                         '5 Chakra': DamageSpec(potency=780+5*80),
                         '4 Chakra': DamageSpec(potency=780+4*80),
                         '3 Chakra': DamageSpec(potency=780+3*80),
                         '2 Chakra': DamageSpec(potency=780+2*80),
                         '1 Chakra': DamageSpec(potency=780+1*80),
                         '0 Chakra': DamageSpec(potency=780)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620, gcd_base_recast_time=4000
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
                base_cast_time=0, animation_lock=650, application_delay=400, gcd_base_recast_time=2000
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rising Phoenix",
            is_GCD=True,
            damage_spec=DamageSpec(potency=900),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760, gcd_base_recast_time=2000
            ),
            follow_up_skills=(formless_fist_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Phantom Rush",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=400, gcd_base_recast_time=2000
            ),
            follow_up_skills=(formless_fist_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Leaping Opo",
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(potency=260),
                "Opo-opo Form": DamageSpec(
                    potency=260, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist": DamageSpec(
                    potency=260, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Opo-opo Form": DamageSpec(
                    potency=260, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                # Add in opo
                "Opo-opo's Fury": DamageSpec(potency=460),
                "Opo-opo's Fury, Opo-opo Form": DamageSpec(
                    potency=460, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Opo-opo's Fury": DamageSpec(
                    potency=460, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
                "Formless Fist, Opo-opo Form, Opo-opo's Fury": DamageSpec(
                    potency=460, guaranteed_crit=ForcedCritOrDH.FORCE_YES
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=400, gcd_base_recast_time=2000
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Rising Raptor",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=330),
                         "Raptor's Fury": DamageSpec(potency=480)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760, gcd_base_recast_time=2000
            ),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Pouncing Coeurl",
            is_GCD=True,
            damage_spec={SimConsts.DEFAULT_CONDITION: DamageSpec(potency=400, use_min_potency=340),
                         "Coeurl's Fury": DamageSpec(potency=500, use_min_potency=440),
                         "No Positional":  DamageSpec(potency=340, use_min_potency=340),
                         "Coeurl's Fury, No Positional":  DamageSpec(potency=440, use_min_potency=440)},
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760, gcd_base_recast_time=2000
            ),
            follow_up_skills=(opo_opo_form_follow_up,)
        )
    )
    skill_library.add_skill(
        Skill(
            name="Elixir Burst",
            is_GCD=True,
            damage_spec=DamageSpec(potency=900),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=400, gcd_base_recast_time=2000
            ),
            follow_up_skills=(formless_fist_follow_up,),
        )
    )
    skill_library.add_skill(
        Skill(
            name="Wind's Reply",
            is_GCD=True,
            damage_spec=DamageSpec(potency=800),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=400, gcd_base_recast_time=2000
            )
        )
    )
    skill_library.add_skill(
        Skill(
            name="Fire's Reply",
            is_GCD=True,
            damage_spec=DamageSpec(potency=1100),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=400, gcd_base_recast_time=2000
            ),
            follow_up_skills=(formless_fist_follow_up,),
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
        Skill(name="Inspirited Meditation", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Forbidden Meditation", is_GCD=False, timing_spec=instant_timing_spec)
    )
    skill_library.add_skill(
        Skill(name="Enlightened Meditation", is_GCD=False, timing_spec=instant_timing_spec)
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
