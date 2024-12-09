import pygame
from env import Environment
import numpy as np

def draw_feature_map(env):
    # Create a new surface for the feature map
    feature_map = pygame.Surface((env.width, env.height))
    feature_map.fill((255, 255, 255))  # White background
    
    # Create a copy of floor plan and convert black to grey
    grey_floor_plan = env.floor_plan.copy()
    # Get pixel array for manipulation
    pixel_array = pygame.PixelArray(grey_floor_plan)
    # Replace black (0, 0, 0) with grey (128, 128, 128)
    pixel_array.replace((0, 0, 0), (128, 128, 128))
    del pixel_array  # Release the pixel array
    
    # Draw the modified floor plan
    feature_map.blit(grey_floor_plan, (0, 0))
    
    # Draw features
    for feature in env.features.values():
        # Draw feature point
        pygame.draw.circle(feature_map, (0, 0, 255), 
                         (int(feature.x), int(feature.y)), 5)
    
    # Save the feature map
    pygame.image.save(feature_map, "feature_map.png")
    
    # Display the feature map in a new window
    pygame.display.set_caption("Feature Map")
    screen = pygame.display.set_mode((env.width, env.height))
    screen.blit(feature_map, (0, 0))
    pygame.display.flip()
    
    # Wait for user to close the window
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                
def main():
    env = Environment()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        measurements = env.update()
        env.draw(measurements)   
        clock.tick(30)
    
    # After main simulation ends, show feature map
    draw_feature_map(env)
    pygame.quit()

if __name__ == "__main__":
   main()