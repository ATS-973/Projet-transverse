#import pygame

class Worm:
    def __init__(self, name, pv, team, skin):
        self.name = name
        self.pv = pv
        self.team = team
        self.attack = 0
        self.move = 1
        self.skin = skin

    def move(self):
        pass

    def attack(self):
        pass

    def status(self, attack, move):
        if attack == 1 and move == 1:
            raise ValueError("Attack and move status can't be active together")
        elif attack == 0 and move == 0:
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

class Player:
    def __init__(self, name, teamName, skin):
        self.name = name
        self.teamName = teamName
        self.skin = skin