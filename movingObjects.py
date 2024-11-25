import numpy as np

# define constants
VELOCITY = 2 # velocity of moving objects
MAX_HISTORY = 20 # maximum history of objects

# Class to define moving objects
class MovingObject:
   def __init__(self, x, y, velocity=VELOCITY):
       self.x = x
       self.y = y
       self.velocity = velocity
       self.theta = np.random.uniform(0, 2*np.pi)
       self.history = [(x, y)]
       
   # update position
   def update(self, env):
       dx = self.velocity * np.cos(self.theta)
       dy = self.velocity * np.sin(self.theta)
       
       new_x = self.x + dx
       new_y = self.y + dy
       
       # Collision detection with walls/objects
       if env.is_collision_object(new_x, new_y):
           self.theta = np.random.uniform(0, 2*np.pi)
           return
           
       self.x = new_x
       self.y = new_y
       self.history.append((self.x, self.y))
       if len(self.history) > MAX_HISTORY:
           self.history.pop(0)