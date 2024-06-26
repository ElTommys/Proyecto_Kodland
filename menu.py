import pygame
from button_class import Button
import sys

class Menu:
    def __init__(self, display, gameStateManager):
        self.display = display 
        self.gameStateManager = gameStateManager
        self.background1 = pygame.image.load("sky.jpg")
        self.background2 = pygame.image.load("room.png")
        self.button_image = pygame.image.load("button.png")
        self.button_image = pygame.transform.scale(self.button_image, (300, 100))
        self.cat = pygame.image.load("cat1.png").convert_alpha()  
        self.cat = pygame.transform.scale(self.cat, (200, 200))
        self.cord_x = 700
        self.cord_y = 400
        self.speed_x = 3

    def get_font(self, scale):
        return pygame.font.Font("font/pixel_font.TTF", scale)

    def run(self):
        self.display.blit(self.background1, (0, 0))  

        menu_mouse_pos = pygame.mouse.get_pos()  

        menu_text = self.get_font(100).render("TOMODACHI", True, "light blue")
        menu_rect = menu_text.get_rect(center=(775, 100))
        self.display.blit(menu_text, menu_rect)

        play_button = Button(image=self.button_image, pos=(775, 250),
                             text_input="PLAY", font=self.get_font(40), base_color="black",
                             hovering_color="dark blue")
        credits_button = Button(image=self.button_image, pos=(775, 400),
                                text_input="CREDITS", font=self.get_font(40), base_color="black",
                                hovering_color="dark blue")
        quit_button = Button(image=self.button_image, pos=(775, 550),
                             text_input="QUIT", font=self.get_font(40), base_color="black",
                             hovering_color="dark blue")

        for button in [play_button, credits_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(self.display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    self.gameStateManager.set_state('Casa')
                elif credits_button.checkForInput(menu_mouse_pos):
                    self.gameStateManager.set_state('Credits')
                elif quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

