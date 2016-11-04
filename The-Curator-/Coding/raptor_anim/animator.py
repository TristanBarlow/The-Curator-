import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()

WIDTH = 900
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))

standing = pygame.image.load('rap_side_stand.png')
run_one = pygame.image.load('rap_side_run1.png')
run_two = pygame.image.load('rap_side_run2.png')
run_thr = pygame.image.load('rap_side_run3.png')
run_fou = pygame.image.load('rap_side_run4.png')
run_fiv = pygame.image.load('rap_side_run5.png')

raptor_images = [standing, run_one, run_two, run_thr, run_fou, run_fiv]

animation_frame_step = 2


class Raptor():
    def __init__(self, image_list):
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = self.image_list[0]

    def standing(self):
        self.keyframe = 0
        self.animation_frame = 0
        self.image = self.image_list[0]

    def running(self):
        self.keyframe += 1

        if self.keyframe == animation_frame_step:

            self.keyframe = 0
            self.animation_frame += 1

            if self.animation_frame == 6:
                self.animation_frame = 1

            self.image = self.image_list[self.animation_frame]


raptor_demo = Raptor(raptor_images)

while True:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        raptor_demo.running()

        #if keys[pygame.K_SPACE]:
        #    raptor.running()
        #else:
        #    raptor.standing()

    window.fill((255, 255, 255))
    window.blit(raptor_demo.image, (0, 0))

    pygame.display.update()

    clock = pygame.time.Clock()
    clock.tick(60)