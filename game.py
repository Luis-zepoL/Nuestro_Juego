import pygame

from config import *
from estados import *

from auto import Auto
from terreno import *
from monedas import *

import terreno
from ui import (
    dibujar_hud,
    dibujar_menu,
    dibujar_selector_mapa,
    dibujar_taller,
    dibujar_game_over,
    dibujar_velocimetro
)


class Game:

    def __init__(self):

        pygame.init()

        self.pantalla = pygame.display.set_mode(
            (ANCHO, ALTO)
        )

        pygame.display.set_caption(
            "prototipo de juego"
        )

        self.clock = pygame.time.Clock()

        self.estado = MENU

        self.opcion_menu = 0

        self.opcion_taller = 0

        self.vehiculos = [
            "Auto",
            "Moto"
        ]

        self.colores = [
            ROJO,
            AZUL_REY,
            ROSA,
            BLANCO,
            MORADO,
            NEGRO
        ]

        self.nombre_colores = [
            "Rojo",
            "Azul Rey",
            "Rosa",
            "Blanco",
            "Morado",
            "Negro"
        ]

        self.color_actual = 0

        self.vehiculo_actual = 0

        self.mapas = [
            "Pradera",
            "Desierto"
        ]

        self.mapa_actual = 0

        generar_control_points()

        generar_puentes()

        self.terrain = generar_terreno()

        generar_nubes()

        generar_cactus()

        self.auto = Auto()

        self.coins = generar_monedas(
            self.terrain
        )

        self.running = True

        self.game_over_timer = 0

        self.opcion_game_over = 0

        self.mensajes_game_over = [
            "¿Y asi tienes licencia?",
            "Mejor suerte la proxima",
            "El seguro no cubre eso",
            "La gravedad gano",
            "El coche no opina igual",
            "Eso dolio mas de lo esperado"
        ]

        self.menu_anim = 0

        self.vehiculos = [
            "Auto",
            "Moto"
        ]

        self.vehiculo_actual = 0

        self.color_actual = 0

        self.opcion_taller = 0

    # ---------------- EVENTOS ----------------

    def eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                self.running = False

            if evento.type == pygame.KEYDOWN:

                # Manejar teclas según el estado
                if self.estado == MENU:

                    if evento.key == pygame.K_UP:
                        self.opcion_menu -= 1

                    if evento.key == pygame.K_DOWN:
                        self.opcion_menu += 1

                    # Asegurar que la opción esté en rango
                    self.opcion_menu %= 4

                    if evento.key == pygame.K_RETURN:

                        if self.opcion_menu == 0:

                            self.auto.reset()

                            self.estado = JUGANDO

                        elif self.opcion_menu == 1:

                            self.estado = SELECCION_MAPA

                        elif self.opcion_menu == 2:

                            self.estado = TALLER

                        elif self.opcion_menu == 3:

                            self.running = False

                #Navegación del menú Game Over
                elif self.estado == GAME_OVER:

                    if evento.key == pygame.K_UP:

                        self.opcion_game_over = (
                            self.opcion_game_over - 1
                        ) % 2

                    elif evento.key == pygame.K_DOWN:

                        self.opcion_game_over = (
                            self.opcion_game_over + 1
                        ) % 2

                    elif evento.key == pygame.K_RETURN:

                        if self.opcion_game_over == 0:

                            self.auto.reset()

                            self.estado = JUGANDO

                        else:

                            self.auto.reset()

                            self.estado = MENU
                
                # Navegación del taller
                elif self.estado == TALLER:

                    if evento.key == pygame.K_UP:
                        self.vehiculo_actual -= 1

                    if evento.key == pygame.K_DOWN:
                        self.vehiculo_actual += 1

                    self.vehiculo_actual %= len(
                        self.vehiculos
                    )

                    if evento.key == pygame.K_RIGHT:
                        self.color_actual += 1

                    if evento.key == pygame.K_LEFT:
                        self.color_actual -= 1

                    self.color_actual %= len(
                        self.colores
                    )

                    self.auto.tipo = self.vehiculos[
                        self.vehiculo_actual
                    ]

                    self.auto.color = self.colores[
                        self.color_actual
                    ]

                    if evento.key == pygame.K_RETURN:

                            self.estado = MENU

                # Navegación del menú de selección de mapa
                elif self.estado == SELECCION_MAPA:

                    if evento.key == pygame.K_UP:
                        self.mapa_actual -= 1

                    if evento.key == pygame.K_DOWN:
                        self.mapa_actual += 1

                    self.mapa_actual %= len(self.mapas)

                    if evento.key == pygame.K_RETURN:

                        self.estado = MENU


    # ---------------- UPDATE ----------------

    def update(self, dt):

        teclas = pygame.key.get_pressed()
        self.menu_anim += dt

        if self.estado == JUGANDO:

            actualizar_terreno(
                self.terrain,
                self.auto.x
            )

            self.auto.update(
                dt,
                teclas,
                self.terrain
            )

            import terreno
            terreno.AUTO_X_GLOBAL = self.auto.x

            recolectar_monedas(
                self.auto,
                self.coins,
                self.terrain
            )

            actualizar_monedas(
                self.coins,
                self.auto,
                self.terrain
            )
            #tiempo de game over para mostrar mensaje antes de pasar a pantalla de game over
            if self.auto.game_over:
                self.game_over_timer = 0.5
                self.estado = GAME_OVER_DELAY
        
        elif self.estado == GAME_OVER_DELAY:

            self.game_over_timer -= dt / FPS

            if self.game_over_timer <= 0:

                self.estado = GAME_OVER

    # ---------------- DIBUJO ----------------

    def draw(self):

        # Si estamos en el selector de mapa, solo dibujar eso
        if self.estado == SELECCION_MAPA:

            dibujar_selector_mapa(
                self.pantalla,
                self.mapas,
                self.mapa_actual
            )

            pygame.display.flip()

            return
    
        if self.estado == TALLER:
            #Taller
            dibujar_taller(
                self.pantalla,
                self.auto,
                self.vehiculos[self.vehiculo_actual],
                self.nombre_colores[self.color_actual]
            )

            pygame.display.flip()

            return

        # Fondo cielo
        if self.estado == MENU:
            self.pantalla.fill((15, 20, 40))
        elif self.estado == SELECCION_MAPA:
            self.pantalla.fill((20, 25, 50))
        elif self.mapas[self.mapa_actual] == "Pradera":
            self.pantalla.fill((135, 206, 235))
        else:
            self.pantalla.fill((255, 210, 120))

        # Nubes
        dibujar_nubes(
            self.pantalla,
            self.auto.cam_x
        )

        # Terreno
        color_terreno = VERDE

        if self.mapas[self.mapa_actual] == "Desierto":

            color_terreno = (194, 178, 128)

        dibujar_terreno(
            self.pantalla,
            self.terrain,
            self.auto.cam_x,
            color_terreno
        )

        # Cactus (solo en desierto)
        if self.mapas[self.mapa_actual] == "Desierto":
            dibujar_cactus(
                self.pantalla,
                self.auto.cam_x,
                self.terrain
            )
        
        # Puentes
        dibujar_puentes(
            self.pantalla,
            self.auto.cam_x,
            self.terrain
        )

        # Monedas
        dibujar_monedas(
            self.pantalla,
            self.coins,
            self.auto.cam_x,
            self.terrain
        )

        # Auto
        self.auto.draw(self.pantalla)

        # HUD
        dibujar_hud(
            self.pantalla,
            self.auto
        )

        # Velocímetro
        dibujar_velocimetro(
            self.pantalla,
            abs(self.auto.vel_x * 10)
        )

        # Menu / Selector / Game over
        if self.estado == MENU:
            dibujar_menu(
            self.pantalla,
            self.opcion_menu,
            self.menu_anim,
            self.vehiculos[
                self.vehiculo_actual
            ],
            self.colores[
                self.color_actual
            ]
        )

        elif self.estado == SELECCION_MAPA:
            dibujar_selector_mapa(
                self.pantalla,
                self.mapas,
                self.mapa_actual
            )

        if self.estado == GAME_OVER_DELAY:

            s = pygame.Surface(
                (ANCHO, ALTO),
                pygame.SRCALPHA
            )

            s.fill((0, 0, 0, 180))

            self.pantalla.blit(
                s,
                (0, 0)
            )

        elif self.estado == GAME_OVER:
            dibujar_game_over(
                self.pantalla,
                self.auto,
                self.opcion_game_over,
                self.mensajes_game_over[
                    int(self.auto.x)
                    % len(self.mensajes_game_over)
                ]
            )

        # Actualizar pantalla
        pygame.display.flip()

    # ---------------- RUN ----------------

    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 16.67

            if dt > 2:

                dt = 1

            self.eventos()

            self.update(dt)

            self.draw()

        pygame.quit()