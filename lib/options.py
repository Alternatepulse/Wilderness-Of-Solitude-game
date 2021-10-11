import sys
from pygame.locals import *
from lib.text import draw_text
import ctypes
import pygame


def options_loop():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    main_clock = pygame.time.Clock()

    pygame.init()
    pygame.display.set_caption("options")
    screen = pygame.display.set_mode(screensize, FULLSCREEN, 32)

    display = pygame.Surface((640, 360))

    bg = pygame.image.load("./assets/map/background/options_bg.png")



    running = True
    while running:
        x, y = screen.get_size()
        display.blit(bg, (0, 0))
        screen.blit(pygame.transform.scale(display, screensize), (0, 0))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False


        screen.blit(pygame.transform.scale(display, pygame.display.get_window_size()), (0, 0))
        pygame.display.update()
        main_clock.tick(60)