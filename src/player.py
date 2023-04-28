from settings import *
from board import Board

'''
Author: Will, Rob
Class: Each object of this class is a player in the game. Allows us to create players and allows players to trade 
and play the game
'''

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
        # the development cards a player has
        self.cards = {KNIGHT: 0, DEVELOPMENTROAD: 0, YEAROFPLENTY: 0, MONOPOLY: 0, VICTORYPOINT: 0}
        # players victory point
        self.victory_points = 0
        # players development cards
        self.resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD: 0}
        # number of knight card player has
        self.knight_counter = 0
        #
        self.largest_army = 0

    def add_victory_point(self):
        self.victory_points += 1

    def get_victory_points(self):
        return self.victory_points + self.largest_army

    def get_resource(self, resource):
        if resource in self.resources.keys():
            self.resources[resource] += 1

    def get_development(self, development):
        if development in self.cards.keys():
            self.cards[development] += 1

    def receive_trade(self, resource_dictionary):
        for resource, amount in resource_dictionary.items():
            self.resources[resource] += amount

    def send_trade(self, resource_dictionary):
        for resource, amount in resource_dictionary.items():
            self.resources[resource] -= amount

