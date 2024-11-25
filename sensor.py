import numpy as np

# define constants
NOISE_STD_MEAS = 0.01 # standard deviation of measurement error
MAX_RANGE = 100 # maximum range of sensor
DISTANCE_THRESHOLD = 10 # threshold for distance
MIN_CLUSTER_SIZE = 5 # minimum points for feature

# Class to define tof sensor
class Sensor:
   def __init__(self, max_range=MAX_RANGE, noise_std=NOISE_STD_MEAS):
       self.max_range = max_range
       self.noise_std = noise_std
       
   # scan the environment
   def scan(self, robot_x, robot_y, env):
       measurements = []
       angles = np.linspace(0, 2*np.pi, 720)
       
       for angle in angles:
           ray_x = robot_x
           ray_y = robot_y
           
           for r in range(self.max_range):
               ray_x += np.cos(angle)
               ray_y += np.sin(angle)
               
               # Check collision
               if env.is_collision_sensor(ray_x, ray_y):
                   dist = np.sqrt((ray_x - robot_x)**2 + (ray_y - robot_y)**2)
                   # Add noise to simulate sensor error
                   dist += np.random.normal(0, self.noise_std)
                   measurements.append((angle, dist, ray_x, ray_y))
                   break
                   
       return measurements
   
   # extract features from measurements
   def extract_features(self, measurements, threshold=DISTANCE_THRESHOLD):
       features = []
       clusters = []
       current_cluster = []
       
       # Simple clustering based on distance between consecutive measurements       
       for i in range(len(measurements)):
           if len(current_cluster) == 0:
               current_cluster.append(measurements[i])
           else:
               prev_x = measurements[i-1][2]
               prev_y = measurements[i-1][3]
               curr_x = measurements[i][2]
               curr_y = measurements[i][3]
               
               dist = np.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2)
               
               if dist < threshold:  # distance threshold
                   current_cluster.append(measurements[i])
               else:
                   if len(current_cluster) > MIN_CLUSTER_SIZE:  # min points for feature
                       clusters.append(current_cluster)
                   current_cluster = [measurements[i]]
                    
       # catch last cluster
       if len(current_cluster) > MIN_CLUSTER_SIZE:
           clusters.append(current_cluster)
            
       
       # Process clusters to extract features
       # Calculate centroid of cluster
       for cluster in clusters:
           x_coords = [m[2] for m in cluster]
           y_coords = [m[3] for m in cluster]
           feature_x = np.mean(x_coords)
           feature_y = np.mean(y_coords)
           features.append((feature_x, feature_y))
           
       return features