import pygame

class Player(pygame.sprite.Sprite):

    #initialisation de toutes les statistiques de chaque joueur
    def __init__(self, x, y,skin, team):

        super().__init__()
        self.is_alive = True
        self.pv = 100

        self.team = team
        #recupere les informations pour afficher le joueur (image, position ...)
        self.sprite_sheet = pygame.image.load(skin)
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        self.rect = self.image.get_rect()

        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 24)
        self.old_position = self.position.copy()

        self.speed = 3
        self.jump = 40

        self.gravity = 1
        self.touchGround = 1


        self.tour = True


    #perte de points de vie
    def loose_pv(self, damage):
        self.pv -= damage
        if self.pv <= 0:
            self.is_alive = False
            self.kill()

    #sauvegarder la position du joueur
    def save_location(self): self.old_position = self.position.copy()

#Tous les déplacements possibles
    def move_right(self):
        self.position[0] += self.speed
    def move_left(self):
        self.position[0] -= self.speed
    def move_up(self):
        self.position[1] -= self.jump
        self.touchGround = 0

    #lorsque le sol est touché
    def groundTouched(self):
        self.touchGround = 1

    #Verif si le joueur est dans les airs et ajuste sa vitesse en conséquence
    def is_in_air(self):
        if self.touchGround == 0:
            self.speed=1
        else:
            self.speed=3

    #actualise la position du joueur à tout instant ainsi que sa gravité
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        if self.touchGround == 0:
            self.position[1] += self.gravity

    #Permet de revenir à l'ancienne position en cas de collision
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    #affiche le joueur
    def get_image(self, x, y):
        image = pygame.Surface([28, 34])
        image.blit(self.sprite_sheet, (0,0), (x, y, 28, 34))
        return image

    #affiche la bar de vie
    def draw_health_bar(self, surface):
        # Position and size of the health bar
        bar_width = 50
        bar_height = 5
        bar_x = self.rect.x + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - bar_height - 5  # 5 pixels above the player's sprite

        # Background of the health bar (gray)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, (60, 60, 60), bg_rect)

        # Health bar (green to red based on hp percentage)
        hp_percentage = self.pv / 100
        bar_fill_width = int(bar_width * hp_percentage)
        bar_fill_rect = pygame.Rect(bar_x, bar_y, bar_fill_width, bar_height)

        if hp_percentage > 0.5:
            bar_color = (0, 255, 0)  # Green
        elif hp_percentage > 0.2:
            bar_color = (255, 255, 0)  # Yellow
        else:
            bar_color = (255, 0, 0)  # Red

        pygame.draw.rect(surface, bar_color, bar_fill_rect)