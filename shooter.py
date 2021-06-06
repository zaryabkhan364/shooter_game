import pygame

pygame.init()
clock = pygame.time.Clock()
screen_width = 800
screen_height = int(screen_width * 0.8)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shooter')

#soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load('assets/img/player/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def movement(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


player = Soldier(200, 200, 2, 5)

run = True
while run:

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


    player.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()