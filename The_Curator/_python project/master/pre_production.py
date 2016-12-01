import pygame, sys, time, random, math, map, load, title_screen, death_screen
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800  # DO NOT CHANGE
WINDOW_HEIGHT = 600  # DO NOT CHANGE

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Map:
    """ This class Handles movement, map generation, colliders and checks whether the
    player has completed the map."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall_list = []
        self.speed = 4
        self.level_1 = None
        self.end_tile_x = x
        self.end_tile_y = y
        self.map_array = None

    # controls
    def move_up(self):
        self.y += self.speed

    def move_down(self):
        self.y += -self.speed

    def move_left(self):
        self.x += self.speed

    def move_right(self):
        self.x += -self.speed

    # Displays map onscreen and handles colliders
    def wall_blit(self, tile_x, tile_y):
        WINDOW.blit(load.tile_wall, (tile_x + self.x, self.y + tile_y))
        collision = pygame.Rect((tile_x + self.x, self.y + tile_y), (load.tile_size, load.tile_size))
        self.wall_list.append(collision)

    def floor_blit(self, tile_x, tile_y):
        WINDOW.blit(load.tile_floor, (tile_x + self.x, tile_y + self.y))

    def end_tile(self, tile_x, tile_y):
        pygame.draw.rect(WINDOW, (173, 216, 230),
                         ((tile_x + self.x, self.y + tile_y), (load.tile_size, load.tile_size)))
        self.end_tile_x = tile_x + self.x
        self.end_tile_y = self.y + tile_y

    def update_map(self):
        if self.level_1:
            self.map_array = map.map_array_sneak
        else:
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
        if player.rect.collidelistall(self.wall_list):
            if last_key == 'w':
                self.y += -self.speed
            if last_key == 'a':
                self.x += -self.speed
            if last_key == 's':
                self.y += self.speed
            if last_key == 'd':
                self.x += self.speed
            else:
                pass
        self.wall_list = []

    def level_complete(self):
        if self.end_tile_x < player.x < self.end_tile_x + load.tile_size:
            if self.end_tile_y < player.y < self.end_tile_y + load.tile_size:
                self.level_1 = False


class Actor:
    """Super class for shared fields of player and raptors"""
    def __init__(self, image_list, x, y):
        self.x = x
        self.y = y

        # for animation
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = self.image_list[0]
        self.look_left = True
        self.moving = True
        self.health = 100
        self.dead = False

    def animator(asset):
        """Sprite animation function using keyframes"""
        ANIMATION_FRAME_STEP = 10
        if not asset.moving:
            asset.animation_frame = 0
        else:
            asset.keyframe += 1
            if asset.keyframe == ANIMATION_FRAME_STEP:
                asset.keyframe = 0
                asset.animation_frame += 1
            if asset.animation_frame >= asset.image_list.__len__():
                asset.animation_frame = 1
        player.check_rifle_equipped(asset)
        return asset.image_list[asset.animation_frame]

    def standing(self):
        # resets animation fields so that subsequent animation begins from first frame
        self.keyframe = 0
        self.animation_frame = 1
        self.image = self.image_list[0]

    def health_bar(self, level_map):
        pygame.draw.rect(WINDOW, (255, 0, 0), (self.x + level_map.x, self.y + level_map.y, self.health, 5))


class Bullet:
    """Bullet class"""
    def __init__(self, player_position, bullet_direction):
        self.x = player_position[0]
        self.y = player_position[1]
        self.direction = bullet_direction
        self.bullet_size = 10
        self.bullet_speed = 100
        self.bullet_colour = 0, 0, 0
        self.rect = pygame.Rect(self.x, self.y, self.bullet_size, self.bullet_size)

    def fire_bullet(self):
        """instantiates bullet list"""
        bullets.append(Bullet((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (normalised_x, normalised_y)))
        enemies[enemies.__len__() - 1].image_list = load.raptor_dead_list

    def move_bullet(self, i, enemies_list):
        self.x += self.direction[0] * self.bullet_speed
        self.y += self.direction[1] * self.bullet_speed

        # removes bullet from game when off screen
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT:
            bullets.pop(i)

        for enemy in enemies_list:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= 25
                if enemy.health < 0:
                    enemy.image_list = load.raptor_dead_list
                    enemy.moving = False
                    enemy.health = 0
                    enemy.dead = True

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
        self.health = 100

    def equip_weapon(self):
        """toggles equip/holster image list and starts the animation"""
        if not level_map.level_1:
            self.equip_rifle_animation = True
            if self.image_list == load.player_walking:
                self.image_list = load.player_rifle_equip
            elif self.image_list == load.player_rifle_walking:
                self.image_list = load.player_rifle_holster

    def face_player_towards_cursor(self, mouse_x):
        """checks mouse position against player position and faces player towards cursor"""
        delta_x = mouse_x - self.x
        if delta_x < 0:
            return True
        else:
            return False

    def check_rifle_equipped(self, asset):
        """checks for end of rifle equip animation and sets the subsequent image_list"""
        if asset.image_list == load.player_rifle_equip and asset.animation_frame == 2:  # final animation frame
            asset.image_list = load.player_rifle_walking
            player.equip_rifle_animation = False
        if asset.image_list == load.player_rifle_holster and asset.animation_frame == 2:  # final animation frame
            asset.image_list = load.player_walking
            player.equip_rifle_animation = False


class Raptor(Actor):
    """Raptor class"""
    def __init__(self, image_list, x, y):
        Actor.__init__(self, image_list, x, y)
        self.attacking = False
        self.rect = pygame.Rect(self.x, self.y, load.RAPTOR_SCALE[0], load.RAPTOR_SCALE[1])
        self.attack_distance = 20
        self.raptor_speed = 7

    def update_collider(self, map_level):
        self.rect = pygame.Rect(self.x + map_level.x, self.y + map_level.y, load.RAPTOR_SCALE[0], load.RAPTOR_SCALE[1])

    def advance(self, map_level):
        # finds enemy/player direction and adjusts figures for movement
        difference_x = player.x - self.x - map_level.x
        difference_y = player.y - self.y - map_level.y

        if not self.dead:
            if self.attacking:
                player.health -= 1
                self.raptor_speed = 2

            # stops divide by zero error
            if math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))) > self.attack_distance:
                # calculates normal vector using pythagorus formula
                normalised_x = difference_x / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
                normalised_y = difference_y / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
                self.x += normalised_x * self.raptor_speed
                self.y += normalised_y * self.raptor_speed
            else:
                # Begin attacking when enemy is close enough
                self.attacking = True
                self.image_list = load.raptor_attack

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

    def patrol(self):
        # moves enemy between positions stored in a list
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

# initiate patrolling enemies list
raptor_patrol_positions_one = [(500, 200), (500, 1200)]
raptor_patrol_positions_two = [(1000, 700), (1500, 700), (1500, 100), (1000, 100)]
patrol_speed_one = 200
patrol_speed_two = 100
patrolling_enemies = [PatrollingRaptor(load.raptor_walking, raptor_patrol_positions_one, patrol_speed_one,
                                       raptor_patrol_positions_one[0][0], raptor_patrol_positions_one[0][1]),
                      PatrollingRaptor(load.raptor_walking, raptor_patrol_positions_two, patrol_speed_two,
                                       raptor_patrol_positions_two[0][0], raptor_patrol_positions_two[0][1])]

print 'wasd controls, e to equip/holster weapon, player faces mouse cursor'


def game_loop():
    mouse_position = (0, 0)
    key_pressed = None
    next_control = None
    spawn_timer = 0
    spawn_time = 150

    while not player.dead:
        WINDOW.fill((100, 100, 100))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                mouse_position = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and player.image_list == load.player_rifle_walking:
                mouse_delta_x = mouse_position[0] - player.x
                mouse_delta_y = mouse_position[1] - player.y

                # normalises player/mouse vector for bullet direction
                normalised_x = mouse_delta_x / (math.sqrt((math.pow(mouse_delta_x, 2) + math.pow(mouse_delta_y, 2))))
                normalised_y = mouse_delta_y / (math.sqrt((math.pow(mouse_delta_x, 2) + math.pow(mouse_delta_y, 2))))

                bullets.append(Bullet((player.x, player.y), (normalised_x, normalised_y)))

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

        # check timer to spawn. Provided level 1 is complete
        if not level_map.level_1:
            if spawn_timer == spawn_time:
                enemies.append(
                    Raptor(load.raptor_running, random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
                spawn_timer = 0
            else:
                spawn_timer += 1

        level_map.update_collider(key_pressed)
        level_map.update_map()

        if level_map.level_1:
            for raptor in patrolling_enemies:
                raptor.patrol()
                WINDOW.blit(Actor.animator(raptor), (raptor.x + level_map.x, raptor.y + level_map.y))

        for enemy in enemies:
            enemy.update_collider(level_map)
            if enemy.rect.colliderect(player.rect) and not enemy.dead:
                player.health -= 1
                if player.health < 0:
                    player.dead = True

            enemy.advance(level_map)
            enemy.image = pygame.transform.flip(Actor.animator(enemy), enemy.look_left, False)
            if enemy.health > 0:
                enemy.health_bar(level_map)
            WINDOW.blit(enemy.image, (enemy.x + level_map.x, enemy.y + level_map.y))

        player.image = Actor.animator(player)
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

        level_map.level_complete()

        pygame.draw.rect(WINDOW, (255, 0, 0), (0, 20, player.health * 2, 10))

        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(120)
    return True


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    enemies = []

    # create map
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
                'e': player.equip_weapon}

    # TITLE SCREEN LOOP set 4th argument to False to not get title screen.
    level_map.level_1 = title_screen.title_screen(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT, True)

    # When title screen ends it continues
    if game_loop():
        death_screen.death_screen(WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT, True)
