import pygame
import random
from button_class import Button

pygame.init()

ANCHO_PANTALLA, ALTO_PANTALLA = 1550, 800
FPS = 60
TAMANO_TERMOMETRO = (600, 400)
GRIS = (185, 174, 172)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  
MAX_EXP = 500  

class Bano:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.fondo = pygame.image.load("fondo_baño.png").convert()
        self.termometro = pygame.image.load("termometro.png").convert_alpha()
        self.termometro.set_colorkey((0, 0, 0))
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.termometro = pygame.transform.scale(self.termometro, TAMANO_TERMOMETRO)
        self.barra = Barra()
        self.button_image = pygame.image.load("button.png")
        self.button_image = pygame.transform.scale(self.button_image, (250, 100))
        self.boton_detener = BotonBano(900, 625, 'detener.png', self.detener_barra)
        self.boton_reiniciar = BotonBano(1050, 625, 'reiniciar.png', self.reiniciar_barra)
        self.sprites = pygame.sprite.Group(self.barra)
        self.pin = pygame.image.load("penguin1.png").convert_alpha()
        self.pin = pygame.transform.scale(self.pin, (200, 200))
        self.get_font = pygame.font.Font("font\pixel_font.TTF", 40)
        self.cord_x = 700
        self.cord_y = 400
        self.speed_x = 3
        self.exp = 0  
        self.game_over = False

    def run(self):
        self.display.blit(self.fondo, [0, 0])
        self.display.blit(self.termometro, [250, 485])
        self.boton_detener.dibujar(self.display)
        self.boton_reiniciar.dibujar(self.display)
        self.sprites.update()
        self.sprites.draw(self.display)
        self.dibujar_barra_experiencia(self.display)
        cuarto_mouse_pos = pygame.mouse.get_pos()
    

        if self.cord_x > 900 or self.cord_x < 300:
            self.speed_x *= -1
        self.cord_x += self.speed_x

        self.display.blit(self.pin, (self.cord_x, self.cord_y))

        cuarto_back = Button(image=self.button_image, pos=(1300, 725), text_input="Back",
                                  font=self.get_font, base_color="Black", hovering_color="dark Blue")
        
        cuarto_back.change_color(cuarto_mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if cuarto_back.checkForInput(cuarto_mouse_pos):
                        self.gameStateManager.set_state('Casa')

        cuarto_back.update(self.display)

        if self.exp >= MAX_EXP:
            self.game_over = True
            print("¡Has alcanzado la experiencia máxima!")

        if self.game_over:
             self.gameStateManager.set_state('Final_baño')
         

    def dibujar_barra_experiencia(self, display):
        bar_length = 700
        bar_height = 50
        fill = (self.exp / MAX_EXP) * bar_length
    
        pygame.draw.rect(display, (150, 150, 150), [ANCHO_PANTALLA // 2 - bar_length // 2, 10, bar_length, bar_height])
       
        pygame.draw.rect(display, GREEN, [ANCHO_PANTALLA // 2 - bar_length // 2, 10, fill, bar_height])
        pygame.draw.rect(display, BLACK, [ANCHO_PANTALLA // 2 - bar_length // 2, 10, bar_length, bar_height], 2)

    def detener_barra(self):
        self.barra.detener()
       
        if 500 <= self.barra.rect.x <= 580:
          
            self.exp += 5
           
    def reiniciar_barra(self):
        self.barra.reiniciar()
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.boton_detener.es_presionado(event.pos):
                self.boton_detener.ejecutar_accion()
                print("Botón de detener presionado")
            elif self.boton_reiniciar.es_presionado(event.pos):
                self.boton_reiniciar.ejecutar_accion()
                print("Botón de reiniciar presionado")

class Barra(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 69))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 646
        self.velocidad_x = random.uniform(5, 15)  

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.left > 750:
            self.rect.right = 250

    def detener(self):
        self.velocidad_x = 0
        print("Barra detenida")

    def reiniciar(self):
        self.velocidad_x = random.uniform(5, 15)
        print("Barra reiniciada")

class BotonBano:
    def __init__(self, x, y, imagen, accion):
        self.image = pygame.image.load(imagen).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.accion = accion

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect.topleft)

    def es_presionado(self, posicion):
        return self.rect.collidepoint(posicion)

    def ejecutar_accion(self):
        self.accion()
