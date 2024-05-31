import pygame, sys, random

#constants
FPS = 10
CELL = 20
display_width = 800
display_length = 800


#colours
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



#snake sprite
class Snake:


#food sprite
class Food:

#mainloop
def main():
    pygame.init()
    display = pygame.display.set_mode((display_width, display_length))
    pygame.display.set_caption("The Snake Game")



if __name__ == "__main__":
    main()



