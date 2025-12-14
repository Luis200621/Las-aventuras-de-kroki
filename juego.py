import pygame
import sys
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from Kroki import Kroki


class Juego:
    def __init__(self, ventana):
        self.VENTANA = ventana
        self.ANCHO = SCREEN_WIDTH
        self.ALTO = SCREEN_HEIGHT
        self.clock = pygame.time.Clock()

        self.cargar_recursos()

        # ================== SPRITES ==================
        self.jugadores = pygame.sprite.Group()

        # Kroki aparece sobre el piso
        x_inicial = self.ANCHO // 2
        y_inicial = self.ALTO - 60 - 64  # piso - altura kroki
        self.kroki = Kroki(x_inicial, y_inicial)

        self.jugadores.add(self.kroki)

    # ================== RECURSOS ==================
    def cargar_recursos(self):
        try:
            # Ruta base del proyecto (donde está juego.py)
            base_path = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(base_path, "Imagenes")

            fondo_path = os.path.join(img_path, "fondo.png")
            suelo_path = os.path.join(img_path, "suelo.png")

            self.fondo = pygame.image.load(fondo_path).convert()
            self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))

            self.piso_img = pygame.image.load(suelo_path).convert_alpha()
            self.piso_img = pygame.transform.scale(self.piso_img, (self.ANCHO, 60))

            print(" Fondo y suelo cargados correctamente")

        except Exception as e:
            print(" Error cargando imágenes:", e)

            self.fondo = pygame.Surface((self.ANCHO, self.ALTO))
            self.fondo.fill((120, 180, 255))

            self.piso_img = pygame.Surface((self.ANCHO, 60))
            self.piso_img.fill((100, 80, 50))
    # ================== EVENTOS ==================
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # ================== UPDATE ==================
    
    def actualizar(self):
        self.jugadores.update()

    # ================== DIBUJO ==================
    def dibujar(self):
        self.VENTANA.blit(self.fondo, (0, 0))
        self.VENTANA.blit(self.piso_img, (0, self.ALTO - 60))
        self.jugadores.draw(self.VENTANA)
        pygame.display.update()

    # ================== LOOP ==================
    def run(self):
        while True:
            self.eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(60)
