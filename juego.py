import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from Kroki import Kroki
pygame.init()


ANCHO = SCREEN_WIDTH
ALTO = SCREEN_HEIGHT

VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Las Aventuras de Kroki")

try:
    fondo = pygame.image.load("Imagenes/fondo.jpeg").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    personaje = Kroki()

    piso_img = pygame.image.load("Imagenes/suelo.jpeg").convert_alpha()
    piso_img = pygame.transform.scale(piso_img, (ANCHO, 60))

except:
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((120, 180, 255))

    personaje = pygame.Surface((80, 80))
    personaje.fill((0, 200, 0))

    piso_img = pygame.Surface((ANCHO, 60))
    piso_img.fill((100, 80, 50))

# Escalar personaje
personaje = pygame.transform.scale(personaje, (80, 80))

# Posición inicial del personaje
personaje_x = ANCHO // 2 - 40
personaje_y = ALTO - 60 - personaje.get_height()

velocidad = 5

clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        personaje_x -= velocidad

    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        personaje_x += velocidad

    # Limites
    if personaje_x < 0:
        personaje_x = 0
    if personaje_x > ANCHO - personaje.get_width():
        personaje_x = ANCHO - personaje.get_width()

    # Dibujar
    VENTANA.blit(fondo, (0, 0))
    VENTANA.blit(piso_img, (0, ALTO - 60))
    VENTANA.blit(personaje, (personaje_x, personaje_y))

    pygame.display.update()
    clock.tick(60)
