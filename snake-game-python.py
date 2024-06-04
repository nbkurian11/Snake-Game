import pygame
import sys
import random

# Constants
FPS = 10
CELL = 20
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

# Colours
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        self.color = WHITE
        self.rect = pygame.Rect(pos, size)
        self.font = pygame.font.SysFont("Times New Roman", 46)
        self.text_surf = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)
        display.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

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
    start_button = Button("Start", (DISPLAY_WIDTH // 2 - 100, DISPLAY_HEIGHT // 2 - 50), (200, 100))
    quit_button = Button("Quit", (DISPLAY_WIDTH // 2 - 100, DISPLAY_HEIGHT // 2 + 100), (200, 100))

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                menu = False
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        display.fill(BLACK)
        start_button.draw(display)
        quit_button.draw(display)
        pygame.display.flip()

# Main loop
def main():
    pygame.mixer.pre_init(44100,16,2,4096)
    pygame.init()
    pygame.font.init()  # Initialize the font module
    display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    background_image = pygame.image.load("bg.png")

    #timer
    start_time = pygame.time.get_ticks()
    timer_font =pygame.font.SysFont(None, 36)
    
    #play background music
    pygame.mixer.music.load("jungle.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #display main_menu
    main_menu(display)

    # Initialize font for score display
    font = pygame.font.SysFont(None, 36)

    snake = Snake()
    food = Food()

    score = 0

    running = True
    while running:
        # Calculate time and render timer
        current_time = pygame.time.get_ticks() - start_time
        seconds = current_time // 1000 
        timer_text = timer_font.render(f'Time: {seconds // 60:02}:{seconds % 60:02}', True, WHITE)
        display.blit(timer_text, (DISPLAY_WIDTH - timer_text.get_width() - 10, 10))
        
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


