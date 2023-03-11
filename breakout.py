import pygame
import random

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BRICK_WIDTH = SCREEN_WIDTH // 10
BRICK_HEIGHT = 20
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
BALL_RADIUS = 5
FPS = 30
BALL_SPEED = 5

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()

# Define functions


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def draw_bricks(brick_grid):
    for i in range(len(brick_grid)):
        for j in range(len(brick_grid[i])):
            if brick_grid[i][j] == 1:
                brick_x = j * BRICK_WIDTH
                brick_y = i * BRICK_HEIGHT + 50
                brick_rect = pygame.Rect(
                    brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
                pygame.draw.rect(screen, GREEN, brick_rect)


def move_paddle(paddle_rect):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and paddle_rect.left > 0:
        paddle_rect.move_ip(-20, 0)
    if keys[pygame.K_d] and paddle_rect.right < SCREEN_WIDTH:
        paddle_rect.move_ip(20, 0)


def move_ball(ball_rect, ball_speed, paddle_rect, brick_grid):
    ball_rect.move_ip(ball_speed)
    # Check for collision with paddle
    if ball_rect.colliderect(paddle_rect):
        ball_speed[1] = -ball_speed[1]
    # Check for collision with walls
    if ball_rect.left < 0 or ball_rect.right > SCREEN_WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball_rect.top < 0:
        ball_speed[1] = -ball_speed[1]
    if ball_rect.bottom > SCREEN_HEIGHT:
        return False
    # Check for collision with bricks
    for i in range(len(brick_grid)):
        for j in range(len(brick_grid[i])):
            if brick_grid[i][j] == 1:
                brick_x = j * BRICK_WIDTH
                brick_y = i * BRICK_HEIGHT + 50
                brick_rect = pygame.Rect(
                    brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
                if ball_rect.colliderect(brick_rect):
                    brick_grid[i][j] = 0
                    ball_speed[1] = -ball_speed[1]
                    break
        else:
            continue
        break
    return True


# Initialize game objects
paddle_rect = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2,
                          SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT //
                        2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [BALL_SPEED, BALL_SPEED]
brick_grid = [[1 for j in range(10)] for i in range(4)]
# Main game loop
game_over = False
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move paddle and ball
    move_paddle(paddle_rect)
    game_over = not move_ball(ball_rect, ball_speed, paddle_rect, brick_grid)

    # Draw objects
    screen.fill(BLACK)
    draw_bricks(brick_grid)
    pygame.draw.rect(screen, BLUE, paddle_rect)
    pygame.draw.circle(screen, RED, ball_rect.center, BALL_RADIUS)

    # Update screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(FPS)

# Game over
font = pygame.font.SysFont(None, 48)
draw_text("Game Over", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
pygame.display.update()
pygame.time.wait(2000)

# Quit Pygame
pygame.quit()
