import pygame as pg

class Rey:
    def __init__(self):
        self.imagen = pg.image.load("Imagenes/Captura de pantalla 2025-11-18 231025(1).png").convert_alpha()

        self.x = 50 #todavia no se define la pocicion en el eje x
        self.y = 50 #todavia no se define la pocision en el eje y

    def dibujar (self, screen):
        screen.blit(self.imagen, (self.x, self.y))
        