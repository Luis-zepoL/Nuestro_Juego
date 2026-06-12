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
        # Si hay sprite, usarlo
        if self.usar_sprites and self.sprite_moto:
            sprite = pygame.transform.rotate(
                self.sprite_moto,
                math.degrees(self.rotacion)
            )
            rect = sprite.get_rect(
                center=(self.x - self.cam_x, self.y)
            )
            pantalla.blit(sprite, rect)
            return

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