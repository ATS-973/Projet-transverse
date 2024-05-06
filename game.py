import pygame
import pytmx
import pyscroll
import math
from character import Player





class Game:

    def __init__(self):

        #definir si le jeu a commencé
        self.is_playing = False

        self.screen = pygame.display.set_mode((1918, 1078))
        pygame.display.set_caption("Test")
        self.background = pygame.image.load("background.png")

        self.start_button = pygame.image.load("start_button.png")
        self.start_button = pygame.transform.scale(self.start_button, (400,125))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.x = math.ceil(self.screen.get_width() / 2.5)
        self.start_button_rect.y = math.ceil(self.screen.get_height() / 2)

        self.quit_button = pygame.image.load("quit_button.png")
        self.quit_button = pygame.transform.scale(self.quit_button, (400, 125))
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.x = math.ceil(self.screen.get_width() / 2.5)
        self.quit_button_rect.y = math.ceil(self.screen.get_height() / 1.65)


        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('Map/Map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        #coordonnées de spawn du joueur
        player_position = tmx_data.get_object_by_name("Player")

        #definir une liste pour les collisions
        self.walls = []
        self.ground = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
            elif obj.type == "ground":
                self.ground.append(pygame.Rect(obj.x, obj.y,obj.width,obj.height))

         # générer le jouer
        self.player = Player(player_position.x,player_position.y)


        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] and self.player.touchGround == 1:
            self.player.move_up()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_ESCAPE]:
            self.is_playing = False

    def update(self):
        self.group.update()

        #verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
            if sprite.feet.collidelist(self.ground) > -1:
                self.player.groundTouched()
            else:
                self.player.touchGround = 0


    def run(self):

        clock = pygame.time.Clock()

        #boucle du jeu
        running = True

        while running:

            # verif si le jeu a commencé
            if self.is_playing:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.group.draw(self.screen)

            else:
                self.screen.blit(self.background, (0,0))
                self.screen.blit(self.start_button, self.start_button_rect)
                self.screen.blit(self.quit_button, self.quit_button_rect)



            #mettre a jour l ecran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #verif si le joueur clique sur un boutton avec la souris
                    if self.start_button_rect.collidepoint(event.pos):
                        #mettre le jeu en mode lancé
                        self.is_playing = True
                    elif self.quit_button_rect.collidepoint(event.pos):
                        running = False

            clock.tick(60)

        pygame.quit()