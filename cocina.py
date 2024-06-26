import pygame
import random
from button_class import Button


ANCHO_PANTALLA, ALTO_PANTALLA = 1550, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Cocina:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.fondo = pygame.image.load("fondo_cocina.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.player = Player()
        self.good_images = [pygame.image.load(f"good{i}.png").convert_alpha() for i in range(1, 4)]
        self.bad_images = [pygame.image.load(f"bad{i}.png").convert_alpha() for i in range(1, 4)]
        self.all_sprites = pygame.sprite.Group()
        self.get_font = pygame.font.Font("font/pixel_font.TTF", 40)
        self.falling_objects = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.button_image = pygame.image.load("button.png")
        self.button_image = pygame.transform.scale(self.button_image, (250, 100))

        
        self.creation_timer = 0

    def run(self):
        self.display.blit(self.fondo, [0, 0])
        cocina_mouse_pos = pygame.mouse.get_pos()

        cocina_back = Button(image=self.button_image, pos=(1300, 725), text_input="Back",
                             font=self.get_font, base_color="Black", hovering_color="dark Blue")

        cocina_back.change_color(cocina_mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cocina_back.checkForInput(cocina_mouse_pos):
                    self.gameStateManager.set_state('Casa')

        cocina_back.update(self.display)

        
        if self.creation_timer <= 0:
            if random.randint(0, 80) < 1:
                good = random.choice([True, False])
                falling_object = FallingObject(good, self.good_images, self.bad_images)
                self.all_sprites.add(falling_object)
                self.falling_objects.add(falling_object)
          
                self.creation_timer = 20  
        else:
            self.creation_timer -= 1

        hits = pygame.sprite.spritecollide(self.player, self.falling_objects, True)
        for hit in hits:
            if hit.good:
                print("¡Objeto bueno recogido!")
                self.player.incrementar_experiencia()  
            else:
                print("¡Objeto malo tocado! Game Over")
                self.player.resetear_experiencia()  
                return False 
       
        if self.player.experiencia >= self.player.max_experiencia:
            self.gameStateManager.set_state('Final_cocina')

        self.all_sprites.update()
        self.all_sprites.draw(self.display)
        self.player.dibujar_barra_experiencia(self.display)  
        return True  
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cat1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 10
        self.speed = 0
        self.experiencia = 0
        self.max_experiencia = 100
        self.experiencia_bar_color = (0, 255, 0)

    def incrementar_experiencia(self):
        self.experiencia += 5
        if self.experiencia >= self.max_experiencia:
            self.experiencia = self.max_experiencia

    def resetear_experiencia(self):
        self.experiencia = 0

    def dibujar_barra_experiencia(self, display):
        bar_length = 700
        bar_height = 50
        fill = (self.experiencia / self.max_experiencia) * bar_length
        
        pygame.draw.rect(display, (150, 150, 150), [ANCHO_PANTALLA // 2 - bar_length // 2, 10, bar_length, bar_height])
        
        pygame.draw.rect(display, self.experiencia_bar_color, [ANCHO_PANTALLA // 2 - bar_length // 2, 10, fill, bar_height])
        pygame.draw.rect(display, BLACK, [ANCHO_PANTALLA // 2 - bar_length // 2, 10, bar_length, bar_height], 2)

    def update(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed = -5
        elif keys[pygame.K_RIGHT]:
            self.speed = 5
        else:
            self.speed = 0

        self.rect.x += self.speed
       
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA
        elif self.rect.left < 0:
            self.rect.left = 0

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, good, good_images, bad_images):
        super().__init__()
        self.good = good
        if self.good:
            self.image = random.choice(good_images)
        else:
            self.image = random.choice(bad_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3,8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > ALTO_PANTALLA:
            self.kill()
