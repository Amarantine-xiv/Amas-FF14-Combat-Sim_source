import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.convenience_timings import (
    get_auto_timing,
    get_instant_timing_spec,
)
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.melee.mnk_data import (
    all_mnk_skills,
)


class MnkSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_mnk_skills)
        self._job_class = "MNK"

    def __get_disciplined_fist_follow_up(self):
        if self._version >= "7.0":
            return None
        name = "_Disciplined Fist buff"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    damage_mult=1.15, duration=int(14.97 * 1000)
                ),
            ),
            delay_after_parent_application=0,
        )

    def __get_leaden_fist_follow_up(self):
        if self._version >= "7.0":
            return None
        name = "Leaden Fist"
        return FollowUp(
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

    @GenericJobClass.is_a_skill
    def auto(self):
        name = "Auto"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.auto_timing_spec,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )

    @GenericJobClass.is_a_skill
    def twin_snakes(self):
        raptor_fury_follow_up = (
            FollowUp(
                skill=Skill(
                    name="Raptor's Fury",
                    buff_spec=StatusEffectSpec(
                        num_uses=self._skill_data.get_skill_data(
                            "Raptor's Fury", "num_uses"
                        ),
                        duration=math.inf,
                        add_to_skill_modifier_condition=True,
                        skill_allowlist=self._skill_data.get_skill_data(
                            "Raptor's Fury", "allowlist"
                        ),
                    ),
                ),
                delay_after_parent_application=0,
            )
            if self._version >= "7.0"
            else None
        )

        name = "Twin Snakes"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=840,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(
                (raptor_fury_follow_up,)
                if self._version >= "7.0"
                else (self.__get_disciplined_fist_follow_up(),)
            ),
        )

    def __get_opo_opo_form_follow_up(self):
        name = "Opo-opo Form"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    max_num_uses=3,
                    duration=30 * 1000,
                    skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
                ),
            ),
            delay_after_parent_application=0,
        )

    @GenericJobClass.is_a_skill
    def demolish(self):
        name = "Demolish"

        demolish_follow_up = (
            None
            if self._version >= "7.0"
            else FollowUp(
                skill=Skill(
                    name="Demolish (dot)",
                    is_GCD=False,
                    damage_spec=DamageSpec(
                        potency=self._skill_data.get_potency("Demolish (dot)"),
                        damage_class=DamageClass.PHYSICAL_DOT,
                    ),
                ),
                delay_after_parent_application=0,
                dot_duration=18 * 1000,
                snapshot_buffs_with_parent=True,
                snapshot_debuffs_with_parent=True,
            )
        )

        coeurl_fury_follow_up = (
            FollowUp(
                skill=Skill(
                    name="Coeurl's Fury",
                    buff_spec=StatusEffectSpec(
                        num_uses=self._skill_data.get_skill_data(
                            "Coeurl's Fury", "num_uses"
                        ),
                        duration=math.inf,
                        add_to_skill_modifier_condition=True,
                        skill_allowlist=self._skill_data.get_skill_data(
                            "Coeurl's Fury", "allowlist"
                        ),
                    ),
                ),
                delay_after_parent_application=0,
            )
            if self._version >= "7.0"
            else None
        )

        demolish_damage_follow_up = (
            FollowUp(
                skill=Skill(
                    name=name,
                    damage_spec={
                        SimConsts.DEFAULT_CONDITION: DamageSpec(
                            potency=self._skill_data.get_potency(name)
                        ),
                        "No Positional": DamageSpec(
                            potency=self._skill_data.get_potency_no_positional(name)
                        ),
                    },
                ),
                delay_after_parent_application=1600,
            )
            if self._version >= "7.0"
            else None
        )

        opo_opo_form_follow_up = self.__get_opo_opo_form_follow_up()

        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=self._skill_data.get_skill_data(name, "damage_spec"),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=self._skill_data.get_skill_data(
                    name, "primary_application_delay"
                ),
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(
                (
                    demolish_damage_follow_up,
                    opo_opo_form_follow_up,
                    coeurl_fury_follow_up,
                )
                if self._version >= "7.0"
                else (demolish_follow_up, opo_opo_form_follow_up)
            ),
        )

    @GenericJobClass.is_a_skill
    def dragon_kick(self):
        name = "Dragon Kick"

        opo_opo_fury_follow_up = (
            FollowUp(
                skill=Skill(
                    name="Opo-opo's Fury",
                    buff_spec=StatusEffectSpec(
                        num_uses=self._skill_data.get_skill_data(
                            "Opo-opo's Fury", "num_uses"
                        ),
                        duration=math.inf,
                        add_to_skill_modifier_condition=True,
                        skill_allowlist=self._skill_data.get_skill_data(
                            "Opo-opo's Fury", "allowlist"
                        ),
                    ),
                ),
                delay_after_parent_application=0,
            )
            if self._version >= "7.0"
            else None
        )

        if self._version == "6.55":
            leaden_fist_follow_up = self.__get_leaden_fist_follow_up()
            dragon_follow_up = {
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Opo-opo Form": (leaden_fist_follow_up,),
                "Formless Fist": (leaden_fist_follow_up,),
                "Formless Fist, Opo-opo Form": (leaden_fist_follow_up,),
            }
        elif self._version == "7.0":
            dragon_follow_up = (opo_opo_fury_follow_up,)
        else:
            dragon_follow_up = {
                SimConsts.DEFAULT_CONDITION: tuple(),
                "Opo-opo Form": (opo_opo_fury_follow_up,),
                "Formless Fist": (opo_opo_fury_follow_up,),
                "Formless Fist, Opo-opo Form": (opo_opo_fury_follow_up,),
            }

        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1290,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=dragon_follow_up,
        )

    @GenericJobClass.is_a_skill
    def formless_fist(self):
        name = "Formless Fist"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=0, application_delay=0
            ),
            buff_spec=StatusEffectSpec(
                add_to_skill_modifier_condition=True,
                num_uses=1,
                duration=30 * 1000,
                skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
            ),
        )

    def __get_formless_fist_follow_up(self):
        name = "Formless Fist"
        return FollowUp(
            skill=Skill(
                name=name,
                is_GCD=False,
                buff_spec=StatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30 * 1000,
                    skill_allowlist=self._skill_data.get_skill_data(name, "allowlist"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
        )

    @GenericJobClass.is_a_skill
    def bootshine(self):
        if self._level >= 92:
            return None
        name = "Bootshine"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Leaden Fist": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_leaden_fist"
                        )
                    ),
                    "Opo-opo Form": DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Leaden Fist, Opo-opo Form": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_leaden_fist"
                        ),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist": DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Leaden Fist": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_leaden_fist"
                        ),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Opo-opo Form": DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Leaden Fist, Opo-opo Form": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_leaden_fist"
                        ),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                }
                if self._version == "6.55"
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Opo-opo Form": DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist": DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Opo-opo Form": DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    # add in opo
                    "Opo-opo's Fury": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fury"),
                    ),
                    "Opo-opo's Fury, Opo-opo Form": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fury"),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Opo-opo's Fury, Formless Fist": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fury"),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                    "Formless Fist, Opo-opo Form, Opo-opo's Fury": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fury"),
                        guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                    ),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1110,
                gcd_base_recast_time=2000,
            ),
        )

    @GenericJobClass.is_a_skill
    def true_strike(self):
        if self._level >= 92:
            return None
        name = "True Strike"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Raptor's Fury": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fury")
                    ),
                }
                if self._version >= "7.0"
                else DamageSpec(potency=self._skill_data.get_potency(name))
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=800,
                gcd_base_recast_time=2000,
            ),
        )

    @GenericJobClass.is_a_skill
    def snap_punch(self):
        if self._level >= 92:
            return None
        name = "Snap Punch"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=(
                {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                    "Formless Fist": DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Formless Fist, No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                    # add in fury
                    "Coeurl's Fury": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fury")
                    ),
                    "Coeurl's Fury, No Positional": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_fury_no_pos"
                        )
                    ),
                    "Coeurl's Fury, Formless Fist": DamageSpec(
                        potency=self._skill_data.get_skill_data(name, "potency_fury")
                    ),
                    "Coeurl's Fury, Formless Fist, No Positional": DamageSpec(
                        potency=self._skill_data.get_skill_data(
                            name, "potency_fury_no_pos"
                        )
                    ),
                }
                if self._version >= "7.0"
                else {
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                    "Formless Fist": DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    ),
                    "Formless Fist, No Positional": DamageSpec(
                        potency=self._skill_data.get_potency_no_positional(name)
                    ),
                }
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=760,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_opo_opo_form_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def rockbreaker(self):
        name = "Rockbreaker"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=940,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_opo_opo_form_follow_up(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def four_point_fury(self):
        name = "Four-point Fury"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=970,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(
                tuple()
                if self._version >= "7.0"
                else (self.__get_disciplined_fist_follow_up(),)
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def the_forbidden_chakra(self):
        name = "The Forbidden Chakra"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1420
            ),
        )

    @GenericJobClass.is_a_skill
    def elixir_field(self):
        name = "Elixir Field"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1070,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_formless_fist_follow_up(),),
            has_aoe=True,
            aoe_dropoff=0.7,
        )

    @GenericJobClass.is_a_skill
    def celestial_revolution(self):
        name = "Celestial Revolution"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=890,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_formless_fist_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def riddle_of_fire(self):
        name = "Riddle of Fire"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,  # Does apply instantly it seems.
            # Riddle of fire seems to last ~0.7-0.8s longer than advertised
            buff_spec=StatusEffectSpec(
                damage_mult=self._skill_data.get_skill_data(name, "damage_mult"),
                duration=self._skill_data.get_skill_data(name, "duration"),
            ),
        )

    @GenericJobClass.is_a_skill
    def brotherhood(self):
        name = "Brotherhood"
        return Skill(
            name=name,
            is_GCD=False,
            # Self is about 800ms after, following is 133-134 in order
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=800
            ),
            buff_spec=StatusEffectSpec(
                damage_mult=self._skill_data.get_skill_data(name, "damage_mult"),
                duration=self._skill_data.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def riddle_of_wind(self):
        name = "Riddle of Wind"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,  # Does apply instantly it seems.
            # Riddle of wind seems to last ~0.8s longer than advertised
            buff_spec=StatusEffectSpec(
                auto_attack_delay_reduction=0.50,
                duration=self._skill_data.get_skill_data(name, "duration"),
            ),
        )

    @GenericJobClass.is_a_skill
    def enlightenment(self):
        name = "Enlightenment"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=760
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def six_sided_star(self):
        name = "Six-sided Star"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=self._skill_data.get_skill_data(name, "damage_spec"),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=620,
                gcd_base_recast_time=4000,
            ),
        )

    @GenericJobClass.is_a_skill
    def shadow_of_the_destroyer(self):
        name = "Shadow of the Destroyer"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Opo-opo Form": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist, Opo-opo Form": DamageSpec(
                    potency=self._skill_data.get_potency(name),
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

    @GenericJobClass.is_a_skill
    def rising_phoenix(self):
        name = "Rising Phoenix"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=760,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_formless_fist_follow_up(),),
            has_aoe=True,
            aoe_dropoff=0.7,
        )

    @GenericJobClass.is_a_skill
    def phantom_rush(self):
        name = "Phantom Rush"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=400,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_formless_fist_follow_up(),),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def leaping_opo(self):
        if self._level < 92:
            return None
        name = "Leaping Opo"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Opo-opo Form": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist, Opo-opo Form": DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                # Add in opo
                "Opo-opo's Fury": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_fury")
                ),
                "Opo-opo's Fury, Opo-opo Form": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_fury"),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist, Opo-opo's Fury": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_fury"),
                    guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                ),
                "Formless Fist, Opo-opo Form, Opo-opo's Fury": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_fury"),
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

    @GenericJobClass.is_a_skill
    def rising_raptor(self):
        if self._level < 92:
            return None
        name = "Rising Raptor"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Raptor's Fury": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_fury")
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=890,
                gcd_base_recast_time=2000,
            ),
        )

    @GenericJobClass.is_a_skill
    def pouncing_coeurl(self):
        if self._level < 92:
            return None
        name = "Pouncing Coeurl"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    use_min_potency=self._skill_data.get_skill_data(
                        name, "min_potency"
                    ),
                ),
                "Coeurl's Fury": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_fury"),
                    use_min_potency=self._skill_data.get_skill_data(
                        name, "min_potency_fury"
                    ),
                ),
                "No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_no_pos"),
                    use_min_potency=self._skill_data.get_skill_data(
                        name, "min_potency"
                    ),
                ),
                "Coeurl's Fury, No Positional": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_no_pos_fury"
                    ),
                    use_min_potency=self._skill_data.get_skill_data(
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
            follow_up_skills=(self.__get_opo_opo_form_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def elixir_burst(self):
        if self._level < 92:
            return None
        name = "Elixir Burst"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1420,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_formless_fist_follow_up(),),
            has_aoe=True,
            aoe_dropoff=0.7,
        )

    @GenericJobClass.is_a_skill
    def winds_reply(self):
        if self._level < 96:
            return None
        name = "Wind's Reply"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1200,
                gcd_base_recast_time=2000,
            ),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def fires_reply(self):
        if self._level < 100:
            return None
        name = "Fire's Reply"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=650,
                application_delay=1420,
                gcd_base_recast_time=2000,
            ),
            follow_up_skills=(self.__get_formless_fist_follow_up(),),
            has_aoe=True,
            aoe_dropoff=0.5,
        )

    @GenericJobClass.is_a_skill
    def perfect_balance(self):
        name = "Perfect Balance"
        opo_opo_form_follow_up = self.__get_opo_opo_form_follow_up()
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,  # Does apply instantly it seems.
            follow_up_skills=(
                opo_opo_form_follow_up,
                opo_opo_form_follow_up,
                opo_opo_form_follow_up,
            ),
        )

    @GenericJobClass.is_a_skill
    def form_shift(self):
        name = "Form Shift"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(base_cast_time=0, gcd_base_recast_time=2000),
            follow_up_skills=(self.__get_formless_fist_follow_up(),),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def steeled_meditation(self):
        name = "Steeled Meditation"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def inspirited_meditation(self):
        name = "Inspirited Meditation"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def forbidden_meditation(self):
        name = "Forbidden Meditation"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def enlightened_meditation(self):
        name = "Enlightened Meditation"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def true_north(self):
        name = "True North"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def meditation(self):
        name = "Meditation"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def thunderclap(self):
        name = "Thunderclap"
        return Skill(name=name, is_GCD=False, timing_spec=self.instant_timing_spec)
