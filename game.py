import pygame

from config import *
from estados import *

from auto import Auto
from terreno import *
from monedas import *
import monedas



import terreno

from ui import (
    dibujar_hud,
    dibujar_menu,
    dibujar_selector_mapa,
    dibujar_preview_mapa,
    dibujar_taller,
    dibujar_ajustes,
    dibujar_game_over,
    dibujar_velocimetro
)

from Datos import guardar_datos, cargar_datos


class Game:
    # ---------------- INICIALIZACIÓN ----------------
    def __init__(self):

        # Inicializar Pygame
        pygame.init()

        # Configurar la pantalla
        self.pantalla = pygame.display.set_mode(
            (ANCHO, ALTO)
        )

        # Establecer el título de la ventana
        pygame.display.set_caption(
            "prototipo de juego"
        )

        # Reloj para controlar los FPS
        self.clock = pygame.time.Clock()

        # Estado actual del juego (MENU, JUGANDO, GAME_OVER, etc.)
        self.estado = MENU

        # Variable para manejar la navegación en el menú principal
        self.opcion_menu = 0

        # Variable para manejar la navegación en el taller
        self.opcion_taller = 0

        # 
        self.opcion_tienda = 0

        #
        self.moto_desbloqueada = False
        self.desierto_desbloqueado = False

        # Vehículos disponibles para el taller
        self.vehiculos = [
            "Auto",
            "Moto"
        ]

        # Colores disponibles para el taller
        self.colores = [
            ROJO,
            AZUL_REY,
            ROSA,
            BLANCO,
            MORADO,
            NEGRO
        ]

        # Nombres de los colores para mostrar en el taller
        self.nombre_colores = [
            "Rojo",
            "Azul Rey",
            "Rosa",
            "Blanco",
            "Morado",
            "Negro"
        ]

        # Color actual (índice en la lista de colores)
        self.color_actual = 0

        # Vehículo actual (índice en la lista de vehículos)
        self.vehiculo_actual = 0

        # Mapas disponibles
        self.mapas = [
            "Pradera",
            "Desierto"
        ]

        # Mapa actual (índice en la lista de mapas)
        self.mapa_actual = 0

        # generar puntos de control para el terreno
        generar_control_points()

        # Generar puentes
        generar_puentes()
        
        # Generar terreno
        self.terrain = generar_terreno()

        # Nubes
        generar_nubes()

        # Cactus
        generar_cactus()

        # Auto
        self.auto = Auto()

        # Monedas
        self.coins = generar_monedas(
            self.terrain
        )
        self.gasolinas = generar_gasolinas(
            self.terrain
        )

        # Variable para controlar el loop principal
        self.running = True

        # Variable para manejar el tiempo antes de mostrar la pantalla de game over
        self.game_over_timer = 0

        # Variable para manejar la navegación en el menú de game over
        self.opcion_game_over = 0

        # Mensajes de game over para mostrar aleatoriamente
        self.mensajes_game_over = [
            "¿Y asi tienes licencia?",
            "Mejor suerte la proxima",
            "El seguro no cubre eso",
            "La gravedad gano",
            "El coche no opina igual",
            "Eso dolio mas de lo esperado"
        ]
        
        # Variable para animar el menú
        self.menu_anim = 0

        # Variable para animar el preview del vehículo en el menú
        self.preview_offset = 0
        self.menu_anim = 0

        # --------------- Guardado ----------------

        datos = cargar_datos()

        self.monedas_totales = datos.get("monedas", 0)
        self.record_distancia = datos.get("distancia", 0)

        self.moto_desbloqueada = datos.get("moto", False)
        self.desierto_desbloqueado = datos.get("desierto", False)

        self.volumen = datos.get("volumen", 50)
        #precios


        # ---------- ajustes -----------------------
        self.volumen = 50

    # ---------------- EVENTOS ----------------

    def eventos(self):
        # Manejar eventos
        for evento in pygame.event.get():
            # Salir del juego
            if evento.type == pygame.QUIT:
                # Detener el loop principal
                self.running = False
            # Manejar eventos de teclado
            if evento.type == pygame.KEYDOWN:

                # Manejar teclas según el estado en el menu principal
                if self.estado == MENU:

                    # Mover hacia arriba en el menú
                    if evento.key == pygame.K_UP:
                        self.opcion_menu -= 1

                    # Mover hacia abajo en el menú
                    if evento.key == pygame.K_DOWN:
                        self.opcion_menu += 1

                    # Asegurar que la opción esté en rango
                    self.opcion_menu %= 6

                    # Seleccionar opción
                    if evento.key == pygame.K_RETURN:

                        # Ejecutar acción según la opción seleccionada
                        if self.opcion_menu == 0:
                            # Reiniciar el juego y empezar a jugar
                            self.auto.reset()
                            # Cambiar al estado de juego
                            self.estado = JUGANDO

                        # Si se selecciona la opción de selección de mapa, cambiar al estado selection mapa para elegir el mapa antes de jugar
                        elif self.opcion_menu == 1:
                            # Cambiar al estado de selección de mapa para elegir el mapa antes de jugar
                            self.estado = SELECCION_MAPA

                        # Si se selecciona la opción de taller, cambiar al estado taller para personalizar el vehículo
                        elif self.opcion_menu == 2:
                            # Cambiar al estado de taller para personalizar el vehículo
                            self.estado = TALLER

                        #
                        elif self.opcion_menu == 3:
                            self.estado = TIENDA

                        elif self.opcion_menu == 4:
                            self.estado = AJUSTES

                        elif self.opcion_menu == 5:
                            self.running = False

                #Navegación del menú Game Over
                elif self.estado == GAME_OVER:

                    # Mover hacia arriba para seleccionar opción
                    if evento.key == pygame.K_UP:
                        self.opcion_game_over = (
                            self.opcion_game_over - 1
                        ) % 2
                    elif evento.key == pygame.K_DOWN:

                        self.opcion_game_over = (
                            self.opcion_game_over + 1
                        ) % 2

                    # Seleccionar opción en el menú de game over 
                    elif evento.key == pygame.K_RETURN:

                        # Si se selecciona la opción de volver a jugar, reiniciar el auto y volver al estado de juego
                        if self.opcion_game_over == 0:
                            self.auto.reset()
                            self.estado = JUGANDO

                        # Si se selecciona la opción de volver al menú, reiniciar el auto y volver al estado de menú
                        else:
                            self.auto.reset()
                            self.estado = MENU
                
                # Navegación del taller
                elif self.estado == TALLER:

                    # Mover hacia arriba o abajo para seleccionar vehículo o color
                    if evento.key == pygame.K_UP:
                        self.vehiculo_actual -= 1

                    if evento.key == pygame.K_DOWN:
                        self.vehiculo_actual += 1

                    # Asegurar que el índice del vehículo esté dentro del rango de vehículos disponibles
                    self.vehiculo_actual %= len(
                        self.vehiculos
                    )

                    # Mover hacia la derecha o izquierda para cambiar el color del vehículo
                    if evento.key == pygame.K_RIGHT:
                        self.color_actual += 1

                    if evento.key == pygame.K_LEFT:
                        self.color_actual -= 1

                    # Asegurar que el índice del color esté dentro del rango de colores disponibles
                    self.color_actual %= len(
                        self.colores
                    )

                    # Actualizar el tipo y color del auto según las selecciones en el taller
                    self.auto.tipo = self.vehiculos[
                        self.vehiculo_actual
                    ]

                    self.auto.color = self.colores[
                        self.color_actual
                    ]

                    if evento.key == pygame.K_RETURN:

                            self.estado = MENU

                #
                elif self.estado == TIENDA:

                    if evento.key == pygame.K_UP:
                        self.opcion_tienda = (
                            self.opcion_tienda - 1
                        ) % 2

                    if evento.key == pygame.K_DOWN:
                        self.opcion_tienda = (
                            self.opcion_tienda + 1
                        ) % 2

                    if evento.key == pygame.K_RETURN:

                        # Comprar Moto
                        if self.opcion_tienda == 0:

                            if not self.moto_desbloqueada:

                                if (
                                    self.monedas_totales >= self.precios["Moto"]["monedas"]
                                    and
                                    self.record_distancia >= self.precios["Moto"]["distancia"]
                                ):

                                    self.monedas_totales -= self.precios["Moto"]["monedas"]

                                    self.moto_desbloqueada = True

                                    guardar_datos({
                                        "monedas": self.monedas_totales,
                                        "distancia": self.record_distancia,
                                        "moto": self.moto_desbloqueada,
                                        "desierto": self.desierto_desbloqueado,
                                        "volumen": self.volumen
                                    })

                        # Comprar Desierto
                        elif self.opcion_tienda == 1:

                            if not self.desierto_desbloqueado:

                                if (
                                    self.monedas_totales >= self.precios["Desierto"]["monedas"]
                                    and
                                    self.record_distancia >= self.precios["Desierto"]["distancia"]
                                ):

                                    self.monedas_totales -= self.precios["Desierto"]["monedas"]

                                    self.desierto_desbloqueado = True

                                    guardar_datos({
                                        "monedas": self.monedas_totales,
                                        "distancia": self.record_distancia,
                                        "moto": self.moto_desbloqueada,
                                        "desierto": self.desierto_desbloqueado,
                                        "volumen": self.volumen
                                    })

                                    

                    if evento.key == pygame.K_ESCAPE:

                        self.estado = MENU

                #
                elif self.estado == AJUSTES:

                    if evento.key == pygame.K_RIGHT:
                        self.volumen += 5

                    if evento.key == pygame.K_LEFT:
                        self.volumen -= 5

                    self.volumen = max(
                        0,
                        min(100, self.volumen)
                    )

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

                        if (
                            self.mapas[self.mapa_actual] == "Desierto"
                            and
                            not self.desierto_desbloqueado
                        ):
                            pass

                        else:
                            self.estado = MENU


    # ---------------- UPDATE ----------------

    def update(self, dt):
        teclas = pygame.key.get_pressed()
        self.menu_anim += dt
        self.preview_offset += 0.3* dt

        if self.estado == JUGANDO:
            actualizar_terreno(self.terrain, self.auto.x)
            self.auto.update(dt, teclas, self.terrain)
            
            import terreno
            terreno.AUTO_X_GLOBAL = self.auto.x

            # --- Monedas ---
            recolectar_monedas(self.auto, self.coins)
            actualizar_monedas(self.coins, self.auto, self.terrain)
            
            # --- Gasolina ---
            recolectar_gasolinas(self.auto, self.gasolinas)
            actualizar_gasolinas(self.gasolinas, self.auto, self.terrain)
            
            # --- Game Over y Guardado ---
            if self.auto.game_over:

                self.monedas_totales += self.auto.monedas

                if self.auto.x > self.record_distancia:
                    self.record_distancia = int(self.auto.x)

                guardar_datos({
                    "monedas": self.monedas_totales,
                    "distancia": self.record_distancia,
                    "moto": self.moto_desbloqueada,
                    "desierto": self.desierto_desbloqueado,
                    "volumen": self.volumen
                })

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

            dibujar_preview_mapa(
                self.pantalla,
                self.mapas[
                    self.mapa_actual
                ],
                self.preview_offset
            )

            dibujar_selector_mapa(
                self.pantalla,
                self.mapas,
                self.mapa_actual
            )
            pygame.display.flip()
            return
    
        if self.estado == TALLER:
            # Taller
            dibujar_taller(
                self.pantalla,
                self.auto,
                self.vehiculos[self.vehiculo_actual],
                self.nombre_colores[self.color_actual]
            )
            pygame.display.flip()
            return
        
        if self.estado == AJUSTES:

            dibujar_ajustes(
                self.pantalla,
                self.volumen
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

        # Monedas y Gasolina
        monedas.dibujar_monedas(
            self.pantalla,
            self.coins,
            self.auto.cam_x
        )
        
        dibujar_gasolinas(
            self.pantalla,
            self.gasolinas,
            self.auto.cam_x
        )

        # Auto
        self.auto.draw(self.pantalla)

        # HUD (Barras y texto base)
        dibujar_hud(
            self.pantalla,
            self.auto
        )
        
        # Interfaz del contador de monedas
        monedas.dibujar_ui_monedas(
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
                self.vehiculos[self.vehiculo_actual],
                self.colores[self.color_actual],
                self.monedas_totales,
                self.record_distancia
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
            # ---> AQUÍ ESTÁ LA CORRECCIÓN DE LOS ARGUMENTOS <---
           dibujar_game_over(
            self.pantalla,
            self.auto,
            self.opcion_game_over,
            self.mensajes_game_over[
                int(self.auto.x) % len(self.mensajes_game_over)
            ],
            self.record_distancia,
            self.monedas_totales
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