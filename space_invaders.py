#Produced by prompting the OpenAI Codex engine. This line is not a part of the prompt.

#Define a python function for playing the classic Space Invaders.
#Display playing field using pygame library.
#Display a score.

import pygame
import random

#Set default window size
WIDTH = 700
HEIGHT = 600
FPS = 60

#Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Initalise pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 25)

#Set background image
background_img = pygame.image.load('spacebg.jpg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_rect = background_img.get_rect()

#Load all game graphics
player_img = pygame.image.load('player.png')
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load('bullet.png')
meteor_images = []
meteor_list = ["meteor_01.png", "meteor_02.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img))

#Game Loop
def gameLoop():
    gameExit = False
    gameOver = False
    
    #Create the player
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img, (50, 38))
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 0
    
        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
    
        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
    
    #Create the enemy
    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image_orig = random.choice(meteor_images)
            #self.image_orig.set_colorkey(BLACK)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * .85 / 2)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)
            self.rot = 0
            self.rot_speed = random.randrange(-8, 8)
            self.last_update = pygame.time.get_ticks()
    
        def rotate(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot + self.rot_speed) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center
    
        def update(self):
            self.rotate()
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)
    
    #Create the bullet
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = bullet_img
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10
    
        def update(self):
            self.rect.y += self.speedy
            #Kill if it moves off the top of the screen
            if self.rect.bottom < 0:
                self.kill()
    
    #Create Message on Screen
    def message_to_screen(msg, color):
        screen_text = font.render(msg, True, color)
        screen.blit(screen_text, [100, HEIGHT/2])
        
    #Create the sprite.Group() and add all sprites
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
        
    #Create player object
    player = Player()
    all_sprites.add(player)
        
    #Create enemy object
    for i in range(8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        
    while not gameExit:
        while gameOver == True:
            screen.fill(WHITE)
            message_to_screen("GAME OVER, press C to play again or Q to quit", RED)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        #Keep loop running at right speed
        clock.tick(FPS)
        #Process input (events)
        for event in pygame.event.get():
            #Check for closing window
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        
        #Update
        all_sprites.update()            
        
        #Check to see if bullet hits mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            
        #Check to see if mob hits player
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            gameOver = True
        
        #Draw/render
        screen.fill(BLACK)
        screen.blit(background_img, background_rect)
        all_sprites.draw(screen)
        # *After drawing everything, flip display
        pygame.display.flip()
    
    pygame.quit()
    quit()

gameLoop()
