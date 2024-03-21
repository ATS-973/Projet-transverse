import pygame
import time

class WeaponFist:
    def __init__(self) -> None:
        self.name = "Bat"
        self.range_weapon = "..."
        self.damage = "..."
        self.rarity = "Common"
        self.angle = "..."
        self.sprite = pygame.image.load("fist.png")

class WeaponBat:
    def __init__(self) -> None:
        self.name = "Bat"
        self.range_weapon = "..."
        self.damage = "..."
        self.rarity = "Common"
        self.angle = "..."
        self.sprite = pygame.image.load("bat.png")

class WeaponRifle:
    def __init__(self) -> None:
        self.name = "Rifle"
        self.range_weapon = "..."
        self.damage = "..."
        self.rarity = "Rare"
        self.angle = "..."
        self.sprite = pygame.image.load("rifle.png")

class WeaponGrenade:
    def __init__(self) -> None:
        self.name = "Grenade"
        self.ray_explosion = "..."
        self.damage = "..."
        self.rarity = "Epic"
        self.angle = "..."
        self.timer = "..."
        self.sprite = pygame.image.load("grenade.png")
    
    def time():
        pass

class BombWeapon:
    def __init__(self) -> None:
        self.name = "Bomb"
        self.ray_explosion = "..."
        self.damage = "..."
        self.rarity = "Legendary"
        self.angle = "..."
        self.timer = 5
        self.sprite = pygame.image.load("bomb.png")
    
    def time(self):
        while self.timer:
            time.sleep
            self.timer -=1