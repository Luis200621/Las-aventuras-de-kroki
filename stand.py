import pygame

class StandClase(pygame.sprite.Sprite):
    def __init__(self, x, y, clase, imagen):
        super().__init__()

        self.clase = clase
        self.image = imagen

        # CLAVE: el stand se apoya en el piso
        self.rect = self.image.get_rect(midbottom=(x, y))
