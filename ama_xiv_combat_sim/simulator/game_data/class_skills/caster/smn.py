import math

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.damage_instance_class import (
    DamageInstanceClass,
)
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.shield_spec import ShieldSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import OffensiveStatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec
from ama_xiv_combat_sim.simulator.specs.trigger_spec import TriggerSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.caster.smn_data import (
    all_smn_skills,
)


class SmnSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_smn_skills)
        self._job_class = "SMN"
        self.__smn_caster_tax_ms = 100
        self.__base_animation_lock = 600
        self.__smn_instant_timing_spec = TimingSpec(
            base_cast_time=0, animation_lock=self.__base_animation_lock
        )

    @GenericJobClass.is_a_skill
    def auto(self):
        name = "Auto"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.AUTO,
            timing_spec=self.auto_timing_spec,
            damage_spec=DamageSpec(
                potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1
            ),
        )

    @GenericJobClass.is_a_skill
    def fester(self):
        if self._level >= 92:
            return None
        name = "Fester"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=930,
            ),
        )

    @GenericJobClass.is_a_skill
    def energy_drain(self):
        name = "Energy Drain"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock + self.__smn_caster_tax_ms,
                application_delay=1070,
            ),
        )

    @GenericJobClass.is_a_skill
    def painflare(self):
        name = "Painflare"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock + self.__smn_caster_tax_ms,
                application_delay=440,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def energy_siphon(self):
        name = "Energy Siphon"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1020,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def ruin_iii(self):
        name = "Ruin III"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "Aethercharge": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_aethercharge"
                    )
                ),
            },
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__smn_caster_tax_ms,
                application_delay=800,
            ),
        )

    @GenericJobClass.is_a_skill
    def astral_impulse(self):
        name = "Astral Impulse"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=670,
            ),
        )

    @GenericJobClass.is_a_skill
    def astral_flare(self):
        name = "Astral Flare"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=540,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def deathflare(self):
        name = "Deathflare"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def ruin_iv(self):
        name = "Ruin IV"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def searing_light(self):
        name = "Searing Light"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                damage_mult=self._skill_data.get_skill_data(name, "damage_mult"),
                duration=self._skill_data.get_skill_data(name, "duration"),
                is_party_effect=True,
            ),
            timing_spec=self.__smn_instant_timing_spec,
        )

    def __get_akh_morn_for_follow_up(self):
        name = "Akh Morn (pet)"
        return FollowUp(
            skill=Skill(
                name=name,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                        pet_scalar=0.88,
                    )
                },
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=0,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

    @GenericJobClass.is_a_skill
    def enkindle_bahamut(self):
        name = "Enkindle Bahamut"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(self.__get_akh_morn_for_follow_up(),),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def akh_morn(self):
        name = "Akh Morn"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(self.__get_akh_morn_for_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def ruby_rite(self):
        name = "Ruby Rite"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2800,
                gcd_base_recast_time=3000,
                animation_lock=self.__smn_caster_tax_ms,
                application_delay=620,
            ),
        )

    @GenericJobClass.is_a_skill
    def topaz_rite(self):
        name = "Topaz Rite"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                animation_lock=self.__base_animation_lock,
                application_delay=620,
            ),
        )

    @GenericJobClass.is_a_skill
    def emerald_rite(self):
        name = "Emerald Rite"
        # Recast really isn't affected by sps for some reason. You can check this in-game.
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=self.__base_animation_lock,
                application_delay=620,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
        )

    @GenericJobClass.is_a_skill
    def tri_disaster(self):
        name = "Tri-disaster"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__base_animation_lock,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def fountain_of_fire(self):
        name = "Fountain of Fire"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=1070,
            ),
        )

    @GenericJobClass.is_a_skill
    def brand_of_purgatory(self):
        name = "Brand of Purgatory"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
        )

    def __get_revelation_follow_up(self):
        name = "Revelation (pet)"
        return FollowUp(
            Skill(
                name=name,
                status_effect_denylist=("Dragon Sight",),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                        pet_scalar=0.88,
                    )
                },
                timing_spec=self.__smn_instant_timing_spec,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=0,
            snapshot_buffs_with_parent=0,
            snapshot_debuffs_with_parent=0,
            primary_target_only=False,
        )

    @GenericJobClass.is_a_skill
    def enkindle_phoenix(self):
        name = "Enkindle Phoenix"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(self.__get_revelation_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def revelation(self):
        name = "Revelation"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(self.__get_revelation_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def ruby_catastrophe(self):
        name = "Ruby Catastrophe"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=2800,
                gcd_base_recast_time=3000,
                animation_lock=self.__smn_caster_tax_ms,
                application_delay=535,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def topaz_catastrophe(self):
        name = "Topaz Catastrophe"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=2500,
                animation_lock=self.__base_animation_lock,
                application_delay=535,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def emerald_catastrophe(self):
        # Recast really isn't affected by sps for some reason. You can check this in-game.
        name = "Emerald Catastrophe"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                gcd_base_recast_time=1500,
                animation_lock=self.__base_animation_lock,
                application_delay=535,
                affected_by_speed_stat=False,
                affected_by_haste_buffs=False,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def crimson_cyclone(self):
        name = "Crimson Cyclone"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def crimson_strike(self):
        name = "Crimson Strike"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=760,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def mountain_buster(self):
        name = "Mountain Buster"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=760,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def slipstream(self):
        name = "Slipstream (dot)"
        slipstream_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    damage_class=DamageClass.MAGICAL_DOT,
                ),
                has_aoe=True,
            ),
            delay_after_parent_application=0,
            dot_duration=int(14.99 * 1000),
            snapshot_buffs_with_parent=True,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )
        slipstream_initial_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency(name),
                    damage_class=DamageClass.MAGICAL_DOT,
                ),
                has_aoe=True,
            ),
            delay_after_parent_application=0,
            primary_target_only=False,
        )
        
        name = "Slipstream"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)                    
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=3000,
                gcd_base_recast_time=3500,
                animation_lock=self.__smn_caster_tax_ms,
                application_delay=1020,
            ),
            follow_up_skills=(slipstream_initial_follow_up, slipstream_follow_up,),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def summon_ifrit_ii(self):
        name = "Inferno (pet)"
        # Model the 2.1s snap with this hack. Damage will not come out correctly though.
        inferno_follow_up = FollowUp(
            skill=Skill(
                name=name,
                status_effect_denylist=("Dragon Sight",),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                        pet_scalar=0.88,
                    )
                },
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=2100,
            primary_target_only=False,
        )

        name = "Summon Ifrit II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(inferno_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def summon_titan_ii(self):
        name = "Earthen Fury (pet)"
        # Model the 2.1s snap with this hack. Damage will not come out correctly though.
        earthen_fury_follow_up = FollowUp(
            skill=Skill(
                name=name,
                status_effect_denylist=("Dragon Sight",),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                        pet_scalar=0.88,
                    )
                },
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=2100,
            primary_target_only=False,
        )

        name = "Summon Titan II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(earthen_fury_follow_up,),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def summon_garuda_ii(self):
        name = "Aerial Blast (pet)"
        # Model the 2.1s snap with this hack. Damage will not come out correctly though.
        aerial_blast_follow_up = FollowUp(
            skill=Skill(
                name=name,
                status_effect_denylist=("Dragon Sight",),
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                        pet_scalar=0.88,
                    )
                },
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            delay_after_parent_application=2100,
            primary_target_only=False,
        )

        name = "Summon Garuda II"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(aerial_blast_follow_up,),
        )

    @GenericJobClass.is_a_skill
    def necrotize(self):
        if self._level < 92:
            return None
        name = "Necrotize"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=710,
            ),
        )

    @GenericJobClass.is_a_skill
    def searing_flash(self):
        if self._level < 96:
            return None
        name = "Searing Flash"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
        )

    def __get_scarlet_flame_skill_for_follow_up(self):
        name = "Scarlet Flame (pet)"
        return Skill(
            name=name,
            status_effect_denylist=("Dragon Sight",),
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PET,
                pet_job_mod_override=100,
                pet_scalar=0.88,
            ),
        )

    @GenericJobClass.is_a_skill
    def scarlet_flame(self):
        name = "Scarlet Flame"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            status_effect_denylist=("Dragon Sight",),
            timing_spec=self.auto_timing_spec,
            follow_up_skills=(
                FollowUp(
                    skill=self.__get_scarlet_flame_skill_for_follow_up(),
                    delay_after_parent_application=0,
                    snapshot_buffs_with_parent=False,
                    snapshot_debuffs_with_parent=False,
                ),
            ),
        )

    # This is going to require special treatment because of the naming,
    # but the skill and the buff have the same name and this triggers
    # conditionally.
    @GenericJobClass.is_a_skill
    def rekindle_buff(self):
        name = "Rekindle (Buff)"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            heal_spec=HealSpec(
                hot_potency=200, duration=15 * 1000, is_party_effect=True
            ),
        )

    @GenericJobClass.is_a_skill
    def rekindle(self):
        name = "Rekindle"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,
            skill_type=SkillType.ABILITY,
            heal_spec=HealSpec(potency=400, is_party_effect=True),
            trigger_spec=TriggerSpec(triggers=("Rekindle (Buff)",)),
        )

    @GenericJobClass.is_a_skill
    def lux_solaris(self):
        if self._level < 100:
            return None
        name = "Lux Solaris"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=self.instant_timing_spec,
            skill_type=SkillType.ABILITY,
            heal_spec=HealSpec(potency=500, is_party_effect=True, is_aoe=True),
        )

    # Convenience for logs parsing
    @GenericJobClass.is_a_skill
    def everlasting_flight(self):
        name = "Everlasting Flight"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            heal_spec=HealSpec(
                hot_potency=100, duration=21 * 1000, is_party_effect=True, is_aoe=True
            ),
        )

    @GenericJobClass.is_a_skill
    def summon_phoenix(self):
        name = "Summon Phoenix"
        scarlet_flame_skill_for_follow_up = (
            self.__get_scarlet_flame_skill_for_follow_up()
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
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
                    FollowUp(
                        skill=self.everlasting_flight(),
                        delay_after_parent_application=0,
                    ),
                ),
                "Manual": (
                    FollowUp(
                        skill=self.everlasting_flight(),
                        delay_after_parent_application=0,
                    ),
                ),
            },
        )

    def __get_wyrmwave_skill_for_follow_up(self):
        name = "Wyrmwave (pet)"
        return Skill(
            name=name,
            status_effect_denylist=("Dragon Sight",),
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PET,
                pet_job_mod_override=100,
                pet_scalar=0.88,
            ),
        )

    @GenericJobClass.is_a_skill
    def wyrmwave(self):
        name = "Wyrmwave"
        return (
            Skill(
                name=name,
                is_GCD=False,
                skill_type=SkillType.ABILITY,
                timing_spec=self.auto_timing_spec,
                follow_up_skills=(
                    FollowUp(
                        skill=self.__get_wyrmwave_skill_for_follow_up(),
                        delay_after_parent_application=0,
                        snapshot_buffs_with_parent=False,
                        snapshot_debuffs_with_parent=False,
                    ),
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def summon_bahamut(self):
        name = "Summon Bahamut"
        wyrmwave_skill_for_follow_up = self.__get_wyrmwave_skill_for_follow_up()
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
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

    @GenericJobClass.is_a_skill
    def luxwave(self, display_name="Luxwave"):
        if self._level < 100:
            return None
        return Skill(
            name=display_name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency("Luxwave"),
                damage_class=DamageClass.PET,
                pet_job_mod_override=100,
                pet_scalar=0.88,
            ),
            timing_spec=self.auto_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def summon_solar_bahamut(self):
        if self._level < 100:
            return None
        name = "Summon Solar Bahamut"
        # hack for aligning
        luxwave_skill_for_follow_up = self.luxwave(display_name="Luxwave (pet)")
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
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

    @GenericJobClass.is_a_skill
    def umbral_impulse(self):
        if self._level < 100:
            return None
        name = "Umbral Impulse"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=800,
            ),
        )

    @GenericJobClass.is_a_skill
    def umbral_flare(self):
        if self._level < 100:
            return None
        name = "Umbral Flare"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=530,
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def sunflare(self):
        if self._level < 100:
            return None
        name = "Sunflare"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0,
                animation_lock=self.__base_animation_lock,
                application_delay=800,
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    def __get_exodus_follow_up(self):
        if self._level < 100:
            return None
        name = "Exodus (pet)"
        return FollowUp(
            skill=Skill(
                name=name,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name),
                        damage_class=DamageClass.PET,
                        pet_job_mod_override=100,
                        pet_scalar=0.88,
                    )
                },
                timing_spec=self.__smn_instant_timing_spec,
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=0,
            snapshot_buffs_with_parent=False,
            snapshot_debuffs_with_parent=False,
            primary_target_only=False,
        )

    @GenericJobClass.is_a_skill
    def exodus(self):
        if self._level < 100:
            return None
        display_name = "Exodus"
        return Skill(
            name=display_name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(self.__get_exodus_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def enkindle_solar_bahamut(self):
        if self._level < 100:
            return None
        name = "Enkindle Solar Bahamut"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__smn_instant_timing_spec,
            follow_up_skills=(self.__get_exodus_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def physick(self):
        name = "Physick"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500, animation_lock=self.__base_animation_lock
            ),
            heal_spec=HealSpec(potency=400, is_party_effect=True),
        )

    @GenericJobClass.is_a_skill
    def radiant_aegis(self):
        name = "Radiant Aegis"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            shield_spec=ShieldSpec(
                shield_on_max_hp=0.2, duration=30 * 1000, is_party_effect=False
            ),
        )

    @GenericJobClass.is_a_skill
    def addle(self):
        name = "Addle"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_debuff_spec=DefensiveStatusEffectSpec(
                damage_reductions=(
                    {
                        DamageInstanceClass.PHYSICAL: 0.05,
                        DamageInstanceClass.MAGICAL: 0.1,
                    }
                ),
                duration=15 * 1000,
                is_party_effect=True,
            ),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def aethercharge(self):
        name = "Aethercharge"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=15 * 1000,
                num_uses=1,
                add_to_skill_modifier_condition=True,
                skill_allowlist=("Ruin III",),
            ),
        )

    @GenericJobClass.is_a_skill
    def swiftcast(self):
        name = "Swiftcast"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.__smn_instant_timing_spec,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                flat_cast_time_reduction=math.inf,
                duration=10 * 1000,
                num_uses=1,
                skill_allowlist=(
                    "Ruin III",
                    "Ruby Rite",
                    "Tri-disaster",
                    "Ruby Catastrophe",
                    "Slipstream",
                    "Physick",
                ),
            ),
        )

    @GenericJobClass.is_a_skill
    def summon_carbuncle(self):
        name = "Summon Carbuncle"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=TimingSpec(
                base_cast_time=1500,
                animation_lock=self.__smn_caster_tax_ms,
            ),
        )

    @GenericJobClass.is_a_skill
    def summon_ifrit(self):
        name = "Summon Ifrit"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def summon_titan(self):
        name = "Summon Titan"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def summon_garuda(self):
        name = "Summon Garuda"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def astral_flow(self):
        name = "Astral Flow"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            timing_spec=self.__smn_instant_timing_spec,
        )
