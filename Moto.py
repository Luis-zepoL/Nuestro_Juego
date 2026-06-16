import pygame
import math
from auto import Auto
from config import *


# ---------------- CLASE MOTO ----------------

# Hereda todas las características del Auto
class Moto(Auto):

    # ---------------- CONSTRUCTOR ----------------

    def __init__(self):

        # Ejecuta primero el constructor de Auto
        super().__init__()

        # Aquí podrían colocarse configuraciones exclusivas de la moto
        # self.color = ROJO


    # ---------------- DIBUJAR MOTO EN EL JUEGO ----------------

    def draw(self, pantalla):
       
        # Crear una superficie transparente donde se construirá la moto
        moto = pygame.Surface(
            (140, 80),
            pygame.SRCALPHA
        )

        # Dibujar ruedas
        pygame.draw.circle(
            moto,
            NEGRO,
            (30, 55),
            18
        )

        pygame.draw.circle(
            moto,
            NEGRO,
            (110, 55),
            18
        )

        # Dibujar chasis o marco principal
        pygame.draw.line(
            moto,
            self.color,
            (30, 55),
            (70, 30),
            5
        )

        pygame.draw.line(
            moto,
            self.color,
            (70, 30),
            (110, 55),
            5
        )

        # Dibujar manillar
        pygame.draw.line(
            moto,
            self.color,
            (70, 30),
            (90, 15),
            5
        )

        pygame.draw.line(
            moto,
            self.color,
            (90, 15),
            (105, 15),
            3
        )

        # Dibujar piloto
        pygame.draw.circle(
            moto,
            (255, 220, 180),
            (65, 5),
            10
        )

        pygame.draw.line(
            moto,
            NEGRO,
            (65, 15),
            (65, 35),
            3
        )

        # Rotar la moto según la inclinación actual
        moto_rotada = pygame.transform.rotate(
            moto,
            math.degrees(self.rotacion)
        )

        # Posicionar la moto en pantalla
        rect = moto_rotada.get_rect(
            center=(
                self.x - self.cam_x,
                self.y
            )
        )

        # Dibujar la moto rotada
        pantalla.blit(
            moto_rotada,
            rect
        )


    # ---------------- DIBUJAR PREVIEW DE LA MOTO ----------------

    def draw_preview(
        self,
        pantalla,
        x,
        y
    ):

        # Guardar valores originales
        x_original = self.x
        y_original = self.y
        cam_original = self.cam_x
        rot_original = self.rotacion

        # Configurar posición temporal para el preview
        self.x = x
        self.y = y
        self.cam_x = 0
        self.rotacion = 0

        # Dibujar la moto
        self.draw(pantalla)

        # Restaurar valores originales
        self.x = x_original
        self.y = y_original
        self.cam_x = cam_original
        self.rotacion = rot_original