import pygame
tile_size = 128
PLAYER_SCALE = (100, 100)
RAPTOR_SCALE = (150, 150)

wall = pygame.image.load('Tile_Wall.png')
tile_wall = pygame.transform.scale(wall, (tile_size, tile_size))
floor = pygame.image.load('Cave_floor.png')
tile_floor = pygame.transform.scale(floor, (tile_size, tile_size))

player_standing = pygame.transform.scale(pygame.image.load('player_new_standing.png'), PLAYER_SCALE)
player_walking1 = pygame.transform.scale(pygame.image.load('player_walk_lfb.png'), PLAYER_SCALE)
player_walking2 = pygame.transform.scale(pygame.image.load('player_walk_lff.png'), PLAYER_SCALE)
player_jacket = pygame.transform.scale(pygame.image.load('player_side_jacket_reach.png'), PLAYER_SCALE)
player_rifle_stand = pygame.transform.scale(pygame.image.load('player_side_stand_rifle.png'), PLAYER_SCALE)
player_rifle_walk1 = pygame.transform.scale(pygame.image.load('player_side_run_lff_rifle.png'), PLAYER_SCALE)
player_rifle_walk2 = pygame.transform.scale(pygame.image.load('player_side_run_lfb_rifle.png'), PLAYER_SCALE)

raptor_standing = pygame.transform.scale(pygame.image.load('rap_side_stand.png'), RAPTOR_SCALE)
raptor_attack = pygame.transform.scale(pygame.image.load('rap_side_attack.png'), RAPTOR_SCALE)
raptor_dead = pygame.transform.scale(pygame.image.load('rap_dead.png'), RAPTOR_SCALE)
raptor_run1 = pygame.transform.scale(pygame.image.load('rap_side_run1.png'), RAPTOR_SCALE)
raptor_run2 = pygame.transform.scale(pygame.image.load('rap_side_run2.png'), RAPTOR_SCALE)
raptor_run3 = pygame.transform.scale(pygame.image.load('rap_side_run3.png'), RAPTOR_SCALE)
raptor_run4 = pygame.transform.scale(pygame.image.load('rap_side_run4.png'), RAPTOR_SCALE)
raptor_run5 = pygame.transform.scale(pygame.image.load('rap_side_run5.png'), RAPTOR_SCALE)

raptor_walk1 = raptor_run1
raptor_walk2 = raptor_run3
raptor_walk3 = raptor_run4

player_walking = [player_standing, player_walking1, player_walking2]
player_rifle_walking = [player_rifle_stand, player_rifle_walk1, player_rifle_walk2]
player_rifle_equip = [player_standing, player_jacket, player_rifle_stand]
player_rifle_holster = [player_rifle_stand, player_jacket, player_standing]

raptor_walking = [raptor_standing, raptor_walk1, raptor_walk2, raptor_walk3]
raptor_running = [raptor_standing, raptor_run1, raptor_run2, raptor_run3, raptor_run4, raptor_run5]
raptor_attack = [raptor_standing, raptor_standing, raptor_attack]
raptor_dead_list = [raptor_dead, raptor_dead]