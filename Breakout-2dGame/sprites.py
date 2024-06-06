import pygame
from settings import *
from random import choice, randint

class Upgrade(pygame.sprite.Sprite):
    def __init__(self, pos, type, groups, game):
        super().__init__(groups)
        self.type = type
        self.image = pygame.image.load(f'../licenta2/graphics/upgrades/{type}.png').convert_alpha()
        self.rect =self.image.get_rect(midtop = pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300
        self.game = game

    def update(self, dt):
        if not self.game.paused:    
            self.pos.y += self.speed * dt
            self.rect.y = round(self.pos.y)

        if self.rect.top > windowH + 100:
            self.kill

class Bar(pygame.sprite.Sprite):
    def __init__(self, groups, surfacemaker, game):
        super().__init__(groups)
        self.game = game
        
        #setup
        self.surfacemaker = surfacemaker
        self.image = surfacemaker.get_surf('bar', (windowW // 5, windowH // 20))

        #position
        self.rect = self.image.get_rect(midbottom = (windowW // 2, windowH - 20))
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.speed = 900
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def input(self):
        if not self.game.paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
            else:
                self.direction.x = 0
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.direction.x = 0
            elif keys[pygame.K_LEFT]:
                self.direction.x = 0
            else:
                self.direction.x = 0

    def screen_constraint(self):
        if self.rect.right > windowW:
            self.rect.right = windowW
            self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    def upgrade(self, upgrade_type):
        if upgrade_type == 'speed+' :
            self.speed += 50
        if upgrade_type == 'size+':
            new_width = self.rect.width * 1.1
            self.image = self.surfacemaker.get_surf('bar', (new_width, self.rect.height))
            self.rect = self. image.get_rect(center = self.rect.center)
            self.pos.x = self.rect.x
        if upgrade_type == 'speed-' :
            self.speed -= 50
        if upgrade_type == 'size-':
            new_width = self.rect.width * 0.9
            self.image = self.surfacemaker.get_surf('bar', (new_width, self.rect.height))
            self.rect = self. image.get_rect(center = self.rect.center)
            self.pos.x = self.rect.x


    def update(self, dt):
        self.input()
        self.old_rect = self.rect.copy()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.screen_constraint()

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, bar, blocks , game):
        super().__init__(groups)

        #collision objects
        self.bar = bar
        self.blocks = blocks
        self.game = game

        #graphics setup
        original_image = pygame.image.load('../licenta2/graphics/res/ball.png').convert_alpha()
        scaled_width = int(original_image.get_width() * 0.7)
        scaled_height = int(original_image.get_height() * 0.7)
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))


        #position setup
        self.rect = self.image.get_rect(midbottom = bar.rect.midtop)
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2((choice((1,-1)),-1))
        self.speed = 700
            
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #active
        self.active = False

        #sounds
        self.impact_sound = pygame.mixer.Sound('../licenta2/sounds/impact.wav')
        self.impact_sound.set_volume(0.1)

        self.fail_sound = pygame.mixer.Sound('../licenta2/sounds/fail.wav')
        self.fail_sound.set_volume(0.1)

    def window_collision(self, direction):
        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1

            if self.rect.right > windowW:
                self.rect.right = windowW 
                self.pos.x = self.rect.x
                self.direction.x *= -1
                
        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1

            if self.rect.bottom > windowH:
                self.active = False
                self.direction.y = -1
                self.fail_sound.play()

    def collision(self, direction):
        #find overlapping objects
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.bar.rect):
            overlap_sprites.append(self.bar)
        
        if overlap_sprites:
            if direction == 'horizontal':
                for sprite in overlap_sprites:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left -1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.impact_sound.play()

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right +1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.impact_sound.play()
                        

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(1)

            if direction == 'vertical':
                    for sprite in overlap_sprites:
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top -1
                            self.pos.y = self.rect.y
                            self.direction.y *= -1
                            self.impact_sound.play()

                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom +1
                            self.pos.y = self.rect.y
                            self.direction.y *= -1
                            self.impact_sound.play()

                        if getattr(sprite, 'health', None):
                            sprite.get_damage(1)

    def update(self, dt):
        if self.active:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            #create old rectangle
            self.old_rect = self.rect.copy()

            #horizontal movement + collision
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.window_collision('horizontal')

            #vertical movement + collision
            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.pos.y)
            self.collision('vertical')
            self.window_collision('vertical')
        else:
            self.rect.midbottom = self.bar.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)
        
        if self.game.paused == True:
            self.speed = 0
        else:
            self.speed = 700

class Block(pygame.sprite.Sprite):
    def __init__(self, type, pos, groups, surfacemaker, create_upgrade):
        super().__init__(groups)
        self.surfacemaker = surfacemaker
        self.image = surfacemaker.get_surf(colorLegend[type], (blockWidth, blockHeight))
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        #damege
        self.health = int(type)

        self.create_upgrade = create_upgrade

    def get_damage(self, amount):
        self.health -= amount

        if self.health > 0:
            self.image = self.surfacemaker.get_surf(colorLegend[str(self.health)], (blockWidth, blockHeight))
        else:
            if randint(0,10)  < 3:
                self.create_upgrade(self.rect.center)
            self.kill()

class TVstyle:
    def __init__(self):
        vignette = pygame.image.load('../licenta2/graphics/res/tv.png').convert_alpha()
        self.scaled_vignette = pygame.transform.scale(vignette,(windowW, windowH))
        self.display_surface = pygame.display.get_surface()
        self.create_tv_lines()

    def create_tv_lines(self):
        line_height = 4
        line_amount = windowH // line_height
        for line in range(line_amount):
            y = line* line_height
            pygame.draw.line(self.scaled_vignette, 'black', (0,y), (windowW,y), 1)

    def draw(self):
        self.scaled_vignette.set_alpha(randint(10,50))
        self.display_surface.blit(self.scaled_vignette,(0,0))