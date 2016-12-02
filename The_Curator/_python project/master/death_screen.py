import pygame, sys, time, random, math, map, load
from pygame.locals import *

pygame.init()


def death_screen(window, window_width, window_height, bool):
    title_image = pygame.image.load("game_over.png")
    title_image_scaled = pygame.transform.scale(title_image, (window_width, window_height))
    menu = bool
    while menu is True:
        window.fill((142, 125, 75))
        window.blit(title_image_scaled, (0, 0))
        text_color = (255, 0, 0)
        mouse_over_color = (0, 0, 0)
        my_font = pygame.font.SysFont("Helvetica", 35, bold=True)
        label = my_font.render("Restart", 1, text_color)
        label_mouse_over = my_font.render("Restart", 1, mouse_over_color)
        label_width = label.get_rect().width
        label_height = label.get_rect().height
        label_center = label_width / 2
        center_width = window_width / 2 - label_center
        center_height = window_height / 2
        # Mouse position data
        mouse_pos = pygame.mouse.get_pos()
        # Split the date into x and y coordinates
        mouse_x, mouse_y = mouse_pos

        if center_width < mouse_x < center_width + label_width and \
           center_height < mouse_y < center_height + label_height:

            window.blit(label_mouse_over, (center_width, center_height))

        else:

            window.blit(label, (center_width, center_height))

        if pygame.event.get(MOUSEBUTTONDOWN):
            if center_width < mouse_x < center_width + label_width and \
               center_height < mouse_y < center_height + label_height:

                menu = False

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
