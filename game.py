import pygame
import pytmx
import pyscroll
from character import Player


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((1918, 1078))
        pygame.display.set_caption("Pygame Tiled Demo")


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

    def update(self):
        self.group.update()
        self.player.update()

        #verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
            if sprite.feet.collidelist(self.ground) > -1:
                self.player.touchGround = 1
            else: #sprite.feet.collidelist(self.ground) == False:
                self.player.touchGround = 0

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu
        running = True

        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()