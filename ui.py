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
    color_vehiculo,
    monedas,
    distancia
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

    # PANEL RECORDS

    pygame.draw.rect(
        pantalla,
        (20,20,20),
        (
            20,
            20,
            300,
            150
        ),
        border_radius=15
    )

    # Moneda grande
    pygame.draw.circle(
        pantalla,
        (180,140,0),
        (55,55),
        18
    )

    pygame.draw.circle(
        pantalla,
        (255,215,0),
        (55,55),
        15
    )

    pygame.draw.circle(
        pantalla,
        (255,235,100),
        (50,50),
        8
    )

    pygame.draw.circle(
        pantalla,
        (200,160,0),
        (55,55),
        15,
        2
    )

    texto1 = fuente.render(
        str(monedas),
        True,
        AMARILLO
    )

    texto2 = fuente.render(
        f"Mayor distancia ",
        True,
        BLANCO
    )

    texto3 = fuente.render(
        f"{distancia} m",
        True,
        BLANCO
    )

    pantalla.blit(
        texto1,
        (85,40)
    )

    pantalla.blit(
        texto2,
        (40,80)
    )

    pantalla.blit(
        texto3,
        (40,120)
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

    # Caja principal (rectangulo del menu)
    pygame.draw.rect(
        pantalla,
        (
            100,
            140,
            200 + int(55 * math.sin(animacion * 0.05))
        ),
        (
            ANCHO // 2 - 260,
            220,
            520,
            420
        ),
        border_radius=25
    )

    opciones = [
        "Jugar",
        "Seleccionar mapa",
        "Taller",
        "Tienda",
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
        "↑↓ para navegar / ENTER para seleccionar",
        True,
        BLANCO
    )

    pygame.draw.rect(
        pantalla,
        (20,20,20),
        (
            ANCHO//2 - 220,
            645,
            440,
            45
        ),
        border_radius=10
    )

    pantalla.blit(
        ayuda,
        (
            ANCHO//2
            - ayuda.get_width()//2,
            655
        )
    )

# ------------ selector de mapa ----------------

def dibujar_selector_mapa(
    pantalla,
    mapas,
    seleccion,
    desbloqueado
):

    s = pygame.Surface(
        (ANCHO, ALTO),
        pygame.SRCALPHA
    )

    s.fill((0, 0, 0, 170))

    pantalla.blit(s, (0, 0))

    dibujar_boton_salir(
        pantalla
    )
    
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
    
    #ASAaaaaaaaaa
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

    # Mostrar bloqueo dentro del preview
    if (
        mapas[seleccion] == "Desierto"
        and
        not desbloqueado
    ):

        sombra = pygame.Surface(
            (230,160),
            pygame.SRCALPHA
        )

        sombra.fill((0,0,0,170))

        pantalla.blit(
            sombra,
            (50,190)
        )

        txt = fuente.render(
            "BLOQUEADO",
            True,
            ROJO
        )

        pantalla.blit(
            txt,
            (
                165 - txt.get_width()//2,
                240
            )
        )

        txt2 = fuente_pequena.render(
            "Compra en Tienda",
            True,
            BLANCO
        )

        pantalla.blit(
            txt2,
            (
                165 - txt2.get_width()//2,
                280
            )
        )

# ---------------- PREVIEW MAPA ----------------

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

    # ---------- BLOQUEO DEL DESIERTO ----------

    if (
        mapas[seleccion] == "Desierto"
        and
        not desbloqueado
    ):

        sombra = pygame.Surface(
            (230,160),
            pygame.SRCALPHA
        )

        sombra.fill((0,0,0,180))

        pantalla.blit(
            sombra,
            (50,190)
        )

        txt = fuente.render(
            "BLOQUEADO",
            True,
            (255,80,80)
        )

        pantalla.blit(
            txt,
            (
                165 - txt.get_width()//2,
                235
            )
        )

        txt2 = fuente_pequena.render(
            "Compra en Tienda",
            True,
            BLANCO
        )

        pantalla.blit(
            txt2,
            (
                165 - txt2.get_width()//2,
                275
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
    color_nombre,
    moto_desbloqueada
):

    pantalla.fill(
        (25,25,35)
    )

    dibujar_boton_salir(
        pantalla
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

    if vehiculo == "Auto":

        pygame.draw.rect(
            pantalla,
            auto.color,
            (
                ANCHO//2 - 70,
                300,
                140,
                40
            ),
            border_radius=10
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (ANCHO//2 - 40, 350),
            18
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (ANCHO//2 + 40, 350),
            18
        )

    else:

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (ANCHO//2 - 50, 350),
            18
        )

        pygame.draw.circle(
            pantalla,
            NEGRO,
            (ANCHO//2 + 50, 350),
            18
        )

        pygame.draw.line(
            pantalla,
            auto.color,
            (ANCHO//2 - 50, 350),
            (ANCHO//2, 320),
            5
        )

        pygame.draw.line(
            pantalla,
            auto.color,
            (ANCHO//2, 320),
            (ANCHO//2 + 50, 350),
            5
        )

        pygame.draw.line(
            pantalla,
            auto.color,
            (ANCHO//2, 320),
            (ANCHO//2 + 25, 290),
            5
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

    if vehiculo == "Moto" and not moto_desbloqueada:

        bloqueado = fuente.render(
            "NO COMPRADA",
            True,
            (255,80,80)
        )

        pantalla.blit(
            bloqueado,
            (
                ANCHO//2
                - bloqueado.get_width()//2,
                560
            )
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
    mensaje,
    record_dist, 
    record_mon
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

    pygame.draw.rect(
        pantalla,
        (30, 30, 45),
        (
            ANCHO // 2 - 280,
            110,
            560,
            440
        ),
        border_radius=20
    )

    pygame.draw.rect(
        pantalla,
        ROJO,
        (
            ANCHO // 2 - 280,
            110,
            560,
            440
        ),
        4,
        border_radius=20
    )

    # --- TÍTULO (MENSAJE) ---
    titulo = fuente_grande.render(
        mensaje,
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2 - titulo.get_width() // 2,
            140
        )
    )

    # --- PUNTUACIÓN DE LA PARTIDA ACTUAL ---
    score_dist = fuente.render(
        f"Distancia: {int(auto.x/10)} m",
        True,
        BLANCO
    )
    pantalla.blit(
        score_dist,
        (
            ANCHO // 2 - score_dist.get_width() // 2,
            300
        )
    )

    score_monedas = fuente.render(
        f"Monedas: {auto.monedas}",
        True,
        AMARILLO
    )
    pantalla.blit(
        score_monedas,
        (
            ANCHO // 2 - score_monedas.get_width() // 2,
            250
        )
    )

    # --- BOTONES ---
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
                    380 + i * 70,
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
                ANCHO // 2 - render.get_width() // 2,
                390 + i * 70
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

# dibujar tienda

def dibujar_tienda(
    pantalla,
    monedas,
    distancia,
    seleccion,
    moto_comprada,
    desierto_comprado
):

    pantalla.fill((20,25,40))

    dibujar_boton_salir(
        pantalla
    )

    titulo = fuente_grande.render(
        "TIENDA",
        True,
        AMARILLO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO//2 - titulo.get_width()//2,
            40
        )
    )

    txt = fuente.render(
        f"Monedas: {monedas}",
        True,
        BLANCO
    )

    pantalla.blit(txt,(40,120))

    txt2 = fuente.render(
        f"Distancia: {distancia}m",
        True,
        BLANCO
    )

    pantalla.blit(txt2,(40,150))

    items = [
        "Moto",
        "Desierto"
    ]

    for i,item in enumerate(items):

        y = 180 + i*180

        color = (50,50,70)

        if i == seleccion:
            color = (80,120,255)

        pygame.draw.rect(
            pantalla,
            color,
            (
                ANCHO//2 - 250,
                y,
                500,
                130
            ),
            border_radius=20
        )

        nombre = fuente.render(
            item,
            True,
            BLANCO
        )

        pantalla.blit(
            nombre,
            (
                ANCHO//2 - 200,
                y+20
            )
        )

        if item == "Moto":

            comprado = moto_comprada

            precio = 50
            req = 1000

        else:

            comprado = desierto_comprado

            precio = 150
            req = 3000

        estado = "COMPRADO"

        color_estado = VERDE

        if not comprado:

            estado = "COMPRAR"

            color_estado = AMARILLO

        txt_estado = fuente.render(
            estado,
            True,
            color_estado
        )

        pantalla.blit(
            txt_estado,
            (
                ANCHO//2 + 80,
                y+20
            )
        )

        precio_txt = fuente_pequena.render(
            f"Costo: {precio} monedas",
            True,
            BLANCO
        )

        pantalla.blit(
            precio_txt,
            (
                ANCHO//2 - 200,
                y+65
            )
        )

        dist_txt = fuente_pequena.render(
            f"Distancia requerida: {req}m",
            True,
            BLANCO
        )

        pantalla.blit(
            dist_txt,
            (
                ANCHO//2 - 200,
                y+95
            )
        )

def dibujar_boton_salir(pantalla):

    texto = fuente_pequena.render(
        "ESC - Salir",
        True,
        BLANCO
    )

    pygame.draw.rect(
        pantalla,
        (40,40,55),
        (
            20,
            20,
            140,
            40
        ),
        border_radius=10
    )

    pantalla.blit(
        texto,
        (
            30,
            30
        )
    )