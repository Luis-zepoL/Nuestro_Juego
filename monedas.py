import pygame
import random
import math
from config import *
from terreno import get_ground

# --- CONFIG ---
DISTANCIA_MONEDAS = 2500
MAX_MONEDAS = 20 
MAX_GASOLINAS = 3 

# --- GENERACIÓN Y ACTUALIZACIÓN ---
def generar_monedas(terrain):
    coins = []
    x_actual = 600
    while x_actual < DISTANCIA_MONEDAS:
        agregar_moneda(coins, x_actual, terrain)
        x_actual += random.randint(300, 600) 
    return coins

def generar_gasolinas(terrain):
    gasolinas = []
    x_actual = 1200
    while x_actual < DISTANCIA_MONEDAS * 2:
        agregar_gasolina(gasolinas, x_actual, terrain)
        x_actual += random.randint(1500, 3000) 
    return gasolinas

def agregar_moneda(coins, x, terrain):
    suelo = get_ground(x, terrain)
    y = suelo - random.randint(80, 140)
    coins.append([x, y])

def agregar_gasolina(gasolinas, x, terrain):
    suelo = get_ground(x, terrain)
    y = suelo - 60
    gasolinas.append([x, y])

def actualizar_monedas(coins, auto, terrain):
    coins[:] = [m for m in coins if m[0] > auto.x - 600]
    while len(coins) < MAX_MONEDAS:
        ultimo_x = coins[-1][0] if coins else auto.x + 400
        agregar_moneda(coins, ultimo_x + random.randint(300, 600), terrain)

def actualizar_gasolinas(gasolinas, auto, terrain):
    gasolinas[:] = [g for g in gasolinas if g[0] > auto.x - 600]
    while len(gasolinas) < MAX_GASOLINAS:
        ultimo_x = gasolinas[-1][0] if gasolinas else auto.x + 1000
        agregar_gasolina(gasolinas, ultimo_x + random.randint(1500, 3000), terrain)

# --- RECOLECCIÓN Y DIBUJO ---
def recolectar_monedas(auto, coins):
    coins[:] = [c for c in coins if math.hypot(auto.x - c[0], auto.y - c[1]) >= 45]

def recolectar_gasolinas(auto, gasolinas):
    nuevas = []
    for gx, gy in gasolinas:
        if math.hypot(auto.x - gx, auto.y - gy) < 50:
            auto.fuel = min(100, auto.fuel + 40)
        else:
            nuevas.append([gx, gy])
    gasolinas[:] = nuevas

def dibujar_monedas(pantalla, coins, cam_x):
    for mx, my in coins:
        pantalla_x = mx - cam_x
        if -50 <= pantalla_x <= ANCHO + 50:
            pygame.draw.circle(pantalla, (180, 140, 0), (int(pantalla_x), int(my)), 12)
            
            pygame.draw.circle(pantalla, (255, 215, 0), (int(pantalla_x), int(my)), 10)
            
            pygame.draw.circle(pantalla, (255, 235, 100), (int(pantalla_x) - 3, int(my) - 3), 6)
            
            pygame.draw.circle(pantalla, (200, 160, 0), (int(pantalla_x), int(my)), 10, 2)

def dibujar_gasolinas(pantalla, gasolinas, cam_x):
    for gx, gy in gasolinas:
        pantalla_x = gx - cam_x
        if -50 <= pantalla_x <= ANCHO + 50:
            rect_cuerpo = pygame.Rect(int(pantalla_x) - 14, int(gy) - 16, 28, 34)
            pygame.draw.rect(pantalla, (160, 20, 20), rect_cuerpo.inflate(4, 4), border_radius=6) # Sombra
            pygame.draw.rect(pantalla, (220, 40, 40), rect_cuerpo, border_radius=5) # Color base
            
            pygame.draw.rect(pantalla, (180, 30, 30), (int(pantalla_x) - 7, int(gy) - 24, 14, 8), border_radius=3)
            
            pygame.draw.rect(pantalla, (255, 255, 255), (int(pantalla_x) - 5, int(gy) - 8, 10, 6), border_radius=2)
            
            pygame.draw.line(pantalla, (255, 255, 255), (int(pantalla_x) - 6, int(gy) + 4), (int(pantalla_x) + 6, int(gy) + 4), 2)

def dibujar_ui_monedas(pantalla, auto):
    fuente = pygame.font.SysFont("Arial", 28, bold=True)
    texto_render = fuente.render(str(auto.monedas), True, BLANCO)
    pantalla.blit(texto_render, (70, 146))
    pygame.draw.circle(pantalla, AMARILLO, (41, 163), 15)