# Empezamos importando la libreria pygame  
import pygame as pg

# Inicializamos los modulos de la biblioteca pygame
pg.init()

# Aqui empezaremos a crear la ventana de nuestro juego
ventana = pg.display.set_mode((800,600))
pg.display.set_caption("Las Aventuras de Kroki")

# Cargar imagen de portada 
portada = pg.image.load("imagenes/portada.png")      # imagen de portada *Falta hacerlo
portada = pg.transform.scale(portada, (800, 600))    # Ajustar a tamaño de pantalla

# Bucle para mantener el juego y poder salir
running = True 
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False 

    # Dibujar portada en pantalla
    ventana.blit(portada, (0, 0))

    # Actualizar pantalla
    pg.display.flip()

pg.quit()



