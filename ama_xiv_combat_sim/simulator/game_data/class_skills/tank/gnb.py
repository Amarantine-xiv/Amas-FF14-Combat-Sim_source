from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.status_effect_spec import StatusEffectSpec
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.gnb_data import (
    all_gnb_skills,
)

class GnbSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_gnb_skills)
        self._job_class = "GNB"

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
    def keen_edge(self):
        name = "Keen Edge"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=0),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=893
            ),
        )
        
    @GenericJobClass.is_a_skill
    def no_mercy(self):
        name = "No Mercy"
        return Skill(
            name=name,
            is_GCD=False,
            buff_spec=StatusEffectSpec(duration=int(19.96 * 1000), damage_mult=1.20),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )
    
    @GenericJobClass.is_a_skill
    def brutal_shell(self):
        name = "Brutal Shell"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Keen Edge",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1074
            ),
        )
        
    @GenericJobClass.is_a_skill
    def demon_slice(self):
        name = "Demon Slice"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=0),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
            has_aoe=True,
        )
    
    @GenericJobClass.is_a_skill
    def lightning_shot(self):
        name = "Lightning Shot"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
        )
    
    @GenericJobClass.is_a_skill
    def solid_barrel(self):
        name = "Solid Barrel"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Brutal Shell",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1653
            ),
        )
        
    @GenericJobClass.is_a_skill
    def burst_strike(self):
        name = "Burst Strike"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=714
            ),
        )
    
    @GenericJobClass.is_a_skill
    def demon_slaughter(self):
        name = "Demon Slaughter"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_group=0, combo_actions=("Demon Slice",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=626
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def sonic_break(self):
        name = "Sonic Break (dot)"
        sonic_break_dot_gnb = Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )
        
        name = "Sonic Break"
        return Skill(
            name=name,
            is_GCD=True,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=581
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=sonic_break_dot_gnb,
                    delay_after_parent_application=0,
                    dot_duration=30 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
        )
        
    @GenericJobClass.is_a_skill
    def rough_divide(self):
        if self._level not in [90]:
            return None
        
        name = "Rough Divide"
        return Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=491
                ),
            )
        
    @GenericJobClass.is_a_skill
    def gnashing_fang(self):
        name = "Gnashing Fang"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
        )
        
    @GenericJobClass.is_a_skill
    def savage_claw(self):
        name = "Savage Claw"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Gnashing Fang",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )
        
    @GenericJobClass.is_a_skill
    def wicked_talon(self):
        name = "Wicked Talon"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Savage Claw",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1162
            ),
        )
        
    @GenericJobClass.is_a_skill
    def bow_shock(self):
        name = "Bow Shock (dot)"
        bow_shock_dot_gnb = Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )
        
        name = "Bow Shock"
        return Skill(
            name=name,
            is_GCD=False,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=627
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=bow_shock_dot_gnb,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True,
        )
    
    @GenericJobClass.is_a_skill
    def jugular_rip(self):
        name = "Jugular Rip"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=802
            ),
        )
    
    @GenericJobClass.is_a_skill
    def abdomen_tear(self):
        name = "Abdomen Tear"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=757
            ),
        )
        
    @GenericJobClass.is_a_skill
    def eye_gouge(self):
        name = "Eye Gouge"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=981
            ),
        )
        
    @GenericJobClass.is_a_skill
    def fated_circle(self):
        name = "Fated Circle"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=537
            ),
            has_aoe=True,
        )
    
    @GenericJobClass.is_a_skill
    def blasting_zone(self):
        name = "Blasting Zone"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=625
            ),
        )
    
    @GenericJobClass.is_a_skill
    def hypervelocity(self):
        name = "Hypervelocity"
        return Skill(
            name=name,
            is_GCD=False,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
        )
    
    @GenericJobClass.is_a_skill
    def double_down(self):
        name = "Double Down"
        return Skill(
            name=name,
            is_GCD=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                )
            },
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=716
            ),
            has_aoe=True,
            aoe_dropoff=0.15,
        )
        
    @GenericJobClass.is_a_skill
    def fated_brand(self):
        if self._level not in [100]:
            return None
        
        name = "Fated Brand"
        return Skill(
                name=name,
                is_GCD=False,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1160
                ),
                has_aoe=True,
            )
    
    @GenericJobClass.is_a_skill
    def reign_of_beasts(self):
        if self._level not in [100]:
            return None
        
        name = "Reign of Beasts"
        return Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1160
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
    
    @GenericJobClass.is_a_skill
    def noble_blood(self):
        if self._level not in [100]:
            return None
        
        name = "Noble Blood"
        return Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1650
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
        
    @GenericJobClass.is_a_skill
    def lion_heart(self):
        if self._level not in [100]:
            return None

        name = "Lion Heart"
        return Skill(
                name=name,
                is_GCD=True,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    )
                },
                timing_spec=TimingSpec(
                    base_cast_time=0, animation_lock=650, application_delay=1790
                ),
                has_aoe=True,
                aoe_dropoff=0.6,
            )
    
    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    
    @GenericJobClass.is_a_skill
    def bloodfest(self):
        return Skill(name="Bloodfest", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def rampart(self):
        return Skill(name="Rampart", is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def provoke(self):
        return Skill(name="Provoke", is_GCD=False, timing_spec=self.instant_timing_spec)

    @GenericJobClass.is_a_skill
    def reprisal(self):
        return Skill(
            name="Reprisal", is_GCD=False, timing_spec=self.instant_timing_spec
        )

    @GenericJobClass.is_a_skill
    def arms_length(self):
        return Skill(
            name="Arm's Length", is_GCD=False, timing_spec=self.instant_timing_spec
        )

    @GenericJobClass.is_a_skill
    def shirk(self):
        return Skill(name="Shirk", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def camouflage(self):
        return Skill(name="Camouflage", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def royal_guard(self):
        return Skill(name="Royal Guard", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def release_royal_guard(self):
        return Skill(name="Release Royal Guard", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def nebula(self):
        if self._level not in [90]:
            return None
        return Skill(name="Nebula", is_GCD=False, timing_spec=self.instant_timing_spec)
                
    @GenericJobClass.is_a_skill
    def great_nebula(self):
        if self._level not in [90]:
            return None
        return Skill(name="Great Nebula", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def aurora(self):
        return Skill(name="Aurora", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def superbolide(self):
        return Skill(name="Superbolide", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def trajectory(self):
        return Skill(name="Trajectory", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def heart_of_light(self):
        return Skill(name="Heart of Light", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def heart_of_stone(self):
        return Skill(name="Heart of Stone", is_GCD=False, timing_spec=self.instant_timing_spec)
    
    @GenericJobClass.is_a_skill
    def heart_of_corundrum(self):
        return Skill(name="Heart of Corundrum", is_GCD=False, timing_spec=self.instant_timing_spec)