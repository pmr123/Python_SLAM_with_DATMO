import pygame
import numpy as np
from features import Feature
from movingObjects import MovingObject
from robot import Robot
from tts_system import TTSSystem

# TODO:
# - add graphical representation of the environment


# define constants
NUM_MOVING_OBJECTS = 3 # number of moving objects
COLLISION_BUFFER = 15 # buffer zone for collision detection
VELOCITY_MAIN_OBJECT = 5 # velocity of main object
ASSOCIATION_THRESHOLD = 3 # threshold for association
MAX_HISTORY = 20 # maximum history of objects
MAX_RANGE = 100 # maximum range of sensor
OBJ_ZONE = MAX_RANGE/2 # zone of main object
MIN_CLUSTER_SIZE = 3 # minimum cluster size for new dynamic objects

# define colors
BLACK = (0, 0, 0, 255) # walls 
WHITE = (255, 255, 255, 255) # background
RED = (255, 0, 0, 255) # robot
GREEN = (0, 255, 0, 255) # moving objects
BLUE = (0, 0, 255, 255) # features
GREY = (128, 128, 128, 255) # path and object zone
YELLOW = (255, 255, 0, 255) # dynamic objects

# Class to define the environment
class Environment:
   def __init__(self, width=1200, height=600):
       pygame.init()
       self.width = width
       self.height = height
       self.screen = pygame.display.set_mode((width, height))
       pygame.display.set_caption("SLAM with DATMO")
       
       # Load and process floor plan       
       self.floor_plan = pygame.image.load("floor_plan.png")
       self.floor_plan = pygame.transform.scale(self.floor_plan, (width, height))
       self.screen.blit(self.floor_plan, (0, 0))
       
       # Create a hidden screen (off-screen surface) for use in collision detection
       self.hidden_screen = pygame.Surface((width, height))
       # Copy the content from the visible screen to the hidden screen
       self.hidden_screen.blit(self.screen, (0, 0))

       pygame.display.flip()
        
       
       # Initialize robot and objects
       self.robot = Robot(width//4 + 5, height//4 + 5)
       self.main_object = MovingObject(width//4 + 50, height//4 + 50)
       self.moving_objects = [MovingObject(np.random.randint(0, width),
                                         np.random.randint(0, height)) 
                            for _ in range(NUM_MOVING_OBJECTS)] # add NUM_MOVING_OBJECTS moving objects
       
       self.features = {}
       self.feature_id_counter = 0
       self.dynamic_objects = {}  # {id: {'positions': [], 'velocity': 0, 'last_update': time}}
       # initialize first dynamic object
       self.dynamic_objects[0] = {
                       'positions': [(self.main_object.x, self.main_object.y)],
                       'velocity': 0,
                       'last_update': 0
                   }
       self.dynamic_object_counter = 1
       self.collision_buffer = COLLISION_BUFFER  # Buffer zone for collision avoidance
       
       # Add these lines for warning messages
       self.font = pygame.font.Font(None, 36)
       self.last_warning_time = 0
       self.current_warning = None
       
       # Add TTS system initialization
       self.tts = TTSSystem()
       
   
   # check for collision for moving objects
   def is_collision_object(self, x, y):
       x, y = int(x), int(y)
       
       # Check bounds with buffer
       if (x < self.collision_buffer or x >= self.width - self.collision_buffer or 
           y < self.collision_buffer or y >= self.height - self.collision_buffer):
           return True
       
       # Check immediate surroundings (buffer zone)
       for dx in range(-self.collision_buffer, self.collision_buffer + 1):
           for dy in range(-self.collision_buffer, self.collision_buffer + 1):
               check_x = x + dx
               check_y = y + dy
               
               if (0 <= check_x < self.width and 0 <= check_y < self.height):
                   if (self.hidden_screen.get_at((check_x, check_y)) == BLACK):
                       return True
       
       return False
    
   # check for collision for sensor
   def is_collision_sensor(self, x, y):
       x, y = int(x), int(y)
       
       # out of bounds
       if x < 0 or x >= self.width or y < 0 or y >= self.height:
           return True
       
       # collision with walls/objects
       return self.screen.get_at((x, y)) == BLACK or self.screen.get_at((x, y)) == GREEN
   
   # check for collision for robot
   def is_collision_robot(self, x, y):
       x, y = int(x), int(y)
       
       # Check bounds with buffer
       if (x < self.collision_buffer or x >= self.width - self.collision_buffer or 
           y < self.collision_buffer or y >= self.height - self.collision_buffer):
           return True
       
       # Check immediate surroundings (buffer zone)
       for dx in range(-self.collision_buffer, self.collision_buffer + 1):
           for dy in range(-self.collision_buffer, self.collision_buffer + 1):
               check_x = x + dx
               check_y = y + dy
               
               if (0 <= check_x < self.width and 0 <= check_y < self.height):
                   if (self.screen.get_at((check_x, check_y)) == BLUE or 
                       self.screen.get_at((check_x, check_y)) == YELLOW):
                       return True
       
       # Check for dynamic objects
       for obj in self.moving_objects:
           dist = np.sqrt((x - obj.x)**2 + (y - obj.y)**2)
           if dist < self.collision_buffer * 2:  # Larger buffer for moving objects
               return True
       
       return False
   
   def update(self):
       keys = pygame.key.get_pressed()
       dx = dy = 0
       if keys[pygame.K_w]: dy = -VELOCITY_MAIN_OBJECT
       if keys[pygame.K_s]: dy = VELOCITY_MAIN_OBJECT
       if keys[pygame.K_a]: dx = -VELOCITY_MAIN_OBJECT
       if keys[pygame.K_d]: dx = VELOCITY_MAIN_OBJECT
       
       new_x = self.main_object.x + dx
       new_y = self.main_object.y + dy
       
       if not self.is_collision_object(new_x, new_y):
           self.main_object.x = new_x
           self.main_object.y = new_y
           
       # Update moving objects
       for obj in self.moving_objects:
           obj.update(self)
           
       # Update robot
       self.robot.move(self.main_object.x, self.main_object.y, self)
       
       # Process sensor measurements
       measurements = self.robot.sensor.scan(self.robot.x, self.robot.y, self)
       # extract features from measurements
       features = self.robot.sensor.extract_features(measurements)
       
       # Update feature map
       self.update_features(features, measurements)
       
       # check proximity of measurements to robot
       self.check_proximity(measurements)
       
       return measurements
   
   def check_proximity(self, measurements):
       min_distance = float('inf')
       min_angle = 0
       
       for measurement in measurements:
           # Calculate distance between measurement and main object
           dx = measurement[2] - self.main_object.x
           dy = measurement[3] - self.main_object.y
           distance = np.sqrt(dx**2 + dy**2)
           
           if distance < 5:
               continue
               
           if distance < min_distance:
               min_distance = distance
               min_angle = np.arctan2(dy, dx)
       
       for feature in self.features.values():
           dx = feature.x - self.main_object.x
           dy = feature.y - self.main_object.y
           distance = np.sqrt(dx**2 + dy**2)
           
           if distance < 5:
               continue
           
           if distance < min_distance:
               min_distance = distance
               min_angle = np.arctan2(dy, dx)
               
       if min_distance < 30:
           angle_degrees = np.degrees(min_angle) % 360
           self.current_warning = f"Warning: Obstacle at {min_distance:.1f} pixels, {angle_degrees:.1f}°"
           print(self.current_warning)  # Still print to console
           self.tts.speak(self.current_warning)  # Add TTS output
       else:
           self.current_warning = None
   
   # Update feature map
   def update_features(self, observed_features, measurements):
       current_time = pygame.time.get_ticks()
       
       # Track dynamic objects
       dynamic_candidates = []
       matched_dynamics = set()  # Keep track of matched dynamic objects
       features_to_remove = set()  # Track features that need to be removed
       
       # First, update existing dynamic objects
       for feat_x, feat_y in observed_features:
           is_dynamic = False
           
           # Check if feature corresponds to known dynamic object
           for obj_id, obj_data in self.dynamic_objects.items():
               if len(obj_data['positions']) == 0:
                   continue
                    
               prev_pos = obj_data['positions'][-1]
               dist = np.sqrt((feat_x - prev_pos[0])**2 + (feat_y - prev_pos[1])**2)
               
               # Only consider it dynamic if it has moved significantly
               if dist < ASSOCIATION_THRESHOLD and obj_data['velocity'] > 0.5:  # Added velocity threshold
                   dt = (current_time - obj_data['last_update']) / 1000.0
                   if dt > 0:
                       velocity = dist / dt
                       obj_data['velocity'] = 0.7 * obj_data['velocity'] + 0.3 * velocity
                   
                   obj_data['positions'].append((feat_x, feat_y))
                   obj_data['last_update'] = current_time
                   is_dynamic = True
                   matched_dynamics.add(obj_id)
                   
                   if len(obj_data['positions']) > MAX_HISTORY:
                       obj_data['positions'].pop(0)
                   break
           
           if not is_dynamic:
               dynamic_candidates.append((feat_x, feat_y))
       
       # Only remove dynamic objects that have shown consistent movement
       current_objects = list(self.dynamic_objects.keys())
       for obj_id in current_objects:
           if obj_id not in matched_dynamics:
               time_since_last_update = current_time - self.dynamic_objects[obj_id]['last_update']
               if time_since_last_update > 5000:  # 5 seconds threshold
                   # Only remove features if the object has shown significant movement
                   if self.dynamic_objects[obj_id]['velocity'] > 0.5:
                       last_pos = self.dynamic_objects[obj_id]['positions'][-1]
                       for feat_id, feature in self.features.items():
                           feat_dist = np.sqrt((last_pos[0] - feature.x)**2 + 
                                             (last_pos[1] - feature.y)**2)
                           if feat_dist < ASSOCIATION_THRESHOLD:
                               features_to_remove.add(feat_id)
                   del self.dynamic_objects[obj_id]
       
       # Process remaining candidates with more strict criteria for new dynamic objects
       for feat_x, feat_y in dynamic_candidates:
           # Check if this could be a new dynamic object by looking at recent feature history
           is_new_dynamic = False
           for feature in self.features.values():
               dist = np.sqrt((feat_x - feature.x)**2 + (feat_y - feature.y)**2)
               
               # More strict criteria for new dynamic objects
               if (dist > ASSOCIATION_THRESHOLD and 
                   dist < ASSOCIATION_THRESHOLD * 2 and 
                   len(self.features) > MIN_CLUSTER_SIZE):  # Ensure we have enough features
                   
                   # Check if the feature has moved consistently
                   consistent_movement = True
                   for other_feature in self.features.values():
                       if np.sqrt((other_feature.x - feat_x)**2 + 
                                (other_feature.y - feat_y)**2) < ASSOCIATION_THRESHOLD:
                           consistent_movement = False
                           break
                   
                   if consistent_movement:
                       self.dynamic_objects[self.dynamic_object_counter] = {
                           'positions': [(feat_x, feat_y)],
                           'velocity': 0,
                           'last_update': current_time
                       }
                       self.dynamic_object_counter += 1
                       is_new_dynamic = True
                       break
           
           # Uses kalman filter to update feature position
           if not is_new_dynamic:
               # Process as static feature
               associated = False
               for feature in self.features.values():
                   dist = np.sqrt((feat_x - feature.x)**2 + (feat_y - feature.y)**2)
                   if dist < ASSOCIATION_THRESHOLD:
                       associated = True
                       # Kalman filter update
                       innovation = np.array([feat_x - feature.x, feat_y - feature.y])
                       K = feature.covariance @ np.linalg.inv(feature.covariance + np.eye(2) * 0.1)
                       feature.x += K[0,0] * innovation[0]
                       feature.y += K[1,1] * innovation[1]
                       feature.covariance = (np.eye(2) - K) @ feature.covariance
                       break
               
               if not associated:
                   new_feature = Feature(feat_x, feat_y, self.feature_id_counter)
                   self.features[self.feature_id_counter] = new_feature
                   self.feature_id_counter += 1
        
        # Use measurements to remove dangling features
       for feat_id, feature in self.features.items():
           dangling_feature = True
           dist_to_robot = np.sqrt((self.robot.x - feature.x)**2 + 
                                 (self.robot.y - feature.y)**2)
           if dist_to_robot >= MAX_RANGE:
               dangling_feature = False
           if dist_to_robot < MAX_RANGE:
               for measurement in measurements:
                   dist = np.sqrt((measurement[2] - feature.x)**2 + 
                                 (measurement[3] - feature.y)**2)
                   if dist <= ASSOCIATION_THRESHOLD:  
                       dangling_feature = False
                       break
                
           if dangling_feature:
               features_to_remove.add(feat_id)
               
       # Remove marked features
       for feat_id in features_to_remove:
           if feat_id in self.features:
               del self.features[feat_id]
        
        
                       
           
   def draw(self, measurements):
       self.screen.fill(WHITE)
       
       # Draw floor plan
       self.screen.blit(self.floor_plan, (0, 0))
       
       # Draw measurements
       for measurement in measurements:
           pygame.draw.circle(self.screen, YELLOW, 
                            (int(measurement[2]), int(measurement[3])), 5)
       
       # Draw features
       for feature in self.features.values():
           pygame.draw.circle(self.screen, BLUE, 
                            (int(feature.x), int(feature.y)), 5)
           
       # Copy the content from the visible screen to the hidden screen
       self.hidden_screen.blit(self.screen, (0, 0))
       
       # Draw moving objects
       for obj in self.moving_objects:
           pygame.draw.circle(self.screen, GREEN, 
                            (int(obj.x), int(obj.y)), 10)
               
           
       # Draw main object
       pygame.draw.line(self.screen, GREEN, 
                       (int(self.main_object.x-5), int(self.main_object.y-5)),
                       (int(self.main_object.x+5), int(self.main_object.y+5)), 2)
       pygame.draw.line(self.screen, GREEN, 
                       (int(self.main_object.x-5), int(self.main_object.y+5)),
                       (int(self.main_object.x+5), int(self.main_object.y-5)), 2)
       pygame.draw.circle(self.screen, GREY, 
                        (int(self.main_object.x), int(self.main_object.y)), int(OBJ_ZONE), 1)
       
       # Draw robot
       pygame.draw.circle(self.screen, RED, 
                        (int(self.robot.x), int(self.robot.y)), 10)
       pygame.draw.circle(self.screen, GREY, 
                        (int(self.robot.x), int(self.robot.y)), MAX_RANGE, 1)
       
       # Draw robot path
       if len(self.robot.path) > 1:
           pygame.draw.lines(self.screen, GREY, False,
                           [(int(x), int(y)) for x, y in self.robot.path])
       
       if self.current_warning:
           warning_text = self.font.render(self.current_warning, True, RED)
           warning_rect = warning_text.get_rect()
           warning_rect.topleft = (10, 10)  # Position in top-left corner
           self.screen.blit(warning_text, warning_rect)
        
       pygame.display.flip()