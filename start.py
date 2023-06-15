import pygame

class Start:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.image = pygame.image.load('graphics/red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40 *2, 32 * 2))
        self.rect = self.image.get_rect(center = (screen_width/2, screen_height/2))
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)
        
        self.font_surf = self.font.render(f'Press Space to start', False, (255,255,255))
        self.font_rect = self.font_surf.get_rect(center = (screen_width/2, screen_height/2 + 100))

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.font_surf, self.font_rect)
