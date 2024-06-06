import pygame, sys, time
from settings import *
from sprites import Bar, Ball, Block, Upgrade, TVstyle 
from surfaceMaker import SurfaceMaker
from random import choice, randint

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.displaySurface = pygame.display.set_mode((windowW, windowH))
        pygame.display.set_caption('Testing')
        #background 
        self.backgroundImage = self.create_background()
        self.MainImage = self.create_background2()
        self.play_text, self.more_text, self.quit_text = self.create_buttons()
        #sprite group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        #setup
        self.surfacemaker = SurfaceMaker()
        self.bar = Bar(self.all_sprites, self.surfacemaker, self)
        self.stage_setup()
        self.ball = Ball(self.all_sprites, self.bar, self.block_sprites, self)
        #crt
        self.crt = TVstyle()
        
        self.state = 'intro'

        self.powerup_sound = pygame.mixer.Sound('../licenta2/sounds/powerup.wav')
        self.powerup_sound.set_volume(0.1)

        self.music = pygame.mixer.Sound('../licenta2/sounds/music.wav')
        self.music.set_volume(1)
        self.music.play(loops =-1)

        self.paused = False
        self.last_time = time.time()
        self.clock = pygame.time.Clock()
        self.show_level_message = True


    def create_upgrade(self, pos):
        upgrade_type = choice(upgrades)
        Upgrade(pos, upgrade_type, [self.all_sprites, self.upgrade_sprites], self)

    def create_background(self):
        backgroundImg = pygame.image.load('../licenta2/graphics/res/bg.png').convert()
        scaledBg = pygame.transform.scale(backgroundImg,(windowW, windowH))
        return scaledBg
    
    def create_background2(self):
        backgroundImg = pygame.image.load('../licenta2/graphics/res/bgMain.png').convert()
        scaledBg = pygame.transform.scale(backgroundImg,(windowW, windowH))
        return scaledBg
    
    def create_buttons(self):
        self.play_text = pygame.image.load('../licenta2/graphics/buttons/play.png').convert()
        self.play2_text = pygame.image.load('../licenta2/graphics/buttons/play2.png').convert()
        self.more_text = pygame.image.load('../licenta2/graphics/buttons/more.png').convert()
        self.more2_text = pygame.image.load('../licenta2/graphics/buttons/more2.png').convert()
        self.quit_text = pygame.image.load('../licenta2/graphics/buttons/quit.png').convert()
        self.quit2_text = pygame.image.load('../licenta2/graphics/buttons/quit2.png').convert()
    
        return self.play_text, self.more_text, self.quit_text

    def stage_setup(self):
        for rowIndex, row in enumerate(blockMap1):
            for colIndex, col in enumerate(row):
                if col != ' ':
                    y = rowIndex * blockHeight
                    x = colIndex * blockWidth 
                    Block(col, (x,y), [self.all_sprites, self.block_sprites], self.surfacemaker, self.create_upgrade)
    
    def upgrade_collision(self):
        overlap_sprites = pygame.sprite.spritecollide(self.bar, self.upgrade_sprites, True)
        for sprite in overlap_sprites:
            self.bar.upgrade(sprite.type)
            self.powerup_sound.play()

    def draw_pause(self):
        pause_surface = pygame.Surface((windowW, windowH), pygame.SRCALPHA)
        pause_surface.fill((0, 0, 0, 150))
        self.displaySurface.blit(pause_surface, (0, 0))
        font = pygame.font.Font(None, 150)
        pause_text = font.render("GAME PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(windowW // 2, windowH // 2))
        self.displaySurface.blit(pause_text, text_rect)
        pygame.display.update()

    def runGame(self):
        # Delta time
        dt = time.time() - self.last_time
        self.last_time = time.time()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE and not self.paused:
                    self.ball.active = True
                    if self.show_level_message:
                        self.show_level_message = False

                if event.key == pygame.K_ESCAPE:
                    if self.paused == True:
                        self.paused = False
                    else:
                        self.paused = True

        # Update the game
        self.all_sprites.update(dt)
        self.upgrade_collision()

        # Draw frame
        self.displaySurface.blit(self.backgroundImage, (0, 0))
        self.all_sprites.draw(self.displaySurface)

        # CRT styling
        self.crt.draw()

        # Display "Level 1" 
        if self.show_level_message:
            font = pygame.font.Font(None, 350)
            pause_text = font.render('Level 1', True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(windowW // 2, windowH // 2))
            self.displaySurface.blit(pause_text, text_rect)

        # Checks pause
        if self.paused:
            self.draw_pause()

        # Update window
        pygame.display.update()

    
    def runMainMenu(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_rect = self.play_text.get_rect(center=(windowW // 2, windowH // 4))
                # Check if the mouse click is within the boundaries of the play button
                if play_rect.collidepoint(mouse_x, mouse_y):
                    self.state = 'game'
                quit_rect = self.quit_text.get_rect(center=(windowW // 2, windowH // 1.3))
                # Check if the mouse click is within the boundaries of the play button
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        # Drawing
        # Draw frame
        self.displaySurface.blit(self.MainImage, (0, 0))

        # Check if the mouse is over the play button
        play_rect = self.play_text.get_rect(center=(windowW // 2, windowH // 4))
        if play_rect.collidepoint(mouse_x, mouse_y):
            # If the mouse is over the play button, draw a different image
            self.displaySurface.blit(self.play2_text, play_rect)
        else:
            # If the mouse is not over the play button, draw the regular play button image
            self.displaySurface.blit(self.play_text, play_rect)
        more_rect = self.more_text.get_rect(center=(windowW // 2, windowH // 2))
        if more_rect.collidepoint(mouse_x, mouse_y):
            self.displaySurface.blit(self.more2_text, more_rect)
        else:
            self.displaySurface.blit(self.more_text, more_rect)
        quit_rect = self.play_text.get_rect(center=(windowW // 2, windowH // 1.3))
        if quit_rect.collidepoint(mouse_x, mouse_y):
            self.displaySurface.blit(self.quit2_text, quit_rect)
        else:
            self.displaySurface.blit(self.quit_text, quit_rect)

        # CRT styling
        self.crt.draw()
        # Update window
        pygame.display.update()

    def state_manager(self):
        if self.state == 'intro':
            self.music.set_volume(0.02)
            self.runMainMenu()
        elif self.state == 'game':
            self.music.set_volume(0.1)
            self.runGame()

if __name__ == '__main__':
    game = Game()
    while True:
        game.state_manager()
        game.clock.tick(fps)

