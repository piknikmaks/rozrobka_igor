import pygame
import core.player

player = core.player.Player

class ShopScreen:
    def money_status():
        font = pygame.font.SysFont('Arial', 36)
        text_string = f"Рівень: {player.level} $"
    
        text_surface = font.render(text_string, True, (0, 255, 0))
        
        pygame.screen.blit(text_surface, (20, 20))