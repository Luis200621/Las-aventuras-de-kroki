import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BOTON_ALTO, BOTON_ANCHO


# Clase Pantalla de inicio
class Pantalla_Inicio ():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('Las aventuras de Kroki')
        icono = pg.image.load("Imagenes/Diseño sin título.png").convert_alpha()
        pg.display.set_icon(icono)

        #Cargar fondo del menú
        self.fondo = pg.image.load("Imagenes/Agregar un título (2).png")                    
        self.fondo = pg.transform.scale(self.fondo, (SCREEN_WIDTH, SCREEN_HEIGHT ))

        #Botones
        self.boton_start = pg.Rect(
            SCREEN_WIDTH // 2 - BOTON_ANCHO // 2, 
            320,
            BOTON_ANCHO,
            BOTON_ALTO
        )

        self.boton_menu=pg.Rect(
            SCREEN_WIDTH //2 - BOTON_ANCHO // 2,
            440,
            BOTON_ANCHO,
            BOTON_ALTO
        )

    def dibujar (self):
        self.screen.blit(self.fondo, (0,0))

        pg.display.update()

    def click(self, pos):
        if self.boton_start.collidepoint(pos):
            return "juego"
        
        if self.boton_menu.collidepoint(pos):
            return "menu_extra"
        
        return None
    
    # PRINT