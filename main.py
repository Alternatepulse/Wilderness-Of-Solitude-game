import pygame
import sys
from lib.options import options_loop
from pygame.locals import *
from lib.text import draw_text
from lib.game import game_loop
import ctypes
from lib.editor import editor_loop

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

main_clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("Main menu")
screen = pygame.display.set_mode(screensize, FULLSCREEN, 32)
font = pygame.font.SysFont(None, 20)

display = pygame.Surface((640, 360))

bg = pygame.image.load("assets/map/background/main_bg.png")
button_play_inactive = pygame.image.load("assets/buttons/button_play_inactive.png")
button_play_active = pygame.image.load("assets/buttons/button_play_active.png")
button_options_inactive = pygame.image.load("assets/buttons/button_tutorial_inactive.png")
button_options_active = pygame.image.load("assets/buttons/button_tutorial_active.png")
button_exit_inactive = pygame.image.load("assets/buttons/button_quit_inactive.png")
button_exit_active = pygame.image.load("assets/buttons/button_quit_active.png")
button_editor_inactive = pygame.image.load("assets/buttons/button_editor_inactive.png")
button_editor_active = pygame.image.load("assets/buttons/button_editor_active.png")

click = False


def main_menu():

    volume = 0.2
    sound = pygame.mixer.Sound("assets/sound/Dreaming.wav")
    channel = sound.play()
    sound.set_volume(volume)

    while True:
        display.blit(bg, (0, 0))
        draw_text(str(int(main_clock.get_fps())) + " FPS", (255, 255, 255), display, 20, 20)
        screen.blit(pygame.transform.scale(display, screensize), (0, 0))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 50, 200, 50)
        button_2 = pygame.Rect(50, 120, 200, 50)
        button_3 = pygame.Rect(50, 190, 200, 50)
        button_4 = pygame.Rect(50, 260, 200, 50)
        if button_1.collidepoint(
                (int(mx / (user32.GetSystemMetrics(0) / 640)), int(my / (user32.GetSystemMetrics(0) / 640)))):
            if click:
                game_loop()
            else:
                display.blit(button_play_active, button_1)
        else:
            display.blit(button_play_inactive, button_1)
        if button_2.collidepoint(
                (int(mx / (user32.GetSystemMetrics(0) / 640)), int(my / (user32.GetSystemMetrics(0) / 640)))):
            if click:
                options_loop()
            else:
                display.blit(button_options_active, button_2)
        else:
            display.blit(button_options_inactive, button_2)
        if button_3.collidepoint(
                (int(mx / (user32.GetSystemMetrics(0) / 640)), int(my / (user32.GetSystemMetrics(0) / 640)))):
            if click:
                editor_loop()
            else:
                display.blit(button_editor_active, button_3)
        else:
            display.blit(button_editor_inactive, button_3)
        if button_4.collidepoint(
                (int(mx / (user32.GetSystemMetrics(0) / 640)), int(my / (user32.GetSystemMetrics(0) / 640)))):
            if click:
                pygame.quit()
                sys.exit()
            else:
                display.blit(button_exit_active, button_4)
        else:
            display.blit(button_exit_inactive, button_4)

        screen.blit(pygame.transform.scale(display, pygame.display.get_window_size()), (0, 0))
        pygame.display.update()
        main_clock.tick(60)


main_menu()
