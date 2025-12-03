import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from pantalla_principal import Pantalla_Inicio
from juego import Juego

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Las Aventuras de Kroki")

menu = Pantalla_Inicio(screen)
juego = Juego(screen)

estado = "menu"

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if estado == "menu":
            if event.type == pg.MOUSEBUTTONDOWN:
                cambio = menu.click(event.pos)
                if cambio == "juego":
                    estado = "juego"

    if estado == "menu":
        menu.dibujar()

    elif estado == "juego":
        juego.actualizar()
        juego.dibujar()

pg.quit()
#HOLA
