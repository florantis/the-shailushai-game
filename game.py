import pygame, sys, random
import config
import time

# Booting up the game
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Пригоди Шайлушая")
player_fs = pygame.image.load("assets/sprites/player.png")  # full size player sprite
pygame.display.set_icon(player_fs)
screen = pygame.display.set_mode(config.SIZE)
clock = pygame.time.Clock()
gamefont = pygame.font.SysFont("Arial", 24)

# Setting up the game
eat_sound = pygame.mixer.Sound("assets/sounds/sfx/eat.mp3")
pygame.mixer.music.load("assets/sounds/music/main.mp3")
pygame.mixer.music.set_volume(0.2)
bg = pygame.transform.scale(pygame.image.load("assets/sprites/bg/bg1.jpg"), config.SIZE)
scale = 0.1
vel = 4

player = pygame.transform.scale_by(player_fs, scale)
player_rect = player.get_rect()
player_rect = player_rect.move(config.SIZE[0] // 2 - player_rect.centerx, config.SIZE[1] // 2 - player_rect.centery)

score = 0
snails = []

# The game starts
start_time = time.time()
pygame.mixer.music.play(-1)
player_looks_left = True
while True:
    clock.tick(60)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT] and not player_looks_left:
                player = pygame.transform.flip(player, True, False)
                player_looks_left == True

            if keys[pygame.K_RIGHT] and player_looks_left:
                player = pygame.transform.flip(player, True, False)
                player_looks_left = False

    # Read controls
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect = player_rect.move(-vel, 0)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_rect = player_rect.move(vel, 0)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_rect = player_rect.move(0, vel)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_rect = player_rect.move(0, -vel)

    # Add snails if none
    if not snails:
        posx, posy = random.random() * config.SIZE[0], random.random() * config.SIZE[1]
        path = "assets/sprites/snails/snail"
        is_golden_snail = True if random.random() < 0.05 else False

        if is_golden_snail:
            path += "gold.png"
        else:
            path += f"{random.randint(1, 5)}.png"

        snail = pygame.transform.scale_by(pygame.image.load(path), 0.2)
        snail_rect = snail.get_rect()
        snail_rect.x, snail_rect.y = posx, posy

        snails.append([snail, snail_rect, is_golden_snail])

    # Check if there is a collision with snails
    collide = player_rect.collidelist([snail[1] for snail in snails])
    if collide >= 0:
            popped_snail = snails.pop(collide)
            score += 1 + 4 * popped_snail[2]
            eat_sound.play()
            # Increase the size of a player
            scale *= (1.025 + 0.1 * popped_snail[2])
            player = pygame.transform.scale_by(player_fs, scale)
            # Preserve the position
            posx, posy = player_rect.x, player_rect.y
            player_rect = player.get_rect()
            player_rect.x, player_rect.y = posx, posy

    # We check if the game ended
    if score > 200:
        end_time = time.time()
        pygame.mixer.music.load("assets/sounds/music/win.mp3")
        break

    # Build the frame
    screen.blit(bg, bg.get_rect())
    screen.blit(pygame.font.Font.render(gamefont,
                                        f"Score: {score}",
                                        1,
                                        (min(175 + score, 255), max(100 - score, 0), max(200 - score, 0))),
                                        bg.get_rect())
    screen.blit(player, player_rect)
    for snail in snails:
        screen.blit(snail[0], snail[1])
    clock.tick()
    pygame.display.flip()

# When the game ends:
bg = pygame.transform.scale(pygame.image.load("assets/sprites/bg/winbg.png"), config.SIZE)
time = f"{time.localtime(end_time - start_time).tm_sec} seconds"
pygame.mixer_music.play(-1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    screen.blit(bg, bg.get_rect())
    screen.blit(pygame.font.Font.render(gamefont, f"YOU WON! Time taken: {time}", 1, (0, 0, 250)), (config.SIZE[0] // 3, 0))
    pygame.display.flip()


