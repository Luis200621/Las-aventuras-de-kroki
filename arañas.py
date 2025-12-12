import pygame
import random

from settings import VELOCIDAD_ARANAS, VIDA_ARAÑA

class Aranas (pygame.sprite.Sprite):
    def __init__(self, x,y):
        super()._init_()

        # Atributos de vida y de daño de las arañas
        self.vida = 50 # Las arañas tendran 50 de vida
        
        # Ataques
        self.dano_ataque = 10 # Daño que le quitan a Kroki
        self.dano_critico = 15 # Daño critico 
        self.probabilidad_critico = 0.20 # 20% de acertar un golpe critico de las arañas

        # Graficos
        self.image = pygame.image.load("Las-aventuras-de-kroki-main/Las-aventuras-de-kroki-main/Imagenes/araña.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64,64))

        # Rectangulo de colision
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocidad = 2
        self.estado = "idle" #Inactivo

        self.dano_recibido = False #Se encuentra en False, cuando recibe daño se pasa True
        self.tiempo_del_dano = 0 

    def uptade (self, jugador_rect):
        self.movimiento(jugador_rect)
        
        # Aqui si la araña su vida es igual o menor a 0, sera eliminado
        if self.vida <= 0:
            self.estado = "eliminado"
            self.kill()

    def ataque_de_kroki (self, dano):
        if self.vida > 0:
            self.vida -= dano
            self.dano_recibido = True
            self.tiempo_del_dano = pygame.time.get_ticks()
            print (f"Golpe a araña! le queda {self.vida} de vida ")

    def dano_a_kroki (self):
        dano_final = self.dano_ataque

        if random.random() < self.probabilidad_critico:
            dano_final += self.dano_critico
            print("¡Golpe crítico de la Araña!")
        else:
            print("¡Golpe normal de la araña!")
            print(f"Daño hecho: {dano_final}")

        return dano_final