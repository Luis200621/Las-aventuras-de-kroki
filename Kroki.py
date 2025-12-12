import pygame
import random

from settings import VELOCIDAD_KROKI

class Kroki(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super()._init_()

        # Atributos estado inicial de Kroki
        self.clase_actual = "None"
        self.orientacion = "Derecha"

        # Graficos de Kroki
        self.sprites = {
            "None": pygame.image.load("Imagenes/Captura de pantalla 2025-12-11 125012.png").convert_alpha(),
            "Guerrero": pygame.image.load("Imagenes/guerrero.png").convert_alpha(),
            "Mago": pygame.image.load("Imagenes/mago.png").convert_alpha()
        }

        for key in self.sprites:
            self.sprites[key] = pygame.transform.scale(self.sprites[key], (64,64))

        self.image = self.sprites[self.clase_actual]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Stats de las clases
        self.stats = {
            "Guerrero":{
                "vida":150,"maximo_mana":50,"velocidad": VELOCIDAD_KROKI -2, "dano": 18, "probabilidad_critico":0.20, "alcance": 50
            },
            "Mago":{
                "vida":100,"maximo_mana":100,"velocidad": VELOCIDAD_KROKI +1, "dano": 10, "probabilidad_critico":0.35, "alcance": 200
            },
            "None": {
                "vida":100,"maximo_mana":0,"velocidad": VELOCIDAD_KROKI, "dano": 5, "probabilidad_critico":0.10, "alcance": 20
            }
        }

        # Estadisticas generales de Kroki
        stats_iniciales = self.stats[self.clase_actual]
        self.vida = stats_iniciales["vida"] # Vida
        self.max_vida = self.vida # Vida maxima
        self.mana = stats_iniciales["maximo_mana"] # Mana
        self.max_mana = self.mana # Mana maximo

        # Habilidades
        self.habilidad = False
        self.escudoM = False
        self.tiempo_habilidad_activada = 0
        self.tiempo_ultimo_uso = 0
        self.duracion_habilidad = 5000
        self.cooldown_habilidad = 10000
        self.costo_mana = 25

        # Combate
        self.atacando = False
        self.cooldawn_ataque = 200
        self.tiempo_ultimo_ataque = 0


    # Cambio de clase
    def cambiar_clase(self, nueva_clase):
        if self.clase_actual == "None" and nueva_clase in ["Guerrero", "Mago"]:
            self.clase_actual = nueva_clase
            stats = self.stats[nueva_clase]

            # Aqui cambiamos los atributos por la clase elegida
            self.vida = stats['vida']
            self.max_vida = stats['vida']
            self.mana = stats['maximo_mana']
            self.max_mana = stats['maximo_mana']
            self.image = self.sprites[nueva_clase]

            return True
        return False
    
    def movimiento(self):
        keys = pygame.key.get_pressed() 
        velocidad = self.stats[self.clase_actual]["velocidad"]

        if keys[pygame.K_LEFT]:
            self.rect.x -= velocidad
            self.orientacion = "izquierda"
        if keys[pygame.K_RIGHT]:
            self.rect.x += velocidad
            self.orientacion = "derecha"
        if keys[pygame.K_UP]:
            self.rect.y -= velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += velocidad
    
        if keys[pygame.K_q]: #Tecla "q" dara la habilidad
                self.activar_habilidad(pygame.time.get_ticks())

    def ataques_kroki (self):
        stats = self.stats[self.clase_actual]
        dano_final = stats["dano"]

        if self.habilidad and self.clase_actual == "Guerrero":
            dano_final *= 1.20

        # Golpe critico
        golpe_critico = False
        if random.random() < stats["probabilidad_critico"]:
            dano_critico_extra = dano_final * 0.5
            dano_final += dano_critico_extra
            golpe_critico = True

        return dano_final, golpe_critico
    
    def dano_recibido (self,dano):
        # Bloqueo por escudo de mago
        if self.escudoM and self.clase_actual == "Mago":
            return
        if self.vida > 0:
            self.vida -= dano

        if self.vida <= 0:
            self.vida = 0


    def activar_habilidad(self, tiempo):
        cooldown_terminado = (tiempo - self.tiempo_ultimo_uso >= self.cooldawn_habilidad)

        if self.clase_actual != "None" and not self.habilidad and cooldown_terminado:

                if self.mana >= self.costo_mana:
                    self.mana -= self.costo_mana
                    self.habilidad = True
                    self.tiempo_habilidad_activada = tiempo

                    if self.clase_actual == "Mago":
                        self.escudoM = True

                    return True
                
                return False
        
    def manejar_habilidad(self, tiempo):
        if self.habilidad:

            self.aplicar_efecto_color(self.clase_actual)

            if tiempo - self.tiempo_habilidad_activada >= self.duracion_habilidad:
                self.habilidad = False
                self.tiempo_ultimo_uso = tiempo

                self.image = self.sprites[self.clase_actual].copy()

                if self.clase_actual == "Mago":
                    self.escudoM = False
        else:
            self.image = self.sprites[self.clase_actual].copy()

    def aplicar_efecto_color(self, clase):
        color_map = {"Guerrero": (255,0,0,100), "Mago": (0,255,0,100)}

        if clase in color_map:
            temp_image = self.sprites[self.clase_actual].copy()
            temp_image.fill(color_map[clase], special_flags=pygame.BLEND_RGBA_MULT)
            self.image = temp_image

        # Actualizacion

    def uptade(self):
        tiempo_actual = pygame.time.get_ticks()
        self.movimiento()
        self.manejar_habilidad(tiempo_actual)