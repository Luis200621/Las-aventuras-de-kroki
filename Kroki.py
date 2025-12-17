import pygame
import os
from settings import VELOCIDAD_KROKI, SCREEN_HEIGHT, GRAVEDAD, FUERZA_SALTO, SCREEN_WIDTH

class Kroki(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.clase_actual = "None"
        self.orientacion = "derecha"

        base_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_path, "Imagenes")

        self.sprites = {
            "None": pygame.image.load(os.path.join(img_path, "Kroki_inicial.png")).convert_alpha(),
            "Guerrero": pygame.image.load(os.path.join(img_path, "guerrero.png")).convert_alpha(),
            "Mago": pygame.image.load(os.path.join(img_path, "mago.png")).convert_alpha()
        }

        for k in self.sprites:
            self.sprites[k] = pygame.transform.scale(self.sprites[k], (125, 125))

        self.image = self.sprites[self.clase_actual]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.stats = {
            "None": {"vida": 100, "velocidad": VELOCIDAD_KROKI, "alcance": 40},
            "Guerrero": {"vida": 150, "velocidad": VELOCIDAD_KROKI, "alcance": 60},
            "Mago": {"vida": 100, "velocidad": VELOCIDAD_KROKI , "alcance": 0}
        }

        self.velocidad_y = 0
        self.en_suelo = True
        self.piso_y = SCREEN_HEIGHT - 55

        self.atacando = False
        self.tiempo_ataque = 0
        self.duracion_ataque = 400
        self.cooldown_ataque = 600

        # ===== ARMAS =====
        self.armas = {
            "None": pygame.transform.scale(
                pygame.image.load(os.path.join(img_path, "palo.png")).convert_alpha(),
                (50, 100)
            ),
            "Guerrero": pygame.transform.scale(
                pygame.image.load(os.path.join(img_path, "Espada_Guerrero.png")).convert_alpha(),
                (30, 100)
            ),
            "Mago": pygame.transform.scale(
                pygame.image.load(os.path.join(img_path, "Baston_Mago.png")).convert_alpha(),
                (30, 110)
            )
        }

        self.mano_offset = {
            "derecha": (60, 2),
            "izquierda": (-60, 2)
        }

        self.magia_img = pygame.transform.scale(
            pygame.image.load(os.path.join(img_path, "proyectil.png")).convert_alpha(),
            (30, 30)
        )

        # ===== Valores para evitar errores =====
        self.arma_rect = pygame.Rect(0, 0, 0, 0)
        self.dano_arma = 10
        self.vida = self.stats[self.clase_actual]["vida"]

    def movimiento(self):
        keys = pygame.key.get_pressed()
        velocidad = self.stats[self.clase_actual]["velocidad"]

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= velocidad
            self.orientacion = "izquierda"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += velocidad
            self.orientacion = "derecha"

            self.rect.x = max(0, self.rect.x)
            self.rect.x = min(SCREEN_WIDTH - self.rect.width, self.rect.x)


        if keys[pygame.K_SPACE] and self.en_suelo:
            self.velocidad_y = FUERZA_SALTO
            self.en_suelo = False

        self.velocidad_y += GRAVEDAD
        self.rect.y += self.velocidad_y

        if self.rect.bottom >= self.piso_y:
            self.rect.bottom = self.piso_y
            self.velocidad_y = 0
            self.en_suelo = True

        if keys[pygame.K_j]:
            tiempo = pygame.time.get_ticks()
            if tiempo - self.tiempo_ataque >= self.cooldown_ataque:
                self.atacando = True
                self.tiempo_ataque = tiempo

    def update(self):
        self.movimiento()
        if self.atacando:
            if pygame.time.get_ticks() - self.tiempo_ataque >= self.duracion_ataque:
                self.atacando = False

    def cambiar_clase(self, nueva_clase):
        if self.clase_actual != nueva_clase:
            self.clase_actual = nueva_clase
            self.image = self.sprites[nueva_clase]
            self.vida = self.stats[nueva_clase]["vida"]
            centro = self.rect.center
            self.rect = self.image.get_rect(center=centro)

    def recibir_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

class ProyectilMagico(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion, imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 10
        self.direccion = direccion
        self.dano = 1  # IMPORTANTE

    def update(self):
        if self.direccion == "derecha":
            self.rect.x += self.velocidad
        else:
            self.rect.x -= self.velocidad

        # Eliminar si sale de la pantalla (CORRECTO)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()