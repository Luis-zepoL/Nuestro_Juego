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
    opcion,
    animacion,
    vehiculo,
    color_vehiculo
):

    # Fondo degradado
    for y in range(ALTO):

        color = (
            10,
            20,
            min(255, 40 + y // 4)
        )

        pygame.draw.line(
            pantalla,
            color,
            (0, y),
            (ANCHO, y)
        )




    for i in range(60):

        x = (i * 137) % ANCHO

        y = (i * 91) % ALTO

        brillo = 180 + int(
         75 * math.sin(
            animacion * 0.05 + i
         )
    )

        pygame.draw.circle(
            pantalla,
            (
                brillo,
                brillo,
                brillo
            ),
            (x, y),
            2
        )

    # Oscurecer
    sombra = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    sombra.fill((0, 0, 0, 120))

    pantalla.blit(sombra, (0, 0))

    # Sombra del título
    titulo_sombra = fuente_grande.render(
        "HILL CLIMB FAKE",
        True,
        NEGRO
    )

    pantalla.blit(
        titulo_sombra,
        (
            ANCHO // 2
            - titulo_sombra.get_width() // 2 + 4,
            104
        )
    )

    # Título
    titulo = fuente_grande.render(
        "HILL CLIMB FAKE",
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2
            - titulo.get_width() // 2,
            100
        )
    )

    # Animación del vehículo
    auto_y = 180 + math.sin(
        animacion * 0.08
    ) * 10

    if vehiculo == "Auto":

        pygame.draw.rect(
            pantalla,
            color_vehiculo,
            (
                ANCHO // 2 - 70,
                auto_y,
                140,
                40
            ),
            border_radius=10
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (
                ANCHO // 2 - 40,
                int(auto_y + 45)
            ),
            18
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (
                ANCHO // 2 + 40,
                int(auto_y + 45)
            ),
            18
        )

    else:

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (
                ANCHO // 2 - 40,
                int(auto_y + 35)
            ),
            18
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (
                ANCHO // 2 + 40,
                int(auto_y + 35)
            ),
            18
        )

        pygame.draw.line(
            pantalla,
            color_vehiculo,
            (
                ANCHO // 2 - 20,
                int(auto_y)
            ),
            (
                ANCHO // 2 + 20,
                int(auto_y)
            ),
            8
        )

        pygame.draw.line(
            pantalla,
            color_vehiculo,
            (
                ANCHO // 2,
                int(auto_y)
            ),
            (
                ANCHO // 2 + 30,
                int(auto_y - 20)
            ),
            5
        )

    # Caja principal
    pygame.draw.rect(
        pantalla,
        (
            100,
            140,
            200 + int(55 * math.sin(animacion * 0.05))
        ),
        (
            ANCHO // 2 - 220,
            230,
            440,
            310
        ),
        border_radius=20
    )

    opciones = [
        "Jugar",
        "Seleccionar mapa",
        "Taller",
        "Salir"
    ]

    for i, texto_opcion in enumerate(opciones):

        color = BLANCO

        if i == opcion:

            pygame.draw.rect(
                pantalla,
                (70, 120, 255),
                (
                    ANCHO // 2 - 200,
                    255 + i * 60,
                    400,
                    45
                ),
                border_radius=10
            )

            color = AMARILLO

            flecha = fuente.render(
                ">",
                True,
                BLANCO
            )

            pantalla.blit(
                flecha,
                (
                    ANCHO // 2 - 170,
                    260 + i * 60
                )
            )

        texto = fuente.render(
            texto_opcion,
            True,
            color
        )

        pantalla.blit(
            texto,
            (
                ANCHO // 2
                - texto.get_width() // 2,
                260 + i * 60
            )
        )

    ayuda = fuente_pequena.render(
        "↑↓ para navegar",
        True,
        BLANCO
    )

    pantalla.blit(
        ayuda,
        (
            ANCHO // 2
            - ayuda.get_width() // 2,
            520
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

    s.fill((0, 0, 0, 170))

    pantalla.blit(s, (0, 0))

    titulo = fuente_grande.render(
        "SELECCIONAR MAPA",
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2
            - titulo.get_width() // 2,
            80
        )
    )

    for i, mapa in enumerate(mapas):

        y = 220 + i * 120

        color_borde = BLANCO

        if i == seleccion:
            color_borde = AMARILLO

        pygame.draw.rect(
            pantalla,
            (30, 30, 45),
            (
                ANCHO // 2 - 220,
                y,
                440,
                90
            ),
            border_radius=15
        )

        pygame.draw.rect(
            pantalla,
            color_borde,
            (
                ANCHO // 2 - 220,
                y,
                440,
                90
            ),
            3,
            border_radius=15
        )

        nombre = fuente.render(
            mapa,
            True,
            BLANCO
        )

        pantalla.blit(
            nombre,
            (
                ANCHO // 2
                - nombre.get_width() // 2,
                y + 15
            )
        )

        descripcion = ""

        if mapa == "Pradera":
            descripcion = "Colinas verdes"

        elif mapa == "Desierto":
            descripcion = "Arena y dunas"

        texto_desc = fuente_pequena.render(
            descripcion,
            True,
            (200, 200, 200)
        )

        pantalla.blit(
            texto_desc,
            (
                ANCHO // 2
                - texto_desc.get_width() // 2,
                y + 50
            )
        )

        pygame.draw.rect(
            pantalla,
            (20, 20, 30),
            (
                40,
                180,
                250,
                180
            ),
            border_radius=15
        )

        if mapas[seleccion] == "Pradera":

            pygame.draw.rect(
                pantalla,
                (135, 206, 235),
                (
                    50,
                    190,
                    230,
                    160
                ),
                border_radius=10
            )

            pygame.draw.rect(
                pantalla,
                VERDE,
                (
                    50,
                    290,
                    230,
                    60
                ),
                border_radius=10
            )

        else:

            pygame.draw.rect(
                pantalla,
                (255, 210, 120),
                (
                    50,
                    190,
                    230,
                    160
                ),
                border_radius=10
            )

            pygame.draw.rect(
                pantalla,
                (194, 178, 128),
                (
                    50,
                    290,
                    230,
                    60
                ),
                border_radius=10
            )

        ayuda = fuente_pequena.render(
            "ENTER confirmar",
            True,
            BLANCO
        )

        pantalla.blit(
            ayuda,
            (
                ANCHO // 2
                - ayuda.get_width() // 2,
                620
            )
        )

# -------------------------cometario faltante

def dibujar_preview_mapa(
    pantalla,
    mapa,
    offset
):
    # 
    if mapa == "Pradera":

        pantalla.fill(
            (135,206,235)
        )

        color_terreno = (
            60,190,70
        )

    else:

        pantalla.fill(
            (255,210,120)
        )

        color_terreno = (
            194,178,128
        )
   
    # ---------------- NUBES ----------------

    preview_nubes = [
        (100, 80),
        (350, 130),
        (600, 90),
        (900, 160),
        (1200, 110),
    ]

    for x, y in preview_nubes:

        nube_x = x - (offset * 3)

        while nube_x < -120:
            nube_x += 1600

        # nube principal
        pygame.draw.circle(
            pantalla,
            BLANCO,
            (int(nube_x), y),
            30
        )

        # lado derecho
        pygame.draw.circle(
            pantalla,
            BLANCO,
            (
                int(nube_x + 25),
                y + 5
            ),
            25
        )

        # lado izquierdo
        pygame.draw.circle(
            pantalla,
            BLANCO,
            (
                int(nube_x - 25),
                y + 5
            ),
            25
        )

        # parte superior
        pygame.draw.circle(
            pantalla,
            BLANCO,
            (
                int(nube_x),
                y - 15
            ),
            22
        )


    puntos = []

    for x in range(-100, ANCHO + 100, 20):

        y = (
            500
            +
            math.sin(
                (x + offset * 30)
                * 0.01
            ) * 60
        )

        puntos.append((x,y))

    

    poligono = puntos[:]

    poligono.append(
        (ANCHO,ALTO)
    )

    poligono.append(
        (0,ALTO)
    )

    pygame.draw.polygon(
        pantalla,
        color_terreno,
        poligono
    )        

#---------------- TALLER ----------------

def dibujar_taller(
    pantalla,
    auto,
    vehiculo,
    color_nombre
):

    pantalla.fill(
        (25,25,35)
    )

    titulo = fuente_grande.render(
        "TALLER",
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO//2
            - titulo.get_width()//2,
            40
        )
    )

    pygame.draw.rect(
        pantalla,
        (45,45,60),
        (
            250,
            120,
            780,
            450
        ),
        border_radius=20
    )

    auto.draw_preview(
        pantalla,
        ANCHO//2,
        350
    )

    txt1 = fuente.render(
        f"Vehiculo: {vehiculo}",
        True,
        BLANCO
    )

    txt2 = fuente.render(
        f"Color: {color_nombre}",
        True,
        BLANCO
    )

    pantalla.blit(
        txt1,
        (430,470)
    )

    pantalla.blit(
        txt2,
        (430,520)
    )

    ayuda = fuente_pequena.render(
        "↑↓ Vehiculo | ←→ Color | ENTER Volver",
        True,
        AMARILLO
    )

    pantalla.blit(
        ayuda,
        (
            ANCHO//2
            - ayuda.get_width()//2,
            620
        )
    )

# ---------------- GAME OVER ----------------

def dibujar_game_over(
    pantalla,
    auto,
    opcion,
    mensaje
):

    sombra = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    sombra.fill((0, 0, 0, 220))

    pantalla.blit(
        sombra,
        (0, 0)
    )

    # Caja principal

    pygame.draw.rect(
        pantalla,
        (30, 30, 45),
        (
            ANCHO // 2 - 280,
            140,
            560,
            340
        ),
        border_radius=20
    )

    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            ANCHO // 2 - 280,
            140,
            560,
            340
        ),
        4,
        border_radius=20
    )

    titulo = fuente_grande.render(
        mensaje,
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2
            - titulo.get_width() // 2,
            190
        )
    )

    score = fuente.render(
        f"Distancia: {int(auto.x/10)} m",
        True,
        BLANCO
    )

    pantalla.blit(
        score,
        (
            ANCHO // 2
            - score.get_width() // 2,
            260
        )
    )

    opciones = [
        "Reiniciar",
        "Volver al menu"
    ]

    for i, texto in enumerate(opciones):

        color = BLANCO

        if i == opcion:

            pygame.draw.rect(
                pantalla,
                (70, 120, 255),
                (
                    ANCHO // 2 - 180,
                    320 + i * 70,
                    360,
                    50
                ),
                border_radius=10
            )

            color = AMARILLO

        render = fuente.render(
            texto,
            True,
            color
        )

        pantalla.blit(
            render,
            (
                ANCHO // 2
                - render.get_width() // 2,
                330 + i * 70
            )
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

