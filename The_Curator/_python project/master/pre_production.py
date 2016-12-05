import pygame
import sys
import random
import map
import load
import math
import title_screen
import winsound
import pygame.mixer
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800  # DO NOT CHANGE
WINDOW_HEIGHT = 600  # DO NOT CHANGE

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Map:
    """This class Handles movement, map generation, colliders and the game state."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collider_wall_list = []
        self.speed = 4
        self.game_state = 0
        self.end_tile_x = x
        self.end_tile_y = y
        self.collider_range = 150
        self.map_array = None

    def move_up(self):
        self.y += self.speed

    def move_down(self):
        self.y -= self.speed

    def move_left(self):
        self.x += self.speed

    def move_right(self):
        self.x -= self.speed

    def wall_blit(self, tile_x, tile_y):
        """Blits the wall image and adds the rect of the wall to the list if its within a certain range
          of the player."""
        WINDOW.blit(load.tile_wall, (tile_x + self.x, self.y + tile_y))
        collision = pygame.Rect((tile_x + self.x, self.y + tile_y), (load.tile_size, load.tile_size))

        # Checks whether the current wall is within collider_range, if it is adds the wall_rect to the wall_list.
        if (tile_x + self.x - self.collider_range) < player.x < (tile_x + self.x + self.collider_range) and \
                                (tile_y + self.y - self.collider_range) < player.y < (
                                tile_y + self.y + self.collider_range):
            self.collider_wall_list.append(collision)

    def floor_blit(self, tile_x, tile_y):
        """Simply blits the floor tile when called."""
        WINDOW.blit(load.tile_floor, (tile_x + self.x, tile_y + self.y))

    def end_tile(self, tile_x, tile_y):
        """When called, it will place a blue tile where it is called. It also stores the x and y co-ords
        for later use."""
        pygame.draw.rect(WINDOW, (173, 216, 230),
                         ((tile_x + self.x, self.y + tile_y), (load.tile_size, load.tile_size)))
        self.end_tile_x = tile_x + self.x
        self.end_tile_y = self.y + tile_y

    def update_map(self):
        """Handles map generation, takes an array and cycles through and executes different functions dependent on
        value in the array."""
        if self.game_state == 1:
            self.map_array = map.map_array_sneak
        if self.game_state == 2:
            self.map_array = map.map_array_swarm
        tile_y = 0
        tile_x = 0
        map_d = {0: self.floor_blit, 1: self.wall_blit, 2: 0, 3: self.end_tile, 9: 0}
        for tile in self.map_array:
            if tile == 2:
                tile_y += load.tile_size
                tile_x = 0
            elif tile == 9:
                tile_x += load.tile_size
            else:
                command = map_d[tile]
                command(tile_x, tile_y)
                tile_x += load.tile_size

    def update_collider(self, last_key):
        """Cycles through the list of rects and if they collide will reverse the last key pressed and then clears the
        wall list afterwards."""
        if player.rect.collidelistall(self.collider_wall_list):
            if last_key == 'w':
                self.y -= self.speed
            if last_key == 'a':
                self.x -= self.speed
            if last_key == 's':
                self.y += self.speed
            if last_key == 'd':
                self.x += self.speed
        self.collider_wall_list = []

    def level_complete(self):
        """If the player is within the co-ords of the end_tile the next level will initiate."""
        if self.end_tile_x < player.x < self.end_tile_x + load.tile_size and \
                                self.end_tile_y < player.y < self.end_tile_y + load.tile_size:
            self.game_state += 1
            self.x = 0
            self.y = 0

            # Used winsound instead, so it stays on the line until sound complete
            winsound.PlaySound('teleport.wav', winsound.SND_FILENAME)


class Actor:
    """Super class for shared fields of player and raptors"""

    def __init__(self, image_list, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.dead = False

        # for animation
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = self.image_list[0]
        self.look_left = True
        self.moving = True

    def animator(self):
        """Sprite animation function using keyframes"""
        ANIMATION_FRAME_STEP = 10
        if not self.moving:
            self.animation_frame = 0
        else:
            self.keyframe += 1
            if self.keyframe == ANIMATION_FRAME_STEP:
                self.keyframe = 0
                self.animation_frame += 1
            if self.animation_frame >= self.image_list.__len__():
                self.animation_frame = 1
        player.check_rifle_equipped()
        return self.image_list[self.animation_frame]

    def standing(self):
        """Resets animation fields so that subsequent animation begins from first frame"""
        self.keyframe = 0
        self.animation_frame = 1
        self.image = self.image_list[0]

    def health_bar(self, map_level):
        """Displays health bar dependent on health, (not player health bar)"""
        if self.health > 100:
            health_bar_length = self.health / 10.0
        else:
            health_bar_length = self.health
        pygame.draw.rect(WINDOW, (255, 0, 0), (self.x + map_level.x, self.y + map_level.y, health_bar_length, 5))


class Bullet:
    """Bullet class"""

    def __init__(self, player_position, bullet_direction):
        self.x = player_position[0]
        self.y = player_position[1]
        self.normalised_x = 0
        self.normalised_y = 0
        self.direction = bullet_direction
        self.bullet_size = 10
        self.bullet_speed = 100
        self.bullet_colour = 0, 0, 0
        self.rect = pygame.Rect(self.x, self.y, self.bullet_size, self.bullet_size)

    def fire_bullet(self):
        """instantiates bullet list"""
        bullets.append(Bullet((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (self.normalised_x, self.normalised_y)))
        enemies[enemies.__len__() - 1].image_list = load.raptor_dead_list

    def move_bullet(self, i, enemies_list):
        """Moves the bullet, also detects if the bullet is off screen if so pops it. Also it checks for bullet
        collisions with enemies."""
        self.x += self.direction[0] * self.bullet_speed
        self.y += self.direction[1] * self.bullet_speed

        # removes bullet from game when off screen
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT:
            bullets.pop(i)

        # Checks for bullets colliding with enemies.
        for enemy in enemies_list:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= 25
                if enemy.health < 0 and not enemy.been_killed:
                    enemy.image_list = load.raptor_dead_list
                    enemy.moving = False
                    enemy.health = 0
                    enemy.dead = True
                    load.raptor_death.play()
                    enemy.been_killed = True

    def update_collider(self):
        self.rect = pygame.Rect(self.x, self.y, self.bullet_size, self.bullet_size)

    def draw_bullet(self):
        pygame.draw.rect(WINDOW, self.bullet_colour, self.rect)


class Player(Actor):
    """player class"""

    def __init__(self, image_list, x, y):
        Actor.__init__(self, image_list, x, y)
        self.equip_rifle_animation = False
        self.REAL_PLAYER_SIZE = (40, 90)
        self.rect = pygame.Rect((self.x + 25, self.y + 5), self.REAL_PLAYER_SIZE)

        # Re initialises health so we can give the player more health for testing.
        self.health = 100

    def equip_weapon(self):
        """toggles equip/holster image list and starts the animation"""
        if level_map.game_state == 2:
            self.equip_rifle_animation = True
            if self.image_list == load.player_walking:
                self.image_list = load.player_rifle_equip
            elif self.image_list == load.player_rifle_walking:
                self.image_list = load.player_rifle_holster
            load.equip.play()

    def face_player_towards_cursor(self, mouse_x):
        """checks mouse position against player position and faces player towards cursor"""
        delta_x = mouse_x - self.x
        if delta_x < 0:
            return True
        else:
            return False

    def check_rifle_equipped(self):
        """checks for end of rifle equip animation and sets the subsequent image_list"""

        # final animation frame
        if self.animation_frame == 2:
            if self.image_list == load.player_rifle_equip:
                self.image_list = load.player_rifle_walking
                player.equip_rifle_animation = False
            if self.image_list == load.player_rifle_holster:
                self.image_list = load.player_walking
                player.equip_rifle_animation = False

    def refill_health(self):
        """ A function for testing purposes, restores players health"""
        self.health = 100


class Raptor(Actor):
    """Raptor class"""

    def __init__(self, image_list, x, y):
        Actor.__init__(self, image_list, x, y)
        self.attacking = False
        self.rect = pygame.Rect(self.x, self.y, load.RAPTOR_SCALE[0], load.RAPTOR_SCALE[1])
        self.attack_distance = 20
        self.raptor_speed = 7
        self.damage = 1
        self.normalised_x = 0
        self.normalised_y = 0
        self.been_killed = False

    def update_collider(self, map_level):
        self.rect = pygame.Rect(self.x + map_level.x, self.y + map_level.y, load.RAPTOR_SCALE[0], load.RAPTOR_SCALE[1])

    def advance(self, map_level):
        """Moves the raptors towards the player and starts attacking animation and dealing the player damage"""
        # finds enemy/player direction and adjusts figures for movement
        difference_x = player.x - self.x - map_level.x
        difference_y = player.y - self.y - map_level.y

        if not self.dead:
            if self.attacking:
                player.health -= self.damage
                self.raptor_speed = 2

            # stops divide by zero error
            if math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))) > self.attack_distance:

                # calculates normal vector using pythagoras formula
                self.normalised_x = difference_x / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
                self.normalised_y = difference_y / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
                self.x += self.normalised_x * self.raptor_speed
                self.y += self.normalised_y * self.raptor_speed
            else:

                # Begin attacking when enemy is close enough
                self.attacking = True
                self.image_list = load.raptor_attacking

            # faces raptor image in direction of movement
            if difference_x < 0:
                self.look_left = True
            else:
                self.look_left = False


class PatrollingRaptor(Raptor):
    """sub class for just the sneak section enemies"""

    def __init__(self, image_list, patrolling_position_list, patrol_speed, x, y):
        Raptor.__init__(self, image_list, x, y)
        self.patrol_position_list = patrolling_position_list
        self.patrol_timer = 0
        self.patrol_index = 0
        self.next_waypoint = 1
        self.patrol_speed = patrol_speed
        self.detection_radius = 150
        self.detected_player = False
        self.detected_attack_speed = 12
        self.damage = 50

    def patrol(self):
        """moves enemy between positions stored in a list"""
        if (self.x, self.y) == self.patrol_position_list[self.next_waypoint]:
            self.patrol_index += 1

        if self.patrol_index == self.patrol_position_list.__len__():
            self.patrol_index = 0

        self.next_waypoint = self.patrol_index + 1

        if self.next_waypoint == self.patrol_position_list.__len__():
            self.next_waypoint = 0

        patrol_path_x = self.patrol_position_list[self.next_waypoint][0] - self.patrol_position_list[self.patrol_index][
            0]
        patrol_path_y = self.patrol_position_list[self.next_waypoint][1] - self.patrol_position_list[self.patrol_index][
            1]
        travel_step_x = patrol_path_x / self.patrol_speed
        travel_step_y = patrol_path_y / self.patrol_speed

        self.x += travel_step_x
        self.y += travel_step_y

    def detect_player(self, map_level):
        """finds enemy/player direction and adjusts figures for movement"""
        difference_x = player.x - self.x - map_level.x
        difference_y = player.y - self.y - map_level.y

        # stops divide by zero error
        if math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))) < self.detection_radius:
            self.raptor_speed = self.detected_attack_speed
            self.detected_player = True
            return True
        else:
            return False


class RaptorOverlord(Raptor):
    """Subclass for the unstoppable Raptor Overlord, GOOD LUCK!"""
    def __init__(self):
        Raptor.__init__(self, load.overload_walking, 100, 100)
        self.health = 5000
        self.raptor_speed = 6
        self.damage = 200

    def update_collider(self, map_level):
        self.rect = pygame.Rect(self.x + map_level.x, self.y + map_level.y, load.OVERLORD_SCALE[0], load.OVERLORD_SCALE[1])


# initiate patrolling enemies list
raptor_patrol_positions_one = [(500, 200), (500, 1200)]
raptor_patrol_positions_two = [(1000, 700), (1500, 700), (1500, 100), (1000, 100)]
PATROL_ONE_SPEED = 200
PATROL_TWO_SPEED = 100

print 'wasd controls, e to equip/holster weapon, player faces mouse cursor'

# Initialises map.
level_map = Map(200, -470)

while True:

    # Initialises and displays titlescreen
    if level_map.game_state == 0:

        # Create list of enemies
        enemies = []

        # Create list of patrolling raptor instances
        patrolling_enemies = [PatrollingRaptor(load.raptor_walking, raptor_patrol_positions_one, PATROL_ONE_SPEED,
                                               raptor_patrol_positions_one[0][0], raptor_patrol_positions_one[0][1]),
                              PatrollingRaptor(load.raptor_walking, raptor_patrol_positions_two, PATROL_TWO_SPEED,
                                               raptor_patrol_positions_two[0][0], raptor_patrol_positions_two[0][1])]

        # create map at the start point for level one.
        level_map = Map(200, -470)

        # create player
        player = Player(load.player_walking, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        # creates bullet list
        bullets = []

        # Controls dictionary
        controls = {'w': level_map.move_up,
                    's': level_map.move_down,
                    'a': level_map.move_left,
                    'd': level_map.move_right,
                    'e': player.equip_weapon,
                    'q': player.refill_health}

        # Initialises variables required in the game loop.
        mouse_position = (0, 0)
        key_pressed = None
        next_control = None
        spawn_timer = 0
        spawn_time = 100
        enemy_counter = 0
        DETECTION_THICKNESS = 4
        DETECTION_ADJUSTMENT = load.RAPTOR_SCALE[0] / 2
        patrol_rap_growl = True

        # Bool for if overlord is currently in game
        overlord = False

        # Sends to file title_screen, which has separate event loop( reduces the size of the main loop )
        level_map.game_state = title_screen.screen(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT, "TitleScreen.png")
        winsound.PlaySound('teleport.wav', winsound.SND_FILENAME)


    WINDOW.fill((100, 100, 100))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Keeps mouse_position updated
        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            mouse_position = pygame.mouse.get_pos()

        # Creates bullet instance, travelling in direction towards the mouse away from the player
        if event.type == pygame.MOUSEBUTTONDOWN and player.image_list == load.player_rifle_walking:
            mouse_delta_x = mouse_position[0] - player.x
            mouse_delta_y = mouse_position[1] - player.y

            # normalises player/mouse vector for bullet direction
            normalised_x = mouse_delta_x / (math.sqrt((math.pow(mouse_delta_x, 2) + math.pow(mouse_delta_y, 2))))
            normalised_y = mouse_delta_y / (math.sqrt((math.pow(mouse_delta_x, 2) + math.pow(mouse_delta_y, 2))))

            # Adds instance of bullet to list
            bullets.append(Bullet((player.x, player.y), (normalised_x, normalised_y)))
            load.gunshot.play()

        # controls
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key)
            if key_pressed in controls:
                player.moving = True
                next_control = controls[key_pressed]

        elif event.type == pygame.KEYUP:
            next_control = None

    # controls to run every frame
    if next_control is not None:
        next_control()

    # to allow rifle equip animation without interruption
    elif not player.equip_rifle_animation:
        player.moving = False

    # check for death
    if player.health < 0:
        player.dead = True

    # check timer to spawn. Provided game state is level 2. Spawns overlord after 10 enemies have been spawned.
    if level_map.game_state == 2:
        if spawn_timer == spawn_time:
            enemy_counter += 1
            if enemy_counter < 10:
                enemies.append(
                    Raptor(load.raptor_running, random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
                load.raptor_alive.play()

            # Spawns overlord after 10 enemies have been spawned.
            elif enemy_counter == 10:
                overlord = True
                enemies.append(RaptorOverlord())

            spawn_timer = 0
        else:
            spawn_timer += 1

    # If the player is on level 1 or 2 it will update the map and colliders.
    if level_map.game_state == 1 or level_map.game_state == 2:
        level_map.update_collider(key_pressed)
        level_map.update_map()
    if overlord:
        load.overload_noise.play()

    if level_map.game_state == 1:
        for raptor in patrolling_enemies:

            # Patrols raptor when player is not detected.
            if not raptor.detected_player:
                raptor.patrol()
            WINDOW.blit(raptor.animator(), (raptor.x + level_map.x, raptor.y + level_map.y))

            # If detected raptor will move toward player.
            if raptor.detect_player(level_map):
                raptor.advance(level_map)
                if patrol_rap_growl:
                    load.raptor_alive.play()
                    patrol_rap_growl = False

    for enemy in enemies:

        # Updates enemy colliders and then it checks if next to play and deals damage if true.
        enemy.update_collider(level_map)
        if enemy.rect.colliderect(player.rect) and not enemy.dead:
            player.health -= enemy.damage

        # Moves enemies advance towards player and and if their health is < 0 removes health bar.
        enemy.advance(level_map)
        enemy.image = pygame.transform.flip(enemy.animator(), enemy.look_left, False)
        if enemy.health > 0:
            enemy.health_bar(level_map)
        WINDOW.blit(enemy.image, (enemy.x + level_map.x, enemy.y + level_map.y))

    player.image = player.animator()
    if player.face_player_towards_cursor(mouse_position[0]):
        WINDOW.blit(pygame.transform.flip(player.image, True, False), (player.x, player.y))
    else:
        WINDOW.blit(player.image, (player.x, player.y))

    # Bullet stuff
    counter = 0
    for bullet in bullets:
        bullet.move_bullet(counter, enemies)
        bullet.update_collider()
        bullet.draw_bullet()
        counter += 1

    # Checks if the player has reached the end of level 1
    if level_map.game_state == 1:
        level_map.level_complete()

    # Checks if player is dead, if so plays death music and shows deathscreen.
    if player.health < 0:
        load.death.play()
        title_screen.screen(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT,"game_over.png" )
        level_map.game_state = 0

    # draws player health bar
    pygame.draw.rect(WINDOW, (255, 0, 0), (0, 20, player.health * 2, 10))

    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(120)
