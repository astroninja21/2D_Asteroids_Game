import pygame
import numpy as np
import random

import collision


class Worldspace:
    def __init__(self, size=(10, 10)):
        self.size = size
        self.maxX = size[0]/2
        self.minX = -(size[0]/2)
        self.maxY = size[1]/2
        self.minY = -(size[1]/2)
        self.center = (size[0]//2, size[1]//2)

        self.ships = list()
        self.asteroids = list()
        self.missiles = list()

        self.min_ast_size = 10
        self.max_ast_size = 50

        self.score = 0
        self.game_over = False

    def spawn_asteroid(self, speed=0, size=0):
        spawn_rotation = random.randint(0, 360)
        spawn_pos = [0, 0]

        value_to_change = random.randint(0, 100)

        if speed == 0:
            speed = random.random()

        if size == 0:
            size = random.randint(self.min_ast_size, self.max_ast_size)

        if 0 <= spawn_rotation < 180:
            if value_to_change < 50:
                spawn_pos = [random.randint(self.minX, self.maxX), self.minY]
            if value_to_change >= 50:
                spawn_pos = [self.minX, random.randint(self.minY, self.maxY)]
        if 180 <= spawn_rotation <= 360:
            if value_to_change < 50:
                spawn_pos = [random.randint(self.minX, self.maxX), self.maxY]
            if value_to_change >= 50:
                spawn_pos = [self.maxX, random.randint(self.minY, self.maxY)]

        self.asteroids.append(Asteroid(spawn_pos, spawn_rotation, speed, size))

    def update(self):
        for missile in self.missiles:
            missile.update()
        for asteroid in self.asteroids:
            asteroid.update()

    def collision(self,):
        for missile in self.missiles:
            for asteroid in self.asteroids:

                if collision.check_collision(missile.pos, asteroid.pos, asteroid.size//2):

                    try:
                        self.missiles.remove(missile)
                    except ValueError:
                        pass

                    no_of_new_ast = random.randint(0, 5)

                    if no_of_new_ast > 0 and asteroid.size//no_of_new_ast > self.min_ast_size//2:
                        for i in range(no_of_new_ast):
                            self.asteroids.append(Asteroid(asteroid.pos,
                                                           np.rad2deg(asteroid.rotation)+random.randint(-15, 15),
                                                           asteroid.speed,
                                                           asteroid.size//no_of_new_ast
                                                           ))
                    self.asteroids.remove(asteroid)
                    self.score += 1

        for ship in self.ships:
            for asteroid in self.asteroids:

                if collision.check_collision(ship.pos, asteroid.pos, asteroid.size//2):
                    self.game_over = True

    def cleanup(self):
        for missile in self.missiles:
            if self.minX <= missile.pos[0] <= self.maxX:
                if self.minY <= missile.pos[1] <= self.maxY:
                    pass
                else:
                    self.missiles.remove(missile)
            else:
                self.missiles.remove(missile)

        for asteroid in self.asteroids:
            if self.minX <= asteroid.pos[0] <= self.maxX:
                if self.minY <= asteroid.pos[1] <= self.maxY:
                    pass
                else:
                    self.asteroids.remove(asteroid)
            else:
                self.asteroids.remove(asteroid)

    def get_rect(self):
        temp = pygame.Rect(0, 0, self.size[0], self.size[1])
        return temp

    def draw(self, surface):
        # Draw worldspace border and axis
        # pygame.draw.rect(surface, (0, 255, 0), self.get_rect(), 1)
        # pygame.draw.line(surface, (255, 0, 0), (0, self.center[1]), (self.size[0], self.center[1]))
        # pygame.draw.line(surface, (0, 0, 255), (self.center[0], 0), (self.center[0], self.size[1]))

        for ship in self.ships:
            ship.draw(self, surface)

        for missile in self.missiles:
            missile.draw(self, surface)

        for asteroid in self.asteroids:
            asteroid.draw(self, surface)


class Ship:
    def __init__(self, pos, size, speed=1, rotation=-90):
        self.pos = list(pos)
        self.size = size
        self.rotation = rotation
        self.speed = speed
        self.rotation_modifier = 2

    def move(self, worldspace):
        theta = np.deg2rad(self.rotation)

        change_to_point = (self.speed*np.cos(theta), self.speed*np.sin(theta))
        if worldspace.minX <= (self.pos[0]+change_to_point[0]) <= worldspace.maxX:
            if worldspace.minY <= (self.pos[1]-change_to_point[1]) <= worldspace.maxY:
                self.pos[0] += change_to_point[0]
                self.pos[1] -= change_to_point[1]

    def rotate(self, direction):
        if direction > 0:
            self.rotation += self.speed * self.rotation_modifier
        if direction < 0:
            self.rotation -= self.speed * self.rotation_modifier

    def shoot(self, worldspace):
        worldspace.missiles.append(Missile(self.pos, self.rotation))

    def get_poly(self, worldspace):
        r = self.size/np.sqrt(3)
        theta = np.deg2rad(self.rotation)

        point1 = (worldspace.center[0]+self.pos[0]+r*np.cos(theta),
                  worldspace.center[1]-self.pos[1]+r*np.sin(theta))

        point2 = (worldspace.center[0]+self.pos[0]+r*np.cos(theta+(4*np.pi/3)),
                  worldspace.center[1]-self.pos[1]+r*np.sin(theta+(4*np.pi/3)))

        point3 = (worldspace.center[0]+self.pos[0]+r*np.cos(theta+(2*np.pi/3)),
                  worldspace.center[1]-self.pos[1]+r*np.sin(theta+(2*np.pi/3)))

        return point1, point2, point3

    def draw(self, worldspace, surface):
        center_point = (worldspace.center[0]+self.pos[0], worldspace.center[1]-self.pos[1])
        pygame.draw.polygon(surface, (0, 255, 0), self.get_poly(worldspace), 1)
        pygame.draw.line(surface, (0, 255, 0), center_point, self.get_poly(worldspace)[0], 1)


class Missile:
    def __init__(self, start_pos, rotation, speed=3):
        self.pos = [0, 0]
        self.pos[0] = start_pos[0]
        self.pos[1] = start_pos[1]
        self.rotation = np.deg2rad(rotation)
        self.speed = speed

    def update(self):
        change_to_point = (self.speed*np.cos(self.rotation), self.speed*np.sin(self.rotation))

        self.pos[0] += change_to_point[0]
        self.pos[1] -= change_to_point[1]

    def draw(self, worldspace, surface):
        start_point = (worldspace.center[0]+self.pos[0], worldspace.center[1]-self.pos[1])
        pygame.draw.line(surface, (0, 255, 0), start_point, (start_point[0]+5*np.cos(self.rotation),
                                                             start_point[1]+5*np.sin(self.rotation)), 1)


class Asteroid:
    def __init__(self, pos=(0, 0), rotation=0, speed=1, size=10):
        self.pos = [0, 0]
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.rotation = np.deg2rad(360-rotation)
        self.speed = speed
        self.size = size

    def update(self):
        change_to_point = (self.speed*np.cos(self.rotation), self.speed*np.sin(self.rotation))

        self.pos[0] += change_to_point[0]
        self.pos[1] -= change_to_point[1]

    def hit(self):
        pass

    def draw(self, worldspace, surface):
        draw_pos = (int(worldspace.center[0]+self.pos[0]), int(worldspace.center[1]-self.pos[1]))
        pygame.draw.circle(surface, (255, 255, 255), draw_pos, self.size//2, 1)
