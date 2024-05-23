import pygame
from game import Game

#Permet de lander le jeu
if __name__ == '__main__':
    pygame.init()
    play = Game()
    play.run()

