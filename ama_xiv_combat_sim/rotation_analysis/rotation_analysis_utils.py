import numpy as np

class RotationAnalysisUtils:
  @staticmethod
  def get_expected_max_in_k_runs(x, k, num_trials=10000):
    res = np.zeros((num_trials,1))
    for i in range(0, num_trials):
      res[i] = np.max(np.random.choice(x,k))
    return np.mean(res)
  