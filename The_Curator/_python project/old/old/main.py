import pygame, sys, time, random
from pygame.locals import *

# wasd movement. Background obviously doesn't work properly, I was
# just experimenting with how to tile background images. I really want to
# figure out how they draw maps with letters without looking it up. Like:
# xxxxxxxxx
# xooooooox
# xooopooox
# xooooooox
# xxxxxxxxx
#
# Space bar brings up gun
# pygame has good mouse support functions, I have a plan with how to
# implement aiming, just haven't done it yet: pygame.math.vector2.normalise()
#
# I drew the pixel art guy about 1:00am after a long Thursday night at work so it's shit
# Tweed suit guy is a cool look for a museum curator though. obv with assult rifle
# The grass background is even worse. But good to figure out how to tile
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
# Declare control variables
moveX = 0.0
moveY = 0.0
lookLeft = False

# Window dimensions
windowWidth = 1000
windowHeight = 1000

# for scaling up shit pixel art to size
grassScale = 100
playerScale = 100

# Usual stuff
window = pygame.display.set_mode((windowWidth, windowHeight))

mouseX = 0
mouseY = 0
a = 0
grass = pygame.image.load('grass.png')
grass = pygame.transform.scale(grass, (grassScale, grassScale))
playerStill = pygame.image.load('curatorPlayer.png')
playerStill = pygame.transform.scale(playerStill, (playerScale, playerScale))
playerRifle = pygame.image.load('curatorPlayerRifleNew.png')
playerRifle = pygame.transform.scale(playerRifle, (playerScale, playerScale))

bullet = pygame.image.load('bullet.png')
bullet = pygame.transform.scale(bullet, (200, 200))

swordup = pygame.image.load('swordup.png')
swordup = pygame.transform.scale(swordup, (playerScale, playerScale))
swordmove1 = pygame.image.load('swordmove1.png')
swordmove1 = pygame.transform.scale(swordmove1, (playerScale, playerScale))
swordmove2 = pygame.image.load('swordmove2.png')
swordmove2 = pygame.transform.scale(swordmove2, (playerScale, playerScale))
sworddown = pygame.image.load('sworddown.png')
sworddown = pygame.transform.scale(sworddown, (playerScale, playerScale))


bullets = []
numberOfBullets = 0


bulletSpeed = 1000


class Bullet:
    'Bullet'
    def __init__(self, x, y, dirXX, dirYY):
        self.x = x
        self.y = y
        self.dirx = dirXX
        self.diry = dirYY
        self.image = bullet

    def moveBullet(self, dirX, dirY):
        self.x += dirX
        self.y += dirY
        #print self.x, self.y


while True:

    player = playerStill
    for i in range(0, numberOfBullets):
        bullets[i].moveBullet(bullets[i].dirx, bullets[i].diry)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            (mouseX, mouseY) = pygame.mouse.get_pos()
            playerPosX = windowWidth / 2 + 46
            playerPosY = windowHeight / 2 + 43
            deltaX = mouseX - playerPosX
            deltaY = mouseY - playerPosY
            if deltaX < 0:
                lookLeft = True
            if deltaX > 0:
                lookLeft = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('Fire')

            #bulletDir = (pygame.cmath.Vector2.normalise(playerPosX, playerPosY))


            bullets.append(Bullet(playerPosX - 100, playerPosY -110, 10, 0)) #deltaX, deltaY))
            numberOfBullets += 1



    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        moveY += 5
    if keys[pygame.K_s]:
        moveY += -5
    if keys[pygame.K_a]:
        moveX += 5
#        lookLeft = True     # Used to flip player image left and right later before blit
    if keys[pygame.K_d]:
        moveX += -5
#        lookLeft = False
    if keys[pygame.K_SPACE]:    # Swaps player image to gun aiming
        player = playerRifle
    if keys[pygame.K_7]:
        a += 1
        if a == 1:
            player = swordup
            pygame.time.wait(10)
        if a == 2:
            player = swordmove1
            pygame.time.wait(10)
        if a == 3:
             player = swordmove2
             pygame.time.wait(10)
        if a == 4:
            player = sworddown
            pygame.time.wait(10)
            a = 0

    if keys[pygame.K_1]:
        player = playerStill

    pygame.mouse.get_pos()

# Tiles the grass.png to fit the window, moveX and moveY are essentially the player controls
    for x in range(0, windowWidth, grassScale):
        for y in range(0, windowHeight, grassScale):
            window.blit(grass, (x + moveX, y + moveY))

# Used to face player image left and right

    player = pygame.transform.flip(player, lookLeft, False)

    for i in range(0, numberOfBullets):
        window.blit(bullet, (bullets[i].x + moveX, bullets[i].y + moveY))

    # Displays player in middle of screen
    window.blit(player, (windowWidth / 2, windowHeight / 2))

    pygame.display.update()