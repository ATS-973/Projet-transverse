#import pygame

class Worm:
    def __init__(self, name, pv, team, skin):
        self.name = name
        self.pv = pv
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
    
    def move_right(self, value):
        self.x = value
    def move_left(self, value):  #Don't put a negative value
        self.x = -value
    def jump(self, value):   #Don't put a negative value
        self.y = -value

    def lose_life(self, value):
        self.pv -= value

    def gain_life(self, value):
        self.pv += value

    def death(self):
        if self.pv <= 0:
            pass

class Player:
    def __init__(self, name, teamName, skin):
        self.name = name
        self.teamName = teamName
        self.skin = pygame.image.load(skin)
    
    def change_skin(self, new_skin):
        if self.skin != pygame.image.load(new_skin):
            self.skin = pygame.image.load(new_skin)
    
    def change_name(self, new_name):
        if self.name != new_name:
            self.name = new_name
    
    def change_teamName(self, new_teamName):
        if self.teamName != new_teamName:
            self.teamName = new_teamName