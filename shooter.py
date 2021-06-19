import pygame
import os

pygame.init()
clock = pygame.time.Clock()
screen_width = 800
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shooter')


#game variables
gravity = 0.75

#soldier class
class Soldier(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.alive = True
        self.direction = 1
        self.flip = False
        self.jump = False
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
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)  
         
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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

        if self.jump == True:
            self.vel_y = -10
            self.jump = False

        self.vel_y += gravity

        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy


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


BG = (150, 200, 130)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0 ,300), (screen_width, 300))   


player = Soldier('player', 200, 200, 2, 5)

run = True
moving_left = True
moving_right = True

while run:

    draw_bg()
    player.draw()
    player.update_animation()

    if player.alive:
        if moving_left or moving_right:
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
            #jump
            if event.key == pygame.K_w and player.alive:
                player.jump = True

        #key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False


    pygame.display.update()
    clock.tick(60)

pygame.quit()