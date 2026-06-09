import pygame
import math

from config import *
from terreno import get_ground, get_slope


class Auto:

    def __init__(self):
        self.reset()

    # ---------------- RESET ----------------
    def reset(self):
        self.x = 300
        self.y = 200

        self.vel_x = 0
        self.vel_y = 0

        self.rotacion = 0
        self.rot_vel = 0

        self.wheel_rotation = 0

        self.fuel = 100

        self.cam_x = 0

        self.game_over = False

    # ---------------- UPDATE ----------------
    def update(self, dt, teclas, terrain):
        suelo = get_ground(self.x, terrain)
        pendiente = get_slope(self.x, terrain)

        tocando_suelo = False

        # ---------------- CONTROLES Y VELOCIDAD ----------------
        aceleracion = 0

        if teclas[pygame.K_d] and self.fuel > 0:
            
            aceleracion += MOTOR * 1.5

           
            self.fuel -= 0.12 * dt

            
            self.fuel -= abs(self.vel_x) * 0.003 * dt

            
            self.fuel -= abs(math.sin(pendiente)) * 0.02 * dt

        if teclas[pygame.K_a]:
            aceleracion -= FRENO

        # ---------------- GRAVEDAD ----------------
        self.vel_y += GRAVEDAD * dt

        # ---------------- MOVIMIENTO ----------------
        traccion = max(0.45, math.cos(pendiente))

        self.vel_x += aceleracion * traccion * dt

        
        self.vel_x *= 0.992

        
        limite_vel = MAX_VEL * 1.5
        self.vel_x = max(-limite_vel, min(limite_vel, self.vel_x))

        
        self.x += self.vel_x * dt

        if self.x < terrain[0][0] + 50:
            self.x = terrain[0][0] + 50
            self.vel_x = max(0, self.vel_x)

        
        self.y += self.vel_y * dt

        # ---------------- LIMITE HACIA ATRAS ----------------
        if self.x < 0:
            self.x = 0
            if self.vel_x < 0:
                self.vel_x = 0

        # ---------------- COLISIONES Y ROTACIÓN ----------------
        wheel_y = self.y + 30
        
        
        rot_real = (self.rotacion + math.pi) % (2 * math.pi) - math.pi

        if wheel_y > suelo:
            tocando_suelo = True

            
            if abs(rot_real) > math.radians(120):
                self.game_over = True
            
            else:
                profundidad = wheel_y - suelo

                
                fuerza_suspension = profundidad * 0.45
                self.y -= fuerza_suspension

                
                self.vel_y *= -0.08

                diferencia = pendiente - rot_real
                self.rot_vel += diferencia * 0.04 * dt
                self.rotacion += diferencia * 0.05 * dt

                self.vel_x *= 0.995
                self.rot_vel *= 0.82

        else:
            # ---------------- CONTROL AEREO (MÁS LENTO) ----------------
            if teclas[pygame.K_RIGHT]:
                self.rot_vel -= 0.015 * dt  

            if teclas[pygame.K_LEFT]:
                self.rot_vel += 0.015 * dt  

            self.rot_vel *= 0.995

        # ---------------- APLICAR ROTACION ----------------
        self.rotacion += self.rot_vel * dt
        

        self.rot_vel = max(-0.12, min(0.12, self.rot_vel))

        # ---------------- RUEDAS ----------------
        self.wheel_rotation += self.vel_x * 0.12

        # ---------------- CAMARA ----------------
        objetivo_camara = self.x - 350
        self.cam_x += (objetivo_camara - self.cam_x) * 0.08

        # ---------------- FUEL ----------------
        self.fuel = max(0, self.fuel)

        # ---------------- CAIDA AL VACIO ----------------
        if self.y > ALTO + 300:
            self.game_over = True

    # ---------------- DIBUJAR ----------------
    def draw(self, pantalla):

        car_surface = pygame.Surface(
            (170, 90),
            pygame.SRCALPHA
        )

        # ---------------- SOMBRA ----------------
        pygame.draw.ellipse(
            car_surface,
            (0, 0, 0, 70),
            (20, 58, 130, 22)
        )

        # ---------------- SUSPENSION ----------------
        pygame.draw.line(
            car_surface,
            GRIS,
            (45, 45),
            (45, 65),
            5
        )

        pygame.draw.line(
            car_surface,
            GRIS,
            (125, 45),
            (125, 65),
            5
        )

        # ---------------- CARROCERIA ----------------
        pygame.draw.rect(
            car_surface,
            ROJO,
            (20, 20, 130, 35),
            border_radius=14
        )

        pygame.draw.rect(
            car_surface,
            (180, 40, 40),
            (55, 5, 60, 25),
            border_radius=10
        )

        # ---------------- VENTANAS ----------------
        pygame.draw.rect(
            car_surface,
            (120, 200, 255),
            (62, 10, 22, 14),
            border_radius=4
        )

        pygame.draw.rect(
            car_surface,
            (120, 200, 255),
            (88, 10, 20, 14),
            border_radius=4
        )

        # ---------------- FAROS ----------------
        pygame.draw.circle(
            car_surface,
            (255, 255, 180),
            (148, 38),
            6
        )

        pygame.draw.circle(
            car_surface,
            (255, 80, 80),
            (22, 38),
            5
        )

        # ---------------- ESCAPE ----------------
        pygame.draw.rect(
            car_surface,
            (90, 90, 90),
            (5, 42, 15, 5),
            border_radius=2
        )

        # ---------------- RUEDAS ----------------
        for rx in (45, 125):

            pygame.draw.circle(
                car_surface,
                (25, 25, 25),
                (rx, 70),
                20
            )

            pygame.draw.circle(
                car_surface,
                (60, 60, 60),
                (rx, 70),
                20,
                3
            )

            pygame.draw.circle(
                car_surface,
                (160, 160, 160),
                (rx, 70),
                8
            )

            ang = self.wheel_rotation

            x_line = rx + math.cos(ang) * 15
            y_line = 70 + math.sin(ang) * 15

            pygame.draw.line(
                car_surface,
                BLANCO,
                (rx, 70),
                (x_line, y_line),
                3
            )

            x_line2 = rx + math.cos(ang + math.pi / 2) * 15
            y_line2 = 70 + math.sin(ang + math.pi / 2) * 15

            pygame.draw.line(
                car_surface,
                BLANCO,
                (rx, 70),
                (x_line2, y_line2),
                3
            )

        # ---------------- ROTACION FINAL PARA PINTAR ----------------
        carro_rotado = pygame.transform.rotate(
            car_surface,
            math.degrees(self.rotacion)
        )

        rect = carro_rotado.get_rect(
            center=(self.x - self.cam_x, self.y)
        )

        pantalla.blit(carro_rotado, rect)