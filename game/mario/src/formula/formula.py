#!/usr/bin/python3
from data import main
from data import menu
from data import config as c
import pygame as pg
import pygame as pg
import os
import sys

class App():
    def __init__(self):
        self.menu = None
        self.main = None

    def run(self):
        self.menu = menu.Menu()
        self.menu.menu_loop()
        if self.menu.quit_state == 'play': #Check whether to continue to game or quit app
            self.main = main.Main()
            self.main.main_loop()
            if self.main.quit_state == 'menu':
                os.execl(sys.executable, sys.executable, *sys.argv) #Restart game

def run():
    pg.init() #Initialize pygame module
    c.screen = pg.display.set_mode((c.SCREEN_SIZE.x, c.SCREEN_SIZE.y))
    pg.display.set_caption(c.CAPTION)
    c.clock = pg.time.Clock()

    # Commands
    print("")
    print("\033[36m📚 HOW TO PLAY?\033[0m")
    print("\033[32m🟢 Select 1 PLAYER GAME on Mario menu with ENTER KEY (2 PLAYERS GAME NOT AVAILABLE YET)\033[0m")
    print("\033[38;5;214m🟠 Play using UP KEY 🔼, DOWN KEY 🔽, LEFT KEY ◀️  and RIGHT KEY ▶️ \033[0m")
    print("\033[31m🔴 Press the \"ESCAPE\" KEY on the Mario menu screen after \"GAME OVER\" to end the game! \033[0m")
    print("")

    app = App()
    app.run()

    pg.quit()
