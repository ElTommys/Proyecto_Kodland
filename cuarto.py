import pygame
import random
from button_class import Button

ANCHO_PANTALLA, ALTO_PANTALLA = 1550, 800
FPS = 60
TAMANO_TERMOMETRO = (600, 400)
GRIS = (185, 174, 172)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ESTRELLA_WIDTH = 70
ESTRELLA_HEIGHT = 68
MASCOTA_WIDTH = 150
MASCOTA_HEIGHT = 150
X_POSITION = 400
Y_POSITION = 660
JUMP_HEIGHT = 24
Y_GRAVITY = 0.4
MOVEMENT_SPEED = 3
IMAGE_STANDING = "mascota.png"
IMAGE_JUMPING = "mascota_salto.png"
ENEMY_WIDTH = 100
ENEMY_HEIGHT = 100
ENEMY_SPEED = 2
EXPERIENCE_GOAL = 15

class Cuarto:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.all_sprite_list = pygame.sprite.Group()
        self.estrella_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = Player()
        self.button_image = pygame.image.load("button.png")
        self.button_image = pygame.transform.scale(self.button_image, (250, 100))
        self.all_sprite_list.add(self.player)
        self.background = pygame.image.load("fondo_cuarto.png").convert()
        self.background = pygame.transform.scale(self.background, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.get_font = pygame.font.Font("font/pixel_font.TTF", 40)
        estrella_image = pygame.image.load("estrella.png")
        estrella_image = pygame.transform.scale(estrella_image, (ESTRELLA_WIDTH, ESTRELLA_HEIGHT))
        estrella_image.set_colorkey(BLACK)
        enemy_image = pygame.image.load("cat1.png")
        enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        enemy_image.set_colorkey(BLACK)

        for _ in range(7):
            estrella = Estrella(estrella_image)
            estrella.rect.x = random.randrange(950)
            estrella.rect.y = random.randrange(500)
            self.estrella_list.add(estrella)
            self.all_sprite_list.add(estrella)

        for _ in range(4):
            enemy = Enemy(enemy_image)
            enemy.rect.x = random.randrange(950)
            enemy.rect.y = random.randrange(500)
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)

        self.experience = 0
        self.experience_bar_length = 700
        self.experience_bar_height = 50
        self.estrella_image = estrella_image
        self.last_star_time = pygame.time.get_ticks()
        self.star_interval = 5000  

    def run(self):
        keys_pressed = pygame.key.get_pressed()
        cuarto_mouse_pos = pygame.mouse.get_pos()
        self.player.change_x = 0
        self.player.change_y = 0

        if keys_pressed[pygame.K_LEFT]:
            self.player.changespeed(-MOVEMENT_SPEED, 0)
        if keys_pressed[pygame.K_RIGHT]:
            self.player.changespeed(MOVEMENT_SPEED, 0)
        if keys_pressed[pygame.K_DOWN] and not self.player.jumping:
            self.player.changespeed(0, MOVEMENT_SPEED)
        if keys_pressed[pygame.K_UP] and not self.player.jumping:
            self.player.jumping = True
            self.player.change_y = 0

        self.all_sprite_list.update()
        self.display.blit(self.background, (0, 0))
        self.all_sprite_list.draw(self.display)

        if keys_pressed[pygame.K_SPACE]:
            for estrella in self.estrella_list:
                if estrella.rect.colliderect(self.player.rect):
                    estrella.metodo(self.player.rect)
                    self.experience += 1

        for enemy in self.enemy_list:
            if enemy.rect.colliderect(self.player.rect):
                self.experience = 0 

        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_star_time > self.star_interval:
            estrella = Estrella(self.estrella_image)
            estrella.rect.x = random.randrange(950)
            estrella.rect.y = random.randrange(500)
            self.estrella_list.add(estrella)
            self.all_sprite_list.add(estrella)
            self.last_star_time = current_time

      
        pygame.draw.rect(self.display, GRIS, [300, 50, self.experience_bar_length, self.experience_bar_height])
        pygame.draw.rect(self.display, GREEN, [300, 50, self.experience * (self.experience_bar_length // EXPERIENCE_GOAL), self.experience_bar_height])

        cuarto_back = Button(image=self.button_image, pos=(1300, 725), text_input="Back",
                             font=self.get_font, base_color="Black", hovering_color="dark Blue")

        cuarto_back.change_color(cuarto_mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cuarto_back.checkForInput(cuarto_mouse_pos):
                    self.gameStateManager.set_state('Casa')

        cuarto_back.update(self.display)

        
        if self.experience >= EXPERIENCE_GOAL:
            self.gameStateManager.set_state('Final_cuarto')  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_standing = pygame.transform.scale(pygame.image.load(IMAGE_STANDING), (MASCOTA_WIDTH, MASCOTA_HEIGHT))
        self.image_jumping = pygame.transform.scale(pygame.image.load(IMAGE_JUMPING), (MASCOTA_WIDTH, MASCOTA_HEIGHT))
        self.image = self.image_standing
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.rect.x = (ANCHO_PANTALLA - MASCOTA_WIDTH) // 2
        self.rect.y = ALTO_PANTALLA - MASCOTA_HEIGHT
        self.jumping = False
        self.Y_velocity = JUMP_HEIGHT

    def update(self):
        self.rect.x += self.change_x
        if self.jumping:
            self.rect.y -= self.Y_velocity
            self.Y_velocity -= Y_GRAVITY
            if self.Y_velocity < -JUMP_HEIGHT:
                self.jumping = False
                self.Y_velocity = JUMP_HEIGHT
        self.image = self.image_jumping if self.jumping else self.image_standing

    def changespeed(self, x, y):
        self.change_x += x
        if not self.jumping:
            self.change_y += y

class Estrella(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def metodo(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.speed_y = random.choice([-ENEMY_SPEED, ENEMY_SPEED])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

   
        if self.rect.left < 0 or self.rect.right > ANCHO_PANTALLA:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > ALTO_PANTALLA:
            self.speed_y = -self.speed_y

