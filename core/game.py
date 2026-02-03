import pygame
from core.player import Player
from ui.window import Window
from ui.menu import MenuScreen
from ui.shop import ShopScreen

class Game:
    def __init__(self):
        pygame.init()

        self.window = Window()
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player()

        self.state = "menu"
        self.screens = {
            "menu": MenuScreen(self),
            "shop": ShopScreen(self),
        }

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.screens[self.state].handle_event(event)

    def update(self):
        self.screens[self.state].update()

    def draw(self):
        self.window.clear()
        self.screens[self.state].draw(self.window.screen)
        self.window.flip()