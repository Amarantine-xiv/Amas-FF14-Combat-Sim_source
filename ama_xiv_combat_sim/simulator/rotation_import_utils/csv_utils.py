import pandas as pd #i need to get rid of this...

from collections import namedtuple
from simulator.skills.skill_modifier import SkillModifier

#@title CSVUtils
class RotationCSV(namedtuple('RotationCSV', ['t', 'skill_name', 'job_class', 'skill_conditional'])):
  pass

class CSVUtils():
  @staticmethod
  def read_rotation_from_csv(filename):
    res = []

    try:
      df= pd.read_csv(filename, keep_default_na=False)
    except FileNotFoundError:
      print('File {} was not found. Make sure you are in the right directory (click the folder icon to the left <--- and navigate as appropriate).')
      return res

    for i in range(0, len(df)):
      t = df['Time'][i]
      skill_name = df['skill_name'][i]
      job_class = None if df['job_class'][i] == '' else df['job_class'][i]
      skill_conditional = df['skill_conditional'][i]
      res.append(RotationCSV(t, skill_name, job_class, skill_conditional))
    return res

  def populate_rotation_from_csv(rb, filename):
    all_skills = CSVUtils.read_rotation_from_csv(filename)
    for sk in all_skills:
      rb.add(sk.t, sk.skill_name, skill_modifier=SkillModifier(with_condition=sk.skill_conditional), job_class=sk.job_class)
    return rb, all_skills