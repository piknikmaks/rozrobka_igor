import pygame

class Window:
    def __init__(self, width=800, height=600, title="Clicker game"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        icon = pygame.image.load('assets/click_logo.png')
        pygame.display.set_icon(icon)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        self.bg_color = (222, 247, 255)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        return self.running

    def update_display(self):
        self.screen.fill(self.bg_color)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def cleanup(self):
        pygame.quit()

    def clear(self):
        self.screen.fill(self.bg_color)

def draw_rect(surface, color=(0, 0, 0)):
    rect = pygame.Rect(0, 0, 795, 25)
    pygame.draw.rect(surface, color, rect)