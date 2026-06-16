import pygame

from config import *
from estados import *

from auto import Auto
from Moto import Moto
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
    dibujar_tienda,
    dibujar_game_over,
    dibujar_velocimetro
)

from Datos import guardar_datos, cargar_datos


class Game:

    # Constructor principal del juego.
    def __init__(self):

        # Inicialización de Pygame y creación de la ventana.
        pygame.init()

        self.pantalla = pygame.display.set_mode(
            (ANCHO, ALTO)
        )

        pygame.display.set_caption(
            "HILL CLIMB FAKE"
        )

        # Controlador de FPS del juego.
        self.clock = pygame.time.Clock()

        # Estado actual del juego.
        # Determina qué pantalla se está mostrando.
        self.estado = MENU

        # Variables de navegación de los diferentes menús.
        self.opcion_menu = 0
        self.opcion_taller = 0
        self.opcion_tienda = 0

        # Variables que almacenan los desbloqueos del jugador.
        self.moto_desbloqueada = False
        self.desierto_desbloqueado = False

        # Catálogo de vehículos disponibles en el taller.
        self.vehiculos = [
            "Auto",
            "Moto"
        ]

        # Colores que puede seleccionar el jugador.
        self.colores = [
            ROJO,
            AZUL_REY,
            ROSA,
            BLANCO,
            MORADO,
            NEGRO
        ]

        # Nombre de cada color para mostrarlo en la interfaz.
        self.nombre_colores = [
            "Rojo",
            "Azul Rey",
            "Rosa",
            "Blanco",
            "Morado",
            "Negro"
        ]

        # Selecciones actuales del taller.
        self.color_actual = 0
        self.vehiculo_actual = 0

        # Catálogo de mapas disponibles.
        self.mapas = [
            "Pradera",
            "Desierto"
        ]

        # Mapa seleccionado actualmente.
        self.mapa_actual = 0

        # Generación inicial de todos los elementos del escenario.
        generar_control_points()
        generar_puentes()

        self.terrain = generar_terreno()

        generar_nubes()
        generar_cactus()

        # Creación del vehículo principal del jugador.
        self.auto = Auto()

        # Creación de objetos recolectables del mapa.
        self.coins = generar_monedas(
            self.terrain
        )

        self.gasolinas = generar_gasolinas(
            self.terrain
        )

        # Control principal del ciclo del juego.
        self.running = True

        # Variables utilizadas durante la transición a Game Over.
        self.game_over_timer = 0
        self.opcion_game_over = 0

        # Frases aleatorias mostradas al perder.
        self.mensajes_game_over = [
            "¿Y asi tienes licencia?",
            "Mejor suerte la proxima",
            "El seguro no cubre eso",
            "La gravedad gano",
            "El coche no opina igual",
            "Eso dolio mas de lo esperado"
        ]

        # Variables utilizadas para animaciones de la interfaz.
        self.menu_anim = 0
        self.preview_offset = 0
        self.menu_anim = 0

        # Carga de datos guardados previamente.
        datos = cargar_datos()

        # Estadísticas y progreso permanente del jugador.
        self.monedas_totales = datos.get("monedas", 0)
        self.record_distancia = datos.get("distancia", 0)

        # Distancia recorrida únicamente en la partida actual.
        self.distancia_partida = 0

        # Restauración de desbloqueos guardados.
        self.moto_desbloqueada = datos.get("moto", False)
        self.desierto_desbloqueado = datos.get("desierto", False)

        # Costos y requisitos de los elementos desbloqueables.
        self.precios = {

            "Moto": {
                "monedas": 50,
                "distancia": 1000
            },

            "Desierto": {
                "monedas": 150,
                "distancia": 3000
            }
        }

       
# ---------------- EVENTOS ----------------
# Este método detecta y procesa todas las entradas del usuario
# (teclado, cerrar ventana, navegación de menús, etc.)

def eventos(self):

    # Recorrer todos los eventos generados por pygame
    for evento in pygame.event.get():

        # Cierre de la ventana
        if evento.type == pygame.QUIT:

            # Termina el ciclo principal del juego
            self.running = False

        # Detectar pulsaciones de teclado
        if evento.type == pygame.KEYDOWN:

            # ==================================================
            # MENÚ PRINCIPAL
            # ==================================================
            if self.estado == MENU:

                # Navegación vertical del menú
                if evento.key == pygame.K_UP:
                    self.opcion_menu -= 1

                if evento.key == pygame.K_DOWN:
                    self.opcion_menu += 1

                # Mantener la selección dentro del rango válido
                self.opcion_menu %= 5

                # Confirmar selección
                if evento.key == pygame.K_RETURN:

                    # Iniciar partida
                    if self.opcion_menu == 0:

                        self.auto.reset()
                        self.estado = JUGANDO

                    # Abrir selector de mapas
                    elif self.opcion_menu == 1:

                        self.estado = SELECCION_MAPA

                    # Abrir taller
                    elif self.opcion_menu == 2:

                        self.estado = TALLER

                    # Abrir tienda
                    elif self.opcion_menu == 3:

                        self.estado = TIENDA

                    # Salir del juego
                    elif self.opcion_menu == 4:

                        self.running = False

            # ==================================================
            # MENÚ GAME OVER
            # ==================================================
            elif self.estado == GAME_OVER:

                # Cambiar opción seleccionada
                if evento.key == pygame.K_UP:

                    self.opcion_game_over = (
                        self.opcion_game_over - 1
                    ) % 2

                elif evento.key == pygame.K_DOWN:

                    self.opcion_game_over = (
                        self.opcion_game_over + 1
                    ) % 2

                # Confirmar opción
                elif evento.key == pygame.K_RETURN:

                    # Reintentar partida
                    if self.opcion_game_over == 0:

                        self.auto.reset()
                        self.estado = JUGANDO

                    # Volver al menú principal
                    else:

                        self.auto.reset()
                        self.estado = MENU

            # ==================================================
            # TALLER
            # ==================================================
            elif self.estado == TALLER:

                # Salir rápidamente al menú principal
                if evento.key == pygame.K_ESCAPE:

                    self.estado = MENU

                # Cambiar vehículo
                if evento.key == pygame.K_UP:

                    self.vehiculo_actual -= 1

                    self.vehiculo_actual %= len(
                        self.vehiculos
                    )

                    self.auto.tipo = self.vehiculos[
                        self.vehiculo_actual
                    ]

                elif evento.key == pygame.K_DOWN:

                    self.vehiculo_actual += 1

                    self.vehiculo_actual %= len(
                        self.vehiculos
                    )

                    self.auto.tipo = self.vehiculos[
                        self.vehiculo_actual
                    ]

                # Cambiar color del vehículo
                elif evento.key == pygame.K_RIGHT:

                    self.color_actual += 1

                    self.color_actual %= len(
                        self.colores
                    )

                    self.auto.color = self.colores[
                        self.color_actual
                    ]

                elif evento.key == pygame.K_LEFT:

                    self.color_actual -= 1

                    self.color_actual %= len(
                        self.colores
                    )

                    self.auto.color = self.colores[
                        self.color_actual
                    ]

                # Confirmar selección del vehículo
                elif evento.key == pygame.K_RETURN:

                    vehiculo = self.vehiculos[
                        self.vehiculo_actual
                    ]

                    # Impedir seleccionar una moto bloqueada
                    if (
                        vehiculo == "Moto"
                        and
                        not self.moto_desbloqueada
                    ):
                        pass

                    else:
                        self.estado = MENU

            # ==================================================
            # TIENDA
            # ==================================================
            elif self.estado == TIENDA:

                # Navegación entre productos
                if evento.key == pygame.K_UP:

                    self.opcion_tienda = (
                        self.opcion_tienda - 1
                    ) % 2

                if evento.key == pygame.K_DOWN:

                    self.opcion_tienda = (
                        self.opcion_tienda + 1
                    ) % 2

                # Comprar producto seleccionado
                if evento.key == pygame.K_RETURN:

                    # Compra de Moto
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
                                })

                    # Compra del mapa Desierto
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
                                })

                # Salir de la tienda
                if evento.key == pygame.K_ESCAPE:

                    self.estado = MENU

            # ==================================================
            # SELECTOR DE MAPAS
            # ==================================================
            elif self.estado == SELECCION_MAPA:

                # Salir al menú principal
                if evento.key == pygame.K_ESCAPE:

                    self.estado = MENU

                # Navegar entre mapas
                if evento.key == pygame.K_UP:

                    self.mapa_actual -= 1

                if evento.key == pygame.K_DOWN:

                    self.mapa_actual += 1

                self.mapa_actual %= len(
                    self.mapas
                )

                # Confirmar mapa seleccionado
                if evento.key == pygame.K_RETURN:

                    # Impedir seleccionar mapa bloqueado
                    if (
                        self.mapas[self.mapa_actual] == "Desierto"
                        and
                        not self.desierto_desbloqueado
                    ):
                        pass

                    else:
                        self.estado = MENU

   # ---------------- UPDATE ----------------
# Actualiza todos los elementos dinámicos del juego cada frame

def update(self, dt):

    # Obtener el estado actual de todas las teclas
    teclas = pygame.key.get_pressed()

    # Actualizar variables usadas para animaciones de interfaz
    self.menu_anim += dt
    self.preview_offset += 0.3 * dt

    # ==================================================
    # LÓGICA PRINCIPAL DEL JUEGO
    # ==================================================
    if self.estado == JUGANDO:

        # Generar y actualizar el terreno según el avance del jugador
        actualizar_terreno(
            self.terrain,
            self.auto.x
        )

        # Actualizar físicas y movimiento del vehículo
        self.auto.update(
            dt,
            teclas,
            self.terrain
        )

        # Compartir la posición actual del vehículo con el módulo terreno
        import terreno
        terreno.AUTO_X_GLOBAL = self.auto.x

        # ==================================================
        # SISTEMA DE MONEDAS
        # ==================================================

        # Detectar monedas recolectadas
        recolectar_monedas(
            self.auto,
            self.coins
        )

        # Generar y eliminar monedas según sea necesario
        actualizar_monedas(
            self.coins,
            self.auto,
            self.terrain
        )

        # ==================================================
        # SISTEMA DE GASOLINA
        # ==================================================

        # Detectar gasolina recolectada
        recolectar_gasolinas(
            self.auto,
            self.gasolinas
        )

        # Generar y eliminar gasolina según sea necesario
        actualizar_gasolinas(
            self.gasolinas,
            self.auto,
            self.terrain
        )

        # ==================================================
        # DETECCIÓN DE GAME OVER Y GUARDADO
        # ==================================================

        if self.auto.game_over:

            # Guardar la distancia recorrida en esta partida
            self.distancia_partida = int(
                self.auto.x
            )

            # Sumar monedas obtenidas a las monedas totales
            self.monedas_totales += self.auto.monedas

            # Actualizar récord si se superó la mejor distancia
            if self.auto.x > self.record_distancia:

                self.record_distancia = int(
                    self.auto.x
                )

            # Guardar progreso permanente
            guardar_datos({

                "monedas": self.monedas_totales,

                "distancia": self.record_distancia,

                "moto": self.moto_desbloqueada,

                "desierto": self.desierto_desbloqueado,

            })

            # Activar pantalla intermedia antes del Game Over
            self.game_over_timer = 0.5

            self.estado = GAME_OVER_DELAY

    # ==================================================
    # RETRASO ANTES DE MOSTRAR GAME OVER
    # ==================================================
    elif self.estado == GAME_OVER_DELAY:

        # Reducir temporizador
        self.game_over_timer -= dt / FPS

        # Cuando termina el tiempo aparece Game Over
        if self.game_over_timer <= 0:

            self.estado = GAME_OVER
    # ---------------- DIBUJO ----------------

# ---------------- DIBUJO Y ACTUALIZACIÓN DE PANTALLA ----------------
def draw(self):

    # Mostrar únicamente la interfaz de selección de mapa
    if self.estado == SELECCION_MAPA:

        # Dibujar vista previa visual del mapa seleccionado
        dibujar_preview_mapa(
            self.pantalla,
            self.mapas[
                self.mapa_actual
            ],
            self.preview_offset
        )

        # Dibujar menú de selección de mapas
        dibujar_selector_mapa(
            self.pantalla,
            self.mapas,
            self.mapa_actual,
            self.desierto_desbloqueado
        )
        pygame.display.flip()
        return

    # Mostrar únicamente la interfaz del taller
    if self.estado == TALLER:

        dibujar_taller(
            self.pantalla,
            self.auto,
            self.vehiculos[self.vehiculo_actual],
            self.nombre_colores[self.color_actual],
            self.moto_desbloqueada
        )

        pygame.display.flip()
        return

    # Mostrar únicamente la interfaz de la tienda
    if self.estado == TIENDA:

        dibujar_tienda(
            self.pantalla,
            self.monedas_totales,
            self.record_distancia,
            self.opcion_tienda,
            self.moto_desbloqueada,
            self.desierto_desbloqueado
        )

        pygame.display.flip()
        return

    # ---------------- FONDO SEGÚN EL ESTADO O MAPA ----------------

    if self.estado == MENU:
        self.pantalla.fill((15, 20, 40))

    elif self.estado == SELECCION_MAPA:
        self.pantalla.fill((20, 25, 50))

    elif self.mapas[self.mapa_actual] == "Pradera":
        self.pantalla.fill((135, 206, 235))

    else:
        self.pantalla.fill((255, 210, 120))

    # ---------------- ELEMENTOS DEL ESCENARIO ----------------

    # Dibujar nubes del fondo
    dibujar_nubes(
        self.pantalla,
        self.auto.cam_x
    )

    # Elegir color del terreno según el mapa
    color_terreno = VERDE

    if self.mapas[self.mapa_actual] == "Desierto":
        color_terreno = (194, 178, 128)

    # Dibujar terreno principal
    dibujar_terreno(
        self.pantalla,
        self.terrain,
        self.auto.cam_x,
        color_terreno
    )

    # Dibujar cactus solamente en el desierto
    if self.mapas[self.mapa_actual] == "Desierto":

        dibujar_cactus(
            self.pantalla,
            self.auto.cam_x,
            self.terrain
        )

    # Dibujar puentes generados en el terreno
    dibujar_puentes(
        self.pantalla,
        self.auto.cam_x,
        self.terrain
    )

    # ---------------- OBJETOS RECOLECTABLES ----------------

    # Dibujar monedas del mapa
    monedas.dibujar_monedas(
        self.pantalla,
        self.coins,
        self.auto.cam_x
    )

    # Dibujar gasolina del mapa
    dibujar_gasolinas(
        self.pantalla,
        self.gasolinas,
        self.auto.cam_x
    )

    # ---------------- VEHÍCULO ----------------

    # Dibujar el vehículo actual
    self.auto.draw(self.pantalla)

    # ---------------- INTERFAZ DEL JUGADOR ----------------

    # Dibujar barras de combustible y distancia
    dibujar_hud(
        self.pantalla,
        self.auto
    )

    # Dibujar contador de monedas
    monedas.dibujar_ui_monedas(
        self.pantalla,
        self.auto
    )

    # Dibujar velocímetro
    dibujar_velocimetro(
        self.pantalla,
        abs(self.auto.vel_x * 10)
    )

    # ---------------- MENÚ PRINCIPAL ----------------

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

    # ---------------- TRANSICIÓN A GAME OVER ----------------

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

    # ---------------- MENÚ DE GAME OVER ----------------

    elif self.estado == GAME_OVER:

        dibujar_game_over(
            self.pantalla,
            self.auto,
            self.opcion_game_over,
            self.mensajes_game_over[
                int(self.auto.x) % len(self.mensajes_game_over)
            ],
            self.distancia_partida,
            self.monedas_totales
        )

    # Actualizar todo lo dibujado en pantalla
    pygame.display.flip()


# ---------------- BUCLE PRINCIPAL DEL JUEGO ----------------
def run(self):

    # Ejecutar el juego mientras siga activo
    while self.running:

        # Controlar FPS y obtener delta de tiempo
        dt = self.clock.tick(FPS) / 16.67

        # Evitar saltos grandes de tiempo
        if dt > 2:
            dt = 1

        # Procesar entradas del usuario
        self.eventos()

        # Actualizar lógica del juego
        self.update(dt)

        # Dibujar todo en pantalla
        self.draw()

    # Cerrar pygame al salir
    pygame.quit()