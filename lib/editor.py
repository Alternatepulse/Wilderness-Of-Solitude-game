import ctypes
import pygame
import sys
from lib.text import draw_text
from lib.map_loader import *
from lib.save_level import save

clock = pygame.time.Clock()  # set up the clock

from pygame.locals import *  # import pygame modules

pygame.init()  # initiate pygame

pygame.display.set_caption("Pygame Window")  # set the window name

user32 = ctypes.windll.user32
WINDOW_SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

screen = pygame.display.set_mode(WINDOW_SIZE, FULLSCREEN, 32)  # initiate screen

display = pygame.Surface((640, 360))

display_ratio = user32.GetSystemMetrics(0) / 640

true_scroll = [0, 0]
tile_list = [0]

grass_top = pygame.image.load("assets/map/jungle_tileset/grass_top.png")
tile_list.append(grass_top)
grass_top_left = pygame.image.load("assets/map/jungle_tileset/grass_top_left.png")
tile_list.append(grass_top_left)
grass_top_right = pygame.image.load("assets/map/jungle_tileset/grass_top_right.png")
tile_list.append(grass_top_right)
grass_left = pygame.image.load("assets/map/jungle_tileset/grass_left.png")
tile_list.append(grass_left)
grass_right = pygame.image.load("assets/map/jungle_tileset/grass_right.png")
tile_list.append(grass_right)
grass_bottom = pygame.image.load("assets/map/jungle_tileset/grass_bottom.png")
tile_list.append(grass_bottom)
grass_bottom_left = pygame.image.load("assets/map/jungle_tileset/grass_bottom_left.png")
tile_list.append(grass_bottom_left)
grass_bottom_right = pygame.image.load("assets/map/jungle_tileset/grass_bottom_right.png")
tile_list.append(grass_bottom_right)

substrate_top = pygame.image.load("assets/map/jungle_tileset/substrate_top.png")
tile_list.append(substrate_top)
substrate_top_left = pygame.image.load("assets/map/jungle_tileset/substrate_top_left.png")
tile_list.append(substrate_top_left)
substrate_top_right = pygame.image.load("assets/map/jungle_tileset/substrate_top_right.png")
tile_list.append(substrate_top_right)
substrate_left = pygame.image.load("assets/map/jungle_tileset/substrate_left.png")
tile_list.append(substrate_left)
substrate_right = pygame.image.load("assets/map/jungle_tileset/substrate_right.png")
tile_list.append(substrate_right)
substrate_bottom = pygame.image.load("assets/map/jungle_tileset/substrate_bottom.png")
tile_list.append(substrate_bottom)
substrate_bottom_left = pygame.image.load("assets/map/jungle_tileset/substrate_bottom_left.png")
tile_list.append(substrate_bottom_left)
substrate_bottom_right = pygame.image.load("assets/map/jungle_tileset/substrate_bottom_right.png")
tile_list.append(substrate_bottom_right)

deep_underground = pygame.image.load("assets/map/jungle_tileset/deep_underground.png")
tile_list.append(deep_underground)

grass_inner_top_right = pygame.image.load("assets/map/jungle_tileset/grass_inner_top_right.png")
tile_list.append(grass_inner_top_right)
grass_inner_top_left = pygame.image.load("assets/map/jungle_tileset/grass_inner_top_left.png")
tile_list.append(grass_inner_top_left)
grass_inner_bottom_right = pygame.image.load("assets/map/jungle_tileset/grass_inner_bottom_right.png")
tile_list.append(grass_inner_bottom_right)
grass_inner_bottom_left = pygame.image.load("assets/map/jungle_tileset/grass_inner_bottom_left.png")
tile_list.append(grass_inner_bottom_left)

substrate_corner_top_right = pygame.image.load("assets/map/jungle_tileset/substrate_corner_top_right.png")
tile_list.append(substrate_corner_top_right)
substrate_corner_top_left = pygame.image.load("assets/map/jungle_tileset/substrate_corner_top_left.png")
tile_list.append(substrate_corner_top_left)
substrate_corner_bottom_right = pygame.image.load("assets/map/jungle_tileset/substrate_corner_bottom_right.png")
tile_list.append(substrate_corner_bottom_right)
substrate_corner_bottom_left = pygame.image.load("assets/map/jungle_tileset/substrate_corner_bottom_left.png")
tile_list.append(substrate_corner_bottom_left)

picker_border = pygame.image.load("assets/map/jungle_tileset/block_picker_border.png")

TILE_SIZE = grass_top.get_width()

bg0_wip = pygame.image.load("assets/map/background/bg0.png")
bg0 = pygame.transform.scale(bg0_wip, WINDOW_SIZE)

bg1_wip = pygame.image.load("assets/map/background/bg1.png")
bg1 = pygame.transform.scale(bg1_wip, (8000, 350))

bg2_wip = pygame.image.load("assets/map/background/bg2.png")
bg2 = pygame.transform.scale(bg2_wip, (800, 350))

bg3_wip = pygame.image.load("assets/map/background/bg3.png")
bg3 = pygame.transform.scale(bg3_wip, (800, 350))

bg4_wip = pygame.image.load("assets/map/background/bg4.png")
bg4 = pygame.transform.scale(bg4_wip, (800, 350))

bg5_wip = pygame.image.load("assets/map/background/bg5.png")
bg5 = pygame.transform.scale(bg5_wip, (800, 350))

Y, N = "./Y", "./N"

maps = [Y, N]

def editor_loop():
    level = read_map("empty map")
    camera_x, camera_y = 500, 175
    moving_right, moving_left, moving_up, moving_down = False, False, False, False
    camera_move_speed = 2.5
    tile_selected = 1
    mouse_rel = 0
    place_block = False
    remove_block = False


    running = True
    while running:  # game loop
        display.fill((146, 244, 255))

        true_scroll[0] += ((camera_x - true_scroll[0] - 320) / 5)
        true_scroll[1] += ((camera_y - true_scroll[1] - 180) / 5)
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        display.blit(bg0, (0, 0))
        display.blit(bg1, (-300 - true_scroll[0], -50 - true_scroll[1]))
        display.blit(bg2, (-100 - true_scroll[0] / 10, -50 - true_scroll[1]))
        display.blit(bg3, (-100 - true_scroll[0] / 20, -50 - true_scroll[1]))
        display.blit(bg4, (-100 - true_scroll[0] / 30, -50 - true_scroll[1]))
        display.blit(bg5, (-100 - true_scroll[0] / 40, -50 - true_scroll[1]))

        tile_rects = []
        y = 0
        for row in level:
            x = 0
            for tile in row:
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if tile == 0:
                    pass
                elif tile == 1:
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

                elif tile == 17:
                    display.blit(deep_underground, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                x += 1
            y += 1

            if moving_right and moving_left:
                pass
            elif moving_right:
                camera_x += camera_move_speed
            elif moving_left:
                camera_x -= camera_move_speed

            if moving_up and moving_down:
                pass
            elif moving_up:
                camera_y -= camera_move_speed
            elif moving_down:
                camera_y += camera_move_speed

        active_cell_x, active_cell_y = 0, 0
        active_cell_image = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for rect in tile_rects:
            if pygame.Rect.collidepoint(rect, (mouse_x / display_ratio + scroll[0]),
                                        (mouse_y / display_ratio + scroll[1])):
                active_cell_x = int(rect.x / TILE_SIZE)
                active_cell_y = int(rect.y / TILE_SIZE)
                active_cell_image = level[active_cell_y][active_cell_x]

        if place_block:
            level[active_cell_y][active_cell_x] = tile_selected
        elif remove_block:
            level[active_cell_y][active_cell_x] = 0

        if tile_selected == 0:
            pass
        else:
            display.blit(tile_list[tile_selected], (display.get_width() - 50, 50))
            display.blit(picker_border, (display.get_width() - 53, 47))


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
                if event.key == K_UP or event.key == K_w:
                    moving_up = True
                if event.key == K_DOWN or event.key == K_s:
                    moving_down = True
                if event.key == K_g:
                    maps.insert(0, ("./" + save(level)))
                if event.key == K_c:
                    camera_x, camera_y = 500, 175
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False
                if event.key == K_UP or event.key == K_w:
                    moving_up = False
                if event.key == K_DOWN or event.key == K_s:
                    moving_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if tile_selected == len(tile_list) - 1:
                        tile_selected = 1
                    else:
                        tile_selected += 1
                elif event.button == 5:
                    if tile_selected == 1:
                        tile_selected = len(tile_list) - 1
                    else:
                        tile_selected -= 1
                if event.button == 1:
                    place_block = True
                elif event.button == 3:
                    remove_block = True
                elif event.button == 2:
                    tile_selected = active_cell_image
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button ==1:
                    place_block = False
                if event.button ==3:
                    remove_block = False


        draw_text(str(int(clock.get_fps())) + " FPS", (255, 255, 255), display, 20, 20)
        draw_text("left mouse: place block", (255, 255, 255),
                  display, 20, 80)
        draw_text("right mouse: remove block", (255, 255, 255),
                  display, 20, 90)
        draw_text("middle mouse: copy block", (255, 255, 255),
                  display, 20, 100)
        draw_text("scroll up: next block", (255, 255, 255),
                  display, 20, 110)
        draw_text("scroll down: previus block", (255, 255, 255),
                  display, 20, 120)
        draw_text("g: save map", (255, 255, 255),
                  display, 20, 130)
        draw_text("c: center camera", (255, 255, 255),
                  display, 20, 140)

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()  # update display
        clock.tick(60)  # maintain 60 fps