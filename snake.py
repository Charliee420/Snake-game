import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Box / Window Dimensions
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game by Antigravity")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Snake Settings
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    win.blit(value, [0, 0])

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    # Center the message
    text_rect = mesg.get_rect(center=(WIDTH/2, HEIGHT/2 + y_offset))
    win.blit(mesg, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    # Starting Position
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Place initial food
    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    clock = pygame.time.Clock()

    while not game_over:

        while game_close == True:
            win.fill(BLACK)
            message("You Lost! Press C-Play Again or Q-Quit", RED, -20)
            message(f"Final Score: {Length_of_snake - 1}", WHITE, 20)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != SNAKE_BLOCK:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -SNAKE_BLOCK:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != SNAKE_BLOCK:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -SNAKE_BLOCK:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Boundary Check
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        win.fill(BLACK)
        
        # Draw Food
        pygame.draw.rect(win, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        
        # Snake Movement Logic
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self Collision Check
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw Snake
        for x in snake_List:
            pygame.draw.rect(win, GREEN, [x[0], x[1], SNAKE_BLOCK, SNAKE_BLOCK])

        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if ate food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

if __name__ == "__main__":
    gameLoop()
