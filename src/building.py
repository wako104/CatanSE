import pygame
from settings import *

'''
Author: Tyler
Class: Handles buildings
'''

class Settlement:

    def __init__(self, player, location, adjacent_vertices, adjacent_hex_centres, board):
        self.player = player
        self.location = location
        self.adjacent_vertices = adjacent_vertices
        self.adjacent_hex_centres = adjacent_hex_centres
        self.board = board

    def get_resources(self):
        pass

    def collect_resource(self, location):
        print("Player " + str(self.player.num) + " gets " + str(self.board.location_number_resource[location][1]))
        self.player.get_resource(self.board.location_number_resource[location][1])

class City:
    def __init__(self, player, location, adjacent_vertices, adjacent_hex_centres, board):
        self.player = player
        self.location = location
        self.adjacent_vertices = adjacent_vertices
        self.adjacent_hex_centres = adjacent_hex_centres
        self.board = board

    def collect_resource(self, location):
        print("Player " + str(self.player.num) + " gets " + str(self.board.location_number_resource[location][1]))
        self.player.get_resource(self.board.location_number_resource[location][1])

class Development:
    def __init__(self):
        pass
