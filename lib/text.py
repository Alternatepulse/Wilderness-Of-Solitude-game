import pygame


def draw_text(text, color, surface, x, y):
    font = pygame.font.SysFont(None, 20)
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)