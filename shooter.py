import pygame
import os

pygame.init()
clock = pygame.time.Clock()
screen_width = 800
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shooter')


#images
bullet_img = pygame.image.load('assets/img/icon/bullet/bullet.png').convert_alpha()

#game variables
gravity = 0.75
shoot = False

#soldier class
class Soldier(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.alive = True
        self.direction = 1
        self.shoot_cooldown = 0
        self.ammo = ammo
        self.start_ammo = ammo
        self.flip = False
        self.jump = False
        self.in_air = False
        self.vel_y = 0
        self.speed = speed
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0

        #load all images
        animation_types = ['idle', 'run', 'jump']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'assets/img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)  
         
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        #update cool down
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1    

    def movement(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            self.flip = False
            self.direction = 1
            dx = self.speed

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -10
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        #check collisions with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #reduce ammo
            self.ammo -= 1




    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #list index keep in range
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        #check if new action is diff from previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


BG = (100, 100, 130)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0 ,300), (screen_width, 300))   


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()

        #check collisions with the players
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                self.kill()

        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                self.kill()        



#create sprite groups
bullet_group = pygame.sprite.Group()
player = Soldier('player', 200, 200, 2, 5, 20)

enemy = Soldier('enemy', 400, 200, 2, 5, 20)

run = True
moving_left = True
moving_right = True

while run:
    #backgroud
    draw_bg()
    player.draw()
    player.update()

    enemy.draw()
    enemy.update()

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    if player.alive:

        if shoot:
            player.shoot()
            
        if player.in_air:
            player.update_action(2) #jump
            
        elif moving_left or moving_right:
            player.update_action(1) #moving animation

        else:
            player.update_action(0) #idle animation

        player.movement(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        #key press
        if event.type == pygame.KEYDOWN:
            #close game
            if event.key == pygame.K_ESCAPE:
                run = False

            #movement when key pressed
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True

            if event.key == pygame.K_SPACE:
                shoot = True

            #jump
            if event.key == pygame.K_w and player.alive:
                player.jump = True

        #key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot = True

        if event.type == pygame.MOUSEBUTTONUP:
            shoot = False    



    pygame.display.update()
    clock.tick(60)

pygame.quit()