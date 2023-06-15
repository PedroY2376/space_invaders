import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((4,20))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(midbottom = (pos))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.constraint_y = screen_height
    
    def move(self):
        self.rect.y -= self.speed
    
    def destroy(self):
        if self.rect.y < -self.rect.height or self.rect.y > self.constraint_y:
            self.kill()
    
    def update(self):
        self.move()
        self.destroy()
