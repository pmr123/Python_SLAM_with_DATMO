import numpy as np
from sensor import Sensor

# define constants
ROBOT_VELOCITY = 10 # velocity of robot 
MAX_RANGE = 100 # maximum range of sensor
OBJ_ZONE = MAX_RANGE/2 # zone of main object
MAX_PATH_LENGTH = 20 # maximum path length


class Robot:
   def __init__(self, x, y):
       self.x = x
       self.y = y
       self.theta = 0
       self.velocity = ROBOT_VELOCITY
       self.sensor = Sensor()
       self.path = [(x, y)]
       
   # move the robot
   def move(self, target_x, target_y, env):
       dx = target_x - self.x
       dy = target_y - self.y
       target_distance = np.sqrt(dx**2 + dy**2)
       
       if target_distance > OBJ_ZONE:
           target_theta = np.arctan2(dy, dx)
           self.theta = target_theta
           
           new_x = self.x + self.velocity * np.cos(self.theta)
           new_y = self.y + self.velocity * np.sin(self.theta)
           
           if not env.is_collision_robot(new_x, new_y):
               self.x = new_x
               self.y = new_y
               self.path.append((self.x, self.y))
               if len(self.path) > MAX_PATH_LENGTH:
                   self.path.pop(0)