import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.job_resource_settings import JobResourceSettings
from ama_xiv_combat_sim.simulator.specs.job_resource_spec import JobResourceSpec
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.pct_data import (
    all_pct_skills,
)


class PctSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_pct_skills)
        self._job_class = "PCT"
        self.__pct_caster_tax_ms = 100
        self.__base_animation_lock = 600
        self.__pct_instant_timing_spec = TimingSpec(
            base_cast_time=0, animation_lock=self.__base_animation_lock
        )
        self.__aetherhue_skills = (
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

    @GenericJobClass.is_a_resource
    def hyperphantasia(self):
        name = "Hyperphantasia"
        job_resource_settings = JobResourceSettings(
            max_value=5, skill_allowlist=self.__aetherhue_skills
        )

        return (name, job_resource_settings)

    def __get_rainbow_bright_follow_up(self):
        name = "Rainbow Bright"
        return FollowUp(
            skill=Skill(
                name=name,
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
    def fire_in_red(self):
        name = "Fire in Red"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=840,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
        )

    @GenericJobClass.is_a_skill
    def aero_in_freen(self):
        name = "Aero in Green"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=890,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
        )

    @GenericJobClass.is_a_skill
    def water_in_blue(self):
        name = "Water in Blue"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=980,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
        )

    @GenericJobClass.is_a_skill
    def fire_ii_in_red(self):
        name = "Fire II in Red"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=840,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def mog_of_the_ages(self):
        name = "Mog of the Ages"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1150,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def pom_muse(self):
        name = "Pom Muse"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=620,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def winged_muse(self):
        name = "Winged Muse"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=980,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def aero_ii_in_green(self):
        name = "Aero II in Green"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=890,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def water_ii_in_blue(self):
        name = "Water II in Blue"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=980,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def hammer_stamp(self):
        name = "Hammer Stamp"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1380,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def blizzard_in_cyan(self):
        name = "Blizzard in Cyan"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=750,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def blizzard_ii_in_cyan(self):
        name = "Blizzard II in Cyan"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=750,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
        )

    @GenericJobClass.is_a_skill
    def stone_in_yellow(self):
        name = "Stone in Yellow"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=800,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
        )

    @GenericJobClass.is_a_skill
    def thunder_in_magenta(self):
        name = "Thunder in Magenta"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=850,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
        )

    @GenericJobClass.is_a_skill
    def stone_ii_in_yellow(self):
        name = "Stone II in Yellow"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=800,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def thunder_ii_in_magenta(self):
        name = "Thunder II in Magenta"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2300,
                animation_lock=self.__pct_caster_tax_ms,
                application_delay=850,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def starry_muse(self):
        inspiration_follow_up = FollowUp(
            skill=Skill(
                name="Inspiration",
                buff_spec=StatusEffectSpec(
                    duration=30 * 1000,
                    num_uses=5,
                    haste_time_reduction=0.25,
                    skill_allowlist=self.__aetherhue_skills,
                ),
            ),
            delay_after_parent_application=0,
        )

        name = "Starry Muse"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=0,
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
            off_class_default_condition="Buff Only",
        )

    @GenericJobClass.is_a_skill
    def holy_in_white(self):
        name = "Holy in White"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1340,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def hammer_brush(self):
        name = "Hammer Brush"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1250,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def polishing_hammer(self):
        name = "Polishing Hammer"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                guaranteed_crit=ForcedCritOrDH.FORCE_YES,
                guaranteed_dh=ForcedCritOrDH.FORCE_YES,
            ),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=2100,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def comet_in_black(self):
        name = "Comet in Black"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1870,
                gcd_base_recast_time=3300,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def rainbow_drip(self):
        if self._level < 92:
            return None
        name = "Rainbow Drip"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=4000,
                    animation_lock=self.__pct_caster_tax_ms,
                    application_delay=1240,
                    gcd_base_recast_time=6000,
                ),
                "Rainbow Bright": TimingSpec(
                    base_cast_time=0,
                    animation_lock=self.__base_animation_lock,
                    application_delay=1240,
                    gcd_base_recast_time=6000,
                ),
            },
            has_aoe=True,
            aoe_dropoff=0.85,
        )

    @GenericJobClass.is_a_skill
    def clawed_muse(self):
        if self._level < 96:
            return None
        name = "Clawed Muse"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=980,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def fanged_muse(self):
        if self._level < 96:
            return None
        name = "Fanged Muse"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1160,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def retribution_of_the_madeen(self):
        if self._level < 96:
            return None
        name = "Retribution of the Madeen"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1300,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def star_prism(self):
        if self._level < 100:
            return None
        name = "Star Prism"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1250,
            ),
            job_resource_spec=(JobResourceSpec(name="Hyperphantasia", change=-1),),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: tuple(),
                "1 Hyperphantasia": (self.__get_rainbow_bright_follow_up(),),
            },
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def swiftcast(self):
        return Skill(
            name="Swiftcast",
            is_GCD=False,
            timing_spec=self.__pct_instant_timing_spec,
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

    @GenericJobClass.is_a_skill
    def tempera_coat(self):
        name = "Tempera Coat"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def smudge(self):
        name = "Smudge"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def creature_motif(self):
        name = "Creature Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def living_muse(self):
        name = "Living Muse"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def pom_motif(self):
        name = "Pom Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def wing_motif(self):
        name = "Wing Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def weapon_motif(self):
        name = "Weapon Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def steel_muse(self):
        name = "Steel Muse"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def hammer_motif(self):
        name = "Hammer Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def striking_muse(self):
        name = "Striking Muse"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def subtractive_palette(self):
        name = "Subtractive Palette"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def landscape_motif(self):
        name = "Landscape Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def scenic_muse(self):
        name = "Scenic Muse"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def starry_sky_motif(self):
        name = "Starry Sky Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def tempera_grassa(self):
        name = "Tempera Grassa"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def claw_motif(self):
        if self._level < 96:
            return None
        name = "Claw Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )

    @GenericJobClass.is_a_skill
    def maw_motif(self):
        if self._level < 96:
            return None
        name = "Maw Motif"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=3000,
                animation_lock=self.__pct_caster_tax_ms,
                gcd_base_recast_time=4000,
                application_delay=650,
            ),
        )
