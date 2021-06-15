import pygame

pygame.init()
clock = pygame.time.Clock()
screen_width = 800
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shooter')

#soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.direction = 1
        self.flip = False
        self.speed = speed
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'assets/img/{self.char_type}/idle/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)    
        temp_list = []    
        for i in range(6):
            img = pygame.image.load(f'assets/img/{self.char_type}/run/{i}.png')
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

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        #check if time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #list index keep in range
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


BG = (150, 200, 130)
def draw_bg():
    screen.fill(BG)        


player = Soldier('player', 200, 200, 2, 5)

run = True
moving_left = True
moving_right = True

while run:

    draw_bg()
    player.draw()
    player.update_animation()
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

        #key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False


    pygame.display.update()
    clock.tick(60)

pygame.quit()