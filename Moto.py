import pygame
import math

from auto import Auto
from config import *


class Moto(Auto):

    def __init__(self):
        super().__init__()
        # Opcional: color específico para moto si se desea
        # self.color = ROJO

    def draw(self, pantalla):
       
        # Dibujar la moto
        moto = pygame.Surface((140, 80), pygame.SRCALPHA)

        # Sombra de las ruedas
        pygame.draw.circle(moto, NEGRO, (30, 55), 18)
        pygame.draw.circle(moto, NEGRO, (110, 55), 18)

        # Marco
        pygame.draw.line(moto, self.color, (30, 55), (70, 30), 5)
        pygame.draw.line(moto, self.color, (70, 30), (110, 55), 5)

        # Manillar
        pygame.draw.line(moto, self.color, (70, 30), (90, 15), 5)
        pygame.draw.line(moto, self.color, (90, 15), (105, 15), 3)

        # Piloto
        pygame.draw.circle(moto, (255, 220, 180), (65, 5), 10)
        pygame.draw.line(moto, NEGRO, (65, 15), (65, 35), 3)

        moto_rotada = pygame.transform.rotate(
            moto,
            math.degrees(self.rotacion)
        )
        rect = moto_rotada.get_rect(center=(self.x - self.cam_x, self.y))
        pantalla.blit(moto_rotada, rect)

    def draw_preview(
        self,
        pantalla,
        x,
        y
    ):

        x_original = self.x
        y_original = self.y
        cam_original = self.cam_x
        rot_original = self.rotacion

        self.x = x
        self.y = y
        self.cam_x = 0
        self.rotacion = 0

        self.draw(pantalla)

        self.x = x_original
        self.y = y_original
        self.cam_x = cam_original
        self.rotacion = rot_original