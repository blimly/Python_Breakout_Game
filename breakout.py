import pygame
import random
import time


class Game:
    def __init__(self):
        # Test
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Breakout Game")
        self.running = True
        self.tick_length = 1 / 30
        self.BACKGROUND_COLOUR = (20, 20, 50)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False

    def update(self):
        pass

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOUR)
        pygame.display.flip()

    def run(self):
        while self.running:
            start = time.time()
            self.input()
            self.update()
            self.render()
            time.sleep(self.tick_length - (time.time() - start))
        pygame.quit()


game = Game()
game.run()
