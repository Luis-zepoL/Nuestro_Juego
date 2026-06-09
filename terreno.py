import math
import pygame

from config import *

# ---------------- CONFIG TERRENO ----------------

ESPACIADO = 20

DISTANCIA_RENDER = 4000
DISTANCIA_ELIMINAR = 1000

altura_base = 520

# ---------------- GENERAR INICIAL ----------------

def generar_terreno():

    terrain = []

    for x in range(0, DISTANCIA_RENDER, ESPACIADO):

        y = generar_altura(x)

        terrain.append((x, y))

    return terrain

# ---------------- ALTURA ----------------

def generar_altura(x):

    y = (
    altura_base
    + math.sin(x * 0.0025) * 90
    + math.sin(x * 0.006) * 35
    + math.sin(x * 0.012) * 15
    )

    # ---------------- LIMITES ----------------

    ALTURA_MINIMA = 250
    ALTURA_MAXIMA = 620

    y = max(ALTURA_MINIMA, min(ALTURA_MAXIMA, y))

    return y

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
    while len(terrain) > 2 and terrain[1][0] < jugador_x - DISTANCIA_ELIMINAR:

        terrain.pop(0)

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

            return y1 * (1 - t) + y2 * t

    # Seguridad extra
    return terrain[-1][1]

# ---------------- PENDIENTE ----------------

def get_slope(x, terrain):

    y1 = get_ground(x - 5, terrain)
    y2 = get_ground(x + 5, terrain)

    return math.atan2(y2 - y1, 10)

# ---------------- DIBUJO ----------------

def dibujar_terreno(pantalla, terrain, cam_x):

    puntos = []

    for x, y in terrain:

        pantalla_x = x - cam_x

        if -200 <= pantalla_x <= ANCHO + 200:

            puntos.append((pantalla_x, y))

    # Seguridad
    if len(puntos) < 2:
        return

    # Cerrar polígono correctamente
    puntos.append((puntos[-1][0], ALTO))
    puntos.append((puntos[0][0], ALTO))

    pygame.draw.polygon(
        pantalla,
        VERDE,
        puntos
    )