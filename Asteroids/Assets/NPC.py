import random
import numpy as np


class Asteroid:
    def __init__(self, game, position, rotation, speed, size, color):
        self.game = game
        self.position = position
        self.rotation = rotation
        self.speed = speed
        self.size = size
        self.color = color

    @staticmethod
    def create_random(game):
        log = game.get_logger("ENV:ASTS:ASTR:RAND")
        log.info("Creating Random Asteroid")

        rotation = random.uniform(0, 360)
        speed = random.random()
        size = random.randint(game.attributes.asteroid.min_size, game.attributes.asteroid.max_size)

        max_val = random.randint(0, 1)
        if max_val > 0:
            position = (random.uniform(game.attributes.game.window.minX, game.attributes.game.window.maxX),
                        game.attributes.game.window.maxY)
        else:
            position = (game.attributes.game.window.maxX,
                        random.uniform(game.attributes.game.window.minY, game.attributes.game.window.maxY))

        ast = Asteroid(game, position, rotation, speed, size, game.attributes.asteroid.color)
        return ast


class Missile:
    def __init__(self, firing_ship):
        self.position = (
            firing_ship.position[0] + firing_ship.size / np.sqrt(3) * np.cos(np.deg2rad(firing_ship.rotation)),
            firing_ship.position[1] + firing_ship.size / np.sqrt(3) * np.sin(np.deg2rad(firing_ship.rotation)))
        self.rotation = firing_ship.rotation
        self.speed = firing_ship.speed * 2
        self.size = firing_ship.game.attributes.missile.size
        self.tick_count = 0
        self.color = firing_ship.color
