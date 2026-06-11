import pygame
import random
import math

from config import *
from terreno import get_ground

# ---------------- CONFIG ----------------

DISTANCIA_MONEDAS = 2500
MAX_MONEDAS = 35

MAX_GASOLINAS = 4

# ---------------- GENERAR INICIAL ----------------

def generar_monedas(terrain):
    coins = []
    x_actual = 600
    while x_actual < DISTANCIA_MONEDAS:
        agregar_moneda(coins, x_actual, terrain)
        x_actual += random.randint(120, 260)
    return coins

def generar_gasolinas(terrain):
    gasolinas = []
    x_actual = 1200
    while x_actual < DISTANCIA_MONEDAS * 2:
        agregar_gasolina(gasolinas, x_actual, terrain)
        x_actual += random.randint(800, 1600)
    return gasolinas

# ---------------- AGREGAR OBJETOS ----------------

def agregar_moneda(coins, x, terrain):
    suelo = get_ground(x, terrain)
    
    offset_y = random.randint(80, 140) 
    y = suelo - offset_y
    coins.append([x, y])

def agregar_gasolina(gasolinas, x, terrain):
    suelo = get_ground(x, terrain)
    
    offset_y = 60 
    y = suelo - offset_y
    gasolinas.append([x, y])

# ---------------- ACTUALIZAR ----------------

def actualizar_monedas(coins, auto, terrain):
    
    coins[:] = [
        moneda for moneda in coins
        if moneda[0] > auto.x - 600
    ]

    
    while len(coins) < MAX_MONEDAS:
        if len(coins) > 0:
            ultimo_x = coins[-1][0]
        else:
            ultimo_x = auto.x + 400

        nuevo_x = ultimo_x + random.randint(120, 260)
        agregar_moneda(coins, nuevo_x, terrain)


def actualizar_gasolinas(gasolinas, auto, terrain):
    
    gasolinas[:] = [
        gas for gas in gasolinas
        if gas[0] > auto.x - 600
    ]

    
    while len(gasolinas) < MAX_GASOLINAS:
        if len(gasolinas) > 0:
            ultimo_x = gasolinas[-1][0]
        else:
            ultimo_x = auto.x + 1000

        nuevo_x = ultimo_x + random.randint(800, 1600)
        agregar_gasolina(gasolinas, nuevo_x, terrain)

# ---------------- RECOLECTAR ----------------

def recolectar_monedas(auto, coins):
    nuevas = []
    for mx, my in coins:
        if math.hypot(auto.x - mx, auto.y - my) < 45:
            
            auto.monedas += 1
            continue

        nuevas.append([mx, my])

    coins[:] = nuevas

def recolectar_gasolinas(auto, gasolinas):
    nuevas = []
    for gx, gy in gasolinas:
        if math.hypot(auto.x - gx, auto.y - gy) < 50:
            
            auto.fuel = min(100, auto.fuel + 40)
            continue
            
        nuevas.append([gx, gy])

    gasolinas[:] = nuevas

# ---------------- DIBUJAR EN EL MAPA ----------------

def dibujar_monedas(pantalla, coins, cam_x):
    for mx, my in coins:
        pantalla_x = mx - cam_x
        if -50 <= pantalla_x <= ANCHO + 50:
            pygame.draw.circle(
                pantalla,
                AMARILLO, "Poner amarillo en config"
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

def dibujar_gasolinas(pantalla, gasolinas, cam_x):
    for gx, gy in gasolinas:
        pantalla_x = gx - cam_x
        if -50 <= pantalla_x <= ANCHO + 50:
            
            
            rect_bidon = pygame.Rect(int(pantalla_x) - 12, int(gy) - 15, 24, 30)
            pygame.draw.rect(pantalla, (220, 40, 40), rect_bidon, border_radius=4)
            
            
            pygame.draw.rect(pantalla, (150, 20, 20), (int(pantalla_x) - 6, int(gy) - 22, 12, 7), 3, border_radius=2)
            
            
            pygame.draw.rect(pantalla, (255, 255, 255), (int(pantalla_x) - 6, int(gy) - 5, 12, 10), border_radius=2)

# ---------------- DIBUJAR UI (CONTADOR EN PANTALLA) ----------------

def dibujar_ui_monedas(pantalla, auto):
    
    fuente = pygame.font.SysFont("Arial", 28, bold=True)
    texto = f"{auto.monedas}"
    texto_render = fuente.render(texto, True, BLANCO) 
    
    
    ancho_texto = texto_render.get_width()
    ancho_caja = ancho_texto + 75  
    alto_caja = 46
    
    
    x_caja = 15
    y_caja = 140
    
    
    caja_surface = pygame.Surface((ancho_caja, alto_caja), pygame.SRCALPHA)
    pygame.draw.rect(
        caja_surface, 
        (0, 0, 0, 160), 
        (0, 0, ancho_caja, alto_caja), 
        border_radius=23
    )
    pantalla.blit(caja_surface, (x_caja, y_caja))
    
    
    centro_moneda_x = x_caja + 26
    centro_moneda_y = y_caja + alto_caja // 2
    
    pygame.draw.circle(pantalla, AMARILLO, (centro_moneda_x, centro_moneda_y), 15)
    
    pygame.draw.circle(pantalla, (200, 150, 0), (centro_moneda_x, centro_moneda_y), 15, 2)
    
    pygame.draw.circle(pantalla, (255, 240, 100), (centro_moneda_x, centro_moneda_y), 7) 
    
    
    pantalla.blit(texto_render, (x_caja + 52, y_caja + 6))