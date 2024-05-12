import math
import pygame

width = 1918
height = 1078
radius = 5


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):

        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.image.load("bullet.png")
        self.position = [x,y]
        self.rect = self.image.get_rect()


    def load_image(self, window):
        window.blit(self.image, (self.position[0] - self.radius, self.position[1] - self.radius))



    @staticmethod
    def path(start_x, start_y, angle, time):
        velocity_x = math.cos(angle)
        velocity_y = math.sin(angle)

        distance_x = velocity_x * time
        distance_y = velocity_y * time

        new_x = round(start_x + distance_x)
        new_y = round(start_y - distance_y)

        return new_x, new_y

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):

        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.image.load("grenade.png")
        self.position = [x,y]
        self.rect = self.image.get_rect()


    def load_image(self, window):
        window.blit(self.image, (self.position[0] - self.radius, self.position[1] - self.radius))



    @staticmethod
    def path(start_x, start_y, power, angle, time):
        velocity_x = power * math.cos(angle)
        velocity_y = power * math.sin(angle)

        distance_x = velocity_x * time
        distance_y = velocity_y * time - (0.5 * 9.8 * time**2)

        new_x = round(start_x + distance_x)
        new_y = round(start_y - distance_y)

        return new_x, new_y