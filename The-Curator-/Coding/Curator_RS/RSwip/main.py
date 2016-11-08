import math, pygame, sys, time, random
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Window dimensions
windowWidth = 1200
windowHeight = 800

# Declare control variables
moveX = 0.0
moveY = 0.0
lookLeft = False
playerPosX = windowWidth / 2 + 46
playerPosY = windowHeight / 2 + 43
mouseX = 0
mouseY = 0
firing = False

# for scaling assets to size
grassScale = 50
playerScale = 100
enemyScale = 100

# Usual stuff
window = pygame.display.set_mode((windowWidth, windowHeight))

grass = pygame.image.load('grass.png')
grass = pygame.transform.scale(grass, (grassScale, grassScale))
playerStill = pygame.image.load('curatorPlayer.png')
playerStill = pygame.transform.scale(playerStill, (playerScale, playerScale))
playerRifle = pygame.image.load('curatorPlayerRifleNew.png')
playerRifle = pygame.transform.scale(playerRifle, (playerScale, playerScale))

bullet = pygame.image.load('bullet2.png')
bullet = pygame.transform.scale(bullet, (20, 20))

swordup = pygame.image.load('swordup.png')
swordup = pygame.transform.scale(swordup, (playerScale, playerScale))
swordmove1 = pygame.image.load('swordmove1.png')
swordmove1 = pygame.transform.scale(swordmove1, (playerScale, playerScale))
swordmove2 = pygame.image.load('swordmove2.png')
swordmove2 = pygame.transform.scale(swordmove2, (playerScale, playerScale))
sworddown = pygame.image.load('sworddown.png')
sworddown = pygame.transform.scale(sworddown, (playerScale, playerScale))

enemy = pygame.image.load('dinosaur.png')
enemy = pygame.transform.scale(enemy, (enemyScale, enemyScale))

bullets = []
numberOfBullets = 0

bulletSpeed = 5

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = playerStill
        self.health = 100

    def health_bar(self):
        pygame.draw.rect(window,RED,(windowWidth/2, windowHeight/2, self.health/2, 5),)
        pygame.draw.rect(window,BLACK,(windowWidth/2, windowHeight/2, self.health/2, 5), 1)


class Camera():
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.image = image

    def update(self, offset_x, offset_y):
        window.blit(self.image, (self.x + offset_x, self.y + offset_y))


class Bullet(Camera):
    'Bullet'

    def __init__(self, bullet_pos_x, bullet_pos_y, direction_x, direction_y):
        Camera.__init__(self, bullet, x, y)
        self.x = bullet_pos_x - moveX
        self.y = bullet_pos_y - moveY
        self.dir_x = direction_x
        self.dir_y = direction_y
#        self.image = bullet
        self.rect = pygame.Rect(x, y, 200, 200)

    def moveBullet(self, dir_x, dir_y):
        self.x += dir_x * bulletSpeed
        self.y += dir_y * bulletSpeed

    def updateCollider(self):
        self.rect = pygame.Rect(self.x, self.y, 50, 50)


class Enemy(Camera):
    'Dinosaur'
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = enemy
        self.rect = pygame.Rect(x, y, 50, 50)
        self.health = 100


    def respawn(self):
        self.x = (random.randint(0, windowWidth) + random.randint(0, windowWidth) + random.randint(0, windowWidth)) / 3
        self.y = (random.randint(0, windowHeight) + random.randint(0, windowHeight) + random.randint(0, windowHeight)) / 3
        print('Kill')

    def updateCollider(self):
        self.rect = pygame.Rect(self.x, self.y, enemyScale, enemyScale)
        pygame.draw.rect(window, (0,0,0), self.rect, 5)

    def health_bar(self,  x, y):
        pygame.draw.rect(window, (255, 0, 0), (x, y - 10, 50, 50))
enemies = []
enemies.append(Enemy(random.randint(0, windowWidth), random.randint(0, windowWidth)))
enemies[0].updateCollider()

player_one = Player(windowWidth, windowHeight)


while True:

    # Move all bullets by each individual bullets stored dir_x, dir_y value
    for i in range(0, numberOfBullets):
        bullets[i].moveBullet(bullets[i].dir_x, bullets[i].dir_y)

        bullets[i].updateCollider()

        # Check if hit colliders
        if bullets[i].rect.colliderect(enemies[0].rect):
            print ('Hit')
            enemies[0].respawn()
            enemies[0].updateCollider()


    # Check for bullets exiting range of window
    for i in range(0, numberOfBullets):

        # Defining range of window
        if bullets[i].x < 0 + moveX or bullets[i].x > windowWidth + moveX or bullets[i].y < 0 + moveY or bullets[i].y > windowHeight + moveY:

            # Remove bullet[i] from list
            bullets.pop(i)
            numberOfBullets += -1
            print numberOfBullets

            # Need to break to exit for loop. It bugs out when the range size is changed mid loop
            break

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            (mouseX, mouseY) = pygame.mouse.get_pos()
            deltaX = mouseX - playerPosX
            deltaY = mouseY - playerPosY
            if deltaX < 0:
                lookLeft = True
            if deltaX > 0:
                lookLeft = False

        # Makes full auto fire, single clicks per bullet was boring. 1 bullet per frame currently. Can slow down later
        if event.type == pygame.MOUSEBUTTONDOWN:
            firing = True
        if event.type == pygame.MOUSEBUTTONUP:
            firing = False

    if firing:

        # Normalises the delta mouse position so the bullets vector length == 1
        # Used pythagoras formula
        normalisedX = deltaX / (math.sqrt((math.pow(deltaX, 2) + math.pow(deltaY, 2))))
        normalisedy = deltaY / (math.sqrt((math.pow(deltaX, 2) + math.pow(deltaY, 2))))

        # Adds a bullet to the scene at player position (adjust for gun pos) and in relative mouse click direction
        bullets.append(Bullet(playerPosX - 100, playerPosY -100, normalisedX, normalisedy))
        numberOfBullets += 1
        print numberOfBullets

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
    else:
        player = playerStill
    if keys[pygame.K_l]:
        player_one.health += -10
    pygame.mouse.get_pos()

    window.fill((255, 255, 255))

# Tiles the grass.png to fit the window, moveX and moveY are basically the player controls
    for x in range(0, windowWidth, grassScale):
        for y in range(0, windowHeight, grassScale):
            window.blit(grass, (x + moveX, y + moveY))

# Used to face player image left and right
    player = pygame.transform.flip(player, lookLeft, False)
    for i in range(0, numberOfBullets):
        window.blit(bullet, (bullets[i].x + moveX, bullets[i].y + moveY))
        #pygame.draw.rect(window, (0, 0, 0), (bullets[i].rect), 5)

# Displays player in middle of screen
    window.blit(player, (windowWidth / 2, windowHeight / 2))
    window.blit(enemy, (enemies[0].x + moveX, enemies[0].y + moveY))
    player_one.health_bar()
#    pygame.draw.rect(window, (0, 0, 0), (enemies[0].rect), 5)
    pygame.display.update()

