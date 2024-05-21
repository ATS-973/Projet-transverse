import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,skin, team):


        super().__init__()
        self.is_alive = True
        self.pv = 100

        self.team = team

        self.sprite_sheet = pygame.image.load(skin)
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()

        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 24)
        self.old_position = self.position.copy()

        self.speed = 3
        self.jump = 40

        self.gravity = 1
        self.touchGround = 1


        self.tour = True

    def loose_pv(self, damage):
        self.pv -= damage
        if self.pv <= 0:
            self.is_alive = False
            self.kill()

    def save_location(self): self.old_position = self.position.copy()

    def move_right(self):
        self.position[0] += self.speed
    def move_left(self):
        self.position[0] -= self.speed
    def move_up(self):
        self.position[1] -= self.jump
        self.touchGround = 0

    def groundTouched(self):
        self.touchGround = 1

    def is_in_air(self):
        if self.touchGround == 0:
            self.speed=1
        else:
            self.speed=3

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        if self.touchGround == 0:
            self.position[1] += self.gravity

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    def get_image(self, x, y):
        image = pygame.Surface([28, 34])
        image.blit(self.sprite_sheet, (0,0), (x, y, 28, 34))
        return image

# Fin code test