import pygame
import core.player

player = core.player.Player

class MenuScreen:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button((300, 200, 200, 50), "Играть", self.start),
            Button((300, 270, 200, 50), "Выход", self.exit)
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

# class MenuScreen:
#     def money_status():
#         font = pygame.font.SysFont('Arial', 36)
#         text_string = f"Гроші: {player.money} $"
    
#         text_surface = font.render(text_string, True, (0, 255, 0))
        
#         pygame.screen.blit(text_surface, (20, 20))