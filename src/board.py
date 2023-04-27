import math
import pygame
import random
import pygame.font

import building
from road import *
from settings import *
from building import Settlement
from building import City
import itertools
from collections import defaultdict


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
        self.existing_cities = []
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
        self.hex_resource = defaultdict(list)
        self.vertex_adjacent_centres = {}
        self.location_number_resource = {}

    # draws the board
    def draw(self):
        v = []
        polygon_v = []
        rows = [3, 4, 5, 4, 3]
        self.screen.fill(BG_COLOUR)
        background_image = pygame.image.load("../resources/game_background.png")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        self.screen.blit(background_image, (0,0))
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

        offset_x = -15
        offset_y = -40

        for i in range(19):
            if self.tiles[i] != SAND:
                text = str(self.tokens[i])
                dest = self.hex_centres[i]
                text_color = RED if self.tokens[i] in (6, 8) else WHITE

                # Dropshadow effect
                shadow_color = (64, 64, 64)  # A dark gray color for the shadow
                shadow_offset = (2, 2)  # The offset for the shadow (x, y)
                shadow_dest = (dest[0] + shadow_offset[0], dest[1] + shadow_offset[1])

                place_text_shadow = self.font.render(text, 1, shadow_color)
                self.screen.blit(place_text_shadow, shadow_dest)

                # Original text
                place_text = self.font.render(text, 1, text_color)
                self.screen.blit(place_text, dest)

                # draws image
                tile_name = self.tiles[i]
                if tile_name == CLAY:
                    CLAY_img = pygame.image.load("../resources/clay.png")
                    CLAY_img = pygame.transform.scale(CLAY_img, (30, 30))
                    dest_offset = (dest[0] + offset_x, dest[1] + offset_y)
                    self.screen.blit(CLAY_img, dest_offset)

                elif tile_name == ORE:
                    ORE_img = pygame.image.load("../resources/ore.png")
                    ORE_img = pygame.transform.scale(ORE_img, (30, 30))
                    dest_offset = (dest[0] + offset_x, dest[1] + offset_y)
                    self.screen.blit(ORE_img, dest_offset)

                elif tile_name == WHEAT:
                    WHEAT_img = pygame.image.load("../resources/wheat.png")
                    WHEAT_img = pygame.transform.scale(WHEAT_img, (30, 30))
                    dest_offset = (dest[0] + offset_x, dest[1] + offset_y)
                    self.screen.blit(WHEAT_img, dest_offset)

                elif tile_name == SHEEP:
                    SHEEP_img = pygame.image.load("../resources/sheep.png")
                    SHEEP_img = pygame.transform.scale(SHEEP_img, (37, 37))
                    dest_offset = (dest[0] + offset_x - 3, dest[1] + offset_y)
                    self.screen.blit(SHEEP_img, dest_offset)

                elif tile_name == WOOD:
                    WOOD_img = pygame.image.load("../resources/wood.png")
                    WOOD_img = pygame.transform.scale(WOOD_img, (30, 30))
                    dest_offset = (dest[0] + offset_x, dest[1] + offset_y)
                    self.screen.blit(WOOD_img, dest_offset)

                count += 1
            else:
                dest = self.hex_centres[i]
                dest_offset = (dest[0] + offset_x, dest[1] + offset_y)
                SAND_img = pygame.image.load("../resources/sand.png")
                SAND_img = pygame.transform.scale(SAND_img, (30,30))
                self.screen.blit(SAND_img, dest_offset)
                pass

            self.location_number_resource[dest] = (self.tokens[i], self.tiles[i])

        print(self.location_number_resource)
        print("number location ^")

        for token, tile in zip(self.tokens, self.tiles):
            self.hex_resource[token].append(tile)
        print(self.hex_resource)
        print("test1")

        # creates a list of unique tuples which represent coordinates of each vertex.d
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
        self.get_vertex_adjacent_centres()

    def get_edge_centres(self):
        for edge in self.edge_vertices:
            new_x = math.floor((edge[0][0] + edge[1][0])/2)
            new_y = math.floor((edge[0][1] + edge[1][1])/2)
            new_coord = (new_x, new_y)
            self.centre_edge.append((new_coord, edge))

    def get_vertex_adjacent_centres(self):
        for vertex in self.unique_v:
            self.vertex_adjacent_centres[vertex] = []
            for centre in self.hex_centres:
                # Find the distance between vertex and centre of hex
                distance = math.sqrt(abs(centre[0]-vertex[0])**2+abs(centre[1]-vertex[1])**2)
                # Checks if the distance is close enough to be an adjacent centre
                if distance < 70:
                    # Check if the centre is in vertex_adjacent_centres
                    if centre not in self.vertex_adjacent_centres[vertex]:
                        self.vertex_adjacent_centres[vertex].append(centre)
        print("Test")
        print(self.vertex_adjacent_centres)

    # method called when clicking on a location you want to place a settlement
    def place_settlement(self, player, location, initial_placement):
        owned = 0

        # check if the placement is not an initial placement
        if not initial_placement:
            owned = 0
            for required in SETTLEMENT:
                if required not in player.resources.keys() or player.resources[required] < 1:
                    print("Do not have required resources for a settlement")
                    return -1
                else:
                    owned += 1


        # Checks whether the location given is close to one of the unique vertices on the board.
        error = 0
        adjacent_vertices = []
        for option in self.unique_v:
            if location[0] in range(option[0] - 10, option[0] + 10):
                if location[1] in range(option[1] - 10, option[1] + 10):
                    # Check if the vertex is already taken, if not, draw a circle and update the dictionary
                    for settlement in self.existing_settlements:
                        if settlement.location == option:
                            error = 1
                        elif option in settlement.adjacent_vertices:
                            error = 2
                    for edge in self.edge_vertices:
                        if option in edge:
                            for vertex in edge:
                                if vertex != option:
                                    adjacent_vertices.append(vertex)
                    if error == 1:
                        print("Location not available")
                    elif error == 2:
                        print("Cannot place adjacent to another settlement.")
                    else:
                        new_settlement\
                            = Settlement(player, option, adjacent_vertices, self.vertex_adjacent_centres[option], self)
                        self.existing_settlements.append(new_settlement)
                        pygame.draw.circle(self.screen, player.colour, option, 10)
                        if owned == len(SETTLEMENT):
                            for required in SETTLEMENT:
                                player.resources[required] -= 1
                        player.add_victory_point()
                        print("settlement created for player " + str(player.num))
                        print("Player " + str(player.num) + " has " + str(player.get_victory_points()) + " victory points")

    def initial_resource_collection(self, player, settlement):
        pass

    # Method to place a road on the board
    def place_road(self, player, option, initial_placement):
        error = 0
        owned = 0
        adjacent_settlement = []
        adjacent_road = []

        # check if the placement is not an initial placement
        if not initial_placement:
            owned = 0
            for required in ROAD:
                if required not in player.resources.keys() or player.resources[required] < 1:
                    print("Do not have required resources for a road")
                    return -1
                else:
                    owned += 1

        for vertex in option[1]:
            for settlement in self.existing_settlements:
                if settlement.location == vertex:
                    adjacent_settlement.append(settlement)

        for road in self.existing_roads:
            for vertex in road.location[1]:
                if vertex in option[1]:
                    adjacent_road.append(road)

        for road in adjacent_road:
            if road.player == player:
                error = 0
                break
            else:
                error = 4

        # Check if the vertex is already taken, if not, draw a circle and update the dictionary
        for road in self.existing_roads:
            if road.location[0] == option[0]:
                print("test1")
                error = 1

        for settlement in adjacent_settlement:
            if settlement.player != player:
                error = 2

        if len(adjacent_settlement) == 0:
            if len(adjacent_road) == 0:
                error = 3

        if error == 1:
            print("Location not available")
        elif error == 2:
            print("Cannot place a road next to enemy settlement.")
        elif error == 3:
            print("Must be next to your settlement or road.")
        elif error == 4:
            print("Must be next to your own road.")
        elif error == 0:
            new_road = Road(player, option)
            self.existing_roads.append(new_road)
            pygame.draw.line(self.screen, player.colour, option[1][0], option[1][1], 5)
            if owned == len(ROAD):
                for required in ROAD:
                    player.resources[required] -= 1
            print("Road created for player " + str(player.num))

    def harvest_resource(self, dice_number):
        for location in self.location_number_resource:
            if self.location_number_resource[location][0] == dice_number:
                for settlement in self.existing_settlements:
                    if location in settlement.adjacent_hex_centres:
                        settlement.collect_resource(location)

    def build_city(self, player, option):
        made = False
        for settlement in self.existing_settlements:
            if settlement.location == option and player == settlement.player:
                new_city = City(settlement.player, settlement.location, settlement.adjacent_vertices, settlement.adjacent_hex_centres, settlement.board)
                self.existing_cities.append(new_city)
                self.existing_settlements.remove(settlement)
                made = True
            elif settlement.location == option:
                print("Can only build a city on your own settlement.")
        if not made:
            print("Can only build a city over a settlement")
