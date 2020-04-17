import pygame

import asteroids

# Screen Variables
res = (500, 500)
window_caption = "2D Asteroids"
tick_rate = 120

# Asteroid Variables
max_asteroids = 20
min_size = 20
max_size = 100
ast_spawn_time = 180

# Missile Variables
missile_tick_life = 180

# Game Used Variables
last_score = 0
last_ast_spawn = ast_spawn_time


ws = asteroids.Worldspace(res)
player = asteroids.Ship((0, 0), 15, 1, 90, 3, missile_tick_life)
ws.ships.append(player)
ws.min_ast_size = min_size
ws.max_ast_size = max_size

# Window Creation
pygame.init()
clock = pygame.time.Clock()
win = pygame.display.set_mode(res)
pygame.display.set_caption(window_caption)

# Main Loop
run = True
paused = False
while run:

    # On Keypress Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not paused:
                player.shoot(ws)
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        # Key Hold Events
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.rotate(-1)
        if keys[pygame.K_d]:
            player.rotate(1)
        if keys[pygame.K_w]:
            player.move(ws)
        if keys[pygame.K_EQUALS]:
            player.speed += 1
            print(player.speed)
        if keys[pygame.K_MINUS]:
            player.speed -= 1
            print(player.speed)

        # Game Logic Here
        if len(ws.asteroids) < max_asteroids and last_ast_spawn >=180:
            last_ast_spawn = 0
            ws.spawn_asteroid()
        last_ast_spawn += 1

        ws.update()
        ws.collision()
        ws.cleanup()

        win.fill((0, 0, 0))

        # Draw Everything Here
        ws.draw(win)

        pygame.display.flip()
        clock.tick(tick_rate)

        if ws.game_over:
            print()
            print("#############")
            print("# GAME OVER #")
            print("#############")
            run = False

pygame.quit()
print()
print("Final Score: " + str(ws.score))
print()
print("Press Enter to Quit")
input()
