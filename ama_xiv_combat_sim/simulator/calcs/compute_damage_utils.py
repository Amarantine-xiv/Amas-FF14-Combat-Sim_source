import numpy as np

from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.calcs.stat_fns import StatFns
from ama_xiv_combat_sim.simulator.game_data.game_consts import GameConsts

class ComputeDamageUtils():
  @staticmethod
  def __get_forced_dh_status(damage_spec, skill_modifier, status_effects):
    return damage_spec.guaranteed_dh is ForcedCritOrDH.FORCE_YES or \
           skill_modifier.guaranteed_dh is ForcedCritOrDH.FORCE_YES or \
           status_effects[0].guaranteed_dh is ForcedCritOrDH.FORCE_YES or \
           status_effects[1].guaranteed_dh is ForcedCritOrDH.FORCE_YES

  @staticmethod
  def __get_forced_crit_status(damage_spec, skill_modifier, status_effects):
    return damage_spec.guaranteed_crit is ForcedCritOrDH.FORCE_YES or \
           skill_modifier.guaranteed_crit is ForcedCritOrDH.FORCE_YES or \
           status_effects[0].guaranteed_crit is ForcedCritOrDH.FORCE_YES or \
           status_effects[1].guaranteed_crit is ForcedCritOrDH.FORCE_YES

  @staticmethod
  def __get_forced_no_dh_status(damage_spec, skill_modifier, status_effects):
    return damage_spec.guaranteed_dh is ForcedCritOrDH.FORCE_NO or \
           skill_modifier.guaranteed_dh is ForcedCritOrDH.FORCE_NO or \
           status_effects[0].guaranteed_dh is ForcedCritOrDH.FORCE_NO or \
           status_effects[1].guaranteed_dh is ForcedCritOrDH.FORCE_NO

  @staticmethod
  def __get_forced_no_crit_status(damage_spec, skill_modifier, status_effects):
    return damage_spec.guaranteed_crit is ForcedCritOrDH.FORCE_NO or \
           skill_modifier.guaranteed_crit is ForcedCritOrDH.FORCE_NO or \
           status_effects[0].guaranteed_crit is ForcedCritOrDH.FORCE_NO or \
           status_effects[1].guaranteed_crit is ForcedCritOrDH.FORCE_NO

  @staticmethod
  def get_guaranteed_dh_bonus_dmg_multiplier(status_effects):
    bonus_dh_rate_add = status_effects[0].dh_rate_add + status_effects[1].dh_rate_add
    return GameConsts.DH_DAMAGE_MULT_BONUS*bonus_dh_rate_add

  @staticmethod
  def get_guaranteed_crit_bonus_dmg_multiplier(stats, status_effects):
    bonus_crit_rate_add = status_effects[0].crit_rate_add + status_effects[1].crit_rate_add
    return stats.processed_stats.crit_bonus*bonus_crit_rate_add

  @staticmethod
  def get_guaranteed_dh_and_crit_bonus_dmg(stats, skill, skill_modifier, status_effects):
    damage_spec = skill.get_damage_spec(skill_modifier)

    forced_dh = ComputeDamageUtils.__get_forced_dh_status(damage_spec, skill_modifier, status_effects)
    forced_crit = ComputeDamageUtils.__get_forced_crit_status(damage_spec, skill_modifier, status_effects)

    bonus_dh_multiplier = ComputeDamageUtils.get_guaranteed_dh_bonus_dmg_multiplier(status_effects) if forced_dh else 0
    bonus_crit_multiplier = ComputeDamageUtils.get_guaranteed_crit_bonus_dmg_multiplier(stats, status_effects) if forced_crit else 0
    return (bonus_dh_multiplier, bonus_crit_multiplier)

  @staticmethod
  def compute_damage_mult(status_effects):
    return status_effects[0].damage_mult*status_effects[1].damage_mult

  @staticmethod
  def compute_crit_rates_and_bonuses(stats, skill, skill_modifier, status_effects):
    damage_spec = skill.get_damage_spec(skill_modifier)
    forced_dh = ComputeDamageUtils.__get_forced_dh_status(damage_spec, skill_modifier, status_effects)
    forced_crit = ComputeDamageUtils.__get_forced_crit_status(damage_spec, skill_modifier, status_effects)

    forced_no_dh = ComputeDamageUtils.__get_forced_no_dh_status(damage_spec, skill_modifier, status_effects)
    forced_no_crit = ComputeDamageUtils.__get_forced_no_crit_status(damage_spec, skill_modifier, status_effects)

    if forced_dh and forced_no_dh:
      raise RuntimeError('Skill specifies both forced_dh and forced_no_dh; only one of these may be true. \
                          On skill: {}. Damage spec/ skill modifier / status effect: {}/{}/{}/{}'.format(skill.name, damage_spec.guaranteed_dh,
                                                                                                         skill_modifier.guaranteed_dh,
                                                                                                         status_effects[0].guaranteed_dh,
                                                                                                         status_effects[1].guaranteed_dh))
    if forced_crit and forced_no_crit:
      raise RuntimeError('Skill specifies both forced_crit and forced_no_crit; only one of these may be true. \
                          On skill: {}. Damage spec/ skill modifier / status effect: {}/{}/{}/{}'.format(skill.name, damage_spec.guaranteed_crit,
                                                                                                         skill_modifier.guaranteed_crit,
                                                                                                         status_effects[0].guaranteed_crit,
                                                                                                         status_effects[1].guaranteed_crit))
    if forced_dh:
      dh_rate = 1
    elif forced_no_dh:
      dh_rate = 0
    else:
      dh_rate = stats.processed_stats.dh_rate + status_effects[0].dh_rate_add + status_effects[1].dh_rate_add

    crit_bonus = stats.processed_stats.crit_bonus
    if forced_crit:
      crit_rate = 1
    elif forced_no_crit:
      crit_rate = 0
    else:
      crit_rate = stats.processed_stats.crit_rate + status_effects[0].crit_rate_add + status_effects[1].crit_rate_add

    return (dh_rate, crit_rate, crit_bonus)

  @staticmethod
  def compute_direct_damage(skill, skill_modifier, stats, status_effects):
    is_tank = stats.job_class_fns.isTank(stats.job_class)
    main_stat = stats.main_stat+status_effects[0].main_stat_add+status_effects[1].main_stat_add
    main_stat = np.floor(main_stat*(1+0.01*stats.num_roles_in_party))

    damage_spec = skill.get_damage_spec(skill_modifier)

    # from HINT
    potency = damage_spec.potency
    ap = StatFns.fAP(main_stat, is_tank)
    wd = StatFns.fWD(stats.wd, stats.processed_stats.job_mod)

    forced_dh = ComputeDamageUtils.__get_forced_dh_status(damage_spec, skill_modifier, status_effects)
    det_dh = StatFns.fDetDH(stats.det_stat, stats.dh_stat) if forced_dh else stats.processed_stats.det_bonus

    # TODO: move to readme or somewhere better than this.
    # 1) main stat changed by pots/party buffs (# of roles)
    # 2) potency and fAP are taken into account
    # 3) det (and potentially dh if autocrit) is taken into account
    # 4) tnc is taken into account, if applicable (tanks)
    # 5) sps/sks is taken into account, if applicable (eg, dots)
    # 6) weapon damage and weapon delay are taken account, if applicable
    # 7) apply the +1 for dots
    # 8) apply guaranteed crit bonus using crit rate up, if applicable
    # 9) apply guaranteed direct hit bonus dh up, if applicable
    # 10) apply +-5% damage variance (on ALL sources of damage, direct, auto, dot)
    # 11) crit/direct hit multipliers are taken into account, if applicable. NO FLOORING IS DONE HERE.
    # 12) traits are taken into account, if applicable
    # 13) each straight up damage buff/enemy increased damage taken is taken into account multiplicatively. NO FLOORING IS DONE BETWEEN APPLYING BUFFS

    if stats.job_class_fns.isHealer(stats.job_class) or stats.job_class_fns.isCaster(stats.job_class):
      base_damage = np.floor(ap*det_dh/1000)/100
      base_damage = np.floor(base_damage*np.floor(wd*potency/100))
    else:
      base_damage = np.floor(np.floor(potency*ap/100)/100*det_dh/10)/100
      if is_tank:
        base_damage = np.floor(base_damage*StatFns.fTnc(stats.tenacity)/10)/100
      base_damage = np.floor(np.floor(base_damage*wd))


    bonus_damage_multipliers_from_guaranteeds = ComputeDamageUtils.get_guaranteed_dh_and_crit_bonus_dmg(stats, skill, skill_modifier, status_effects)
    base_damage += np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[0]) + np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[1])

    return base_damage

  @staticmethod
  def compute_magical_dot_damage(skill, skill_modifier, stats, status_effects):
    is_tank = stats.job_class_fns.isTank(stats.job_class)
    main_stat = stats.main_stat+status_effects[0].main_stat_add+status_effects[1].main_stat_add
    main_stat = np.floor(main_stat*(1+0.01*stats.num_roles_in_party))

    damage_spec = skill.get_damage_spec(skill_modifier)

    potency = damage_spec.potency
    spd = StatFns.fSpd(stats.speed_stat)
    ap = StatFns.fAP(main_stat, is_tank)
    wd = StatFns.fWD(stats.wd, stats.processed_stats.job_mod)

    forced_dh = ComputeDamageUtils.__get_forced_dh_status(damage_spec, skill_modifier, status_effects)
    det_dh = StatFns.fDetDH(stats.det_stat, stats.dh_stat) if forced_dh else stats.processed_stats.det_bonus

    # INVESTIGATE ROUNDING- THIS SHOULD FOLLOW THE SAME TRUNCATIONS AS THE OTHER DAMAGE FORMULAS, PROBABLY
    base_damage = np.floor(np.floor(potency*wd)/100)
    base_damage = np.floor(np.floor(np.floor(base_damage*ap)*spd))
    base_damage = np.floor(np.floor(base_damage*det_dh)/1000)
    if is_tank:
      base_damage = np.floor(base_damage*StatFns.fTnc(stats.tenacity)/1000)
    base_damage = np.floor(np.floor(base_damage/1000)/100)
    # ignore +1 for now

    bonus_damage_multipliers_from_guaranteeds = ComputeDamageUtils.get_guaranteed_dh_and_crit_bonus_dmg(stats, skill, skill_modifier, status_effects)
    base_damage += np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[0]) + np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[1])

    return base_damage

  @staticmethod
  def compute_physical_dot_damage(skill, skill_modifier, stats, status_effects):
    is_tank = stats.job_class_fns.isTank(stats.job_class)
    main_stat = stats.main_stat+status_effects[0].main_stat_add+status_effects[1].main_stat_add
    main_stat = np.floor(main_stat*(1+0.01*stats.num_roles_in_party))

    damage_spec = skill.get_damage_spec(skill_modifier)

    potency = damage_spec.potency
    spd = StatFns.fSpd(stats.speed_stat)
    ap = StatFns.fAP(main_stat, is_tank)
    wd = StatFns.fWD(stats.wd, stats.processed_stats.job_mod)

    forced_dh = ComputeDamageUtils.__get_forced_dh_status(damage_spec, skill_modifier, status_effects)
    det_dh = StatFns.fDetDH(stats.det_stat, stats.dh_stat) if forced_dh else stats.processed_stats.det_bonus

    # INVESTIGATE ROUNDING- THIS SHOULD FOLLOW THE SAME TRUNCATIONS AS THE OTHER DAMAGE FORMULAS, PROBABLY
    base_damage = np.floor(potency*ap*det_dh/100)/1000
    if is_tank:
      base_damage = np.floor(base_damage*StatFns.fTnc(stats.tenacity)/1000)
    base_damage = np.floor(np.floor(base_damage*spd)/1000)
    base_damage = np.floor(np.floor(base_damage*wd)/100)
    # ignore +1 for now

    bonus_damage_multipliers_from_guaranteeds = ComputeDamageUtils.get_guaranteed_dh_and_crit_bonus_dmg(stats, skill, skill_modifier, status_effects)
    base_damage += np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[0]) + np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[1])

    return base_damage

  @staticmethod
  def compute_pet_damage(skill, skill_modifier, stats, status_effects):
    level_main = GameConsts.LEVEL_MAINS[stats.level]
    is_tank =  stats.job_class_fns.isTank(stats.job_class)

    damage_spec = skill.get_damage_spec(skill_modifier)

    # # party bonus to stats does not apply to pets (eg, no 5% bonus for 1 of each type)
    job_mod_use = stats.processed_stats.job_mod if damage_spec.pet_job_mod_override is None else damage_spec.pet_job_mod_override
    main_stat_diff = np.floor(level_main*stats.processed_stats.job_mod/100) - np.floor(level_main*job_mod_use/100)

    main_stat = (stats.main_stat - main_stat_diff) + status_effects[0].main_stat_add+status_effects[1].main_stat_add
    main_stat *= damage_spec.pet_scalar

    potency = damage_spec.potency
    # For whatever reason, pets are never considered tanks, even if they come from a tank. Don't think too hard about it.
    ap = StatFns.fAP(main_stat, is_tank=False)
    wd = StatFns.fWD(stats.wd, job_mod_use)
    forced_dh = ComputeDamageUtils.__get_forced_dh_status(damage_spec, skill_modifier, status_effects)
    det_dh = StatFns.fDetDH(stats.det_stat, stats.dh_stat) if forced_dh else stats.processed_stats.det_bonus

    base_damage = np.floor(np.floor(potency*ap/100)/100*det_dh/10)/100
    # pets will scale off tenacity though
    if is_tank:
      base_damage = np.floor(base_damage*StatFns.fTnc(stats.tenacity)/10)/100
    base_damage = np.floor(np.floor(base_damage*wd))

    bonus_damage_multipliers_from_guaranteeds = ComputeDamageUtils.get_guaranteed_dh_and_crit_bonus_dmg(stats, skill, skill_modifier, status_effects)
    base_damage += np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[0]) + np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[1])
    return base_damage

  @staticmethod
  def compute_auto_damage(skill, skill_modifier, stats, status_effects):
    if (stats.job_class_fns.isHealer(stats.job_class) or stats.job_class_fns.isCaster(stats.job_class)):
      # for healers/casters, the stat used to compute autos is strength, not main stat. So use that and pots and party bonus doesn't affect it
      if stats.healer_or_caster_strength is None:
        raise RuntimeError('Cannot compute auto attack damage for healer/caster unless healer_or_caster_strength stat is specified.')
      main_stat = stats.healer_or_caster_strength*(1+0.01*stats.num_roles_in_party)
    else:
      # for non-healers/casters, the stat used to compute autos is our main stat, and we get all the buffs/bonuses on it
      main_stat = stats.main_stat+status_effects[0].main_stat_add+status_effects[1].main_stat_add
      main_stat = np.floor(main_stat*(1+0.01*stats.num_roles_in_party))

    damage_spec = skill.get_damage_spec(skill_modifier)

    is_tank = stats.job_class_fns.isTank(stats.job_class)
    potency = damage_spec.potency
    spd = StatFns.fSpd(stats.speed_stat) if stats.job_class in stats.job_class_fns.USES_SKS else 1000
    ap = StatFns.fAP(main_stat, is_tank)
    weapon_delay = stats.weapon_delay
    auto = StatFns.fAuto(stats.wd, weapon_delay, stats.processed_stats.job_mod)

    forced_dh = ComputeDamageUtils.__get_forced_dh_status(damage_spec, skill_modifier, status_effects)
    det_dh = StatFns.fDetDH(stats.det_stat, stats.dh_stat) if forced_dh else stats.processed_stats.det_bonus

    base_damage = np.floor(np.floor(potency*ap/100)/100*det_dh/10)/100
    if is_tank:
      base_damage = np.floor(base_damage*StatFns.fTnc(stats.tenacity)/10)/100
    base_damage = np.floor(base_damage*spd)/10

    # #add the +1 here?
    # if damage_spec.potency < 100:
    #   base_damage += 1

    base_damage = np.floor(np.floor(base_damage*auto)/100)

    bonus_damage_multipliers_from_guaranteeds = ComputeDamageUtils.get_guaranteed_dh_and_crit_bonus_dmg(stats, skill, skill_modifier, status_effects)
    base_damage += np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[0]) + np.floor(base_damage*bonus_damage_multipliers_from_guaranteeds[1])

    # jackal's formula with tank tnc injected
    # base_damage1 = np.floor(np.floor(np.floor(np.floor(np.floor(potency*ap*det_dh)/100)/1000)*1000)/1000)
    # if is_tank:
    #     base_damage1 = np.floor(base_damage1*StatFns.fTnc(stats.tenacity)/10)/100  
    # base_damage2 = np.floor(np.floor(base_damage1*spd)/1000)
    # base_damage = np.floor(np.floor(np.floor(np.floor(base_damage2*auto)/100)*100)/100)    

    return base_damage

  @staticmethod
  def get_base_damage(skill, skill_modifier, stats, status_effects):
    if skill.get_damage_spec(skill_modifier) is None:
      return None

    damage_spec = skill.get_damage_spec(skill_modifier)

    if (damage_spec.damage_class == DamageClass.DIRECT):
      base_damage = ComputeDamageUtils.compute_direct_damage(skill, skill_modifier, stats, status_effects)
    elif (damage_spec.damage_class == DamageClass.MAGICAL_DOT):
      base_damage = ComputeDamageUtils.compute_magical_dot_damage(skill, skill_modifier, stats, status_effects)
    elif (damage_spec.damage_class == DamageClass.PHYSICAL_DOT):
      base_damage = ComputeDamageUtils.compute_physical_dot_damage(skill, skill_modifier, stats, status_effects)
    elif (damage_spec.damage_class == DamageClass.AUTO):
      base_damage = ComputeDamageUtils.compute_auto_damage(skill, skill_modifier, stats, status_effects)
    elif (damage_spec.damage_class == DamageClass.PET):
      base_damage = ComputeDamageUtils.compute_pet_damage(skill, skill_modifier, stats, status_effects)
    else:
      raise RuntimeError("No support damage fn for damage class: {}". format(damage_spec.damage_class))
    return base_damage
