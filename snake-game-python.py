import pygame
import sys
import random

# Constants
FPS = 10
CELL = 20
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)]
        self.direction = pygame.K_LEFT
        self.growth = False

    def movement(self):
        head_x, head_y = self.body[0]
        if self.direction == pygame.K_UP:
            head_y -= CELL
        elif self.direction == pygame.K_DOWN:
            head_y += CELL
        elif self.direction == pygame.K_LEFT:
            head_x -= CELL
        elif self.direction == pygame.K_RIGHT:
            head_x += CELL

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        if not self.growth:
            self.body.pop()
        else:
            self.growth = False

    def change_direction(self, new_direction):
        if new_direction in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            opposite_directions = {pygame.K_UP: pygame.K_DOWN, pygame.K_DOWN: pygame.K_UP,
                                   pygame.K_LEFT: pygame.K_RIGHT, pygame.K_RIGHT: pygame.K_LEFT}
            if new_direction != opposite_directions[self.direction]:
                self.direction = new_direction

    def check_collision(self):
        head_x, head_y = self.body[0]
        # Check collision with walls
        if head_x < 0 or head_x >= DISPLAY_WIDTH or head_y < 0 or head_y >= DISPLAY_HEIGHT:
            return True
        # Check collision with itself
        if len(self.body) > 1 and (head_x, head_y) in self.body[1:]:
            return True
        return False

    def grow_snake(self):
        self.growth = True

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (*segment, CELL, CELL))

# Food class
class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, (DISPLAY_WIDTH - CELL) // CELL) * CELL,
                random.randint(0, (DISPLAY_HEIGHT - CELL) // CELL) * CELL)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (*self.position, CELL, CELL))

# Main menu
def main_menu(display):
    font = pygame.font.SysFont("Arial", 48)
    menu_text = font.render("Enter to Start", True, WHITE)
    text_rect = menu_text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
    display.blit(menu_text, text_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False


# Main loop
def main():
    pygame.mixer.pre_init(44100,16,2,4096)
    pygame.init()
    pygame.font.init()  # Initialize the font module
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    background_image = pygame.image.load("back.png")


    #play background music
    pygame.mixer.music.load("jungle.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)


    

    # Initialize font for score display
    font = pygame.font.SysFont(None, 36)

    snake = Snake()
    food = Food()

    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)

        snake.movement()

        if snake.body[0] == food.position:
            snake.grow_snake()
            food.position = food.random_position()
            score += 1

        if snake.check_collision():
            running = False

        display.blit(background_image, (0, 0))
        snake.draw(display)
        food.draw(display)

        # Display the score
        score_text = font.render(f'Score: {score}', True, WHITE)
        display.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


