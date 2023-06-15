import pygame

class Won:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font('font/Pixeled.ttf', 30)
        
        self.surf = self.font.render(f'You Won', False, (255,255,255))
        self.rect = self.surf.get_rect(center = (screen_width/2, screen_height/2))
        

    def draw_message(self):
        self.screen.blit(self.surf,self.rect)