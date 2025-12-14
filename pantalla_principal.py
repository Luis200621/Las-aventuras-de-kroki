import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BOTON_ALTO, BOTON_ANCHO

class Pantalla_Inicio:
    def __init__(self, screen):
        self.screen = screen

        # Titulo e icono (esto sí se puede quedar)
        icono = pg.image.load("Imagenes/favicon.png").convert_alpha()
        pg.display.set_icon(icono)
        pg.display.set_caption('Las aventuras de Kroki')

        # Fondo del menú
        self.fondo = pg.image.load("Imagenes/Pantalla_de_inicio.png")
        self.fondo = pg.transform.scale(self.fondo, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Botones
        self.boton_start = pg.Rect(
            SCREEN_WIDTH // 2 - BOTON_ANCHO // 2,
            320,
            BOTON_ANCHO,
            BOTON_ALTO
        )

        self.boton_menu = pg.Rect(
            SCREEN_WIDTH // 2 - BOTON_ANCHO // 2,
            440,
            BOTON_ANCHO,
            BOTON_ALTO
        )

    def dibujar(self):
        self.screen.blit(self.fondo, (0,0))
        pg.display.update()

    def click(self, pos):
        if self.boton_start.collidepoint(pos):
            return "juego"

        if self.boton_menu.collidepoint(pos):
            return "menu_extra"

        return None
