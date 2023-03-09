import math
import pygame
import random

from settings import *
from building import Settlement


class Board:
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.tile_size = TILESIZE
        self.width = math.sqrt(3) * self.tile_size
        self.height = 2 * self.tile_size
        self.tiles = []
        self.tiles += [CLAY, ORE] * 3
        self.tiles += [WHEAT, SHEEP, WOOD] * 4
        self.tiles += [SAND]
        random.shuffle(self.tiles)
        self.unique_v = []
        self.location_materials = {}
        self.existing_settlements = []

    # draws the board
    def draw(self):
        v = []
        polygon_v = []
        rows = [3, 4, 5, 4, 3]
        self.screen.fill(BGCOLOUR)
        x = 170
        y = 150
        count = 0

        for row in range(5):
            x_offset = 0

            if row == 2:
                x_offset -= self.width / 2

            elif row % 2 == 0:
                x_offset = self.width / 2

            # loops x times for number of hexagons in row
            for i in range(rows[row]):
                x += self.width
                centre = (round(x + x_offset), round(y))  # stores centre of a hexagon in a tuple
                vertices = []

                # calculate vertices from centre of a hexagon
                for j in range(6):
                    angle_deg = 60 * j - 30
                    angle_rad = math.pi / 180 * angle_deg
                    vert_x = centre[0] + self.tile_size * math.cos(angle_rad)
                    vert_y = centre[1] + self.tile_size * math.sin(angle_rad)
                    vertices.append((math.floor(vert_x), math.floor(vert_y)))
                    v.append((math.floor(vert_x), math.floor(vert_y)))

                polygon_v.append(vertices)

                pygame.draw.polygon(self.screen, self.tiles[count], vertices)
                pygame.draw.polygon(self.screen, BLACK, vertices, 3)
                pygame.draw.circle(self.screen, BLACK, centre, 4, 4)
                count += 1

            y += self.height * 3/4
            x -= self.width * rows[row]  # resets x back to starting position

        # creates a list of unique tuples which represent coordinates of each vertex.
        # i.e. list of the coordinates for possible settlement locations
        for vertex in v:
            if vertex not in self.unique_v:
                if (vertex[0]+1, vertex[1]) not in self.unique_v:
                    if (vertex[0]-1, vertex[1]) not in self.unique_v:
                        self.unique_v.append(vertex)

        # creating a dictionary with each unique vertex as keys and empty lists as values
        for vertex in self.unique_v:
            self.location_materials[vertex] = []

        # updating the lists for each vertex with the materials in hexagons adjacent to them
        polynum = 0
        for polygon in polygon_v:
            for vertex in self.unique_v:
                if vertex in polygon or (vertex[0] + 1, vertex[1]) in polygon or (vertex[0] - 1, vertex[1]) in polygon:
                    self.location_materials[vertex].append(self.tiles[polynum])
            polynum += 1

        print(len(self.unique_v))
        print(self.unique_v)
        print(len(self.location_materials))
        print(self.location_materials)

    # method called when clicking on a location you want to place a settlement
    def place_settlement(self, location):
        # Checks whether the location given is close to one of the unique vertices on the board.
        exist = 0
        for option in self.unique_v:
            if location[0] in range(option[0] - 10, option[0] + 10):
                if location[1] in range(option[1] - 10, option[1] + 10):
                    # Check if the vertex is already taken, if not, draw a circle and update the dictionary

                    for settlement in self.existing_settlements:
                        if settlement.location == option:
                            exist = 1
                            break

                    if exist == 1:
                        print("Location not available")
                    else:
                        new_settlement = Settlement("player", option)
                        self.existing_settlements.append(new_settlement)
                        pygame.draw.circle(self.screen, (200, 123, 112), option, 10)
                        print("settlement created")
                        print(self.existing_settlements)
