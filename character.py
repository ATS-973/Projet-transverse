import pygame

class Worm:
    def __init__(self, name, pv, team, skin):
        self.name = name

        self.team = team
        self.attack = 0
        self.move = 1
        self.skin = pygame.image.load(skin)


    def attack(self):
        pass

    def change_status(self, attack, move):  #Take two 1 or 0 as parameters, 1 for True and 0 for False
        if attack == 1 and move == 1:
            raise ValueError("Attack and move status can't be active together")
        if attack == 0 and move == 0:
            raise ValueError("Attack and move status can't be inactive together")
        if attack != 1 and attack != 0:
            raise ValueError("Attack must be a boolean")
        if move != 1 and move != 0:
            raise ValueError("Move must be a boolean")
        else:
            self.attack = attack
            self.move = move

    def lose_life(self, value):
        self.pv -= value

    def gain_life(self, value):
        self.pv += value

    def death(self):
        if self.pv <= 0:
            pass

#code pour les test
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
        image = pygame.Surface([20, 24])
        image.blit(self.sprite_sheet, (0,0), (x, y, 20, 24))
        return image

# Fin code test