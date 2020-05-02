import random

import numpy as np
import pygame

import Asteroids


def to_pygame_position(game, position):
    return int(game.attributes.game.window.center[0] + position[0]), int(
        game.attributes.game.window.center[1] - position[1])


def break_asteroid(game, asteroid):

    no_of_new_ast = random.randint(0, game.attributes.asteroid.max_break_cluster)

    if no_of_new_ast > 0 and asteroid.size / 2 >= game.attributes.asteroid.min_size:
        for _ in range(no_of_new_ast):
            game.asteroids.append(
                Asteroids.Assets.NPC.Asteroid(game, asteroid.position, asteroid.rotation + random.uniform(-(game.attributes.asteroid.spread_angle/2), game.attributes.asteroid.spread_angle/2),
                                              asteroid.speed,
                                              int(asteroid.size * 2 / 3), asteroid.color))


def tick(game):
    log = game.get_logger("ENV:LGIC:TICK")

    # Spawn asteroid if needed
    if len(
            game.asteroids) < game.attributes.asteroid.max_spawned and game.attributes.asteroid.last_spawned >= game.attributes.asteroid.spawn_delay:
        log.info("Spawning New Asteroid")
        game.asteroids.append(Asteroids.Assets.NPC.Asteroid.create_random(game))
        game.attributes.asteroid.last_spawned = 0
    else:
        game.attributes.asteroid.last_spawned += 1

    # Update Positions
    # # Asteroid Positions
    for asteroid in game.asteroids:
        change_to_point = (
            asteroid.speed * np.cos(np.deg2rad(asteroid.rotation)),
            asteroid.speed * np.sin(np.deg2rad(asteroid.rotation)))
        x = asteroid.position[0] + change_to_point[0]
        y = asteroid.position[1] + change_to_point[1]

        if x < game.attributes.game.window.minX:
            x = game.attributes.game.window.maxX
        if x > game.attributes.game.window.maxX:
            x = game.attributes.game.window.minX
        if y < game.attributes.game.window.minY:
            y = game.attributes.game.window.maxY
        if y > game.attributes.game.window.maxY:
            y = game.attributes.game.window.minY

        asteroid.position = (x, y)

    # # Missile Positions
    for missile in game.player.missiles:
        change_to_point = (
            missile.speed * np.cos(np.deg2rad(missile.rotation)), missile.speed * np.sin(np.deg2rad(missile.rotation)))
        x = missile.position[0] + change_to_point[0]
        y = missile.position[1] + change_to_point[1]

        if x < game.attributes.game.window.minX:
            x = game.attributes.game.window.maxX
        if x > game.attributes.game.window.maxX:
            x = game.attributes.game.window.minX
        if y < game.attributes.game.window.minY:
            y = game.attributes.game.window.maxY
        if y > game.attributes.game.window.maxY:
            y = game.attributes.game.window.minY

        missile.position = (x, y)

    # Asteroid Collision
    # # Asteroid - Ship Collision
    for asteroid in game.asteroids:
        dist = np.sqrt((asteroid.position[0] - game.player.position[0]) ** 2 + (
                asteroid.position[1] - game.player.position[1]) ** 2)
        sum_of_radii = asteroid.size + (game.player.size / 2)

        if dist < sum_of_radii:
            log.info("Ship Collided with Asteroid")
            return Asteroids.States.GAME_OVER

    # # Asteroid - Missile Collision
    for asteroid in game.asteroids:
        for missile in game.player.missiles:
            change_to_point = (
                missile.speed * np.cos(np.deg2rad(missile.rotation)),
                missile.speed * np.sin(np.deg2rad(missile.rotation)))
            x = missile.position[0] + change_to_point[0]
            y = missile.position[1] + change_to_point[1]

            missile_end = (x, y)

            dist = np.sqrt((asteroid.position[0] - missile_end[0]) ** 2 + (asteroid.position[1] - missile_end[1]) ** 2)

            if dist < asteroid.size:
                log.info("Missile Collided with Asteroid")
                game.player.missiles.remove(missile)
                game.player.score += 1
                break_asteroid(game, asteroid)
                try:
                    log.debug("Removed Asteroid")
                    game.asteroids.remove(asteroid)
                except ValueError:
                    log.error("Asteroid Removal Error")

    # Missile Life
    for missile in game.player.missiles:
        if missile.tick_count >= game.attributes.missile.tick_life:
            log.debug("Missile Died")
            game.player.missiles.remove(missile)
        else:
            missile.tick_count += 1


def render(game):
    # Draw Asteroids
    for asteroid in game.asteroids:
        pygame.draw.circle(game.screen, asteroid.color, to_pygame_position(game, asteroid.position),
                           asteroid.size, 1)

    # Draw Missiles
    for missile in game.player.missiles:
        start_position = to_pygame_position(game, missile.position)
        modified_point = (missile.position[0] + missile.size * np.cos(np.deg2rad(missile.rotation)),
                          missile.position[1] + missile.size * np.sin(np.deg2rad(missile.rotation)))
        stop_position = to_pygame_position(game, modified_point)
        pygame.draw.line(game.screen, missile.color, start_position, stop_position, 1)

    # Draw Ship
    theta = np.deg2rad(game.player.rotation)

    ship_top = to_pygame_position(game, (
        game.player.position[0] + game.player.size * np.cos(theta),
        game.player.position[1] + game.player.size * np.sin(theta)))
    ship_left = to_pygame_position(game, (game.player.position[0] + game.player.size * np.cos(theta + (4 * np.pi / 3)),
                                          game.player.position[1] + game.player.size * np.sin(theta + (4 * np.pi / 3))))
    ship_right = to_pygame_position(game, (game.player.position[0] + game.player.size * np.cos(theta + (2 * np.pi / 3)),
                                           game.player.position[1] + game.player.size * np.sin(
                                               theta + (2 * np.pi / 3))))

    pygame.draw.polygon(game.screen, game.player.color, (ship_top, ship_left, ship_right))
    pygame.draw.circle(game.screen, game.attributes.asteroid.color, to_pygame_position(game, game.player.position),
                       int(game.player.size / 2), 1)

    # Draw Score
    font = pygame.font.Font(pygame.font.get_default_font(), 28)
    scr = "Score: " + str(game.player.score)

    score_text = font.render(scr, True, game.attributes.menus.text_color)
    score_rect = score_text.get_rect()
    score_rect.topleft = (0, 0)
    game.screen.blit(score_text, score_rect)
