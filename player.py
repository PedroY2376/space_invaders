import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, x_constraint, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (pos))
        self.mask = pygame.mask.from_surface(self.image)
        self.max_x_constraint = x_constraint
        self.speed = speed
        
        self.lasers = pygame.sprite.Group() 
        self.ready_to_shoot = True
        self.laser_time = 0
        self.laser_cooldown = 600
        
        self.laser_sound = pygame.mixer.Sound('sounds/laser.wav')
        self.laser_sound.set_volume(0.07)
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < self.max_x_constraint:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE] and self.ready_to_shoot:
            self.shoot_laser() 
            self.ready_to_shoot = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
             
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, 8, self.rect.bottom)) 
        
    def recharge_laser(self):
        if not self.ready_to_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready_to_shoot = True
    
    def update(self):
        self.get_input()
        self.recharge_laser()