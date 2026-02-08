import pygame
import numpy as np
from math import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

SCALE = 6
CENTER = (640, 360)
points = []
angles = []

eccentric_bearing_OD = 15 # non changing
output_bearing_OD = 13 # non changing
roller_radius = 6.5 # non changing
eccentricity = roller_radius * 0.325
output_hole_diameter = output_bearing_OD + 2 * eccentricity # non changing
outer_radius = 40
number_of_rollers = 15
distance_from_eccentric_center = 20
number_of_output_holes = 5

number_of_hills = number_of_rollers - 1

def get_disk_points():
    global points
    points.clear()

    for t in np.arange(0, pi, ((SCALE * 0.001)) * (pi / 180)):
        x = (outer_radius * cos(t)) - (roller_radius * cos(t + atan(sin((-number_of_hills) * t) / ((outer_radius / (eccentricity * number_of_rollers)) - cos((-number_of_hills) * t))))) - (eccentricity * cos(number_of_rollers * t))
        y = (-outer_radius * sin(t)) + (roller_radius * sin(t + atan(sin((-number_of_hills) * t) / ((outer_radius / (eccentricity * number_of_rollers)) - cos((-number_of_hills) * t))))) + (eccentricity * sin(number_of_rollers * t))
        points.append(((x+eccentricity) * SCALE + CENTER[0], y * SCALE + CENTER[1]))

def draw_disk():
    pygame.draw.aalines(screen, "white", False, points)
    points_flipped = [(x, -y + 2 * CENTER[1]) for x, y in points]
    pygame.draw.aalines(screen, "white", False, points_flipped)

    pygame.draw.aacircle(screen, "white", (CENTER[0] + eccentricity * SCALE, CENTER[1]), eccentric_bearing_OD * SCALE/2)
    pygame.draw.aacircle(screen, "black", (CENTER[0] + eccentricity * SCALE, CENTER[1]), (eccentric_bearing_OD-0.25) * SCALE/2)

    for i in range(number_of_output_holes):
        angle = (i + 1) * 2 * pi / number_of_output_holes
        x = distance_from_eccentric_center * SCALE * sin(angle) + CENTER[0] + eccentricity * SCALE
        y = distance_from_eccentric_center * SCALE * cos(angle) + CENTER[1]
        pygame.draw.aacircle(screen, "white", (x, y), output_hole_diameter * SCALE/2)
        pygame.draw.aacircle(screen, "black", (x, y), (output_hole_diameter-0.25) * SCALE/2)


get_disk_points()

def draw_roller():
    for i in range(number_of_rollers):
        angle = (i + 1) * 2 * pi / number_of_rollers

        if number_of_rollers % 2 == 0:
            if (number_of_rollers-2) % 4 == 0:
                shift = number_of_hills
            else:
                shift = 0

        else:
            if (number_of_rollers-1) % 4 == 0:
                shift = 1/2
            else:
                shift = -1/2


        shifted_angle = angle + shift * pi / number_of_rollers
        angles.append(shifted_angle)

        x = outer_radius * SCALE * sin(shifted_angle) + CENTER[0]
        y = outer_radius * SCALE * cos(shifted_angle) + CENTER[1]

        pygame.draw.aacircle(screen, (255, 255, 255), (x,y), roller_radius*SCALE)

def check_collision():
    for i in range(number_of_rollers):
        roller_x = outer_radius * SCALE * sin(angles[i]) + CENTER[0]
        roller_y = outer_radius * SCALE * cos(angles[i]) + CENTER[1]
        for x,y in points:
            distance = sqrt((x-roller_x)**2 + (y-roller_y)**2)
            if distance < roller_radius:
                print("touch")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    draw_disk()
    draw_roller()
    check_collision()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
            if SCALE >= 1:
                SCALE += event.y
                get_disk_points()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()