from pygame import QUIT
from baño import Bano
from cocina import Cocina
from cuarto import Cuarto
from credits import Credits
from final_baño import Final_bano
from final_cocina import Final_cocina
from final_cuarto import Final_cuarto
from casa import Casa
from menu import Menu
import pygame
import sys

ANCHO_PANTALLA, ALTO_PANTALLA = 1550, 800 
FPS = 60
TAMANO_TERMOMETRO = (600, 400)
GRIS = (185, 174, 172)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager('Menu')
        self.bano = Bano(self.screen, self.gameStateManager)
        self.cocina = Cocina(self.screen, self.gameStateManager)
        self.casa = Casa(self.screen, self.gameStateManager)
        self.final_cocina = Final_cocina(self.screen, self.gameStateManager)
        self.final_bano = Final_bano(self.screen, self.gameStateManager)
        self.final_cuarto = Final_cuarto(self.screen, self.gameStateManager)
        self.credits = Credits(self.screen, self.gameStateManager)
        self.cuarto = Cuarto(self.screen, self.gameStateManager)
        self.menu = Menu(self.screen,self.gameStateManager)
        self.states = {'Baño': self.bano, 'Cuarto': self.cuarto, 'Menu':self.menu, 'Credits':self.credits, 
                       'Casa':self.casa, 'Cocina':self.cocina, 'Final_baño':self.final_bano, 'Final_cocina':self.final_cocina, 'Final_cuarto': self.final_cuarto}

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run()
            pygame.display.update()
            self.clock.tick(FPS)
            self.bano.handle_event(e)


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

if __name__ == '__main__':
    game = Game()
    game.run()
