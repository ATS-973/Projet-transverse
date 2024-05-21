import pygame
import pytmx
import pyscroll
import math
from character import Player
from weapon import *

class Game:

    def __init__(self):

    #definir si le jeu a commencé
        self.is_playing = False
    #definir le winner
        self.winner = None

    #musique de fond
        pygame.mixer.init()
        self.music = pygame.mixer.music.load("menu.mp3")
        pygame.mixer.music.play()

    #création de la fenetre
        self.screen = pygame.display.set_mode((1918, 1078))
        pygame.display.set_caption("Test")
        self.background = pygame.image.load("background.png")
        #initialisation du start button
        self.start_button = pygame.image.load("start_button.png")
        self.start_button = pygame.transform.scale(self.start_button, (400,125))
        self.start_button_rect = self.start_button.get_rect()
        self.start_button_rect.x = math.ceil(self.screen.get_width() / 2.5)
        self.start_button_rect.y = math.ceil(self.screen.get_height() / 2)
        #initialisation du quit button
        self.quit_button = pygame.image.load("quit_button.png")
        self.quit_button = pygame.transform.scale(self.quit_button, (400, 125))
        self.quit_button_rect = self.quit_button.get_rect()
        self.quit_button_rect.x = math.ceil(self.screen.get_width() / 2.5)
        self.quit_button_rect.y = math.ceil(self.screen.get_height() / 1.65)


        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame('Map/Map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())


        #coordonnées de spawn des joueurs
        player_position1_1 = tmx_data.get_object_by_name("Player_1_1")
        player_position1_2 = tmx_data.get_object_by_name("Player_1_2")
        player_position1_3 = tmx_data.get_object_by_name("Player_1_3")
        player_position2_1 = tmx_data.get_object_by_name("Player_2_1")
        player_position2_2 = tmx_data.get_object_by_name("Player_2_2")
        player_position2_3 = tmx_data.get_object_by_name("Player_2_3")

        #coordonnées des tuyaux
        self.tuyaux1 = tmx_data.get_object_by_name("Tuyau 1")
        self.tuyaux2 = tmx_data.get_object_by_name("Tuyau 2")

        # générer les joueurs
        self.player1_1 = Player(player_position1_1.x, player_position1_1.y, "skin_orange.png", 1)
        self.player1_2 = Player(player_position1_2.x, player_position1_2.y, "skin_orange.png", 1)
        self.player1_3 = Player(player_position1_3.x, player_position1_3.y, "skin_orange.png", 1)
        self.player2_1 = Player(player_position2_1.x, player_position2_1.y, "skin_rose.png", 2)
        self.player2_2 = Player(player_position2_2.x, player_position2_2.y, "skin_rose.png", 2)
        self.player2_3 = Player(player_position2_3.x, player_position2_3.y, "skin_rose.png", 2)



    #definir listes pour les collisions
        self.walls = []
        self.ground = []
        self.team1 = []
        self.team2 = []
        self.tuyaux = []

        #ajout des coordonnées dans les listes de coliision
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))
            elif obj.type == "ground":
                self.ground.append(pygame.Rect(obj.x, obj.y,obj.width,obj.height))
            elif obj.type == "tuyaux":
                self.tuyaux.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.team1.append(pygame.Rect(self.player1_1.position[0],self.player1_1.position[1],20,24))
        self.team1.append(pygame.Rect(self.player1_2.position[0],self.player1_2.position[1],20,24))
        self.team1.append(pygame.Rect(self.player1_3.position[0],self.player1_3.position[1],20,24))
        self.team2.append(pygame.Rect(self.player2_1.position[0],self.player2_1.position[1],20,24))
        self.team2.append(pygame.Rect(self.player2_2.position[0],self.player2_2.position[1],20,24))
        self.team2.append(pygame.Rect(self.player2_3.position[0],self.player2_3.position[1],20,24))




        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player1_1)
        self.group.add(self.player1_2)
        self.group.add(self.player1_3)
        self.group.add(self.player2_1)
        self.group.add(self.player2_2)
        self.group.add(self.player2_3)



#Actualise en temps réel les coordonnées des joueurs dans leur liste respective
    def actu_liste_collision(self):
        self.team1[0] = pygame.Rect(self.player1_1.position[0],self.player1_1.position[1],20,24)
        self.team1[1] = pygame.Rect(self.player1_2.position[0],self.player1_2.position[1],20,24)
        self.team1[2] = pygame.Rect(self.player1_3.position[0],self.player1_3.position[1],20,24)
        self.team2[0] = pygame.Rect(self.player2_1.position[0],self.player2_1.position[1],20,24)
        self.team2[1] = pygame.Rect(self.player2_2.position[0],self.player2_2.position[1],20,24)
        self.team2[2] = pygame.Rect(self.player2_3.position[0],self.player2_3.position[1],20,24)



#Permet de récupérer les inputs clavier et d'assigner des commandes aux touches
    def handle_input(self,player):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] and player.touchGround == 1:
            player.move_up()
        elif pressed[pygame.K_DOWN] and player.touchGround == 1:
            self.take_tuyaux(player, self.is_on_tuyaux(player))

        elif pressed[pygame.K_LEFT]:
            player.move_left()
        elif pressed[pygame.K_RIGHT]:
            player.move_right()
        elif pressed[pygame.K_ESCAPE]:
            self.is_playing = False
            pygame.mixer.music.stop()
            self.music = pygame.mixer.music.load("menu.mp3")
            pygame.mixer.music.play(100)

        elif pressed[pygame.K_1] and player.touchGround == 1 and self.winner == None:
            self.tir(player)
        elif pressed[pygame.K_2] and player.touchGround == 1 and self.winner == None:
            self.grenades(player)


#detecte si le joueur se trouve sur le tuyaux 1 ou 2
    def is_on_tuyaux(self, player):
        if player.rect.colliderect(self.tuyaux[0]):
            return self.tuyaux2
        elif player.rect.colliderect(self.tuyaux[1]):
            return self.tuyaux1

#téléporte le joueur au tuyau suivant
    def take_tuyaux(self, player, pos_tuyau):
        player.position[0] = pos_tuyau.x
        player.position[1] = pos_tuyau.y


#Permet de détecter à tous moment si le joueur entre en collision avec le décor ou si il est dans les airs
    def update(self, player):
        self.group.update()

        #verif collision
        if player.feet.collidelist(self.walls) > -1:
            player.move_back()
        if player.feet.collidelist(self.ground) > -1:
            player.groundTouched()
        else:
            player.touchGround = 0
        player.is_in_air()



#Permet d'afficher l'écran d'affichage du gagnant
    def win_screen(self):
        # Display win screen
        self.screen.blit(self.background, (0, 0))
        font = pygame.font.SysFont(None, 100)
        if self.winner == 1:
            text = font.render("PLAYER 1 IS THE WINNER", True, (255, 0, 0))
        else:
            text = font.render("PLAYER 2 IS THE WINNER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()



    ################################### BULLET BEGINNING ###################################
    #création de la balle
    bullet_1 = Bullet(0, 0, 10, (255, 255, 255))



#Permet de dessiner la ligne pour viser et l'image de la balle
    def redraw(self):
        global bullet_1
        self.group.draw(self.screen)
        bullet_1.load_image(self.screen)
        pygame.draw.line(self.screen, (0, 0, 0), line[0], line[1])
        pygame.display.update()



#Permet de changer l'angle de tir à l'aide de la souris
    def findAngle(self, pos):
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



#Gestion du tir
    def tir(self, player):
        global line, pos, bullet_1
        bullet_1 = Bullet(player.position[0]+14, player.position[1]+21.25, radius, (255, 255, 255))
        x, y, time, angle, shoot = player.position[0]+14, player.position[1]+21.25, 0, 0, False
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
                    bullet_1.position[0] = player.position[0]+14
                    bullet_1.position[1] = player.position[1]+21.25
                    run = False
                    player.tour = False
                #verif collision joueur
                if player.team == 1:
                    if bullet_1.rect.colliderect(self.team2[0]) and self.player2_1.is_alive:
                        self.player2_1.loose_pv(bullet_1.damage)
                        player.tour = False
                    elif bullet_1.rect.colliderect(self.team2[1]) and self.player2_2.is_alive:
                        self.player2_2.loose_pv(bullet_1.damage)
                        player.tour = False
                    elif bullet_1.rect.colliderect(self.team2[2]) and self.player2_3.is_alive:
                        self.player2_3.loose_pv(bullet_1.damage)
                        player.tour = False
                elif player.team == 2:
                    if bullet_1.rect.colliderect(self.team1[0]) and self.player1_1.is_alive:
                        self.player1_1.loose_pv(bullet_1.damage)
                        player.tour = False
                    elif bullet_1.rect.colliderect(self.team1[1]) and self.player1_2.is_alive:
                        self.player1_2.loose_pv(bullet_1.damage)
                        player.tour = False
                    elif bullet_1.rect.colliderect(self.team1[2]) and self.player1_3.is_alive:
                        self.player1_3.loose_pv(bullet_1.damage)
                        player.tour = False
                if player.tour == False:
                    shoot = False
                    bullet_1.position[0] = player.position[0] + 14
                    bullet_1.position[1] = player.position[1] + 21.25
                    run = False


            pos = pygame.mouse.get_pos()
            line = [(player.position[0]+14, player.position[1]+21.25), pos]
            self.redraw()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not shoot:
                        shoot = True
                        x = bullet_1.position[0]
                        y = bullet_1.position[1]
                        time = 0
                        angle = self.findAngle(pos)
                elif pygame.key.get_pressed()[pygame.K_TAB]:
                    run = False

    ################################### BULLET END ###################################

    ################################### GRENADE BEGINNING ###################################
    grenade_1 = Grenade(0, 0, 10, (255, 255, 255))


    def redraw_grenade(self):
        # Update grenade position and trajectory
        global grenade_1
        self.group.draw(self.screen)
        grenade_1.load_image(self.screen)
        pygame.draw.line(self.screen, (0, 0, 0), grenade_line[0], grenade_line[1])
        pygame.display.update()

    def findAngle_grenade(self, pos):
        # Calculate angle for grenade trajectory
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
        # Check collision for grenade
        return sprite.rect.collidelist(group)

    def grenades(self, player):
        # Grenade weapon functionality
        global grenade_line, grenade_pos, grenade_1
        grenade_1 = Grenade(player.position[0] + 14,player.position[1] + 21.25, radius, (255, 255, 255))
        x, y, time, power, angle, shoot = player.position[0] + 14, player.position[1] + 21.25, 0, 0, 0, False
        run = True
        while run:
            grenade_1.rect[0] = grenade_1.position[0]
            grenade_1.rect[1] = grenade_1.position[1]

            if shoot:
                time += 0.02
                po = Grenade.path(x, y, power, angle, time)
                grenade_1.position[0] = po[0]
                grenade_1.position[1] = po[1]

                if grenade_1.rect.collidelist(self.walls) > -1:

                    shoot = False
                    grenade_1.explo_pos[0] = grenade_1.rect[0]
                    grenade_1.explo_pos[1] = grenade_1.rect[1]
                    grenade_1.position[0] = player.position[0] + 14
                    grenade_1.position[1] = player.position[1] + 21.25
                    player.tour = False
                    run = False

                    #degat joueur 2_1
                    if abs(self.player2_1.position[0] - grenade_1.explo_pos[0]) <= 40:
                        self.player2_1.loose_pv(grenade_1.full_damage)
                    elif abs(self.player2_1.position[0]-grenade_1.explo_pos[0]) <= 70:
                        self.player2_1.loose_pv(grenade_1.mid_damage)
                    elif abs(self.player2_1.position[0]-grenade_1.explo_pos[0]) <= 100:
                        self.player2_1.loose_pv(grenade_1.low_damage)
                    #degat joueur 2_2
                    if abs(self.player2_2.position[0] - grenade_1.explo_pos[0]) <= 40:
                        self.player2_2.loose_pv(grenade_1.full_damage)
                    elif abs(self.player2_2.position[0]-grenade_1.explo_pos[0]) <= 70:
                        self.player2_2.loose_pv(grenade_1.mid_damage)
                    elif abs(self.player2_2.position[0]-grenade_1.explo_pos[0]) <= 100:
                        self.player2_2.loose_pv(grenade_1.low_damage)
                    #degat joueur 2_3
                    if abs(self.player2_3.position[0] - grenade_1.explo_pos[0]) <= 40:
                        self.player2_3.loose_pv(grenade_1.full_damage)
                    elif abs(self.player2_3.position[0]-grenade_1.explo_pos[0]) <= 70:
                        self.player2_3.loose_pv(grenade_1.mid_damage)
                    elif abs(self.player2_3.position[0]-grenade_1.explo_pos[0]) <= 100:
                        self.player2_3.loose_pv(grenade_1.low_damage)

                    # degat joueur 1_1
                    if abs(self.player1_1.position[0] - grenade_1.explo_pos[0]) <= 40:
                        self.player1_1.loose_pv(grenade_1.full_damage)
                    elif abs(self.player1_1.position[0] - grenade_1.explo_pos[0]) <= 70:
                        self.player1_1.loose_pv(grenade_1.mid_damage)
                    elif abs(self.player1_1.position[0] - grenade_1.explo_pos[0]) <= 100:
                        self.player1_1.loose_pv(grenade_1.low_damage)
                    # degat joueur 2_2
                    if abs(self.player1_2.position[0] - grenade_1.explo_pos[0]) <= 40:
                        self.player1_2.loose_pv(grenade_1.full_damage)
                    elif abs(self.player1_2.position[0] - grenade_1.explo_pos[0]) <= 70:
                        self.player1_2.loose_pv(grenade_1.mid_damage)
                    elif abs(self.player1_2.position[0] - grenade_1.explo_pos[0]) <= 100:
                        self.player1_2.loose_pv(grenade_1.low_damage)
                    # degat joueur 2_3
                    if abs(self.player1_3.position[0] - grenade_1.explo_pos[0]) <= 40:
                        self.player1_3.loose_pv(grenade_1.full_damage)
                    elif abs(self.player1_3.position[0] - grenade_1.explo_pos[0]) <= 70:
                        self.player1_3.loose_pv(grenade_1.mid_damage)
                    elif abs(self.player1_3.position[0] - grenade_1.explo_pos[0]) <= 100:
                        self.player1_3.loose_pv(grenade_1.low_damage)


            grenade_pos = pygame.mouse.get_pos()
            grenade_line = [(player.position[0] + 14, player.position[1] + 21.25), grenade_pos]
            self.redraw_grenade()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not shoot:
                        shoot = True
                        x = grenade_1.position[0]
                        y = grenade_1.position[1]
                        time = 0
                        power = math.sqrt((grenade_pos[0] - grenade_1.position[0]) ** 2 + (
                                    grenade_pos[1] - grenade_1.position[1]) ** 2) / 8
                        angle = self.findAngle_grenade(grenade_pos)
                elif pygame.key.get_pressed()[pygame.K_TAB]:
                    run = False
    ################################### GRENADE END ###################################




#Fonction principale du jeu
    def run(self):

        clock = pygame.time.Clock()

        #boucle du jeu
        running = True

        while running:
            # verif si le jeu a commencé
            if self.is_playing:

                self.actu_liste_collision()

                if self.player1_1.is_alive and self.player1_1.tour == True:
                    player = self.player1_1
                    player.save_location()
                    self.handle_input(player)
                    self.update(self.player2_3)
                    self.update(player)
                    self.group.draw(self.screen)
                elif self.player2_1.is_alive and self.player2_1.tour == True:
                    player = self.player2_1
                    player.save_location()
                    self.handle_input(player)
                    self.update(self.player1_1)
                    self.update(player)
                    self.group.draw(self.screen)
                elif self.player1_2.is_alive and self.player1_2.tour == True:
                    player = self.player1_2
                    player.save_location()
                    self.handle_input(player)
                    self.update(self.player2_1)
                    self.update(player)
                    self.group.draw(self.screen)
                elif self.player2_2.is_alive and self.player2_2.tour == True:
                    player = self.player2_2
                    player.save_location()
                    self.handle_input(player)
                    self.update(self.player1_2)
                    self.update(player)
                    self.group.draw(self.screen)
                elif self.player1_3.is_alive and self.player1_3.tour == True:
                    player = self.player1_3
                    player.save_location()
                    self.handle_input(player)
                    self.update(self.player2_2)
                    self.update(player)
                    self.group.draw(self.screen)
                elif self.player2_3.is_alive and self.player2_3.tour == True:
                    player = self.player2_3
                    player.save_location()
                    self.handle_input(player)
                    self.update(self.player1_3)
                    self.update(player)
                    self.group.draw(self.screen)
                else:
                    self.player1_1.tour = True
                    self.player1_2.tour = True
                    self.player1_3.tour = True
                    self.player2_1.tour = True
                    self.player2_2.tour = True
                    self.player2_3.tour = True

                if self.player1_1.is_alive == self.player1_2.is_alive == self.player1_3.is_alive == False:
                    self.winner = 2
                    self.win_screen()
                elif self.player2_1.is_alive == self.player2_2.is_alive == self.player2_3.is_alive == False:
                    self.winner = 1
                    self.win_screen()


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
                    if self.start_button_rect.collidepoint(event.pos) and self.is_playing == False:
                        pygame.mixer.music.stop()
                        self.music = pygame.mixer.music.load("music_ig.mp3")
                        pygame.mixer.music.play(100)
                        #mettre le jeu en mode lancé
                        self.is_playing = True
                    elif self.quit_button_rect.collidepoint(event.pos) and self.is_playing == False:
                        running = False

            clock.tick(60)

        pygame.quit()