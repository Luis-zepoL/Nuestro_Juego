import math
import pygame
import random

from config import *

# ---------------- CONFIG TERRENO ----------------

ESPACIADO = 20

DISTANCIA_RENDER = 4000
DISTANCIA_ELIMINAR = 1000

altura_base = 520

AUTO_X_GLOBAL = 0

def generar_control_points():

    global PUNTOS_CONTROL

    PUNTOS_CONTROL = []

    x = -3000

    while x < 200000:

        y = random.randint(
            250,
            600
        )

        PUNTOS_CONTROL.append(
            (x, y)
        )

        x += random.randint(
            600,
            1800
        )

def generar_puentes():

    global PUENTES

    PUENTES = []

    x = 6000

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

SEMILLA = 0

PUNTOS_CONTROL = []
PUENTES = []

CACTUS = []
NUBES = []

def smoothstep(t):

    return t * t * (3 - 2 * t)

# ---------------- GENERAR INICIAL ----------------

def generar_terreno():

    terrain = []

    for x in range(
        -2000,
        DISTANCIA_RENDER,
        ESPACIADO
    ):

        y = generar_altura(x)

        terrain.append((x, y))

    return terrain

#---------------- GENERAR NUBES ----------------

def generar_nubes():

    global NUBES

    NUBES = []

    for i in range(50):

        NUBES.append(
            (
                i * 600,
                60 + (i * 37) % 180,
                50 + (i * 17) % 40
            )
        )

#---------------- GENERAR CACTUS ----------------

def generar_cactus():

    global CACTUS

    CACTUS = []

    x = 1000

    while x < 100000:

        dentro_puente = False

        for puente in PUENTES:

            if puente["inicio"] - 100 <= x <= puente["fin"] + 100:

                dentro_puente = True
                break

        if not dentro_puente:

            CACTUS.append(x)

        x += random.randint(
            500,
            1500
        )

#---------------- DIBUJAR CACTUS ----------------

def dibujar_cactus(
    pantalla,
    cam_x,
    terrain
):

    for x in CACTUS:

        px = x - cam_x

        if -100 <= px <= ANCHO + 100:

            suelo = get_ground(
                x,
                terrain
            )

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

# ---------------- ALTURA ----------------

def generar_altura(x):

    for i in range(
        len(PUNTOS_CONTROL) - 1
    ):

        x1, y1 = PUNTOS_CONTROL[i]
        x2, y2 = PUNTOS_CONTROL[i + 1]

        if x1 <= x <= x2:

            t = (
                (x - x1)
                /
                (x2 - x1)
            )

            t = smoothstep(t)

            return (
                y1 * (1 - t)
                +
                y2 * t
            )

    return altura_base

# ---------------- EXPANDIR TERRENO ----------------

def actualizar_terreno(terrain, jugador_x):

    ultimo_x = terrain[-1][0]

    # Generar hacia adelante
    while ultimo_x < jugador_x + DISTANCIA_RENDER:

        ultimo_x += ESPACIADO

        terrain.append(
            (
                ultimo_x,
                generar_altura(ultimo_x)
            )
        )

    # Eliminar puntos viejos
    #while len(terrain) > 2 and terrain[1][0] < jugador_x - DISTANCIA_ELIMINAR:

    #    terrain.pop(0)

# ---------------- GROUND ----------------

def get_ground(x, terrain):

    # Si está antes del terreno
    if x <= terrain[0][0]:
        return terrain[0][1]

    # Si está después del terreno
    if x >= terrain[-1][0]:
        return terrain[-1][1]

    # Buscar segmento correcto
    for i in range(len(terrain) - 1):

        x1, y1 = terrain[i]
        x2, y2 = terrain[i + 1]

        if x1 <= x <= x2:

            t = (x - x1) / (x2 - x1)

            altura = y1 * (1 - t) + y2 * t

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

                    t = distancia / (largo / 2)

                    factor = math.cos(
                        t * math.pi / 2
                    )

                    factor = max(0, factor)

                    altura += (
                        factor ** 2
                    ) * puente["profundidad"]

                    altura += deformacion_puente(
                        x,
                        AUTO_X_GLOBAL
                    )

            return altura
    # Seguridad extra
    return terrain[-1][1]

# ---------------- DIBUJAR PUENTES ----------------

def dibujar_puentes(
    pantalla,
    cam_x,
    terrain
):

    for puente in PUENTES:

        puntos = []

        x = puente["inicio"]

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

            # =====================
            # TABLONES DEL PUENTE
            # =====================

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

            # =====================
            # EXTREMOS DEL PUENTE
            # =====================

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

            # =====================
            # POSTES
            # =====================

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

            # =====================
            # CABLE SUPERIOR
            # =====================

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

            # =====================
            # TENSORES
            # =====================

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
# ---------------- DEFORMACION PUENTE ----------------

def deformacion_puente(x, auto_x):

    for puente in PUENTES:

        if puente["inicio"] <= x <= puente["fin"]:

            if puente["inicio"] <= auto_x <= puente["fin"]:

                distancia = abs(x - auto_x)

                if distancia < 140:

                    influencia_auto = (
                        1 - distancia / 140
                    )

                    largo = (
                        puente["fin"]
                        - puente["inicio"]
                    )

                    posicion = (
                        x - puente["inicio"]
                    ) / largo

                    # extremos totalmente fijos
                    anclaje = math.sin(
                        posicion * math.pi
                    )

                    # endurecer extremos
                    anclaje = anclaje ** 1.5

                    return (
                        influencia_auto
                        * anclaje
                        * 25
                    )

    return 0
#-------- GROUND SIN DEFORMACION PARA PUENTE -----------

def get_ground_sin_deformacion(x, terrain):

    if x <= terrain[0][0]:
        return terrain[0][1]

    if x >= terrain[-1][0]:
        return terrain[-1][1]

    for i in range(len(terrain)-1):

        x1, y1 = terrain[i]
        x2, y2 = terrain[i+1]

        if x1 <= x <= x2:

            t = (x - x1)/(x2 - x1)

            altura = y1*(1-t) + y2*t

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

# ---------------- PENDIENTE ----------------

def get_slope(x, terrain):

    y1 = get_ground(x - 5, terrain)
    y2 = get_ground(x + 5, terrain)

    return math.atan2(y2 - y1, 10)

# ---------------- DIBUJO ----------------

def dibujar_terreno(pantalla, terrain, cam_x, color_terreno):

    puntos = []
    segmentos = []
    segmento_actual = []

    for x, y in terrain:

        dentro_puente = False

        for puente in PUENTES:

            if puente["inicio"] <= x <= puente["fin"]:

                dentro_puente = True
                break

        pantalla_x = x - cam_x

        if -200 <= pantalla_x <= ANCHO + 200:

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

    if len(segmento_actual) > 1:

        segmentos.append(
            segmento_actual
        )

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

    for x, y, tam in NUBES:

        px = x - cam_x * 0.3

        if -200 <= px <= ANCHO + 200:

            pygame.draw.circle(
                pantalla,
                BLANCO,
                (int(px), int(y)),
                tam
            )

            pygame.draw.circle(
                pantalla,
                BLANCO,
                (int(px + tam * 0.8), int(y)),
                int(tam * 0.8)
            )

            pygame.draw.circle(
                pantalla,
                BLANCO,
                (int(px - tam * 0.8), int(y)),
                int(tam * 0.8)
            )