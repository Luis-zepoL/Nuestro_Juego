import pygame
import math

from config import *

pygame.font.init()

fuente = pygame.font.SysFont("Arial", 28)
fuente_grande = pygame.font.SysFont("Arial", 48)
fuente_pequena = pygame.font.SysFont("Arial", 18)

# ---------------- HUD ----------------

def dibujar_hud(pantalla, auto):

    hud = pygame.Surface((240, 120))
    hud.set_alpha(180)
    hud.fill((20, 20, 20))

    pantalla.blit(hud, (10, 10))

    texto_score = fuente.render(
        f"Score: {int(auto.x / 10)}",
        True,
        BLANCO
    )

    texto_fuel = fuente.render(
        f"Fuel: {int(auto.fuel)}",
        True,
        BLANCO
    )

    pantalla.blit(texto_score, (20, 20))
    pantalla.blit(texto_fuel, (20, 55))

    # Barra fuel fondo
    pygame.draw.rect(
        pantalla,
        ROJO,
        (20, 90, 200, 20),
        border_radius=5
    )

    # Barra fuel
    pygame.draw.rect(
        pantalla,
        VERDE,
        (20, 90, auto.fuel * 2, 20),
        border_radius=5
    )

# ---------------- MENU ----------------

def dibujar_menu(
    pantalla,
    opcion
):

    s = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    s.fill((0, 0, 0, 190))

    pantalla.blit(s, (0, 0))

    titulo = fuente_grande.render(
        "PROTOTIPO DE JUEGO",
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2 - titulo.get_width() // 2,
            120
        )
    )

    opciones = [
        "Jugar",
        "Seleccionar mapa",
        "Salir"
    ]

    for i, texto_opcion in enumerate(opciones):

        color = BLANCO

        if i == opcion:
            color = AMARILLO

        texto = fuente.render(
            texto_opcion,
            True,
            color
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                260 + i * 60
            )
        )
# ------------ selector de mapa ----------------
def dibujar_selector_mapa(
    pantalla,
    mapas,
    seleccion
):

    s = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    s.fill((0, 0, 0, 190))

    pantalla.blit(s, (0, 0))

    titulo = fuente_grande.render(
        "SELECCIONAR MAPA",
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2 - titulo.get_width() // 2,
            120
        )
    )

    for i, mapa in enumerate(mapas):

        color = BLANCO

        if i == seleccion:
            color = AMARILLO

        texto = fuente.render(
            mapa,
            True,
            color
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2 - texto.get_width() // 2,
                260 + i * 60
            )
        )

    ayuda = fuente_pequena.render(
        "ENTER para elegir",
        True,
        BLANCO
    )

    pantalla.blit(
        ayuda,
        (
            ANCHO // 2 - ayuda.get_width() // 2,
            500
        )
    )

# ---------------- GAME OVER ----------------

def dibujar_game_over(pantalla, auto):

    s = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    s.fill((0, 0, 0, 210))

    pantalla.blit(s, (0, 0))

    texto = fuente_grande.render(
        "GAME OVER",
        True,
        ROJO
    )

    pantalla.blit(
        texto,
        (ANCHO // 2 - texto.get_width() // 2, 180)
    )

    score = fuente.render(
        f"Distancia: {int(auto.x / 10)} m",
        True,
        BLANCO
    )

    pantalla.blit(
        score,
        (ANCHO // 2 - score.get_width() // 2, 300)
    )

    reiniciar = fuente.render(
        "Presiona R para reiniciar",
        True,
        AMARILLO
    )

    pantalla.blit(
        reiniciar,
        (ANCHO // 2 - reiniciar.get_width() // 2, 420)
    )

# ---------------- VELOCIMETRO ----------------

def dibujar_velocimetro(pantalla, velocidad):

    cx = ANCHO - 130
    cy = ALTO - 130

    radio = 90

    # Fondo
    pygame.draw.circle(
        pantalla,
        (20, 20, 20),
        (cx, cy),
        radio
    )

    pygame.draw.circle(
        pantalla,
        BLANCO,
        (cx, cy),
        radio,
        3
    )

    # Marcas
    for i in range(0, 220, 10):

        ang = math.radians(135 + i)

        x1 = cx + (radio - 15) * math.cos(ang)
        y1 = cy + (radio - 15) * math.sin(ang)

        x2 = cx + (radio - 2) * math.cos(ang)
        y2 = cy + (radio - 2) * math.sin(ang)

        color = BLANCO

        if i > 150:
            color = ROJO

        elif i > 80:
            color = AMARILLO

        pygame.draw.line(
            pantalla,
            color,
            (x1, y1),
            (x2, y2),
            3
        )

    # Números
    valores = [
        (0, 135),
        (60, 190),
        (120, 245),
        (180, 300)
    ]

    for valor, angulo in valores:

        ang = math.radians(angulo)

        tx = cx + (radio - 35) * math.cos(ang)
        ty = cy + (radio - 35) * math.sin(ang)

        texto = fuente_pequena.render(
            str(valor),
            True,
            BLANCO
        )

        pantalla.blit(
            texto,
            (tx - 10, ty - 10)
        )

    # Aguja
    velocidad = min(180, velocidad)

    angulo_aguja = math.radians(
        135 + velocidad * 1.1
    )

    px = cx + (radio - 25) * math.cos(angulo_aguja)
    py = cy + (radio - 25) * math.sin(angulo_aguja)

    pygame.draw.line(
        pantalla,
        ROJO,
        (cx, cy),
        (px, py),
        5
    )

    pygame.draw.circle(
        pantalla,
        BLANCO,
        (cx, cy),
        8
    )

    # Texto digital
    texto_vel = fuente.render(
        f"{int(velocidad)} km/h",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_vel,
        (cx - 50, cy + 45)
    )