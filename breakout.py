import pygame
import random
import time


class Paddle:
    def __init__(self, initial_location, height, width, colour):
        self.location = initial_location
        self.height = height
        self.width = width
        self.colour = colour
        self.moving = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.location - self.width // 2, 480 - self.height, self.width, self.height))

    def move(self):
        new_location = self.location + 10 * self.moving
        if new_location - self.width // 2 >= 0 and new_location + self.width // 2 <= 640:
            self.location = new_location


class Ball:
    def __init__(self, x, y, game, vx, vy):
        self.x = x
        self.y = y
        self.game = game
        self.vx = vx
        self.vy = vy
        self.radius = 5
        self.colour = (0, 255, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

    def update(self):
        self.move()
        self.handle_collision()

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def handle_collision(self):
        if self.x < self.radius:
            self.vertical_collision(self.radius)
        if self.x > self.game.width - self.radius:
            self.vertical_collision(self.game.width - self.radius)
        at_paddle = self.game.paddle.location - self.game.paddle.width / 2 < self.x < self.game.paddle.location + self.game.paddle.width / 2
        if self.y < self.radius:
            self.horizontal_collision(self.radius)
        if self.y > self.game.height - self.radius - self.game.paddle.height and at_paddle:
            self.horizontal_collision(self.game.height - self.radius - self.game.paddle.height)
            self.vx += self.game.paddle.moving * (2 + random.random())
        for brick in self.game.bricks:
            if not brick.alive:
                continue
            collides = brick.x - self.radius < self.x < brick.x + brick.w + self.radius and brick.y - self.radius < self.y < brick.y + brick.h + self.radius
            if collides:
                brick.alive = False
                self.horizontal_collision(brick.y + brick.h + self.radius)

    def vertical_collision(self, collision_line):
        self.vx = -(self.vx + random.uniform(-1, 1))
        self.x = collision_line - (self.x - collision_line)

    def horizontal_collision(self, collision_line):
        self.vy = -(self.vy + random.uniform(-1, 1))
        self.y = collision_line - (self.y - collision_line)


class Brick:
    def __init__(self, x, y, w, h, colour, game):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.colour = colour
        self.alive = True
        self.game = game

    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.w, self.h))

    def check_collision(self):
        if not self.alive:
            return


class Game:
    def __init__(self):
        # Test
        pygame.init()
        self.width = 640
        self.height = 480
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Breakout Game")
        self.running = True
        self.tick_length = 1 / 30
        self.BACKGROUND_COLOUR = (20, 20, 50)
        self.paddle = Paddle((640 - 60) // 2, 20, 60, (255, 255, 255))
        self.ball = Ball(self.width // 2, self.height // 2, self, random.random() * 4 - 2, 8)
        self.bricks = []
        for y in range(1):
            for x in range(10):
                self.bricks.append(Brick(x * 64, y * 20, 64, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), self))
        self.state = "running"
        self.font = pygame.font.SysFont('Arial', 30)
        self.text = self.font.render('TalTech INIT23', True, (227, 10, 127))
        self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))

    def set_state(self, state):
        self.state = state
        if state == 'won':
            self.text = self.font.render('W', True, (255, 255, 255))
            self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
        elif state == 'lost':
            self.text = self.font.render('L', True, (255, 255, 255))
            self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
        elif state == 'running':
            self.text = self.font.render('TalTech INIT23', True, (227, 10, 127))
            self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOUR)  # clear the screen
        for brick in self.bricks:
            brick.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        if self.state == 'running':
            self.screen.blit(self.text, self.text_rect)
        elif self.state == 'won':
            self.text = self.font.render('W', True, (0, 255, 0))
            self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(self.text, self.text_rect)
            end_text = self.font.render(f"You {self.state}! Press \"R\" to try again.", True, (255, 255, 255))
            self.screen.blit(end_text, (self.width // 2 - end_text.get_width() // 2, self.height // 2 + 40))
        elif self.state == 'lost':
            self.text = self.font.render('L', True, (255, 0, 0))
            self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(self.text, self.text_rect)
            end_text = self.font.render(f"You {self.state}! Press \"R\" to try again.", True, (255, 255, 255))
            self.screen.blit(end_text, (self.width // 2 - end_text.get_width() // 2, self.height // 2 + 40))

        pygame.display.update()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False
                if event.key == pygame.K_a:
                    self.paddle.moving = -1
                if event.key == pygame.K_d:
                    self.paddle.moving = 1
                # Add this block to check for a key press to restart the game
                if self.state in ["won", "lost"] and event.key == pygame.K_r:
                    self.restart_game()
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    self.paddle.moving = 0

    def restart_game(self):
        self.paddle = Paddle((640 - 60) // 2, 20, 60, (255, 255, 255))
        self.ball = Ball(self.width // 2, self.height // 2, self, random.random() * 4 - 2, 8)
        self.bricks = []
        for y in range(1):
            for x in range(10):
                self.bricks.append(Brick(x * 64, y * 20, 64, 20,
                                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                         self))
        self.state = "running"
        self.set_state('running')
        self.text = self.font.render('TalTech INIT23', True, (227, 10, 127))
        self.text_rect = self.text.get_rect(center=(self.width // 2, self.height // 2))

    def update(self):
        if self.state == "running":
            self.paddle.move()
            self.ball.update()

            if self.ball.y > self.height:
                self.state = "lost"
            elif all(brick.alive == False for brick in self.bricks):
                self.state = "won"

        self.draw()

    def render(self):
        # Fill the screen with the background colour
        self.screen.fill(self.BACKGROUND_COLOUR)

        # Render the bricks, paddle, and ball
        for brick in self.bricks:
            brick.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

    def run(self):
        while self.running:
            start_time = time.time()
            self.input()
            self.update()
            self.draw()
            elapsed_time = time.time() - start_time
            if elapsed_time < self.tick_length:
                pygame.time.wait(int((self.tick_length - elapsed_time) * 1000))


game = Game()
game.run()
