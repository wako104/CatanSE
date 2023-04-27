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
        self.cards = []
        # players victory points
        self.victory_points = 0
        self.resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD:0}

    # check player has cards required
    def check_cards(self, cards):
        for card in cards:
            if self.cards.count(card) == 0:
                return False
        return True

    # add card(s) to players deck
    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    # remove card(s) from players deck
    def remove_cards(self, cards):
        for card in cards:
            del self.cards[self.cards.index(card)]

    def add_victory_point(self):
        self.victory_points += 1

    def get_victory_points(self):
        return self.victory_points

    def get_resource(self, resource):
        if resource in self.resources.keys():
            self.resources[resource] += 1

    def receive_trade(self, resource_dictionary):
        for resource, amount in resource_dictionary.items():
            self.resources[resource] += amount

    def send_trade(self, resource_dictionary):
        for resource, amount in resource_dictionary.items():
            self.resources[resource] -= amount

