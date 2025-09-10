from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.game_data.generic_job_class import GenericJobClass
from ama_xiv_combat_sim.simulator.game_data.skill_type import SkillType
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.skills.skill import Skill
from ama_xiv_combat_sim.simulator.specs.channeling_spec import ChannelingSpec
from ama_xiv_combat_sim.simulator.specs.combo_spec import ComboSpec
from ama_xiv_combat_sim.simulator.specs.damage_spec import DamageSpec
from ama_xiv_combat_sim.simulator.specs.heal_spec import HealSpec
from ama_xiv_combat_sim.simulator.specs.follow_up import FollowUp
from ama_xiv_combat_sim.simulator.specs.shield_spec import ShieldSpec
from ama_xiv_combat_sim.simulator.specs.defensive_status_effect_spec import (
    DefensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.offensive_status_effect_spec import (
    OffensiveStatusEffectSpec,
)
from ama_xiv_combat_sim.simulator.specs.timing_spec import TimingSpec

from ama_xiv_combat_sim.simulator.game_data.class_skills.tank.pld_data import (
    all_pld_skills,
)


class PldSkills(GenericJobClass):

    def __init__(self, version, level):
        super().__init__(version=version, level=level, skill_data=all_pld_skills)
        self._job_class = "PLD"

    def get_status_effect_priority(self):
        return ("Divine Might", "Requiescat")

    def get_combo_breakers(self):
        # combo group 0: 1-2-3, with fast blade and AOE
        # combo 1: Confiteor + blade of X combos
        combo_breakers = ((1, (0,)),)
        return combo_breakers

    def __req_charges_follow_up(self):
        name = "Requiescat"
        return FollowUp(
            skill=Skill(
                name=name,
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=4,
                    duration=30 * 1000,
                    skill_allowlist=(
                        "Holy Spirit",
                        "Holy Circle",
                        "Confiteor",
                        "Blade of Faith",
                        "Blade of Truth",
                        "Blade of Valor",
                    ),
                ),
            ),
            delay_after_parent_application=0,
        )

    def __divine_might_follow_up(self):
        return FollowUp(
            skill=Skill(
                name="Divine Might",
                offensive_buff_spec=OffensiveStatusEffectSpec(
                    add_to_skill_modifier_condition=True,
                    num_uses=1,
                    duration=30 * 1000,
                    skill_allowlist=("Holy Spirit", "Holy Circle"),
                ),
            ),
            delay_after_parent_application=0,
            primary_target_only=True,
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
    def fast_blade(self):
        name = "Fast Blade"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
        )

    @GenericJobClass.is_a_skill
    def fight_or_flight(self):
        name = "Fight or Flight"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            offensive_buff_spec=OffensiveStatusEffectSpec(
                duration=20000, damage_mult=1.25
            ),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=620
            ),
        )

    @GenericJobClass.is_a_skill
    def riot_blade(self):
        name = "Riot Blade"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_actions=("Fast Blade",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
        )

    @GenericJobClass.is_a_skill
    def total_eclipse(self):
        name = "Total Eclipse"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(),),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=758
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def shield_bash(self):
        name = "Shield Bash"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=446
            ),
        )

    @GenericJobClass.is_a_skill
    def shield_lob(self):
        name = "Shield Lob"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=889
            ),
        )

    @GenericJobClass.is_a_skill
    def prominence(self):
        name = "Prominence"
        promimence_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            ),
            delay_after_parent_application=623,
            primary_target_only=False,
        )
        promimence_no_combo_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec=DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            ),
            delay_after_parent_application=623,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            combo_spec=(ComboSpec(combo_actions=("Total Eclipse",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (
                    promimence_follow_up,
                    self.__divine_might_follow_up(),
                ),
                "No Combo": (promimence_no_combo_follow_up,),
            },
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def circle_of_scorn(self):
        name = "Circle of Scorn (dot)"
        circle_of_scorn_dot_pld = Skill(
            name=name,
            damage_spec=DamageSpec(
                potency=self._skill_data.get_potency(name),
                damage_class=DamageClass.PHYSICAL_DOT,
            ),
        )

        name = "Circle of Scorn"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1023
            ),
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            follow_up_skills=(
                FollowUp(
                    skill=circle_of_scorn_dot_pld,
                    delay_after_parent_application=0,
                    dot_duration=15 * 1000,
                    snapshot_buffs_with_parent=True,
                    snapshot_debuffs_with_parent=True,
                ),
            ),
            has_aoe=True,
        )

    @GenericJobClass.is_a_skill
    def goring_blade(self):
        name = "Goring Blade"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=534
            ),
        )

    @GenericJobClass.is_a_skill
    def royal_authority(self):
        name = "Royal Authority"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_potency(name)
                ),
                "No Combo": DamageSpec(
                    potency=self._skill_data.get_potency_no_combo(name)
                ),
            },
            combo_spec=(ComboSpec(combo_actions=("Riot Blade",)),),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=578
            ),
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (self.__divine_might_follow_up(),),
                "No Combo": tuple(),
            },
        )

    @GenericJobClass.is_a_skill
    def holy_spirit(self):
        name = "Holy Spirit"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency")
                ),
                "Divine Might": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_divine_might"
                    )
                ),
                "Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_req")
                ),
                "Divine Might, Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_divine_might_req"
                    )
                ),
            },
            heal_spec=HealSpec(potency=400),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=1500,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
                "Divine Might": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
                "Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
                "Divine Might, Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=758,
                    affected_by_speed_stat=False,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def requiescat(self):
        if self._level >= 96:
            return None

        name = "Requiescat"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            follow_up_skills=(self.__req_charges_follow_up(),),
        )

    @GenericJobClass.is_a_skill
    def imperator(self):
        if self._level < 96:
            return None

        name = "Imperator"
        imperator_damage_follow_up = FollowUp(
            skill=Skill(
                name=name,
                damage_spec={
                    SimConsts.DEFAULT_CONDITION: DamageSpec(
                        potency=self._skill_data.get_potency(name)
                    )
                },
                has_aoe=True,
                aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
            ),
            delay_after_parent_application=1290,
            primary_target_only=False,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=0
            ),
            follow_up_skills=(
                imperator_damage_follow_up,
                self.__req_charges_follow_up(),
            ),
        )

    @GenericJobClass.is_a_skill
    def holy_circle(self):
        name = "Holy Circle"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            has_aoe=True,
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency")
                ),
                "Divine Might": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_divine_might"
                    )
                ),
                "Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_req")
                ),
                "Divine Might, Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(
                        name, "potency_divine_might_req"
                    )
                ),
            },
            heal_spec=HealSpec(potency=400),
            timing_spec={
                SimConsts.DEFAULT_CONDITION: TimingSpec(
                    base_cast_time=1500,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
                "Divine Might": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
                "Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
                "Divine Might, Requiescat": TimingSpec(
                    base_cast_time=0,
                    animation_lock=100,
                    application_delay=623,
                    affected_by_speed_stat=False,
                ),
            },
        )

    @GenericJobClass.is_a_skill
    def intervene(self):
        name = "Intervene"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=578
            ),
        )

    @GenericJobClass.is_a_skill
    def atonement(self):
        name = "Atonement"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1293
            ),
        )

    @GenericJobClass.is_a_skill
    def supplication(self):
        if self._version < "7.0":
            return None
        name = "Supplication"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
        )

    @GenericJobClass.is_a_skill
    def sepulchre(self):
        if self._version < "7.0":
            return None
        name = "Sepulchre"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.WEAPONSKILL,
            damage_spec=DamageSpec(potency=self._skill_data.get_potency(name)),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=1290
            ),
        )

    @GenericJobClass.is_a_skill
    def confiteor(self):
        name = "Confiteor"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(combo_group=1),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_req")
                ),
            },
            heal_spec=HealSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=623
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def expiacion(self):
        name = "Expiacion"
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
                base_cast_time=0, animation_lock=650, application_delay=357
            ),
            has_aoe=True,
            aoe_dropoff=0.6,
        )

    @GenericJobClass.is_a_skill
    def blade_of_faith(self):
        name = "Blade of Faith"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Confiteor",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_req")
                ),
            },
            heal_spec=HealSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=666
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def blade_of_truth(self):
        name = "Blade of Truth"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Blade of Faith",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_req")
                ),
            },
            heal_spec=HealSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=891
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def blade_of_valor(self):
        name = "Blade of Valor"
        return Skill(
            name=name,
            is_GCD=True,
            skill_type=SkillType.SPELL,
            combo_spec=(ComboSpec(combo_group=1, combo_actions=("Blade of Truth",)),),
            damage_spec={
                SimConsts.DEFAULT_CONDITION: DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency")
                ),
                "Requiescat": DamageSpec(
                    potency=self._skill_data.get_skill_data(name, "potency_req")
                ),
            },
            heal_spec=HealSpec(potency=400),
            timing_spec=TimingSpec(
                base_cast_time=0, animation_lock=650, application_delay=891
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    @GenericJobClass.is_a_skill
    def blade_of_honor(self):
        if self._level < 100:
            return None
        name = "Blade of Honor"
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
                base_cast_time=0, animation_lock=650, application_delay=1160
            ),
            has_aoe=True,
            aoe_dropoff=self._skill_data.get_skill_data(name, "aoe_dropoff"),
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def knights_resolve(self):
        name = "Knight's Resolve"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            # Super gross way to ensure we don't double count a
            # Knight's Resolve buff.
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Other": DefensiveStatusEffectSpec(
                    damage_reductions=0.15,
                    duration=4 * 1000,
                    is_party_effect=True,
                ),
            },
            off_class_default_condition="Other",
        )

    @GenericJobClass.is_a_skill
    def holy_sheltron(self):
        resolve_follow_up = FollowUp(
            skill=self.knights_resolve(), delay_after_parent_application=0
        )
        benediction_follow_up = FollowUp(
            skill=self.knights_benediction(), delay_after_parent_application=0
        )

        name = "Holy Sheltron"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.15, duration=8 * 1000
            ),
            follow_up_skills=(
                resolve_follow_up,
                benediction_follow_up,
            ),
        )

    @GenericJobClass.is_a_skill
    def sentinel(self):
        if self._level >= 92:
            return None
        name = "Sentinel"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.30, duration=15 * 1000
            ),
        )

    @GenericJobClass.is_a_skill
    def bulwark(self):
        name = "Bulwark"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                increase_block_chance=1.0,
                duration=10 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def divine_veil(self):
        name = "Divine Veil"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            shield_spec=ShieldSpec(
                # Fucking gross. Fuck.
                shield_on_your_max_hp=0.1,
                duration=30 * 1000,
                is_party_effect=True,
                is_aoe=True,
            ),
            heal_spec=HealSpec(potency=400, is_party_effect=True, is_aoe=True),
        )

    @GenericJobClass.is_a_skill
    def clemency(self):
        heal_self_follow_up = FollowUp(
            skill=Skill(
                name="Clemency (Heal)",
                is_GCD=False,
                heal_spec=HealSpec(potency=500),
                skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
                timing_spec=self.uncontrolled_timing_spec,
            ),
            delay_after_parent_application=0,
        )
        return Skill(
            name="Clemency",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            heal_spec={
                SimConsts.DEFAULT_CONDITION: None,
                "Target": HealSpec(potency=1000, is_party_effect=True),
            },
            follow_up_skills={
                SimConsts.DEFAULT_CONDITION: (heal_self_follow_up,),
                "Target": tuple(),
            },
            # If PLD heals itself, just specify it as "Target".
            off_class_default_condition="Target",
        )

    # For logs parsing convenience
    @GenericJobClass.is_a_skill
    def knights_benediction(self):
        name = "Knight's Benediction"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
            timing_spec=self.uncontrolled_timing_spec,
            heal_spec=HealSpec(hot_potency=250, duration=12 * 1000),
        )

    @GenericJobClass.is_a_skill
    def intervention(self):
        # Because if this is on YOU, it's 10%, but someone else is 15%.
        personal_knights_resolve_follow_up = FollowUp(
            skill=Skill(
                name="Knight's Resolve",
                is_GCD=False,
                skill_type=SkillType.UNCONTROLLED_FOLLOW_UP,
                timing_spec=self.uncontrolled_timing_spec,
                defensive_buff_spec=DefensiveStatusEffectSpec(
                    damage_reductions=0.10,
                    duration=4 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )
        benediction_follow_up = FollowUp(
            skill=self.knights_benediction(), delay_after_parent_application=0
        )

        regular_def = DefensiveStatusEffectSpec(
            damage_reductions=0.10,
            duration=8 * 1000,
            is_party_effect=True,
        )
        buffed_def = DefensiveStatusEffectSpec(
            damage_reductions=0.20,
            duration=8 * 1000,
            is_party_effect=True,
        )

        name = "Intervention"
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: regular_def,
                "Rampart": buffed_def,
                "Guardian": buffed_def,
                "Guardian, Rampart": buffed_def,
            },
            follow_up_skills=(
                personal_knights_resolve_follow_up,
                benediction_follow_up,
            ),
        )

    @GenericJobClass.is_a_skill
    def guardian(self):
        if self._level < 92:
            return None
        return Skill(
            name="Guardian",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.4,
                duration=15 * 1000,
                add_to_skill_modifier_condition=True,
            ),
            shield_spec=ShieldSpec(potency=1000, duration=15 * 1000),
        )

    @GenericJobClass.is_a_skill
    def hallowed_ground(self):
        return Skill(
            name="Hallowed Ground",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                is_invuln=True,
                duration=10 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def passage_of_arms(self):
        name = "Passage of Arms"

        block_follow_up = FollowUp(
            skill=Skill(
                name=f"{name} (Block)",
                defensive_buff_spec=DefensiveStatusEffectSpec(
                    increase_block_chance=1.0,
                    duration=18 * 1000,
                ),
            ),
            delay_after_parent_application=0,
        )
        return Skill(
            name=name,
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec={
                SimConsts.DEFAULT_CONDITION: self.instant_timing_spec,
                "Cancel": self.uncontrolled_timing_spec,
            },
            channeling_spec={
                SimConsts.DEFAULT_CONDITION: ChannelingSpec(duration=18 * 1000),
                "Cancel": None,
            },
            defensive_buff_spec={
                SimConsts.DEFAULT_CONDITION: DefensiveStatusEffectSpec(
                    damage_reductions=0.15,
                    duration=18 * 1000,
                    is_party_effect=True,
                ),
                "Cancel": DefensiveStatusEffectSpec(
                    expires_status_effects=(name, f"{name} (Block)")
                ),
            },
            follow_up_skills=(block_follow_up,),
        )

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.

    @GenericJobClass.is_a_skill
    def cover(self):
        # TODO: implement. Fuck this skill.
        return Skill(
            name="Cover",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def provoke(self):
        return Skill(
            name="Provoke",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def rampart(self):
        return Skill(
            name="Rampart",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_buff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.2,
                hp_recovery_up_via_healing_actions=0.15,
                duration=20 * 1000,
                add_to_skill_modifier_condition=True,
            ),
        )

    @GenericJobClass.is_a_skill
    def reprisal(self):
        return Skill(
            name="Reprisal",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
            defensive_debuff_spec=DefensiveStatusEffectSpec(
                damage_reductions=0.1,
                duration=15 * 1000,
            ),
        )

    @GenericJobClass.is_a_skill
    def arms_length(self):
        return Skill(
            name="Arm's Length",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )

    @GenericJobClass.is_a_skill
    def shirk(self):
        return Skill(
            name="Shirk",
            is_GCD=False,
            skill_type=SkillType.ABILITY,
            timing_spec=self.instant_timing_spec,
        )
