import math
import pygame

# Constants for screen dimensions and bullet radius
width = 1918
height = 1078
radius = 5

################################### BULLET CLASS ###################################
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        # Initialize bullet properties
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.image.load("bullet.png")
        self.position = [x, y]
        self.rect = self.image.get_rect()
        self.damage = 20


    def load_image(self, window):
        # Method to load bullet image onto the window
        window.blit(self.image, (self.position[0] - self.radius, self.position[1] - self.radius))

    # Static method to calculate the trajectory of the bullet
    @staticmethod
    def path(start_x, start_y, angle, time):
        # Calculate velocity components based on angle
        velocity_x = math.cos(angle)
        velocity_y = math.sin(angle)

        # Calculate distance traveled in x and y directions
        distance_x = velocity_x * time
        distance_y = velocity_y * time

        # Calculate new position based on distance traveled
        new_x = round(start_x + distance_x)
        new_y = round(start_y - distance_y)

        return new_x, new_y

################################### GRENADE CLASS ###################################
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        # Initialize grenade properties
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.image.load("grenade.png")
        self.position = [x, y]
        self.rect = self.image.get_rect()
        self.full_damage = 60
        self.mid_damage = 30
        self.low_damage = 10
        self.explo_pos = [0,0]





    def load_image(self, window):
        # Method to load grenade image onto the window
        window.blit(self.image, (self.position[0] - self.radius, self.position[1] - self.radius))

    # Static method to calculate the trajectory of the grenade
    @staticmethod
    def path(start_x, start_y, power, angle, time):
        # Calculate velocity components based on angle and power
        velocity_x = power * math.cos(angle)
        velocity_y = power * math.sin(angle)

        # Calculate distance traveled in x and y directions, accounting for gravity
        distance_x = velocity_x * time
        distance_y = velocity_y * time - (0.5 * 9.8 * time**2)          # Using gravity constant of 9.8 m/s^2

        # Calculate new position based on distance traveled
        new_x = round(start_x + distance_x)
        new_y = round(start_y - distance_y)

        return new_x, new_y
