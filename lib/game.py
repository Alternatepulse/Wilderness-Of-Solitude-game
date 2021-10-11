import ctypes
import pygame
import sys
from lib.text import draw_text
from lib.map_loader import read_map
from lib.editor import maps

clock = pygame.time.Clock()  # set up the clock

from pygame.locals import *  # import pygame modules

pygame.init()  # initiate pygame

pygame.display.set_caption("Pygame Window")  # set the window name

# initiate screen
user32 = ctypes.windll.user32
WINDOW_SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

screen = pygame.display.set_mode(WINDOW_SIZE, FULLSCREEN, 32)
display = pygame.Surface((640, 360))

true_scroll = [0, 0]

substrate_top = pygame.image.load("./assets/map/jungle_tileset/substrate_top.png")
substrate_left = pygame.image.load("./assets/map/jungle_tileset/substrate_left.png")
substrate_right = pygame.image.load("./assets/map/jungle_tileset/substrate_right.png")
substrate_bottom = pygame.image.load("./assets/map/jungle_tileset/substrate_bottom.png")
substrate_top_right = pygame.image.load("./assets/map/jungle_tileset/substrate_top_right.png")
substrate_top_left = pygame.image.load("./assets/map/jungle_tileset/substrate_top_left.png")
substrate_bottom_right = pygame.image.load("./assets/map/jungle_tileset/substrate_bottom_right.png")
substrate_bottom_left = pygame.image.load("./assets/map/jungle_tileset/substrate_bottom_left.png")

grass_top = pygame.image.load("./assets/map/jungle_tileset/grass_top.png")
grass_left = pygame.image.load("./assets/map/jungle_tileset/grass_left.png")
grass_right = pygame.image.load("./assets/map/jungle_tileset/grass_right.png")
grass_bottom = pygame.image.load("./assets/map/jungle_tileset/grass_bottom.png")
grass_top_right = pygame.image.load("./assets/map/jungle_tileset/grass_top_right.png")
grass_top_left = pygame.image.load("./assets/map/jungle_tileset/grass_top_left.png")
grass_bottom_right = pygame.image.load("./assets/map/jungle_tileset/grass_bottom_right.png")
grass_bottom_left = pygame.image.load("./assets/map/jungle_tileset/grass_bottom_left.png")

grass_inner_top_right = pygame.image.load("./assets/map/jungle_tileset/grass_inner_top_right.png")
grass_inner_top_left = pygame.image.load("./assets/map/jungle_tileset/grass_inner_top_left.png")
grass_inner_bottom_right = pygame.image.load("./assets/map/jungle_tileset/grass_inner_bottom_right.png")
grass_inner_bottom_left = pygame.image.load("./assets/map/jungle_tileset/grass_inner_bottom_left.png")

substrate_corner_top_right = pygame.image.load("./assets/map/jungle_tileset/substrate_corner_top_right.png")
substrate_corner_top_left = pygame.image.load("./assets/map/jungle_tileset/substrate_corner_top_left.png")
substrate_corner_bottom_right = pygame.image.load("./assets/map/jungle_tileset/substrate_corner_bottom_right.png")
substrate_corner_bottom_left = pygame.image.load("./assets/map/jungle_tileset/substrate_corner_bottom_left.png")

deep_underground = pygame.image.load("./assets/map/jungle_tileset/deep_underground.png")

TILE_SIZE = grass_top.get_width()

bg0_wip = pygame.image.load("./assets/map/background/bg0.png")
bg0 = pygame.transform.scale(bg0_wip, WINDOW_SIZE)

bg1_wip = pygame.image.load("./assets/map/background/bg1.png")
bg1 = pygame.transform.scale(bg1_wip, (8000, 350))

bg2_wip = pygame.image.load("./assets/map/background/bg2.png")
bg2 = pygame.transform.scale(bg2_wip, (800, 350))

bg3_wip = pygame.image.load("./assets/map/background/bg3.png")
bg3 = pygame.transform.scale(bg3_wip, (800, 350))

bg4_wip = pygame.image.load("./assets/map/background/bg4.png")
bg4 = pygame.transform.scale(bg4_wip, (800, 350))

bg5_wip = pygame.image.load("./assets/map/background/bg5.png")
bg5 = pygame.transform.scale(bg5_wip, (800, 350))


def game_loop():

    level = read_map(maps[0])
    print(level)
    player_image = pygame.image.load("./assets/character/idle-1.png.png")
    player_idle = []
    player_idle_frame = 0
    goal = False
    goal_tile = []
    die_tile = []
    player_running = []
    player_mid_air = []
    player_running_frame = 0
    player_jump = pygame.image.load("./assets/character/jump.png")
    player_jump_frame = 0
    player_mid_air_frame = 0
    moved_left = False
    mid_air_time = 0



    for image in range(12):
        player_idle.append("./assets/character/idle/idle-" + str(image + 1) + ".png")

    for image in range(8):
        player_running.append("./assets/character/run/run_" + str(image) + ".png")

    for image in range(2):
        player_mid_air.append("./assets/character/mid_air/mid_air_" + str(image) + ".png")  # for future remarks

    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(rect, movement, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        rect.x += movement[0]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types["right"] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types["left"] = True
        rect.y += movement[1]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types["bottom"] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types["top"] = True
        return rect, collision_types

    moving_right = False
    moving_left = False

    player_y_momentum = 0
    air_timer = 0

    player_rect = pygame.Rect(332, 175, player_image.get_width(), (player_image.get_height() - 6))

    true_scroll[0] = len(level[1]) * 32 - 500

    v = 0
    running = True
    while running:  # game loop
        display.fill((146, 244, 255))

        true_scroll[0] += (player_rect.x - true_scroll[0] - 320 + (player_image.get_width() / 2)) / 20
        true_scroll[1] += (player_rect.y - true_scroll[1] - 180 + (player_image.get_height() / 2)) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        display.blit(bg0, (0, 0))
        display.blit(bg1, (-300 - true_scroll[0], -50 - true_scroll[1]))
        display.blit(bg2, (-100 - true_scroll[0] / 10, -50 - true_scroll[1]))
        display.blit(bg3, (-100 - true_scroll[0] / 20, -50 - true_scroll[1]))
        display.blit(bg4, (-100 - true_scroll[0] / 30, -50 - true_scroll[1]))
        display.blit(bg5, (-100 - true_scroll[0] / 40, -50 - true_scroll[1]))

        goal_tile = []
        die_tile = []
        tile_rects = []
        y = 0
        for row in level:
            x = 0
            for tile in row:
                if tile == 1:
                    display.blit(grass_top, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 2:
                    display.blit(grass_top_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 3:
                    display.blit(grass_top_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 4:
                    display.blit(grass_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 5:
                    display.blit(grass_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 6:
                    display.blit(grass_bottom, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 7:
                    display.blit(grass_bottom_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 8:
                    display.blit(grass_bottom_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                elif tile == 9:
                    display.blit(substrate_top, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 10:
                    display.blit(substrate_top_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 11:
                    display.blit(substrate_top_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 12:
                    display.blit(substrate_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 13:
                    display.blit(substrate_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 14:
                    display.blit(substrate_bottom, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 15:
                    display.blit(substrate_bottom_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 16:
                    display.blit(substrate_bottom_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                elif tile == 18:
                    display.blit(grass_inner_top_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 19:
                    display.blit(grass_inner_top_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 20:
                    display.blit(grass_inner_bottom_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 21:
                    display.blit(grass_inner_bottom_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                elif tile == 22:
                    display.blit(substrate_corner_top_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 23:
                    display.blit(substrate_corner_top_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 24:
                    display.blit(substrate_corner_bottom_right, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 25:
                    display.blit(substrate_corner_bottom_left, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                elif tile == 28:
                    die_tile.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif tile == 17:
                    display.blit(deep_underground, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))

                elif tile == 69:
                    goal_tile.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                if tile != 0 and tile != 69 and tile != 28:
                    tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x += 1
            y += 1

        for tile in goal_tile:
            if pygame.Rect.colliderect(player_rect, tile):
                goal = True
                player_rect.x, player_rect.y = 332, 175
                goal_tile = []
                die_tile = []
                v += 1
                if v >= len(maps):
                    v = 0
                level = read_map(maps[v])

        for tile in die_tile:
            if pygame.Rect.colliderect(player_rect, tile):
                player_rect.x, player_rect.y = 332, 175

        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 5
        if moving_left:
            player_movement[0] -= 5
        player_movement[1] += player_y_momentum
        player_y_momentum += 2
        if player_y_momentum > 6:
            player_y_momentum = 6
        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if player_movement[0] > 0 and collisions["bottom"]:
            if player_running_frame % 2 == 0:
                player_image = pygame.image.load(player_running[int(player_running_frame / 2)])
            if player_running_frame < 14:
                player_running_frame += 1
            elif player_running_frame >= 14:
                player_running_frame = 0
            elif not collisions["bottom"]:
                player_running_frame = 0

        elif player_movement[0] < 0 and collisions["bottom"]:
            if player_running_frame % 2 == 0:
                player_image = pygame.image.load(player_running[int(player_running_frame / 2)])
            if player_running_frame < 14:
                player_running_frame += 1
            elif player_running_frame >= 14:
                player_running_frame = 0
            elif not collisions["bottom"]:
                player_running_frame = 0

        if collisions["bottom"]:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1

        if player_movement[0] >= 0:
            display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
        else:
            display.blit(pygame.transform.flip(player_image, True, False),
                         (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:  # check for window quit
                pygame.quit()  # stop pygame
                sys.exit()  # stop script
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = True
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = True
                if event.key == K_UP or event.key == K_SPACE or event.key == K_w:
                    player_image = player_jump
                    if air_timer < 6:
                        player_y_momentum = -20
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
                    moved_left = True
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                    moved_left = False

        if player_movement[0] == 0 and player_movement[1] == 0:
            if not moved_left:
                player_image = pygame.image.load(player_idle[player_idle_frame])
            elif moved_left:
                player_idle_flipped = pygame.image.load(player_idle[player_idle_frame])
                player_image = pygame.transform.flip(player_idle_flipped, True, False)
            if player_idle_frame < 11:
                player_idle_frame += 1
            elif player_idle_frame >= 11:
                player_idle_frame = 0

        elif not player_movement[1] == 0 and collisions["bottom"]:
            if collisions["bottom"]:
                mid_air_time = 0
            mid_air_time += 1
            if mid_air_time == 5:
                player_image = pygame.image.load(player_mid_air[player_mid_air_frame])
                if player_mid_air_frame < 1:
                    player_mid_air_frame += 1
                elif player_mid_air_frame >= 1:
                    player_mid_air_frame = 0
                mid_air_time = 0

        draw_text(str(int(clock.get_fps())) + " FPS", (255, 255, 255), display, 20, 20)

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()  # update display
        clock.tick(60)  # maintain 60 fps
