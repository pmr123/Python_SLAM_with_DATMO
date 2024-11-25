import numpy as np

# define constants
NOISE_STD_COV = 0.1 # covariance of pose

# Class to define features
class Feature:
   def __init__(self, x, y, feature_id):
       self.x = x
       self.y = y
       self.id = feature_id
       self.covariance = np.eye(2) * NOISE_STD_COV