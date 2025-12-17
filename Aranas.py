import pygame
import random
from settings import VELOCIDAD_ARANAS, VIDA_ARAÑA

class Aranas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # ===== STATS =====
        self.vida = VIDA_ARAÑA
        self.dano_ataque = 10
        self.dano_critico = 15
        self.probabilidad_critico = 0.20

        # ===== IMAGEN =====
        self.image = pygame.image.load("Imagenes/araña.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(topleft=(x, y))

        # HITBOX GRANDE
        self.hitbox = self.rect.inflate(50, 50)

        # ===== MOVIMIENTO LENTO =====
        self.velocidad = VELOCIDAD_ARANAS
        self.tiempo_movimiento = 0
        self.delay_movimiento = 40  # CUANTO MÁS GRANDE, MÁS LENTA

        # ===== ATAQUE LENTO =====
        self.cooldown_ataque = 1500
        self.tiempo_ultimo_ataque = 0

    def update(self, jugador_rect):
        self.movimiento(jugador_rect)
        self.hitbox.center = self.rect.center

        if self.vida <= 0:
            self.kill()

    def movimiento(self, jugador_rect):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_movimiento < self.delay_movimiento:
            return

        self.tiempo_movimiento = ahora

        if jugador_rect.centerx > self.rect.centerx:
            self.rect.x += self.velocidad
        else:
            self.rect.x -= self.velocidad

    def ataque_de_kroki(self, dano):
        self.vida -= dano
        print(f"Araña golpeada: {self.vida}")

    def dano_a_kroki(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_ataque < self.cooldown_ataque:
            return 0

        self.tiempo_ultimo_ataque = ahora

        dano = self.dano_ataque
        if random.random() < self.probabilidad_critico:
            dano += self.dano_critico

        return dano
