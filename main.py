import pygame, random, os
from player import Player
import obstacle
from alien import Alien, Extra
from laser import Laser
from game_over import Game_over
from start import Start
from victory import Won
 
#! Game class - armazena todo o jogo
class Game:
    def __init__(self):
        #? Instanciar as sprites - Player e obstáculos
        #! Player Setup
        self.player = pygame.sprite.GroupSingle(Player((SCREEN_WIDTH/2,SCREEN_HEIGHT), SCREEN_WIDTH, 5))
    
        #! Health System and Score
        self.health_surf = pygame.image.load('graphics/player.png')
        self.health_surf = pygame.transform.rotozoom(self.health_surf, 0, 0.75)
        self.health = 3
        self.health_x_start_pos = SCREEN_WIDTH - (self.health_surf.get_size()[0] * 2 + 20)
        
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)
    
        #! - Obstacle Setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num*(SCREEN_WIDTH/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.blocks = pygame.sprite.Group()
        self.create_multi_obstacles(self.obstacle_x_positions, x_start=SCREEN_WIDTH/15, y_start=480)
    
        #! - Alien Setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1
        
        #! Extra Alien
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = random.randint(400,800)
        
        #! Audio
        self.music = pygame.mixer.Sound('sounds/music.wav')
        self.music.set_volume(0.05)
        self.music.play(loops=-1)
        
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
        self.explosion_sound.set_volume(0.1)
        
        self.laser_sound = pygame.mixer.Sound('sounds/laser.wav')
        self.laser_sound.set_volume(0.07)
  
    #! Obstacle functions
    def create_multi_obstacles(self,offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(offset_x, x_start, y_start)
    
    def create_obstacle(self, offset_x, x_start, y_start):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + (col_index * self.block_size) + offset_x
                    y  = y_start + (row_index * self.block_size)
                    block = obstacle.Block(self.block_size, vermelho, x, y)
                    self.blocks.add(block)

    #! Alien functions
    def alien_setup(self,rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                
                if row_index == 0: alien_sprite = Alien('yellow', x,y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('green', x,y)
                else: alien_sprite = Alien('red', x,y)
                self.aliens.add(alien_sprite)
    
    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= SCREEN_WIDTH or alien.rect.x <= 0:
                self.alien_direction *= -1
                self.alien_move_down(3)
                break
    
    def alien_move_down(self, distance):
        if self.aliens:
            all_aliens = self.aliens.sprites()
            for alien in all_aliens:
                alien.rect.y += distance
    
    def alien_shoot(self):
        if self.aliens:
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,-6, SCREEN_HEIGHT)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()
    
    #! Extra Alien functions
    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(random.choice(['right', 'left']), SCREEN_WIDTH))
            self.extra_spawn_time = random.randint(400,800)
    
    #! Collisions
    def collision_checks(self):
        global game_over, run_game
        #? Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #? Obstacle Collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True): laser.kill()
                
                #? Alien Collisions
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True, pygame.sprite.collide_mask)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                        if self.score >= 1000:
                            pygame.time.set_timer(alien_laser_timer, 500)
                        elif self.score >= 2000:
                            pygame.time.set_timer(alien_laser_timer, 400)
                        elif self.score >= 3000:
                            pygame.time.set_timer(alien_laser_timer, 300)
                        elif self.score >= 4000:
                            pygame.time.set_timer(alien_laser_timer, 100)
                    laser.kill()
                    self.explosion_sound.play()
    
                #? Extra Alien Collision
                if pygame.sprite.spritecollide(laser, self.extra, True, pygame.sprite.collide_mask): 
                    self.score += 500
                    laser.kill()
    
        #? Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                #? Player Collision
                if pygame.sprite.spritecollide(laser, self.player, False, pygame.sprite.collide_mask): 
                    laser.kill()
                    self.health -= 1
                    if self.health <= 0:
                        run_game = False
                        game_over = True    
                        self.aliens.empty()         
                        self.alien_lasers.empty()   
                        self.blocks.empty()
                
                #? Obstacle Collision
                if pygame.sprite.spritecollide(laser, self.blocks, True): laser.kill()
    
        #? Aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    run_game = False
                    game_over = True    
                    self.aliens.empty()         
                    self.alien_lasers.empty()   
                    self.blocks.empty()
                    
    
    #! Health System and Score
    def display_lives(self):
        for live in range(self.health - 1):
            x = self.health_x_start_pos + (live * (self.health_surf.get_size()[0] + 10))
            screen.blit(self.health_surf, (x, 8))
    
    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', False, branco)
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf, score_rect)
        return self.score
    
    def run(self):
    #? draw all sprite groups
        #! Draw Player
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        
        #! Draw Obstacles
        self.blocks.draw(screen)
        
        #! Draw Aliens
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        
        #! Extra Alien  
        self.extra.draw(screen)
        
        #! Health System and Score
        self.display_lives()
        self.display_score()
        
    #? update all sprite groups
        #! Player Update
        self.player.sprite.lasers.update()
        self.player.update()
        
        #! Alien Update
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        
        #! Extra Alien Update
        self.extra_alien_timer()
        self.extra.update()
        
        #! Collision
        self.collision_checks()

class CRT:
    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (SCREEN_WIDTH,SCREEN_HEIGHT), )
        
    def create_crt_lines(self):
        line_height = 3
        line_amount = int(SCREEN_HEIGHT / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, (0,0,0),(0,y_pos), (SCREEN_WIDTH, y_pos), 1)
        
    def draw(self):
        self.tv.set_alpha(random.randint(75,90))
        self.create_crt_lines()
        screen.blit(self.tv, (0,0))
    
def restart_game():
    global game_over, start, run_game
    game.score = 0
    game.health = 3
    game.block_size = 6
    game.obstacle_amount = 4
    game.extra_spawn_time = random.randint(400,800)
    game.alien_setup(rows=6, cols=8)
    obstacle_x_positions = [num*(SCREEN_WIDTH/game.obstacle_amount) for num in range(game.obstacle_amount)]
    game.create_multi_obstacles(obstacle_x_positions, x_start=SCREEN_WIDTH/15, y_start=480)
    game.player.sprite.lasers.empty()
    
    game_over = False
    start = False
    run_game = True
    
#! cores
preto = (30,30,30)
vermelho = (241,79,80)
branco = (255,255,255)

#! Game Screen and Basic Setup
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    game = Game()
    crt = CRT()
    run_game_over = Game_over(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    start_game = Start(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    victory_game = Won(screen, SCREEN_WIDTH,SCREEN_HEIGHT)
    
    game_over = False
    start = True
    run_game = False
    
#! Timer
    alien_laser_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(alien_laser_timer, 800)
    
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if run_game:    
                if event.type == alien_laser_timer:
                    game.alien_shoot()
            
            if event.type == pygame.KEYDOWN:     
                if game_over:
                    if event.key == pygame.K_SPACE:
                        restart_game()
                
                elif start:
                    if event.key == pygame.K_SPACE:
                        game_over = False
                        start = False
                        run_game = True
                        
                        
                elif not game.aliens:
                    if event.key == pygame.K_SPACE:
                        restart_game()
                
        screen.fill(preto)
    
        if game_over:
            run_game_over.draw_message(game.score)
        else:
            if start:
                start_game.draw()
            else:
                if game.aliens:
                    game.run()
                    crt.draw()
                else:
                    run_game = False
                    game_over = False
                    victory_game.draw_message()    
        
        pygame.display.update()
    