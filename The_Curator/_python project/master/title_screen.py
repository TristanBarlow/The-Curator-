import pygame, sys, time, random, math, map, load
from pygame.locals import *

pygame.init()


def title_screen(window, window_width, window_height, bool):
    title_image = pygame.image.load("TitleScreen.png")
    title_image_scaled = pygame.transform.scale(title_image, (window_width, window_height))
    menu = bool
    while menu is True:
        window.fill((142, 125, 75))
        window.blit(title_image_scaled, (0, 0))
        text_color = (255, 255, 255)
        mouse_over_color = (0, 0, 0)
        my_font = pygame.font.SysFont("Helvetica", 35, bold=True)
        label = my_font.render("Play Level 1", 1, text_color)
        label_mouse_over = my_font.render("Play Level 1", 1, mouse_over_color)
        label_2 = my_font.render("Play Level 2", 1, text_color)
        label_mouse_over_2 = my_font.render("Play Level 2", 1, mouse_over_color)
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

        if center_width < mouse_x < center_width + label_width and \
           center_height + 100 < mouse_y < center_height + label_height + 100:

            window.blit(label_mouse_over_2, (center_width, center_height + 100))

        else:
            window.blit(label_2, (center_width, center_height + 100))

        if pygame.event.get(MOUSEBUTTONDOWN):
            if center_width < mouse_x < center_width + label_width and \
               center_height + 100 < mouse_y < center_height + label_height + 100:

                level_1 = False
                menu = False

            if center_width < mouse_x < center_width + label_width and \
               center_height < mouse_y < center_height + label_height:

                level_1 = True
                menu = False

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    return level_1
