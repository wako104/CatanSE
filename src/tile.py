from enum import Enum
from road import Road


# enum for all edges of a tile
class TileEdge(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    LEFT = 3
    RIGHT = 4
    BOTTOM_LEFT = 5
    BOTTOM_RIGHT = 6


# enum for all vertices of a tile
class TileVertex(Enum):
    TOP = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5
    BOTTOM = 6


class Tile:

    roads = dict()
    buildings = dict()

    def __init__(self):
        pass

# add road to specific tile edge
    def add_road(self, position: TileEdge, road: Road):
        self.roads[position] = road

# add building to specific vertex
    def add_building(self, position: TileVertex, building):
        self.buildings[position] = building
