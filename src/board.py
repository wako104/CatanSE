import math
import pygame
import random

import building
from road import *
from settings import *
from building import Settlement


class Board:
    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.tile_size = TILE_SIZE
        self.width = math.sqrt(3) * self.tile_size
        self.height = 2 * self.tile_size
        self.tiles = []
        self.tiles += [CLAY, ORE] * 3
        self.tiles += [WHEAT, SHEEP, WOOD] * 4
        self.tiles += [SAND]
        random.shuffle(self.tiles)
        # Will store each unique vertex on the board
        self.unique_v = []
        # Will store each vertex as a key with a list of adjacent resources as value
        self.location_materials = {}
        # Will store the location of each existing settlement as an object of Settlement
        self.existing_settlements = []
        self.hex_centres = []
        # Will store and array of tuples containing the vertices of each unique edge
        self.edge_vertices = []
        self.tokens = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R]
        random.shuffle(self.tokens)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)
        # Will store the middle of each edge
        self.centre_edge = []
        # Will store all edges which already have a road
        self.existing_roads = []
        # Store tile with resource
        self.hex_resource = []

    # draws the board
    def draw(self):
        v = []
        polygon_v = []
        rows = [3, 4, 5, 4, 3]
        self.screen.fill(BG_COLOUR)
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
                self.hex_centres.append(centre)

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
                count += 1

            y += self.height * 3/4
            x -= self.width * rows[row]  # resets x back to starting position

        # places the token number on each tile
        desert = self.tiles.index(SAND)
        self.tokens.insert(desert, None)

        for i in range(19):
            if self.tiles[i] != SAND:
                text = str(self.tokens[i])
                dest = self.hex_centres[i]
                place_text = self.font.render(text, 1, WHITE)
                self.screen.blit(place_text, dest)
                count += 1
            else:
                pass

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
                if vertex in polygon:
                    self.location_materials[vertex].append(self.tiles[polynum])
                if (vertex[0] + 1, vertex[1]) in polygon:
                    self.location_materials[vertex].append(self.tiles[polynum])
                if (vertex[0] - 1, vertex[1]) in polygon:
                    self.location_materials[vertex].append(self.tiles[polynum])
            polynum += 1

        # Finds each edge between the unique vertices and stores them in edge_vertices
        for vertex in self.unique_v:
            for vertex_2 in self.unique_v:
                # Find the distance between vertex and vertex_2
                distance = math.sqrt(abs(vertex_2[0]-vertex[0])**2+abs(vertex_2[1]-vertex[1])**2)
                # Checks if the distance is close enough to be an adjacent vertex but not zero
                if distance < 60:
                    if distance != 0:
                        # Check if the edge is in edge_vertices, including the reverse edge
                        if (vertex, vertex_2) not in self.edge_vertices:
                            if (vertex_2, vertex) not in self.edge_vertices:
                                self.edge_vertices.append((vertex, vertex_2))
        self.get_edge_centres()

    def get_edge_centres(self):
        for edge in self.edge_vertices:
            new_x = math.floor((edge[0][0] + edge[1][0])/2)
            new_y = math.floor((edge[0][1] + edge[1][1])/2)
            new_coord = (new_x, new_y)
            self.centre_edge.append((new_coord, edge))

    # method called when clicking on a location you want to place a settlement
    def place_settlement(self, player, location):
        # check if the placement is not an initial placement
        if not self.check_initial_placements(player, building.Settlement):
            # if it is not an initial placement, check the player has the correct cards
            if not player.check_cards(SETTLEMENT):
                print("Player does not have required cards")
                return -1
            else:
                # if player has correct cards, remove them from their deck
                player.remove_cards(SETTLEMENT)

        # Checks whether the location given is close to one of the unique vertices on the board.
        error = 0
        adjacent = []
        for option in self.unique_v:
            if location[0] in range(option[0] - 10, option[0] + 10):
                if location[1] in range(option[1] - 10, option[1] + 10):
                    # Check if the vertex is already taken, if not, draw a circle and update the dictionary
                    for settlement in self.existing_settlements:
                        if settlement.location == option:
                            error = 1
                        elif option in settlement.adjacent:
                            error = 2
                    for edge in self.edge_vertices:
                        if option in edge:
                            for vertex in edge:
                                if vertex != option:
                                    adjacent.append(vertex)
                    if error == 1:
                        print("Location not available")
                    elif error == 2:
                        print("Cannot place adjacent to another settlement.")
                    else:
                        new_settlement = Settlement(player, option, adjacent)
                        self.existing_settlements.append(new_settlement)
                        print(player.colour)
                        pygame.draw.circle(self.screen, player.colour, option, 10)
                        print("settlement created")
                        print(self.existing_settlements)

    # checks the number of placements a player has.
    def check_initial_placements(self, player, placement_type):
        count = 0
        if placement_type == building.Settlement:
            for settlement in self.existing_settlements:
                if settlement.player == player:
                    count += 1
        if count < 2:
            return True
        else:
            return False

    # Method to place a road on the board
    def place_road(self, player, option):
        error = 0
        # Check if the vertex is already taken, if not, draw a circle and update the dictionary
        for road in self.existing_roads:
            if road.location[0] == option[0]:
                error = 1
        if error == 1:
            print("Location not available")
        else:
            new_road = Road(player, option)
            self.existing_roads.append(new_road)
            pygame.draw.line(self.screen, player.colour, option[1][0], option[1][1], 5)
            print("road created")
            print(self.existing_roads)



