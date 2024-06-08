import math

from simulator.calcs.damage_class import DamageClass
from simulator.game_data.patch_655.convenience_timings import get_auto_timing, get_instant_timing_spec, get_cast_gcd_timing_spec
from simulator.sim_consts import SimConsts
from simulator.skills.skill import Skill
from simulator.specs.damage_spec import DamageSpec
from simulator.specs.follow_up import FollowUp
from simulator.specs.job_resource_settings import JobResourceSettings
from simulator.specs.job_resource_spec import JobResourceSpec
from simulator.specs.status_effect_spec import StatusEffectSpec
from simulator.specs.timing_spec import TimingSpec


def add_ast_skills(skill_library):

    auto_timing = get_auto_timing()
    cast_gcd_timing_spec = get_cast_gcd_timing_spec()
    instant_timing_spec = get_instant_timing_spec()

    skill_library.set_current_job_class('AST')
    skill_library.add_skill(Skill(name='Auto',
                                  is_GCD=False,
                                  timing_spec=auto_timing,
                                  damage_spec=DamageSpec(potency=90, damage_class=DamageClass.AUTO, trait_damage_mult_override=1)))
    skill_library.add_skill(Skill(name='Divination',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec,
                                  buff_spec=StatusEffectSpec(duration=15*1000, damage_mult=1.06, is_party_effect=True)))
    skill_library.add_skill(Skill(name='Fall Malefic',
                                  is_GCD=True,
                                  timing_spec=TimingSpec(
                                      base_cast_time=1500, animation_lock=100, application_delay=1070),
                                  damage_spec=DamageSpec(potency=250)))
    dot_ast = Skill(name='_Combust III dot',
                    is_GCD=False,
                    damage_spec=DamageSpec(potency=55,
                                           damage_class=DamageClass.MAGICAL_DOT))
    skill_library.add_skill(Skill(name='Combust III',
                                  is_GCD=True,
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, animation_lock=650, application_delay=620),
                                  follow_up_skills=(FollowUp(skill=dot_ast,
                                                             delay_after_parent_application=0, dot_duration=30*1000,
                                                             snapshot_buffs_with_parent=True,
                                                             snapshot_debuffs_with_parent=True),)))
    skill_library.add_skill(Skill(name='Astrodyne',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec,
                                  buff_spec={SimConsts.DEFAULT_CONDITION: None,
                                             '1 Moon, 1 Asterisk, 1 Circle': StatusEffectSpec(duration=15*1000, haste_time_reduction=0.10, damage_mult=1.05),
                                             '1 Moon, 1 Asterisk': StatusEffectSpec(duration=15*1000, haste_time_reduction=0.10),
                                             '1 Moon, 1 Circle': StatusEffectSpec(duration=15*1000, haste_time_reduction=0.10),
                                             '1 Circle, 1 Asterisk': StatusEffectSpec(duration=15*1000, haste_time_reduction=0.10)},
                                  job_resource_spec=(JobResourceSpec(name='Moon', change=-math.inf),
                                                     JobResourceSpec(
                                      name='Asterisk', change=-math.inf),
                                      JobResourceSpec(name='Circle', change=-math.inf),)))

    skill_library.add_skill(Skill(name='Lightspeed',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec,
                                  buff_spec=StatusEffectSpec(duration=15*1000, flat_cast_time_reduction=2500)))
    skill_library.add_skill(Skill(name='Gravity II',
                                  is_GCD=True,
                                  timing_spec=TimingSpec(
                                      base_cast_time=1500, animation_lock=100, application_delay=1160),
                                  damage_spec=DamageSpec(potency=130)))
    skill_library.add_skill(Skill(name='Macrocosmos',
                                  is_GCD=True,
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, animation_lock=100, application_delay=620),
                                  damage_spec=DamageSpec(potency=250)))
    skill_library.add_skill(Skill(name='Lord of Crowns',
                                  is_GCD=False,
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, animation_lock=650, application_delay=620),
                                  damage_spec=DamageSpec(potency=250)))
    skill_library.add_skill(Skill(name='Card',
                                  is_GCD=False,
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, animation_lock=650, application_delay=620),
                                  buff_spec={SimConsts.DEFAULT_CONDITION: StatusEffectSpec(duration=15*1000, damage_mult=1.06, is_party_effect=True),
                                             'Small': StatusEffectSpec(duration=15*1000, damage_mult=1.03, is_party_effect=True)}))
    skill_library.add_skill(Skill(name='Card Small',
                                  is_GCD=False,
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, animation_lock=650, application_delay=620),
                                  buff_spec=StatusEffectSpec(duration=15*1000, damage_mult=1.03, is_party_effect=True)))
    skill_library.add_skill(Skill(name='Swiftcast',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec,
                                  buff_spec=StatusEffectSpec(flat_cast_time_reduction=math.inf, duration=10*1000, num_uses=1, skill_allowlist=('Fall Malefic', 'Gravity II'))))

    stellar_detonation_follow_up = FollowUp(skill=Skill(name='Stellar Detonation',
                                                        is_GCD=False,
                                                        status_effect_denylist=(
                                                            'Dragon Sight',),
                                                        damage_spec={SimConsts.DEFAULT_CONDITION: None,
                                                                     'Earthly Dominance': DamageSpec(damage_class=DamageClass.PET, potency=205, pet_job_mod_override=118),
                                                                     'Giant Dominance': DamageSpec(damage_class=DamageClass.PET, potency=310, pet_job_mod_override=118)}),
                                            delay_after_parent_application=20*1000,
                                            snapshot_buffs_with_parent=False,
                                            snapshot_debuffs_with_parent=False)
    stellar_detonation_follow_up2 = FollowUp(skill=Skill(name='Stellar Detonation',
                                                         is_GCD=False,
                                                         status_effect_denylist=(
                                                              'Dragon Sight',),
                                                         damage_spec={SimConsts.DEFAULT_CONDITION: None,
                                                                      'Earthly Dominance': DamageSpec(damage_class=DamageClass.PET, potency=205, pet_job_mod_override=118),
                                                                      'Giant Dominance': DamageSpec(damage_class=DamageClass.PET, potency=310, pet_job_mod_override=118)}),
                                             delay_after_parent_application=10*1000,
                                             snapshot_buffs_with_parent=False,
                                             snapshot_debuffs_with_parent=False)

    giant_dom_follow_up = FollowUp(skill=Skill(name='Giant Dominance',
                                               is_GCD=False,
                                               buff_spec={SimConsts.DEFAULT_CONDITION: None,
                                                          'Earthly Dominance': StatusEffectSpec(duration=int(10.1*1000),
                                                                                                is_party_effect=False,
                                                                                                add_to_skill_modifier_condition=True,
                                                                                                num_uses=1, skill_allowlist=('Stellar Detonation',))}),
                                   delay_after_parent_application=10*1000,
                                   snapshot_buffs_with_parent=False,
                                   snapshot_debuffs_with_parent=False)

    earthly_dom_follow_up = FollowUp(skill=Skill(name='Earthly Dominance',
                                                 is_GCD=False,
                                                 buff_spec=StatusEffectSpec(duration=int(10.1*1000),
                                                                            is_party_effect=False,
                                                                            add_to_skill_modifier_condition=True,
                                                                            num_uses=1,
                                                                            skill_allowlist=('Stellar Detonation', 'Giant Dominance'))),
                                     delay_after_parent_application=0,
                                     snapshot_buffs_with_parent=False,
                                     snapshot_debuffs_with_parent=False)

    skill_library.add_skill(Skill(name='Giant Dominance',
                                  is_GCD=False,
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, animation_lock=0, application_delay=0),
                                  buff_spec=StatusEffectSpec(duration=int(10.1*1000),
                                                             is_party_effect=False,
                                                             add_to_skill_modifier_condition=True,
                                                             num_uses=1,
                                                             skill_allowlist=('Stellar Detonation',)),
                                  follow_up_skills=(stellar_detonation_follow_up2,)))

    skill_library.add_skill(Skill(name='Earthly Dominance',
                                  is_GCD=False,
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, animation_lock=0, application_delay=0),
                                  buff_spec=StatusEffectSpec(duration=int(10.1*1000),
                                                             is_party_effect=False,
                                                             add_to_skill_modifier_condition=True,
                                                             num_uses=1,
                                                             skill_allowlist=('Stellar Detonation', 'Giant Dominance')),
                                  follow_up_skills=(giant_dom_follow_up, stellar_detonation_follow_up)))

    skill_library.add_skill(Skill(name='Stellar Detonation',
                                  is_GCD=False,
                                  status_effect_denylist=('Dragon Sight',),
                                  timing_spec=TimingSpec(
                                      base_cast_time=0, application_delay=0),
                                  damage_spec={SimConsts.DEFAULT_CONDITION: None,
                                               'Earthly Dominance': DamageSpec(damage_class=DamageClass.PET, potency=205, pet_job_mod_override=118),
                                               'Giant Dominance': DamageSpec(damage_class=DamageClass.PET, potency=310, pet_job_mod_override=118)}))

    skill_library.add_skill(Skill(name='Earthly Star',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec,
                                  follow_up_skills=(earthly_dom_follow_up, giant_dom_follow_up, stellar_detonation_follow_up)))

    # These skills do not damage, but grants resources/affects future skills.
    # Since we do not model resources YET, we just record their usage/timings but
    # not their effect.
    skill_library.add_skill(Skill(name='Draw',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec))
    skill_library.add_skill(Skill(name='Redraw',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec))
    skill_library.add_skill(Skill(name='Play',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec))

    skill_library.add_resource(name="Asterisk", job_resource_settings=JobResourceSettings(
        max_value=1, skill_allowlist=('Astrodyne',)))
    skill_library.add_resource(name="Moon", job_resource_settings=JobResourceSettings(
        max_value=1, skill_allowlist=('Astrodyne',)))
    skill_library.add_resource(name="Circle", job_resource_settings=JobResourceSettings(
        max_value=1, skill_allowlist=('Astrodyne',)))

    skill_library.add_skill(Skill(name='the Arrow',
                                  is_GCD=False,
                                  job_resource_spec=(
                                      JobResourceSpec(name='Moon', change=+1),),
                                  timing_spec=instant_timing_spec))
    skill_library.add_skill(Skill(name='the Balance',
                                  is_GCD=False,
                                  job_resource_spec=(JobResourceSpec(
                                      name='Asterisk', change=+1),),
                                  timing_spec=instant_timing_spec))
    skill_library.add_skill(Skill(name='the Ewer',
                                  is_GCD=False,
                                  job_resource_spec=(
                                      JobResourceSpec(name='Moon', change=+1),),
                                  timing_spec=instant_timing_spec))
    skill_library.add_skill(Skill(name='the Spire',
                                  is_GCD=False,
                                  job_resource_spec=(JobResourceSpec(
                                      name='Circle', change=+1),),
                                  timing_spec=instant_timing_spec))
    skill_library.add_skill(Skill(name='the Spear',
                                  is_GCD=False,
                                  job_resource_spec=(JobResourceSpec(
                                      name='Circle', change=+1),),
                                  timing_spec=instant_timing_spec))
    skill_library.add_skill(Skill(name='the Bole',
                                  is_GCD=False,
                                  job_resource_spec=(JobResourceSpec(
                                      name='Asterisk', change=+1),),
                                  timing_spec=instant_timing_spec))

    skill_library.add_skill(Skill(name='Minor Arcana',
                                  is_GCD=False,
                                  timing_spec=instant_timing_spec))
    return skill_library
