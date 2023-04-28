import pygame

FPS = 60
TITLE = 'Settlers'
BG_COLOUR = 58, 117, 163
BG_COLOUR2 = 64, 123, 170
BG_COLOUR3 = 58, 116, 162
WIDTH = 1000
HEIGHT = 750
TILE_SIZE = 50
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE
HEX_COLOUR = 255, 255, 255
BLACK = 0,0,0
WHITE = 255, 255, 255
RED = 219, 46, 26
CLAY = (230,111,45)
ORE = (171,177,173)
WHEAT = (250,197,115)
SHEEP = (149,182,8)
WOOD = (133,94,66)
SAND = (218,211,150)

KNIGHT = (138, 137, 132)
DEVELOPMENTROAD = (0, 0, 0)
YEAROFPLENTY = (67, 191, 33)
MONOPOLY = (171, 76, 21)
VICTORYPOINT = (214, 180, 11)

PLAYERCOLOUR1 = (241,0,0)
PLAYERCOLOUR2 = (18,147,255)
PLAYERCOLOUR3 = (23,228,46)
PLAYERCOLOUR4 = (255, 165, 0)

#ROAD = [Resource.Wood, Resource.Brick]
# SETTLEMENT = [Resource.Wood, Resource.Brick, Resource.Sheep, Resource.Wheat]
ROAD = [WOOD, CLAY]
SETTLEMENT = [WOOD, CLAY, SHEEP, WHEAT]
CITY = [WHEAT, WHEAT, ORE, ORE, ORE]
DEVELOPMENT = [SHEEP, WHEAT, ORE]

# board tokens
A = 5
B = 2
C = 6
D = 3
E = 8
F = 10
G = 9
H = 12
I = 11
J = 4
K = 8
L = 10
M = 9
N = 4
O = 5
P = 6
Q = 3
R = 11

r_clay = pygame.image.load('../resources/r_clay.jpg')
r_ore = pygame.image.load('../resources/r_ore.jpg')
r_sheep = pygame.image.load('../resources/r_sheep.jpg')
r_wheat = pygame.image.load('../resources/r_wheat.jpg')
r_wood = pygame.image.load('../resources/r_wood.jpg')

d_knight = pygame.image.load("../resources/d_knight.png")
d_road = pygame.image.load("../resources/d_road.png")
d_yofp = pygame.image.load("../resources/d_yofp.png")
d_monopoly = pygame.image.load("../resources/d_monopoly.png")
d_victory_point = pygame.image.load("../resources/d_victory_point.png")
