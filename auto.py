import pygame
import math
from config import *
from terreno import get_ground

class Rueda:
    def __init__(self, offset_x, offset_y):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.x = 0
        self.y = 0
        self.radio = 20

class Auto:
    def __init__(self):
        self.tipo = "Auto"
        self.color = ROJO
        self.monedas = 0
        self.ruedas = [Rueda(-40, 30), Rueda(40, 30)]
        self.reset()

    def reset(self):
        self.x, self.y = 300, 200
        self.vel_x = self.vel_y = 0
        self.rotacion = self.rot_vel = 0
        self.wheel_rotation = 0
        self.fuel = 100
        self.monedas = 0
        self.cam_x = 0
        self.game_over = False
        self.danio_cabeza = 0 

    def update(self, dt, teclas, terrain):
        self.vel_y += GRAVEDAD * dt
        
        aceleracion = 0
        
        if teclas[pygame.K_d] and self.fuel > 0:
            aceleracion += MOTOR * 1.5
            self.fuel -= 0.12 * dt
        
        if teclas[pygame.K_a] and self.fuel > 0:
            aceleracion -= MOTOR * 1.0
            self.fuel -= 0.10 * dt

        if self.fuel <= 0:
            self.fuel = 0
            self.game_over = True
        
        # Fisicas (NO MOVER)
        self.vel_x += aceleracion * dt
        self.vel_x *= 0.992
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        cos_r = math.cos(self.rotacion)
        sin_r = math.sin(self.rotacion)
        tocando_suelo = False
        
        for r in self.ruedas:
            r.x = self.x + (r.offset_x * cos_r - r.offset_y * sin_r)
            r.y = self.y + (r.offset_x * sin_r + r.offset_y * cos_r)
            suelo = get_ground(r.x, terrain)
            
            if r.y + r.radio > suelo:
                tocando_suelo = True
                profundidad = (r.y + r.radio) - suelo
                self.y -= profundidad * 0.8
                self.vel_y = min(self.vel_y, 0)
                self.rot_vel += (r.offset_x * 0.00005) * profundidad * dt

        rot_n = (self.rotacion + math.pi) % (2 * math.pi) - math.pi
        distancia_suelo = get_ground(self.x, terrain) - self.y
        if abs(rot_n) > math.radians(90) and distancia_suelo < 40:
            self.game_over = True

        if not tocando_suelo:
            if teclas[pygame.K_RIGHT]: self.rot_vel -= 0.015 * dt
            if teclas[pygame.K_LEFT]: self.rot_vel += 0.015 * dt
        else:
            self.rot_vel -= math.sin(self.rotacion) * 0.05 * dt
            if abs(self.vel_x) < 0.2:
                self.vel_x = 0
                self.vel_y = 0

        self.rot_vel *= 0.995
        self.rotacion += self.rot_vel * dt
        self.wheel_rotation += self.vel_x * 0.12
        self.cam_x += ((self.x - 350) - self.cam_x) * 0.08

        rot_n = (self.rotacion + math.pi) % (2 * math.pi) - math.pi
        if abs(rot_n) > math.radians(90) and tocando_suelo and abs(self.vel_x) < 0.5:
            self.game_over = True
            
        if self.y > ALTO + 300: 
            self.game_over = True

    def draw(self, pantalla):
        self.draw_auto(pantalla)
        
    def draw_auto(self, pantalla):
        car_surface = pygame.Surface((170, 90), pygame.SRCALPHA)
        pygame.draw.ellipse(car_surface, (0, 0, 0, 70), (20, 58, 130, 22))
        pygame.draw.line(car_surface, GRIS, (45, 45), (45, 65), 5)
        pygame.draw.line(car_surface, GRIS, (125, 45), (125, 65), 5)
        pygame.draw.rect(car_surface, self.color, (15, 25, 140, 30), border_radius=12)
        pygame.draw.polygon(car_surface, self.color, [(40,25), (75,5), (110,5), (140,25)])
        pygame.draw.circle(car_surface, (255,220,180), (90,5), 10)
        pygame.draw.line(car_surface, NEGRO, (90,15), (90,30), 3)
        pygame.draw.rect(car_surface, (120, 200, 255), (62, 10, 22, 14), border_radius=4)
        pygame.draw.rect(car_surface, (120, 200, 255), (88, 10, 20, 14), border_radius=4)
        pygame.draw.circle(car_surface, (255, 255, 180), (148, 38), 6)
        pygame.draw.circle(car_surface, (255, 80, 80), (22, 38), 5)
        pygame.draw.rect(car_surface, (90, 90, 90), (5, 42, 15, 5), border_radius=2)
        
        for rx in (45, 125):
            pygame.draw.circle(car_surface, (25, 25, 25), (rx, 70), 20)
            pygame.draw.circle(car_surface, (60, 60, 60), (rx, 70), 20, 3)
            pygame.draw.circle(car_surface, (160, 160, 160), (rx, 70), 8)
            ang = self.wheel_rotation
            pygame.draw.line(car_surface, BLANCO, (rx, 70), (rx + math.cos(ang)*15, 70 + math.sin(ang)*15), 3)
            pygame.draw.line(car_surface, BLANCO, (rx, 70), (rx + math.cos(ang+math.pi/2)*15, 70 + math.sin(ang+math.pi/2)*15), 3)

        carro_rotado = pygame.transform.rotate(car_surface, math.degrees(self.rotacion))
        rect = carro_rotado.get_rect(center=(self.x - self.cam_x, self.y))
        pantalla.blit(carro_rotado, rect)

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