import pygame

class Game_over:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_game_over = pygame.font.Font('font/Pixeled.ttf', 30)
        self.font_score = pygame.font.Font('font/Pixeled.ttf', 20)
        
        self.surf_game_over = self.font_game_over.render(f'GAME OVER', False, (255,255,255))
        self.rect_game_over = self.surf_game_over.get_rect(center = (screen_width/2, screen_height/2))
        

    def draw_message(self,score):
        self.score_surf = self.font_score.render(f'Your Score: {score}', False, (255,255,255))
        self.score_rect = self.score_surf.get_rect(center = (self.screen_width/2, self.screen_height/2 + 100))
        
        self.screen.blit(self.surf_game_over, self.rect_game_over)
        self.screen.blit(self.score_surf, self.score_rect)
