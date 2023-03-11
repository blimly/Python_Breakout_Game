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
        self.location += 10 * self.moving


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
        self.handle_collision()
        self.move()

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def handle_collision(self):
        if self.x < self.radius or self.x > self.game.width - self.radius:
            self.vertical_collision()
        at_paddle = self.game.paddle.location - self.game.paddle.width / 2 < self.x < self.game.paddle.location + self.game.paddle.width / 2
        if self.y < self.radius or self.y > self.game.height - self.radius - self.game.paddle.height and at_paddle:
            self.horizontal_collision()
        for brick in self.game.bricks:
            if not brick.alive:
                continue
            collides = brick.x - self.radius < self.x < brick.x + brick.w + self.radius and brick.y - self.radius < self.y < brick.y + brick.h + self.radius
            if collides:
                brick.alive = False
                self.horizontal_collision()

    def vertical_collision(self):
        self.vx = - self.vx

    def horizontal_collision(self):
        self.vy = - self.vy


class Brick:
    def __init__(self, x, y, w, h, colour, game):
        self.x, self.y, self.w, self.h = x, y, w, h
        print(x, y, w, h)
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
        self.paddle = Paddle((640 - 60) // 2, 20, 60, (150, 150, 255))
        self.ball = Ball(self.width // 2, self.height // 2, self, random.random() * 4 - 2, 8)
        self.bricks = []
        for y in range(1):
            for x in range(10):
                self.bricks.append(Brick(x * 64, y * 20, 64, 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), self))
        self.state = "running"

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
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    self.paddle.moving = 0

    def update(self):
        if self.state == "running":
            self.paddle.move()
            self.ball.update()
            if self.ball.y > self.height:
                self.state = "lost"
            if not [x for x in self.bricks if x.alive]:
                self.state = "won"

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOUR)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            # print("a")
            brick.draw(self.screen)
        if self.state == "lost":
            self.screen.fill((255, 0, 0))
        if self.state == "won":
            self.screen.fill((0, 255, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            start = time.time()
            self.input()
            self.update()
            self.render()
            time.sleep(max(0, self.tick_length - (time.time() - start)))
        pygame.quit()


game = Game()
game.run()
