import numpy as np

from Asteroids import Assets


class Ship:
    class Direction:
        LEFT = 0
        RIGHT = 1

    def __init__(self, game, position, rotation, speed, rotation_modifier, size, color):
        self.game = game
        self.position = position
        self.rotation = rotation
        self.speed = speed
        self.rotation_modifier = rotation_modifier
        self.size = size
        self.color = color

        self.score = 0
        self.missiles = []

    @staticmethod
    def default(game):
        position = (0, 0)
        rotation = 90
        speed = game.attributes.ship.speed
        rotation_modifier = game.attributes.ship.rotation_modifier
        size = game.attributes.ship.size
        color = game.attributes.ship.color

        return Ship(game, position, rotation, speed, rotation_modifier, size, color)

    def shoot_missile(self):
        log = self.game.get_logger("ENV:ASTS:SHIP:SHOT")

        if len(self.missiles) < self.game.attributes.ship.max_missiles:
            log.info("Creating New Missile")
            self.missiles.append(Assets.NPC.Missile(self))
        elif len(self.missiles) >= self.game.attributes.ship.max_missiles:
            log.info("Max Missiles Fired")
        else:
            log.error("Missile Fire Error")

    def move_forward(self):
        change_to_point = (
            self.speed * np.cos(np.deg2rad(self.rotation)), self.speed * np.sin(np.deg2rad(self.rotation)))
        x = self.position[0] + change_to_point[0]
        y = self.position[1] + change_to_point[1]

        if x < self.game.attributes.game.window.minX:
            x = self.game.attributes.game.window.maxX
        if x > self.game.attributes.game.window.maxX:
            x = self.game.attributes.game.window.minX
        if y < self.game.attributes.game.window.minY:
            y = self.game.attributes.game.window.maxY
        if y > self.game.attributes.game.window.maxY:
            y = self.game.attributes.game.window.minY

        self.position = (x, y)

    def rotate(self, direction):
        log = self.game.get_logger("ENV:ASTS:SHIP:ROT8")

        if direction == self.Direction.LEFT:
            # Rotate Left
            self.rotation += self.speed * self.rotation_modifier
        elif direction == self.Direction.RIGHT:
            # Rotate Right
            self.rotation -= self.speed * self.rotation_modifier
        else:
            log.error("Ship Rotate Error")