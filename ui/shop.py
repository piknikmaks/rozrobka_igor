import pygame
import core.player
from ui.widgets import Button

player = core.player.Player()

class ShopScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button((300, 200, 200, 50), player.level, self.start),
            Button((300, 270, 200, 50), player.money, self.exit)
        ]

    def start(self):
        self.game.state = "play"

    def exit(self):
        self.game.running = False

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def draw(self, surface):
        for b in self.buttons:
            b.draw(surface)