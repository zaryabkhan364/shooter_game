import pygame

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = int(screen_width * 0.8)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Shooter')


class Soldier(pygame.sprite.Sprite):

    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/img/player/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


x = 200
y = 200
scale = 2
player = Soldier(x, y, scale)


run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(player.image, player.rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()