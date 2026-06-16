import math
import pygame
import random

from config import *

# ---------------- CONFIGURACIÓN GENERAL DEL TERRENO ----------------

# Distancia entre cada punto del terreno
ESPACIADO = 20

# Distancia máxima que se genera por delante del jugador
DISTANCIA_RENDER = 4000

# Distancia a partir de la cual se eliminan segmentos viejos
DISTANCIA_ELIMINAR = 1000

# Altura base usada como referencia para el terreno
altura_base = 520

# Guarda la posición global del vehículo para otros módulos
AUTO_X_GLOBAL = 0


# ---------------- GENERACIÓN DE PUNTOS DE CONTROL ----------------

def generar_control_points():

    global PUNTOS_CONTROL

    # Reinicia la lista de puntos de control
    PUNTOS_CONTROL = []

    x = -3000

    # Genera puntos de referencia a lo largo de todo el mapa
    while x < 200000:

        y = random.randint(
            250,
            600
        )

        PUNTOS_CONTROL.append(
            (x, y)
        )

        # Distancia aleatoria entre puntos
        x += random.randint(
            600,
            1800
        )


# ---------------- GENERACIÓN DE PUENTES ----------------

def generar_puentes():

    global PUENTES

    # Reinicia la lista de puentes
    PUENTES = []

    x = 6000

    # Crea puentes a intervalos regulares
    while x < 100000:

        largo = 700

        PUENTES.append(
            {
                "inicio": x,
                "fin": x + largo,
                "profundidad": 80
            }
        )

        x += 12000


# ---------------- VARIABLES GLOBALES DEL TERRENO ----------------

SEMILLA = 0

PUNTOS_CONTROL = []
PUENTES = []

CACTUS = []
NUBES = []


# ---------------- SUAVIZADO DE CURVAS ----------------

def smoothstep(t):

    return t * t * (3 - 2 * t)


# ---------------- GENERACIÓN INICIAL DEL TERRENO ----------------

def generar_terreno():

    terrain = []

    # Genera puntos visibles del terreno
    for x in range(
        -2000,
        DISTANCIA_RENDER,
        ESPACIADO
    ):

        y = generar_altura(x)

        terrain.append((x, y))

    return terrain


# ---------------- GENERACIÓN DE NUBES ----------------

def generar_nubes():

    global NUBES

    # Reinicia la lista de nubes
    NUBES = []

    # Genera posiciones predefinidas para las nubes
    for i in range(50):

        NUBES.append(
            (
                i * 600,
                60 + (i * 37) % 180,
                50 + (i * 17) % 40
            )
        )


# ---------------- GENERACIÓN DE CACTUS ----------------

def generar_cactus():

    global CACTUS

    # Reinicia la lista de cactus
    CACTUS = []

    x = 1000

    while x < 100000:

        dentro_puente = False

        # Evita colocar cactus cerca de puentes
        for puente in PUENTES:

            if puente["inicio"] - 100 <= x <= puente["fin"] + 100:

                dentro_puente = True
                break

        # Solo agrega cactus si no hay puente cerca
        if not dentro_puente:

            CACTUS.append(x)

        # Distancia aleatoria entre cactus
        x += random.randint(
            500,
            1500
        )


# ---------------- DIBUJO DE CACTUS ----------------

def dibujar_cactus(
    pantalla,
    cam_x,
    terrain
):

    # Recorre todos los cactus generados
    for x in CACTUS:

        # Convierte coordenada global a coordenada de pantalla
        px = x - cam_x

        # Solo dibuja cactus visibles
        if -100 <= px <= ANCHO + 100:

            suelo = get_ground(
                x,
                terrain
            )

            # Tronco principal
            pygame.draw.rect(
                pantalla,
                (20,120,20),
                (
                    px-8,
                    suelo-80,
                    16,
                    80
                )
            )

            # Brazo izquierdo
            pygame.draw.rect(
                pantalla,
                (20,120,20),
                (
                    px-25,
                    suelo-60,
                    15,
                    40
                )
            )

            # Brazo derecho
            pygame.draw.rect(
                pantalla,
                (20,120,20),
                (
                    px+10,
                    suelo-55,
                    15,
                    35
                )
            )

# ---------------- CÁLCULO DE ALTURA DEL TERRENO ----------------

def generar_altura(x):

    # Busca entre qué dos puntos de control se encuentra la posición x
    for i in range(
        len(PUNTOS_CONTROL) - 1
    ):

        x1, y1 = PUNTOS_CONTROL[i]
        x2, y2 = PUNTOS_CONTROL[i + 1]

        if x1 <= x <= x2:

            # Obtiene la posición relativa entre ambos puntos
            t = (
                (x - x1)
                /
                (x2 - x1)
            )

            # Suaviza la transición
            t = smoothstep(t)

            # Calcula la altura interpolada
            return (
                y1 * (1 - t)
                +
                y2 * t
            )

    # Altura por defecto si no encuentra puntos válidos
    return altura_base


# ---------------- EXPANSIÓN DINÁMICA DEL TERRENO ----------------

def actualizar_terreno(terrain, jugador_x):

    ultimo_x = terrain[-1][0]

    # Genera nuevo terreno delante del jugador
    while ultimo_x < jugador_x + DISTANCIA_RENDER:

        ultimo_x += ESPACIADO

        terrain.append(
            (
                ultimo_x,
                generar_altura(ultimo_x)
            )
        )

    # Sistema para eliminar terreno antiguo (actualmente desactivado)

    #while len(terrain) > 2 and terrain[1][0] < jugador_x - DISTANCIA_ELIMINAR:
    #    terrain.pop(0)


# ---------------- OBTENER ALTURA DEL SUELO ----------------

def get_ground(x, terrain):

    # Si está antes del primer punto generado
    if x <= terrain[0][0]:
        return terrain[0][1]

    # Si está después del último punto generado
    if x >= terrain[-1][0]:
        return terrain[-1][1]

    # Busca el segmento donde se encuentra x
    for i in range(len(terrain) - 1):

        x1, y1 = terrain[i]
        x2, y2 = terrain[i + 1]

        if x1 <= x <= x2:

            # Interpolación lineal entre dos puntos del terreno
            t = (x - x1) / (x2 - x1)

            altura = y1 * (1 - t) + y2 * t

            # Verifica si está dentro de algún puente
            for puente in PUENTES:

                if puente["inicio"] <= x <= puente["fin"]:

                    # Calcula deformación base del puente
                    centro = (
                        puente["inicio"]
                        + puente["fin"]
                    ) / 2

                    largo = (
                        puente["fin"]
                        - puente["inicio"]
                    )

                    distancia = abs(x - centro)

                    t = distancia / (largo / 2)

                    factor = math.cos(
                        t * math.pi / 2
                    )

                    factor = max(0, factor)

                    altura += (
                        factor ** 2
                    ) * puente["profundidad"]

                    # Añade deformación causada por el vehículo
                    altura += deformacion_puente(
                        x,
                        AUTO_X_GLOBAL
                    )

            return altura

    # Valor de seguridad
    return terrain[-1][1]


# ---------------- DIBUJO DE PUENTES ----------------

def dibujar_puentes(
    pantalla,
    cam_x,
    terrain
):

    # Recorre todos los puentes existentes
    for puente in PUENTES:

        puntos = []

        x = puente["inicio"]

        # Genera los puntos que forman la curva del puente
        while x <= puente["fin"]:

            y = get_ground(
                x,
                terrain
            )

            puntos.append(
                (
                    x - cam_x,
                    y
                )
            )

            x += 10

        if len(puntos) > 1:

            # ---------------- TABLONES DEL PUENTE ----------------

            pygame.draw.lines(
                pantalla,
                (120, 75, 35),
                False,
                puntos,
                12
            )

            pygame.draw.lines(
                pantalla,
                (170, 120, 70),
                False,
                puntos,
                3
            )

            # ---------------- EXTREMOS DEL PUENTE ----------------

            inicio = (
                puente["inicio"] - cam_x,
                get_ground_sin_deformacion(
                    puente["inicio"],
                    terrain
                )
            )

            fin = (
                puente["fin"] - cam_x,
                get_ground_sin_deformacion(
                    puente["fin"],
                    terrain
                )
            )

            # Plataforma izquierda
            pygame.draw.polygon(
                pantalla,
                (100, 70, 35),
                [
                    inicio,
                    (inicio[0] - 60, inicio[1]),
                    (inicio[0] - 60, inicio[1] + 40),
                    (inicio[0], inicio[1] + 20)
                ]
            )

            # Tabla superior izquierda
            pygame.draw.polygon(
                pantalla,
                (170, 130, 80),
                [
                    inicio,
                    (inicio[0] - 60, inicio[1]),
                    (inicio[0] - 60, inicio[1] + 8),
                    (inicio[0], inicio[1] + 8)
                ]
            )

            # Plataforma derecha
            pygame.draw.polygon(
                pantalla,
                (100, 70, 35),
                [
                    fin,
                    (fin[0] + 60, fin[1]),
                    (fin[0] + 60, fin[1] + 40),
                    (fin[0], fin[1] + 20)
                ]
            )

            # Tabla superior derecha
            pygame.draw.polygon(
                pantalla,
                (170, 130, 80),
                [
                    fin,
                    (fin[0] + 60, fin[1]),
                    (fin[0] + 60, fin[1] + 8),
                    (fin[0], fin[1] + 8)
                ]
            )

            # ---------------- POSTES DEL PUENTE ----------------

            altura_poste = 80

            pygame.draw.rect(
                pantalla,
                (110, 75, 35),
                (
                    inicio[0] - 5,
                    inicio[1] - altura_poste,
                    10,
                    altura_poste
                )
            )

            pygame.draw.rect(
                pantalla,
                (110, 75, 35),
                (
                    fin[0] - 5,
                    fin[1] - altura_poste,
                    10,
                    altura_poste
                )
            )

            # ---------------- CABLE SUPERIOR ----------------

            cable = []

            for px, py in puntos:

                cable.append(
                    (
                        px,
                        py - 65
                    )
                )

            cable[0] = (
                inicio[0],
                inicio[1] - altura_poste
            )

            cable[-1] = (
                fin[0],
                fin[1] - altura_poste
            )

            pygame.draw.lines(
                pantalla,
                (80, 80, 80),
                False,
                cable,
                3
            )

            # ---------------- TENSORES ----------------

            for i in range(
                0,
                len(puntos),
                4
            ):

                pygame.draw.line(
                    pantalla,
                    (120, 120, 120),
                    cable[i],
                    puntos[i],
                    2
                )

# ---------------- GENERACIÓN DE DEFORMACIÓN DE PUENTES ----------------

def deformacion_puente(x, auto_x):

    # Recorre todos los puentes existentes
    for puente in PUENTES:

        # Verifica que el punto consultado esté dentro del puente
        if puente["inicio"] <= x <= puente["fin"]:

            # Verifica que el vehículo también esté sobre ese puente
            if puente["inicio"] <= auto_x <= puente["fin"]:

                # Distancia entre el punto del puente y el vehículo
                distancia = abs(x - auto_x)

                # Solo se deforma una zona cercana al vehículo
                if distancia < 140:

                    influencia_auto = (
                        1 - distancia / 140
                    )

                    largo = (
                        puente["fin"]
                        - puente["inicio"]
                    )

                    # Posición relativa dentro del puente (0 a 1)
                    posicion = (
                        x - puente["inicio"]
                    ) / largo

                    # Mantener extremos del puente fijos
                    anclaje = math.sin(
                        posicion * math.pi
                    )

                    # Suavizar deformación cerca de los extremos
                    anclaje = anclaje ** 1.5

                    # Retornar deformación final
                    return (
                        influencia_auto
                        * anclaje
                        * 25
                    )

    # Si no aplica deformación devuelve 0
    return 0


# -------- OBTENER ALTURA DEL TERRENO SIN DEFORMACIÓN DEL PUENTE -----------

def get_ground_sin_deformacion(x, terrain):

    # Protección si la posición está antes del terreno generado
    if x <= terrain[0][0]:
        return terrain[0][1]

    # Protección si la posición está después del terreno generado
    if x >= terrain[-1][0]:
        return terrain[-1][1]

    # Buscar el segmento correcto del terreno
    for i in range(len(terrain)-1):

        x1, y1 = terrain[i]
        x2, y2 = terrain[i+1]

        if x1 <= x <= x2:

            # Interpolación entre puntos del terreno
            t = (x - x1)/(x2 - x1)

            altura = y1*(1-t) + y2*t

            # Aplicar forma base del puente
            for puente in PUENTES:

                if puente["inicio"] <= x <= puente["fin"]:

                    centro = (
                        puente["inicio"]
                        + puente["fin"]
                    ) / 2

                    largo = (
                        puente["fin"]
                        - puente["inicio"]
                    )

                    distancia = abs(x - centro)

                    factor = math.cos(
                        (distancia/(largo/2))
                        * math.pi/2
                    )

                    factor = max(0, factor)

                    altura += (
                        factor**2
                    ) * puente["profundidad"]

            return altura

    return terrain[-1][1]


# ---------------- CALCULAR INCLINACIÓN DEL TERRENO ----------------

def get_slope(x, terrain):

    # Obtiene dos alturas cercanas
    y1 = get_ground(x - 5, terrain)
    y2 = get_ground(x + 5, terrain)

    # Convierte la diferencia en un ángulo
    return math.atan2(y2 - y1, 10)


# ---------------- DIBUJAR TERRENO ----------------

def dibujar_terreno(pantalla, terrain, cam_x, color_terreno):

    # Listas para construir segmentos visibles del terreno
    puntos = []
    segmentos = []
    segmento_actual = []

    # Recorrer todos los puntos del terreno
    for x, y in terrain:

        dentro_puente = False

        # Detectar si el punto pertenece a un puente
        for puente in PUENTES:

            if puente["inicio"] <= x <= puente["fin"]:

                dentro_puente = True
                break

        pantalla_x = x - cam_x

        # Solo procesar puntos visibles
        if -200 <= pantalla_x <= ANCHO + 200:

            # Cortar el terreno donde existan puentes
            if dentro_puente:

                if len(segmento_actual) > 1:

                    segmentos.append(
                        segmento_actual
                    )

                segmento_actual = []

            else:

                segmento_actual.append(
                    (pantalla_x, y)
                )

    # Guardar último segmento válido
    if len(segmento_actual) > 1:

        segmentos.append(
            segmento_actual
        )

    # Dibujar cada segmento del terreno
    for segmento in segmentos:

        poligono = segmento[:]

        poligono.append(
            (
                segmento[-1][0],
                ALTO
            )
        )

        poligono.append(
            (
                segmento[0][0],
                ALTO
            )
        )

        pygame.draw.polygon(
            pantalla,
            color_terreno,
            poligono
        )


# ---------------- DIBUJAR NUBES ----------------

def dibujar_nubes(
    pantalla,
    cam_x
):

    # Recorrer todas las nubes generadas
    for x, y, tam in NUBES:

        # Movimiento lento para efecto parallax
        px = x - cam_x * 0.3

        # Dibujar solo las visibles
        if -200 <= px <= ANCHO + 200:

            # Círculo central
            pygame.draw.circle(
                pantalla,
                BLANCO,
                (int(px), int(y)),
                tam
            )

            # Lado derecho
            pygame.draw.circle(
                pantalla,
                BLANCO,
                (int(px + tam * 0.8), int(y)),
                int(tam * 0.8)
            )

            # Lado izquierdo
            pygame.draw.circle(
                pantalla,
                BLANCO,
                (int(px - tam * 0.8), int(y)),
                int(tam * 0.8)
            )