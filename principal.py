import pygame
import sys

pygame.init()

ANCHO = 1280
ALTO = 800
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Las Aventuras de Kroki")

try:
    fondo = pygame.image.load("POO-ULAGOS/proyecto/assets/Gemini_Generated_Image_5p2lts5p2lts5p2l.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    personaje = pygame.image.load("POO-ULAGOS/proyecto/assets/WhatsApp Image 2025-11-18 at 10.57.33 PM.png").convert_alpha()
    piso_img = pygame.image.load("POO-ULAGOS/proyecto/assets/Gemini_Generated_Image_98c23l98c23l98c2.png").convert_alpha()
    piso_img = pygame.transform.scale(piso_img, (ANCHO, 60))
except:
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((120, 180, 255))

    personaje = pygame.Surface((80, 80))
    personaje.fill((0, 200, 0))

personaje = pygame.transform.scale(personaje, (80, 80))


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

    if personaje_x < 0:
        personaje_x = 0
    if personaje_x > ANCHO - personaje.get_width():
        personaje_x = ANCHO - personaje.get_width()


    VENTANA.blit(fondo, (0, 0))
    VENTANA.blit(piso_img, (0, ALTO - 60))
    VENTANA.blit(personaje, (personaje_x, personaje_y))

    pygame.display.update()
    clock.tick(60)
