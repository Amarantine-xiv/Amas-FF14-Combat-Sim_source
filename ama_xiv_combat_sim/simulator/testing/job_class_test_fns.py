class JobClassTestFns:
  JOB_MODS = {'test_job': 115, 'test_job2': 105, 'test_tank_job': 105, 'test_healer_job': 115, 'test_job_haste': 115}
  USES_SKS = {'test_job', 'test_tank_job'}

  @staticmethod
  def compute_trait_damage_mult(job_class):
    if job_class == 'test_job2':
      return 1.40
    elif job_class == 'test_healer_job':
      return 1.30
    else:
      return 1

  @staticmethod
  def compute_trait_haste_time_reduction(job_class):
    job_to_trait_haste_time_reduction = {'test_job_haste': 0.2}
    if job_class in job_to_trait_haste_time_reduction:
      return job_to_trait_haste_time_reduction[job_class]
    return 0

  @staticmethod
  def compute_trait_auto_attack_delay_reduction(job_class):
    job_to_trait_auto_attack_delay_reduction = {'test_job_haste': 0.2}
    if job_class in job_to_trait_auto_attack_delay_reduction:
      return job_to_trait_auto_attack_delay_reduction[job_class]
    return 0

  @staticmethod
  def isTank(job_class):
    return job_class in ['test_tank_job']

  @staticmethod
  def isHealer(job_class):
    return job_class in ['test_healer_job']

  @staticmethod
  def isMelee(job_class):
    return job_class in ['test_job', 'test_job2']

  @staticmethod
  def isCaster(job_class):
    return False

  @staticmethod
  def isPhysRanged(job_class):
    return job_class in ['test_job_haste']