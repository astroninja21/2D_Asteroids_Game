import pygame  # Drawing of menus

import Asteroids


def main(game):
    log = game.get_logger("ENV:MENU:MAIN")

    log.info("Displaying Main Menu")

    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text_color = game.attributes.menus.text_color

    run = True
    while run:

        # pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit Game
                log.info("Window Closed. Quiting")
                return Asteroids.States.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Start Game
                    log.info("Start Selected. Starting game")
                    return Asteroids.States.START_GAME
                if event.key == pygame.K_q:
                    # Quit Game
                    log.info("Quit Selected. Quitting")
                    return Asteroids.States.QUIT

        game.screen.fill((0, 0, 0))

        # Render Everything Here
        main_text = font.render("Main Menu", True, text_color)
        play_text = font.render("Press P to play", True, text_color)
        quit_text = font.render("Press Q to quit", True, text_color)

        main_rect = main_text.get_rect()
        play_rect = play_text.get_rect()
        quit_rect = quit_text.get_rect()

        play_pos = game.attributes.game.window.center
        main_pos = (game.attributes.game.window.center[0], play_pos[1] - 40)
        quit_pos = (game.attributes.game.window.center[0], play_pos[1] + 40)

        main_rect.center = main_pos
        play_rect.center = play_pos
        quit_rect.center = quit_pos

        game.screen.blit(main_text, main_rect)
        game.screen.blit(play_text, play_rect)
        game.screen.blit(quit_text, quit_rect)

        pygame.display.flip()
        game.clock.tick(game.attributes.game.tick_rate)


def pause(game):
    log = game.get_logger("ENV:MENU:PAUSE")

    log.info("Displaying Pause Menu")

    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text_color = game.attributes.menus.text_color

    run = True
    while run:

        # pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.info("Window Closed. Quiting")
                # Quit Game
                return Asteroids.States.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    log.info("Continue Selected. Continuing.")
                    # Un-pause Game
                    return Asteroids.States.IN_GAME
                if event.key == pygame.K_q:
                    log.info("Quit Selected. Quiting")
                    # Go To Main Menu
                    return Asteroids.States.MAIN_MENU

        game.screen.fill((0, 0, 0))

        # Render Everything Here
        pause_text = font.render("Paused", True, text_color)
        play_text = font.render("Press P to continue", True, text_color)
        quit_text = font.render("Press Q to quit", True, text_color)

        pause_rect = pause_text.get_rect()
        play_rect = play_text.get_rect()
        quit_rect = quit_text.get_rect()

        play_pos = game.attributes.game.window.center
        pause_pos = (game.attributes.game.window.center[0], play_pos[1] - 40)
        quit_pos = (game.attributes.game.window.center[0], play_pos[1] + 40)

        pause_rect.center = pause_pos
        play_rect.center = play_pos
        quit_rect.center = quit_pos

        game.screen.blit(pause_text, pause_rect)
        game.screen.blit(play_text, play_rect)
        game.screen.blit(quit_text, quit_rect)

        pygame.display.flip()
        game.clock.tick(game.attributes.game.tick_rate)


def game_over(game):
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text_color = game.attributes.menus.text_color

    run = True
    while run:

        # pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Asteroids.States.QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return Asteroids.States.START_GAME
                if event.key == pygame.K_q:
                    return Asteroids.States.MAIN_MENU

        game.screen.fill((0, 0, 0))

        # Render Everything Here
        scr = "Score: " + str(game.player.score)

        game_over_text = font.render("Game Over!", True, text_color)
        score_text = font.render(scr, True, text_color)
        play_text = font.render("Press P to play again", True, text_color)
        quit_text = font.render("Press Q to quit", True, text_color)

        game_over_rect = game_over_text.get_rect()
        score_rect = score_text.get_rect()
        play_rect = play_text.get_rect()
        quit_rect = quit_text.get_rect()

        game_over_pos = (game.attributes.game.window.center[0], game.attributes.game.window.center[1] - 60)
        score_pos = (game.attributes.game.window.center[0], game.attributes.game.window.center[1] - 30)
        play_pos = (game.attributes.game.window.center[0], game.attributes.game.window.center[1] + 30)
        quit_pos = (game.attributes.game.window.center[0], game.attributes.game.window.center[1] + 60)

        game_over_rect.center = game_over_pos
        score_rect.center = score_pos
        play_rect.center = play_pos
        quit_rect.center = quit_pos

        game.screen.blit(game_over_text, game_over_rect)
        game.screen.blit(score_text, score_rect)
        game.screen.blit(play_text, play_rect)
        game.screen.blit(quit_text, quit_rect)

        pygame.display.flip()
        game.clock.tick(game.attributes.game.tick_rate)
