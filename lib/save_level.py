import ctypes
import pygame
import sys
from lib.text import draw_text
from pygame.locals import *  # import pygame modules
from lib.map_loader import save_map


clock = pygame.time.Clock()  # set up the clock
pygame.init()  # initiate pygame
pygame.display.set_caption("Pygame Window")  # set the window name
user32 = ctypes.windll.user32
WINDOW_SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(WINDOW_SIZE, FULLSCREEN, 32)  # initiate screen
display = pygame.Surface((640, 360))
base_font = pygame.font.Font(None, 64)
save_level_bg = pygame.image.load("assets/map/background/save_level_bg.png")


def save(level):
    user_text = ""
    running = True
    while running:  # game loop
        display.blit(save_level_bg, (0, 0))

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:  # check for window quit
                pygame.quit()  # stop pygame
                sys.exit()  # stop script
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_BACKSPACE:
                    user_text = user_text[:-1]
                if event.key == K_RETURN and user_text != "":
                    save_map(level, user_text)
                    running = False
                if event.key != K_BACKSPACE and event.key != K_RETURN:
                    user_text += event.unicode
        text_surface = base_font.render(user_text, True, (255,255,255))
        display.blit(text_surface, ((display.get_width() / 2) - (text_surface.get_width() / 2), display.get_height() / 2))

        draw_text(str(int(clock.get_fps())) + " FPS", (255, 255, 255), display, 20, 20)

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()  # update display
        clock.tick(60)  # maintain 60 fps
    return user_text