import pygame, sys, time, random, math, map, load
from pygame.locals import *
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def death_screen(WINDOW,WINDOW_WIDTH,WINDOW_HEIGHT,Bool):
    title_image = pygame.image.load("gameover.png")
    title_image_scaled = pygame.transform.scale(title_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    Menu = Bool
    while Menu is True:
        WINDOW.fill((142,125,75))
        WINDOW.blit(title_image_scaled,(0,0))
        textColor = (255,255,255)
        mouseOverColor = (0,0,0)
        myfont = pygame.font.SysFont("Helvetica", 35, bold=True)
        label = myfont.render("Restart", 1, textColor)
        label_mouseover = myfont.render("Restart", 1, mouseOverColor)
        label_width = label.get_rect().width
        label_height = label.get_rect().height
        label_center = label_width / 2
        center_width = WINDOW_WIDTH / 2 - label_center
        center_height = WINDOW_HEIGHT / 2
        # Mouse position data
        MOUSE_POS = pygame.mouse.get_pos()
        # Split the date into x and y coordinates
        mouse_x, mouse_y = MOUSE_POS
        if center_width < mouse_x < center_width + label_width and\
                                center_height < mouse_y < center_height + label_height:
            WINDOW.blit(label_mouseover, (center_width, center_height))
        else:
            WINDOW.blit(label, (center_width,center_height))

        if pygame.event.get(MOUSEBUTTONDOWN):
            if center_width < mouse_x < center_width + label_width and\
                                            center_height< mouse_y < center_height + label_height:
                Menu = False




        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    return True