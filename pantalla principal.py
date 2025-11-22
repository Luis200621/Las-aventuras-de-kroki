import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT 


# Clase Pantalla de inicio
class Pantalla_Inicio ():
    def __init__(self, ventana):
        pg.init()
        self.ventana = ventana


    
    


    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


    pg.display.update()

pg.quit()