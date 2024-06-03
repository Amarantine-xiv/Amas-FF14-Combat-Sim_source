import os

from simulator.rotation_import_utils.csv_utils import CSVUtils
from simulator.stats import Stats
from simulator.timeline_builders.rotation_builder import RotationBuilder

def get_my_rotation(skill_library):
  # input your stats here (TODO: etro gear link).
  # these stats include food only; 5% party buffs are added automatically during the sim.
  stats = Stats(wd=132, weapon_delay=3.36, main_stat=3330, det_stat=2182, crit_stat=2596, dh_stat=940, speed_stat=400, tenacity=601, job_class = 'WAR')

  rb = RotationBuilder(stats, skill_library, ignore_trailing_dots=True, enable_autos=True, snap_dots_to_server_tick_starting_at=0)
  rotation_name = 'My Rotation'

  # Example of party buffs/debuffs.
  # This sim supports all buffs/debyffs; seem the skill tank/healer/melee/ranged/caster skill libraries for all job classes).
  # Generally, just type in 1) the time the buff/debuff is used, 2) the name of the buff/debuff as it appears on the ff14 job
  # site, and the job class it belongs to. For skills that apply a status effect that also have damage,
  # you may need to specify that you only want to add the buff/debuff portion. Eg:
  #    rb.add(6.3, 'Mug', job_class='NIN', skill_modifier=SkillModifier(with_condition='Debuff Only'))
  rb.add(6.3, 'Chain Stratagem', job_class='SCH')
  rb.add(7.1, 'Battle Litany', job_class='DRG')
  rb.add(0.8, 'Arcane Circle', job_class='RPR')
  rb.add(6.28, 'Embolden', job_class='RDM')

  # Example of rotation of interest.
  # Generally, you just type in the name of the skill you want to use as it appears
  # on the ff14 job site. For certain special conditions (eg, no positional), you may have to use
  # the skill_modifier field to indicate the condition under which you're using the skill.
  # Example of SkillModifier:
  # For SAM:
  #    rb.add_next('Gekko', skill_modifier=SkillModifier(with_condition='No Positional'))
  # Will indicate that Gekko was used, but the positional was not hit. Note that
  # the sim will automatically track combos and conditions that can be inferred from
  # skill usage (eg, using Inner Release on WAR, Meikyo Shisui on SAM) that result in
  # changes to skills (guaranteed crit/dh for Inner Release, automatically meeting combo requirements for Meikyo Shisui).
  # Please see the class SkillModifier and the corresponding class's skill library for information on the conditionals.
  rb.add_next('Tomahawk')
  rb.add_next('Infuriate')
  rb.add_next('Heavy Swing')
  rb.add_next('Maim')
  rb.add_next('Grade 8 Tincture')
  rb.add_next("Storm's Eye")
  rb.add_next('Inner Release')
  rb.add_next('Inner Chaos')
  rb.add_next('Upheaval')
  rb.add_next('Onslaught')
  rb.add_next('Primal Rend')
  rb.add_next('Inner Chaos')
  rb.add_next('Onslaught')
  rb.add_next('Fell Cleave')
  rb.add_next('Onslaught')
  rb.add_next('Fell Cleave')
  rb.add_next('Fell Cleave')
  rb.add_next('Heavy Swing')
  rb.add_next('Maim')
  rb.add_next("Storm's Path")
  rb.add_next('Fell Cleave')
  rb.add_next('Inner Chaos')

  return (rotation_name, rb)

def get_my_rotation_from_CSV(skill_library, csv_filename='', rotation_name= ''):
  stats = Stats(wd=132, weapon_delay=3.36, main_stat=3330, det_stat=2182, crit_stat=2596, dh_stat=940, speed_stat=400, tenacity=601, job_class = 'WAR')
  rb = RotationBuilder(stats, skill_library, ignore_trailing_dots=True, enable_autos=True, snap_dots_to_server_tick_starting_at=0)

  if not os.path.exists(csv_filename):
    print('File does not exist: {}. Make sure you are in the right directory and have the right file name (see the folder icon on the left <----).'.format(csv_filename))
  else:
    rb, _ = CSVUtils.populate_rotation_from_csv(rb, csv_filename)
  return (rotation_name, rb)
