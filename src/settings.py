from cards import Resource, Development

FPS = 60
TITLE = 'Settlers'
BG_COLOUR = 58, 117, 163
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 50
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE
HEX_COLOUR = 255, 255, 255
BLACK = 0,0,0
WHITE = 255, 255, 255

CLAY = (255, 0, 0)
ORE = (190, 190, 190)
WHEAT = (255, 215, 0)
SHEEP = (124, 252, 0)
WOOD = (0, 100, 0)
SAND = (139, 69, 19)

PLAYERCOLOUR1 = (255, 0, 0)
PLAYERCOLOUR2 = (0, 0, 255)
PLAYERCOLOUR3 = (0, 255, 0)
PLAYERCOLOUR4 = (255, 255, 0)

ROAD = [Resource.Wood, Resource.Brick]
SETTLEMENT = [Resource.Wood, Resource.Brick, Resource.Sheep, Resource.Wheat]
