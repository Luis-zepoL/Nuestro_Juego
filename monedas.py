import pygame
import random
import math

from config import *
from terreno import get_ground

# ---------------- CONFIG ----------------

DISTANCIA_MONEDAS = 2500
MAX_MONEDAS = 35

# ---------------- GENERAR INICIAL ----------------

def generar_monedas(terrain):

    coins = []

    x_actual = 600

    while x_actual < DISTANCIA_MONEDAS:

        agregar_moneda(coins, x_actual, terrain)

        x_actual += random.randint(120, 260)

    return coins

# ---------------- AGREGAR MONEDA ----------------

def agregar_moneda(coins, x, terrain):

    suelo = get_ground(x, terrain)

    # Altura relativa al suelo
    offset_y = random.randint(45, 90)

    y = suelo - offset_y

    coins.append([x, y])

# ---------------- ACTUALIZAR ----------------

def actualizar_monedas(coins, auto, terrain):

    # Eliminar monedas muy atrás
    coins[:] = [
        moneda
        for moneda in coins
        if moneda[0] > auto.x - 600
    ]

    # Generar nuevas monedas delante
    while len(coins) < MAX_MONEDAS:

        if len(coins) > 0:
            ultimo_x = coins[-1][0]
        else:
            ultimo_x = auto.x + 400

        nuevo_x = ultimo_x + random.randint(120, 260)

        agregar_moneda(
            coins,
            nuevo_x,
            terrain
        )

# ---------------- RECOLECTAR ----------------

def recolectar_monedas(auto, coins, terrain):

    nuevas = []

    for mx, my in coins:

        if math.hypot(auto.x - mx, auto.y - my) < 45:

            auto.fuel = min(
                100,
                auto.fuel + 12
            )

            continue

        nuevas.append([mx, my])

    coins[:] = nuevas

# ---------------- DIBUJAR ----------------

def dibujar_monedas(pantalla, coins, cam_x, terrain):

    for mx, my in coins:

        pantalla_x = mx - cam_x

        if -50 <= pantalla_x <= ANCHO + 50:

            pygame.draw.circle(
                pantalla,
                AMARILLO,
                (int(pantalla_x), int(my)),
                10
            )

            pygame.draw.circle(
                pantalla,
                (200, 150, 0),
                (int(pantalla_x), int(my)),
                10,
                2
            )