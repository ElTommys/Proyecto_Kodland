import pygame
import sys
from button_class import Button

ANCHO_PANTALLA, ALTO_PANTALLA = 1550, 800

class Casa: 
    def __init__(self, display, gameStateManager):
        pygame.display.set_caption("Casa")
        self.display = display
        self.gameStateManager = gameStateManager
        self.button_image = pygame.image.load("button.png")
        self.button_image = pygame.transform.scale(self.button_image, (300, 100))
        self.background2 = pygame.image.load("room.png")
        self.background2 = pygame.transform.scale(self.background2, (ANCHO_PANTALLA, ALTO_PANTALLA))
        self.font = pygame.font.Font("font/pixel_font.TTF", 40)
        self.cat = pygame.image.load("cat1.png").convert_alpha()  
        self.cat = pygame.transform.scale(self.cat, (200, 200))
        self.cord_x = 700
        self.cord_y = 400
        self.speed_x = 10

    def run(self):

        play_mouse_pos = pygame.mouse.get_pos()
        

        if self.cord_x > 900 or self.cord_x < 300:
            self.speed_x *= -1
        self.cord_x += self.speed_x

        self.display.blit(self.background2, (0, 0))  
        self.display.blit(self.cat, (self.cord_x, self.cord_y))  


        back_button = Button(image= self.button_image, pos=(1300, 718),
                                text_input="BACK", font=self.font, base_color="black",
                                hovering_color="dark blue")
        sleep_button = Button(image=self.button_image, pos=(250, 200),
                                  text_input="SLEEP", font=self.font, base_color="black",
                                  hovering_color="dark blue")
        food_button = Button(image=self.button_image, pos=(250, 350),
                                 text_input="FOOD", font=self.font, base_color="black",
                                 hovering_color="dark blue")
        bath_button = Button(image=self.button_image, pos=(250, 500),
                                 text_input="BATH", font=self.font, base_color="black",
                                 hovering_color="dark blue")
          
    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
       
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(play_mouse_pos):
                    self.gameStateManager.set_state('Menu')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sleep_button.checkForInput(play_mouse_pos):
                    self.gameStateManager.set_state('Cuarto')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if food_button.checkForInput(play_mouse_pos):
                    self.gameStateManager.set_state('Cocina')

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bath_button.checkForInput(play_mouse_pos):
                    self.gameStateManager.set_state('Baño')

        

        back_button.change_color(play_mouse_pos)
        back_button.update(self.display)

        sleep_button.change_color(play_mouse_pos)
        sleep_button.update(self.display)

        food_button.change_color(play_mouse_pos)
        food_button.update(self.display)

        bath_button.change_color(play_mouse_pos)
        bath_button.update(self.display)

        


  