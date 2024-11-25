import pygame
from env import Environment
      
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
       
   pygame.quit()
if __name__ == "__main__":
   main()