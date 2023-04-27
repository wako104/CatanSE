from settings import *
from board import Board


class Player:

    def __init__(self, num):
        # player number
        self.num = num
        # player colour
        if self.num == 1:
            self.colour = PLAYERCOLOUR1
        if self.num == 2:
            self.colour = PLAYERCOLOUR2
        if self.num == 3:
            self.colour = PLAYERCOLOUR3
        if self.num == 4:
            self.colour = PLAYERCOLOUR4
        # initial road placements
        self.initial_placements = []
        # the cards a player has
        self.cards = {KNIGHT: 0, DEVELOPMENTROAD: 0, YEAROFPLENTY: 0, MONOPOLY: 0, VICTORYPOINT: 0}
        # players victory point
        self.victory_points = 0
        self.resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD:0}

    def add_victory_point(self):
        self.victory_points += 1

    def get_victory_points(self):
        return self.victory_points

    def get_resource(self, resource):
        if resource in self.resources.keys():
            self.resources[resource] += 1
