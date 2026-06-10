import pygame

from config import *
from estados import *

from auto import Auto
from terreno import *
from monedas import *

from ui import (
    dibujar_hud,
    dibujar_menu,
    dibujar_selector_mapa,
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

        self.mapas = [
            "Pradera",
            "Desierto"
        ]

        self.mapa_actual = 0

        generar_control_points()

        self.terrain = generar_terreno()

        generar_nubes()

        self.auto = Auto()

        self.coins = generar_monedas(
            self.terrain
        )

        self.running = True
        self.menu_anim = 0

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
                    self.opcion_menu %= 3

                    if evento.key == pygame.K_RETURN:

                        if self.opcion_menu == 0:

                            self.auto.reset()

                            self.estado = JUGANDO

                        elif self.opcion_menu == 1:

                            self.estado = SELECCION_MAPA

                        elif self.opcion_menu == 2:

                            self.running = False

                elif self.estado == GAME_OVER:

                    if evento.key == pygame.K_r:

                        self.auto.reset()

                        self.estado = JUGANDO

                    elif evento.key == pygame.K_m:

                        self.auto.reset()

                        self.estado = MENU

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

            if self.auto.game_over:

                self.estado = GAME_OVER

    # ---------------- DIBUJO ----------------

    def draw(self):

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
        dibujar_terreno(
            self.pantalla,
            self.terrain,
            self.auto.cam_x
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
                self.menu_anim
            )

        elif self.estado == SELECCION_MAPA:
            dibujar_selector_mapa(
                self.pantalla,
                self.mapas,
                self.mapa_actual
            )

        elif self.estado == GAME_OVER:
            dibujar_game_over(
                self.pantalla,
                self.auto
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