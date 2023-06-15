import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color,x,y):
        pygame.sprite.Sprite.__init__(self)
        file_path = f'graphics/{color}.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.mask = pygame.mask.from_surface(self.image)
        
        if color == 'red': self.value = 100
        elif color == 'green': self.value = 200
        else: self.value = 300
        
    def update(self, direction):
        self.rect.x += direction
        
class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics/extra.png')
        self.screen_width = screen_width
                
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3
            
        self.rect = self.image.get_rect(topleft = (x,70))
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        self.rect.x += self.speed
