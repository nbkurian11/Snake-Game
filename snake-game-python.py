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
    def __init__(self):
        self.body = [display_width // 3, display_length // 3]
        self.move = 'LEFT'
        self.growth = False
    
    #MOVEMENT OF SNAKE CTRL
    def movement(self):
        position = self.body(0)
        x, y = position
        if self.move == 'UP':
            y -= CELL
        elif self.move == 'DOWN':
            y += CELL
        elif self.move == 'RIGHT':
            y += CELL
        elif self.move == 'LEFT':
            y -= CELL
        self.body.insert(0, (x, y))
        if not self.growth:
            self.body.pop()
        else:
            self.growth = False
    
    def snake_size(self):
        self.growth = True 

    def display_snake(self, display):
        for segment in self.body:
            pygame.draw.rect(display, GREEN, (segment[0], segment[1], CELL, CELL))


    def snakeimpact(self):
        position = self.body(0)
        if position[0] < 0 or position[0] >= display_width or position[1] < 0 or position[1] >= display_length:
            return True
        for segment in self.body[1:]:
            if position == segment:
                return True
            
        return False 




#food sprite
class Food:
    def __init__(self):
        self.movement = (random.randint(0, display_length - CELL) // CELL * CELL,
                               random.randint(0, display_length - CELL) // CELL * CELL)


    def draw(self, display):
        pygame.draw.circle(display, RED, (self.movement, CELL, CELL))
        
    def interaction(self, Snake):
        position = Snake.body[0]
        if position == self.movement:
            Snake.growth()
            self.movement = (random.randint(0, display_length - CELL) // CELL * CELL,
                               random.randint(0, display_length - CELL) // CELL * CELL)

#mainloop
def main():
    pygame.init()
    display = pygame.display.set_mode((display_width, display_length))
    pygame.display.set_caption("The Snake Game")
    timer = pygame.time.Clock()

    snake = Snake()
    food = Food()


    running = True 
    while running :
        display.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and Snake.direction != 'DOWN':
                    Snake.direction = 'UP'
                elif event.key == pygame.K_DOWN and Snake.direction != 'UP':
                    Snake.direction = 'DOWN'
                elif event.key == pygame.K_LEFT and Snake.direction != 'RIGHT':
                    Snake.direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and Snake.direction != 'LEFT':
                    Snake.direction = 'RIGHT'


        Snake.movement()
        Snake.display_snake()
        food.draw()


        if Snake.snakeimpact():
            running = False

        food.interaction(Snake)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
        


