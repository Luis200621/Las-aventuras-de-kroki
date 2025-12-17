import pygame
import sys
import os
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, VELOCIDAD_ARANAS, VIDA_ARAÑA
from Kroki import Kroki, ProyectilMagico
from stand import StandClase
from Aranas import Aranas

class Juego:
    def __init__(self, ventana):
        self.VENTANA = ventana
        self.ANCHO = SCREEN_WIDTH
        self.ALTO = SCREEN_HEIGHT
        self.clock = pygame.time.Clock()

        self.cargar_recursos()

        # ===== GRUPOS =====
        self.jugadores = pygame.sprite.Group()
        self.proyectiles = pygame.sprite.Group()
        self.stands = pygame.sprite.Group()
        self.aranas = pygame.sprite.Group()

        # ===== KROKI =====
        self.kroki = Kroki(self.ANCHO // 2, self.ALTO - 185)
        self.jugadores.add(self.kroki)

        # ===== STANDS =====
        self.crear_stands()

        # ===== SPAWN ARAÑAS =====
        self.tiempo_spawn_aranas = 2000  # 2 segundos
        self.ultimo_spawn_arana = pygame.time.get_ticks()

        # Fuente para vida
        self.font = pygame.font.SysFont(None, 24)

    # ================== RECURSOS ==================
    def cargar_recursos(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_path, "Imagenes")

        self.fondo = pygame.transform.scale(
            pygame.image.load(os.path.join(img_path, "fondo.png")).convert(),
            (self.ANCHO, self.ALTO)
        )

        self.piso_img = pygame.transform.scale(
            pygame.image.load(os.path.join(img_path, "suelo.png")).convert_alpha(),
            (self.ANCHO, 60)
        )

        self.stand_guerrero_img = pygame.transform.scale(
            pygame.image.load(os.path.join(img_path, "stand_guerrero.png")).convert_alpha(),
            (125, 125)
        )

        self.stand_mago_img = pygame.transform.scale(
            pygame.image.load(os.path.join(img_path, "stand_mago.png")).convert_alpha(),
            (125, 125)
        )

    # ================== STANDS ==================
    def crear_stands(self):
        piso_y = self.ALTO - 50  # altura real del suelo

        stand_guerrero = StandClase(120, piso_y, "Guerrero", self.stand_guerrero_img)
        stand_mago = StandClase(260, piso_y, "Mago", self.stand_mago_img)

        self.stands.add(stand_guerrero, stand_mago)

    # ================== SPAWN ARAÑAS ==================
    def crear_arana(self):
        lado = random.choice(["izquierda", "derecha"])
    
        # ALTURA DEL SUELO
        y = self.ALTO - 124  # 128px araña - suelo
    
        if lado == "izquierda":
            x = -150  # FUERA de la pantalla
        else:
            x = self.ANCHO + 150  # FUERA de la pantalla
    
        arana = Aranas(x, y)
        self.aranas.add(arana)


    # ================== EVENTOS ==================
    def eventos(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # ================== UPDATE ==================
    def actualizar(self):
        self.jugadores.update()
        self.proyectiles.update()

        # PROYECTIL MAGO
        if self.kroki.atacando and self.kroki.clase_actual == "Mago":
            self.proyectiles.add(
                ProyectilMagico(
                    self.kroki.rect.centerx,
                    self.kroki.rect.centery,
                    self.kroki.orientacion,
                    self.kroki.magia_img
                )
            )

        # CAMBIO DE CLASE (E)
        keys = pygame.key.get_pressed()
        for stand in self.stands:
            if self.kroki.rect.colliderect(stand.rect):
                if keys[pygame.K_e]:
                    self.kroki.cambiar_clase(stand.clase)

        # === SPAWN DE ARAÑAS ===
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_spawn_arana > self.tiempo_spawn_aranas:
            self.crear_arana()
            self.ultimo_spawn_arana = tiempo_actual

        # === ACTUALIZAR ARAÑAS ===
        self.aranas.update(self.kroki.rect)

        # === COLISIONES KROKI <-> ARAÑAS ===
        for arana in self.aranas:
            # Colisión cuerpo a cuerpo
            try:
                if self.kroki.arma_rect.colliderect(arana.hitbox):
                    arana.ataque_de_kroki(self.kroki.dano_arma)
            except AttributeError:
                pass

            # Colisión proyectiles
            for proyectil in self.proyectiles:
                if hasattr(proyectil, "rect") and proyectil.rect.colliderect(arana.hitbox):
                    dano = getattr(proyectil, "dano", 10)
                    arana.ataque_de_kroki(dano)
                    proyectil.kill()

            # Daño de la araña a Kroki
            if self.kroki.rect.colliderect(arana.hitbox):
                if hasattr(self.kroki, "recibir_dano"):
                    dano = arana.dano_a_kroki()
                    self.kroki.recibir_dano(dano)

    # ================== DIBUJO ==================
    def dibujar(self):
        self.VENTANA.blit(self.fondo, (0, 0))
        self.VENTANA.blit(self.piso_img, (0, self.ALTO - 60))

        self.stands.draw(self.VENTANA)
        self.jugadores.draw(self.VENTANA)
        self.aranas.draw(self.VENTANA)
        self.proyectiles.draw(self.VENTANA)

        # ===== ARMA =====
        if self.kroki.clase_actual in self.kroki.armas:
            arma_base = self.kroki.armas[self.kroki.clase_actual]
            if self.kroki.atacando:
                arma = pygame.transform.rotate(arma_base, -90)
            else:
                arma = arma_base
            if self.kroki.orientacion == "izquierda":
                arma = pygame.transform.flip(arma, True, False)

            offset_x, offset_y = self.kroki.mano_offset[self.kroki.orientacion]
            self.kroki.arma_rect = arma.get_rect(
                center=(self.kroki.rect.centerx + offset_x, self.kroki.rect.centery + offset_y)
            )
            self.VENTANA.blit(arma, self.kroki.arma_rect)

        # ===== VIDA ARAÑAS =====
        for arana in self.aranas:
            vida_texto = self.font.render(str(arana.vida), True, (255, 0, 0))
            self.VENTANA.blit(vida_texto, (arana.rect.centerx - vida_texto.get_width() // 2, arana.rect.top - 20))

        # ===== VIDA KROKI =====
        if hasattr(self.kroki, "vida"):
            vida_texto = self.font.render(str(self.kroki.vida), True, (0, 255, 0))
            self.VENTANA.blit(vida_texto, (self.kroki.rect.centerx - vida_texto.get_width() // 2, self.kroki.rect.top - 20))

        pygame.display.update()

    # ================== LOOP ==================
    def run(self):
        while True:
            self.eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(30)
