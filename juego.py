import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED

class Juego:
    def __init__(self, screen):
        self.screen = screen

        # Cargar personaje PNG
        imagen_original = pg.image.load("Imagenes/Captura de pantalla 2025-11-18 220154(1).png").convert_alpha()

        # ====== AJUSTAR TAMAÑO DEL PERSONAJE ======
        NUEVO_ANCHO = 80
        NUEVO_ALTO = 80

        self.kroki = pg.transform.scale(imagen_original, (NUEVO_ANCHO, NUEVO_ALTO))

        # Guardar tamaño nuevo
        self.ancho = NUEVO_ANCHO
        self.alto = NUEVO_ALTO

        # Posición inicial
        self.x = 100
        self.y = 300

        # Velocidad desde settings
        self.vel = PLAYER_SPEED

    def actualizar(self):
        teclas = pg.key.get_pressed()

        # Movimiento
        if teclas[pg.K_LEFT]:
            self.x -= self.vel
        if teclas[pg.K_RIGHT]:
            self.x += self.vel
        if teclas[pg.K_UP]:
            self.y -= self.vel
        if teclas[pg.K_DOWN]:
            self.y += self.vel

        # Límites de pantalla
        if self.x < 0:
            self.x = 0
        if self.x + self.ancho > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.ancho
        if self.y < 0:
            self.y = 0
        if self.y + self.alto > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.alto

    def dibujar(self):
        self.screen.fill((0, 0, 0))  # fondo negro temporal
        self.screen.blit(self.kroki, (self.x, self.y))
        pg.display.update()
