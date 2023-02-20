import pygame
import sys
from time import time
from options import *
from vector import *
from objects import *
from copy import deepcopy
from math import radians

"""
False: blanc
True: noir
"""

# setup
pygame.init()
clock = pygame.time.Clock()
start_time = time()

# screen
screen = pygame.display.set_mode((screen_width, screen_height))
fov = 90
projection = Matrix.projection(fov, 0.1, 1000)
position = Vector(0, 0, -5, 0)
light = Vector(0, 0, -1, 0).normalize()
rotation = Matrix.rotationy(0)


# engine

cube = Mesh([ Triangle([Vector(0, 0, 0, 0), Vector(0, 1, 0, 0), Vector(1, 1, 0, 0)]),
         Triangle([Vector(0, 0, 0, 0), Vector(1, 1, 0, 0), Vector(1, 0, 0, 0)]),
         
         Triangle([Vector(1, 0, 0, 0), Vector(1, 1, 0, 0), Vector(1, 1, 1, 0)]),
         Triangle([Vector(1, 0, 0, 0), Vector(1, 1, 1, 0), Vector(1, 0, 1, 0)]),

         Triangle([Vector(1, 0, 1, 0), Vector(1, 1, 1, 0), Vector(0, 1, 1, 0)]),
         Triangle([Vector(1, 0, 1, 0), Vector(0, 1, 1, 0), Vector(0, 0, 1, 0)]),

         Triangle([Vector(0, 0, 1, 0), Vector(0, 1, 1, 0), Vector(0, 1, 0, 0)]),
         Triangle([Vector(0, 0, 1, 0), Vector(0, 1, 0, 0), Vector(0, 0, 0, 0)]),

         Triangle([Vector(0, 1, 0, 0), Vector(0, 1, 1, 0), Vector(1, 1, 1, 0)]),
         Triangle([Vector(0, 1, 0, 0), Vector(1, 1, 1, 0), Vector(1, 1, 0, 0)]),

         Triangle([Vector(1, 0, 1, 0), Vector(0, 0, 1, 0), Vector(0, 0, 0, 0)]),
         Triangle([Vector(1, 0, 1, 0), Vector(0, 0, 0, 0), Vector(1, 0, 0, 0)]) ])

for triangle in cube:
    triangle += Vector(-0.5, -0.5, -0.5, 0)

def tick(dt):
    global rotation, light

    dx, dy = 0, 0

    if not pygame.mouse.get_visible() and pygame.mouse.get_focused():
        dx, dy = pygame.display.Info().current_w / 2 - pygame.mouse.get_pos()[0],  pygame.display.Info().current_h / 2 - pygame.mouse.get_pos()[1]
        pygame.mouse.set_pos(pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2)

    rotation *= Matrix.rotationy(-dx/12) * Matrix.rotationx(dy/12)


def draw(screen):
    screen.fill((0, 0, 0))

    for triangle in cube:
        t = (deepcopy(triangle) * rotation + position) * projection
        n = t.normal().dot(light)
        for i in range(len(t.points)):
            t.points[i][0] += 1
            t.points[i][1] += 1
            t.points[i][0] *= 0.5 * screen_width
            t.points[i][1] *= 0.5 * screen_height
        if t.normal().dot(Vector(0, 0, -1)) > 0 :
            t.draw(screen, color=(127*(1+n), 127*(1+n), 127*(1+n)))

    font = pygame.font.SysFont(None, 24)
    img = font.render(str(int(clock.get_fps())), True, (255, 255, 255))
    screen.blit(img, (20, 20))

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.mouse.set_visible(True)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_visible(False)
            pygame.mouse.set_pos(pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2)
    
    tick(clock.get_rawtime())
    draw(screen)

    pygame.display.flip()
    clock.tick(FPS_MAX)


