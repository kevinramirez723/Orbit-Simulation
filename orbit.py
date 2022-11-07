from math import atan2, cos, sin
import numpy as np
import pygame

pygame.init()
pygame.display.set_caption("Celestial Bodies")
WIDTH, HEIGHT = 800, 800 # True Canvas size is affected by dpi settings
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CANVAS = pygame.Surface((WIDTH, HEIGHT))
CANVAS.set_alpha(1) # Determines tail length (0 for infinite)
CANVAS_COLOR = (0, 0, 0, 50)
BLUE = (115, 186, 255)
GREY = (180, 180, 180)
ORANGE = (255, 100, 0)
PURPLE = (255, 0, 150)
GREEN = (0, 255, 50)
G = 6.674e-11 # Nm^2/kg^2

class Planet:
    # WARNING - Larger timesteps could lead to numerically unstable results
    TIMESTEP = 3600 # sec/hour
    SCALE = 1 / 1e6  # pixels/m

    def __init__(self, pos, init_vel, radius, mass, color):
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array(init_vel, dtype=float)
        self.radius = radius
        self.mass = mass
        self.color = color

    def draw(self, CANVAS):
        offset = np.array([WIDTH / 2, HEIGHT / 2])
        scaled_pos = (self.SCALE * self.pos + offset)
        scaled_radius = self.SCALE * self.radius
        pygame.draw.circle(CANVAS, self.color, scaled_pos, scaled_radius)

    def attraction(self, other):
        diff = other.pos - self.pos
        distance = np.linalg.norm(diff)
        accel = G * other.mass / distance ** 2
        a_vec = accel * diff / distance
        return a_vec

    def calc_new_pos(self, planets):
        total_a_vec = np.zeros(2)
        for planet in planets:
            if planet != self:
                total_a_vec += self.attraction(planet)
        self.vel += total_a_vec * self.TIMESTEP
        return self.pos + self.vel * self.TIMESTEP
    
    def update_pos(self, i, positions):
        self.pos = positions[i]


def conserve_momentum(planets):
    total_M = 0
    momentum_vec = np.zeros(2)
    for planet in planets:
        total_M += planet.mass
        momentum_vec += planet.vel * planet.mass
    total_vel = momentum_vec / total_M
    for planet in planets:
        planet.vel -= total_vel

def main():
    run = True
    clock = pygame.time.Clock()

    Earth = Planet((0, 0), (0, 12.4412), 6.378e6, 5.972e24, BLUE)
    Moon = Planet((3.844e8, 0), (0, -1.012e3), 1.738e6, 7.342e22, GREY)
    planets = [Earth, Moon]
    # UNCOMMENT TO ADD MORE EXAMPLE CELESTIAL BODIES OR ADD YOUR OWN
    # ------------------------------------------------------------------
    #O_planet = Planet((2.844e8, 1.3e8), (-4.25e2, 1.247e3), 4.738e6, 2.342e24, ORANGE)
    #planets.append(O_planet)
    #P_planet = Planet((1.323e8, -3e7), (-1.58e2, 2.87e3), 3.99e6, 6.1e24, PURPLE)
    #planets.append(P_planet)
    #G_planet = Planet((-3.613e8, 0), (1.9e2, 0), 2.738e6, 2.02e23, GREEN)
    #planets.append(G_planet)

    conserve_momentum(planets)

    while run:
        clock.tick(120)
        CANVAS.fill(CANVAS_COLOR)
        WINDOW.blit(CANVAS, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        new_positions = []
        for planet in planets:
            new_positions.append(planet.calc_new_pos(planets))
        for i, planet in enumerate(planets):
            planet.update_pos(i, new_positions)
            planet.draw(WINDOW)
        pygame.display.update()

    pygame.quit()

main()
