# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import random
from Ball import *  # bring in the Ball class code

class Main_BallBounce():
    # 2 - Define constants
    def __init__(self):        
        self.BLACK = (0, 0, 0)
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480
        self.FRAMES_PER_SECOND = 30      
               
    # 3 - Initialize the world
    def start(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
    # 4 - Load assets: image(s), sounds, etc.

    # 5 - Initialize variables
    def init_variables(self):
        self.oBall = Ball(self.window, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    # 6 - Loop forever
    def run(self):
        self.start()
        self.init_variables()
        while True:    
            # 7 - Check for and handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()          

            # 8 - Do any "per frame" actions
            self.oBall.update()  # tell the Ball to update itself

            # 9 - Clear the window before drawing it again
            self.window.fill(self.BLACK)
            
            # 10 - Draw the window elements
            self.oBall.draw()   # tell the Ball to draw itself

            # 11 - Update the window
            pygame.display.update()

            # 12 - Slow things down a bit
            self.clock.tick(self.FRAMES_PER_SECOND)  # make pygame wait


if __name__ == "__main__":
    main = Main_BallBounce()
    main.run()


