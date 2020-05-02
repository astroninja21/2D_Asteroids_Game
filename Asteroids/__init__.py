import pygame  # Main Pygame Logic

import logging

from Asteroids import Attributes, Menus, Assets, Logic

formatter = logging.Formatter("%(name)s:%(levelname)s: %(message)s")
file_handler = logging.FileHandler("log.txt", mode='w')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


class States:
    QUIT = 0
    MAIN_MENU = 1
    START_GAME = 2
    IN_GAME = 3
    PAUSED = 4
    GAME_OVER = 5


class Environment:

    def get_logger(self, logger_name):
        log = logging.getLogger(logger_name)
        log.setLevel(logging.DEBUG)
        stream_handler.setLevel(self.attributes.game.log_level)
        log.addHandler(file_handler)
        log.addHandler(stream_handler)
        return log

    def __init__(self, game_attributes, log_level=logging.ERROR):
        # Logging Initialization
        stream_handler.setLevel(log_level)

        self.log = logging.getLogger("ENV")
        self.log.setLevel(log_level)
        self.log.addHandler(file_handler)
        self.log.addHandler(stream_handler)

        self.attributes = Attributes.Attributes(game_attributes)
        self.attributes.game.name = "Asteroids - Developed by Nolan Emerson"
        self.attributes.game.log_level = log_level
        self.state = None
        self.screen = None

        self.asteroids = []
        self.player = None

        pygame.init()
        self.clock = pygame.time.Clock()

    def init(self):
        log = self.get_logger("ENV:INIT")

        log.info("Creating Window")
        self.screen = pygame.display.set_mode(self.attributes.game.resolution)
        log.info("Setting Window Caption")
        pygame.display.set_caption(self.attributes.game.name)

    def entry_point(self):
        log = self.get_logger("ENV:ENTR")

        log.info("Initializing Game Environment")
        self.init()
        self.state = States.MAIN_MENU
        log.info("Starting Main Loop")
        self.main_loop()

    def no_menus(self):
        log = self.get_logger("ENV:ENTR")

        log.info("Initializing Game Environment")
        self.init()
        log.info("Resetting Game Environment")
        self.reset()
        log.info("Starting Game Loop")
        self.game_loop()

    def main_loop(self):
        log = self.get_logger("ENV:MAIN")

        run = True
        while run:

            # pygame event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit Game
                    run = False

            log.debug("Firing State")
            # State Launcher
            if self.state == States.MAIN_MENU:
                log.debug("State: MAIN MENU")
                # Display Main Menu
                self.state = Menus.main(self)

            elif self.state == States.START_GAME:
                log.debug("State: START GAME")
                # Reset Game Space
                self.reset()

                # Start Game
                self.state = States.IN_GAME

            elif self.state == States.IN_GAME:
                log.debug("State: IN GAME")
                # Continue Game
                self.state = self.game_loop()

            elif self.state == States.PAUSED:
                log.debug("State: PAUSED")
                log.info("Game Paused")
                # Display Pause Menu
                self.state = Menus.pause(self)

            elif self.state == States.GAME_OVER:
                log.debug("State: GAME OVER")
                # Display Game Over Menu
                self.state = Menus.game_over(self)

            elif self.state == States.QUIT:
                log.debug("State: QUIT")
                log.info("Quitting Game")
                run = False

            self.clock.tick(self.attributes.game.tick_rate)

        log.info("Quitting Window")
        pygame.quit()

    def reset(self):
        log = self.get_logger("ENV:REST")

        log.info("Resetting Game Environment")
        self.asteroids = []
        self.player = Assets.PC.Ship.default(self)

    def game_loop(self):
        log = self.get_logger("ENV:GAME")

        log.info("Entering/Re-Entering Game Loop")
        while True:

            # pygame event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    log.debug("Handling Pygame Event: QUIT")
                    # Quit Game
                    return States.QUIT

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        log.debug("Player Pausing")
                        # Pause Game
                        return States.PAUSED
                    if event.key == pygame.K_SPACE:
                        log.debug("Player Shooting")
                        # Make Player Shoot
                        self.player.shoot_missile()

                    # Logging
                    if event.key == pygame.K_w:
                        log.debug("Player Start Moving")
                    if event.key == pygame.K_a:
                        log.debug("Player Start Rotate Left")
                    if event.key == pygame.K_d:
                        log.debug("Player Start Rotate Right")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        log.debug("Player Stop Moving")
                    if event.key == pygame.K_a:
                        log.debug("Player Stop Rotate Left")
                    if event.key == pygame.K_d:
                        log.debug("Player Stop Rotate Right")

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                # Turn Player Left
                self.player.rotate(self.player.Direction.LEFT)
            if keys[pygame.K_d]:
                # Turn Player Right
                self.player.rotate(self.player.Direction.RIGHT)
            if keys[pygame.K_w]:
                # Move Player Forward
                self.player.move_forward()

            # Game Logic Here
            if Logic.tick(self) == States.GAME_OVER:
                log.info("Game Over")
                return States.GAME_OVER

            self.screen.fill((0, 0, 0))

            # Render Here
            Logic.render(self)

            pygame.display.flip()
            self.clock.tick(self.attributes.game.tick_rate)
