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


class Game:
    def __init__(self):
        # Test
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Breakout Game")
        self.running = True
        self.tick_length = 1 / 30
        self.BACKGROUND_COLOUR = (20, 20, 50)
        self.paddle = Paddle((640 - 60) // 2, 20, 60, (150, 150, 255))

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
        self.paddle.move()

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOUR)
        self.paddle.draw(self.screen)
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
