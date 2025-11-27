import pygame as pg
from pantalla_principal import Pantalla_Inicio

pg.init()

menu = Pantalla_Inicio()

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    menu.dibujar() 

pg.quit()
