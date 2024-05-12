import pygame
import pytmx
import pyscroll
import math
from character import Player
from Weapon import *



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
        player_position = tmx_data.get_object_by_name("Player_1_1")

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

        elif pressed[pygame.K_1]:
            self.rifle()
        elif pressed[pygame.K_2]:
            self.grenades()

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
        


        #TEST
    bullet_1 = Bullet(0, 0, 10, (255, 255, 255))
    grenade_1 = Grenade(0, 0, 10, (255, 255, 255))

    def redraw_bullet(self):
        global bullet_1
        self.group.draw(self.screen)
        bullet_1.load_image(self.screen)
        pygame.draw.line(self.screen, (0, 0, 0), bullet_line[0], bullet_line[1])
        pygame.display.update()

    def findAngle_bullet(self, pos):
        global bullet_1
        x = bullet_1.position[0]
        y = bullet_1.position[1]
        try:
            angle = math.atan((y - pos[1]) / (x - pos[0]))
        except:
            angle = math.pi / 2
        if pos[1] < y and pos[0] > x:
            angle = abs(angle)
        elif pos[1] < y and pos[0] < x:
            angle = math.pi - angle
        elif pos[1] > y and pos[0] < x:
            angle = math.pi + abs(angle)
        elif pos[1] > y and pos[0] > x:
            angle = (2 * math.pi) - angle
        return angle

    def check_collision_bullet(self, sprite, group):
        return sprite.rect.collidelist(group)

    def rifle(self):
        global bullet_line, bullet_pos, bullet_1
        bullet_1 = Bullet(self.player.position[0]+10, self.player.position[1]+15, radius, (255, 255, 255))
        x, y, time, angle, shoot = self.player.position[0]+10, self.player.position[1]+15, 0, 0, False
        run = True
        while run:
            bullet_1.rect[0]=bullet_1.position[0]
            bullet_1.rect[1]=bullet_1.position[1]

            if shoot:
                time += 0.5
                po = Bullet.path(x, y, angle, time)
                bullet_1.position[0] = po[0]
                bullet_1.position[1] = po[1]

                #verif balle hors map
                if bullet_1.rect.collidelist(self.walls) > -1:
                    shoot = False
                    bullet_1.position[0] = self.player.position[0]+10
                    bullet_1.position[1] = self.player.position[1]+15
                    run = False


            bullet_pos = pygame.mouse.get_pos()
            bullet_line = [(self.player.position[0]+10, self.player.position[1]+15), bullet_pos]
            self.redraw_bullet()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not shoot:
                        shoot = True
                        x = bullet_1.position[0]
                        y = bullet_1.position[1]
                        time = 0
                        angle = self.findAngle_bullet(bullet_pos)
                elif pygame.key.get_pressed()[pygame.K_TAB]:
                    run = False

    

    def redraw_grenade(self):
        global grenade_1
        self.group.draw(self.screen)
        grenade_1.load_image(self.screen)
        pygame.draw.line(self.screen, (0, 0, 0), grenade_line[0], grenade_line[1])
        pygame.display.update()

    def findAngle_grenade(self, pos):
        global grenade_1
        x = grenade_1.position[0]
        y = grenade_1.position[1]
        try:
            angle = math.atan((y - pos[1]) / (x - pos[0]))
        except:
            angle = math.pi / 2
        if pos[1] < y and pos[0] > x:
            angle = abs(angle)
        elif pos[1] < y and pos[0] < x:
            angle = math.pi - angle
        elif pos[1] > y and pos[0] < x:
            angle = math.pi + abs(angle)
        elif pos[1] > y and pos[0] > x:
            angle = (2 * math.pi) - angle
        return angle

    def check_collision_grenade(self, sprite, group):
        return sprite.rect.collidelist(group)

    def grenades(self):
        global grenade_line, grenade_pos, grenade_1
        grenade_1 = Grenade(self.player.position[0] + 10, self.player.position[1] + 15, radius, (255, 255, 255))
        x, y, time, power, angle, shoot = self.player.position[0] + 10, self.player.position[1] + 15, 0, 0, 0, False
        run = True
        while run:
            grenade_1.rect[0] = grenade_1.position[0]
            grenade_1.rect[1] = grenade_1.position[1]

            if shoot:
                time += 0.02
                po = Grenade.path(x, y, power, angle, time)
                grenade_1.position[0] = po[0]
                grenade_1.position[1] = po[1]

                #verif balle hors map
                if grenade_1.rect.collidelist(self.walls) > -1:
                    shoot = False
                    grenade_1.position[0] = self.player.position[0]+10
                    grenade_1.position[1] = self.player.position[1]+15
                    run = False

            grenade_pos = pygame.mouse.get_pos()
            grenade_line = [(self.player.position[0] + 10, self.player.position[1] + 15), grenade_pos]
            self.redraw_grenade()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not shoot:
                        shoot = True
                        x = grenade_1.position[0]
                        y = grenade_1.position[1]
                        time = 0
                        power = math.sqrt((grenade_pos[0] - grenade_1.position[0])**2 + (grenade_pos[1] - grenade_1.position[1])**2)/8
                        angle = self.findAngle_grenade(grenade_pos)
                elif pygame.key.get_pressed()[pygame.K_TAB]:
                    run = False



            # FIN DU TEST
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