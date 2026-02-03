import pygame

def draw_rect(surface, color=(0, 0, 0)):
    rect = pygame.Rect(5, 5, 795, 25)
    pygame.draw.rect(surface, color, rect)