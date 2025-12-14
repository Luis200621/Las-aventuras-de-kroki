import pygame
import random
import os

from settings import VELOCIDAD_KROKI, SCREEN_WIDTH, SCREEN_HEIGHT, GRAVEDAD,FUERZA_SALTO


class Kroki(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # ================== ESTADO ==================
        self.clase_actual = "None"
        self.orientacion = "Derecha"

        # ================== GRAFICOS ==================
        base_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_path, "Imagenes")
        
        self.sprites = {
            "None": pygame.image.load(os.path.join(img_path, "Kroki_inicial.png")).convert_alpha(),
            "Guerrero": pygame.image.load(os.path.join(img_path, "guerrero.png")).convert_alpha(),
            "Mago": pygame.image.load(os.path.join(img_path, "mago.png")).convert_alpha()
        }
        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (125, 125))

        self.image = self.sprites[self.clase_actual]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # ================== STATS ==================
        self.stats = {
            "None": {
                "vida": 100,
                "maximo_mana": 0,
                "velocidad": VELOCIDAD_KROKI,
                "dano": 5,
                "probabilidad_critico": 0.10,
                "alcance": 20
            },
            "Guerrero": {
                "vida": 150,
                "maximo_mana": 50,
                "velocidad": VELOCIDAD_KROKI - 2,
                "dano": 18,
                "probabilidad_critico": 0.20,
                "alcance": 50
            },
            "Mago": {
                "vida": 100,
                "maximo_mana": 100,
                "velocidad": VELOCIDAD_KROKI + 1,
                "dano": 15,
                "probabilidad_critico": 0.35,
                "alcance": 200
            }
        }

        self._cargar_stats()

        # ================== SALTO ==================
        self.velocidad_y = 0
        self.gravedad = GRAVEDAD
        self.fuerza_salto = FUERZA_SALTO
        self.en_suelo = True
        self.piso_y = SCREEN_HEIGHT - 60
        
        # ================== HABILIDAD ==================
        self.habilidad = False
        self.escudoM = False
        self.tiempo_habilidad_activada = 0
        self.tiempo_ultimo_uso = 0
        self.duracion_habilidad = 5000
        self.cooldown_habilidad = 10000
        self.costo_mana = 25

    # ================== CARGA DE STATS ==================
    def _cargar_stats(self):
        stats = self.stats[self.clase_actual]
        self.vida = stats["vida"]
        self.max_vida = stats["vida"]
        self.mana = stats["maximo_mana"]
        self.max_mana = stats["maximo_mana"]

    # ================== CAMBIO DE CLASE ==================
    def cambiar_clase(self, nueva_clase):
        if self.clase_actual == "None" and nueva_clase in ["Guerrero", "Mago"]:
            self.clase_actual = nueva_clase
            self._cargar_stats()
            self.image = self.sprites[nueva_clase]
            return True
        return False

    # ================== MOVIMIENTO ==================
    def movimiento(self):
        keys = pygame.key.get_pressed()
        velocidad = self.stats[self.clase_actual]["velocidad"]

        # Horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= velocidad
            self.orientacion = "izquierda"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += velocidad
            self.orientacion = "derecha"

        # Limites horizontales
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))


        # Salto
        if keys[pygame.K_SPACE] and self.en_suelo:
            self.velocidad_y = self.fuerza_salto
            self.en_suelo = False

        # Gravedad
        self.velocidad_y += self.gravedad

        if self.velocidad_y > 10:
            self.velocidad_y = 10
        self.rect.y += self.velocidad_y

        # Piso
        if self.rect.bottom >= self.piso_y:
            self.rect.bottom = self.piso_y
            self.velocidad_y = 0
            self.en_suelo = True

        # Habilidad
        if keys[pygame.K_q]:
            self.activar_habilidad(pygame.time.get_ticks())

    # ================== ATAQUE ==================
    def ataques_kroki(self):
        stats = self.stats[self.clase_actual]
        dano_final = stats["dano"]

        if self.habilidad and self.clase_actual == "Guerrero":
            dano_final *= 1.20

        golpe_critico = False
        if random.random() < stats["probabilidad_critico"]:
            dano_final += dano_final * 0.5
            golpe_critico = True

        return dano_final, golpe_critico

    # ================== DAÑO ==================
    def dano_recibido(self, dano):
        if self.escudoM and self.clase_actual == "Mago":
            return

        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    # ================== HABILIDAD ==================
    def activar_habilidad(self, tiempo):
        if (
            self.clase_actual != "None"
            and not self.habilidad
            and tiempo - self.tiempo_ultimo_uso >= self.cooldown_habilidad
            and self.mana >= self.costo_mana
        ):
            self.mana -= self.costo_mana
            self.habilidad = True
            self.tiempo_habilidad_activada = tiempo

            if self.clase_actual == "Mago":
                self.escudoM = True

            return True
        return False

    def manejar_habilidad(self, tiempo):
        if self.habilidad:
            self.aplicar_efecto_color()

            if tiempo - self.tiempo_habilidad_activada >= self.duracion_habilidad:
                self.habilidad = False
                self.tiempo_ultimo_uso = tiempo
                self.image = self.sprites[self.clase_actual]
                self.escudoM = False

        else:
            self.image = self.sprites[self.clase_actual]

    # ================== EFECTO VISUAL ==================
    def aplicar_efecto_color(self):
        colores = {
            "Guerrero": (255, 0, 0, 120),
            "Mago": (0, 255, 0, 120)
        }

        if self.clase_actual in colores:
            temp = self.sprites[self.clase_actual].copy()
            temp.fill(colores[self.clase_actual], special_flags=pygame.BLEND_RGBA_MULT)
            self.image = temp

    # ================== UPDATE ==================
    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        self.movimiento()
        self.manejar_habilidad(tiempo_actual)
