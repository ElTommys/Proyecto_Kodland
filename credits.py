import pygame
from button_class import Button
import sys

import pygame
from button_class import Button

class Credits:
    def __init__(self, display, gameStateManager):
        pygame.display.set_caption("Credits")
        self.display = display
        self.gameStateManager = gameStateManager
        self.background1 = pygame.image.load("sky.jpg")
        self.get_font = pygame.font.Font("font\pixel_font.TTF", 40)
        self.button_image = pygame.image.load("button.png")
        self.button_image = pygame.transform.scale(self.button_image, (300, 100))

    def run(self):
            credits_mouse_pos = pygame.mouse.get_pos()

            self.display.blit(self.background1, (0, 0))

            credits_text = self.get_font.render("CREDITS", True, "light blue")
            name1_text = self.get_font.render("Tomas Sandoval", True, "white")
           
            credits_rect = credits_text.get_rect(center=(775, 100))
            self.display.blit(credits_text, credits_rect)

            name1_rect = name1_text.get_rect(center=(775, 250))
            self.display.blit(name1_text, name1_rect)

            credits_back = Button(image=self.button_image, pos=(775, 650), text_input="Back",
                                  font=self.get_font, base_color="Black", hovering_color="dark Blue")

            credits_back.change_color(credits_mouse_pos)
            credits_back.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if credits_back.checkForInput(credits_mouse_pos):
                        self.gameStateManager.set_state('Menu')
                        return
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        
