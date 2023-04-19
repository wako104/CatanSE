from cards import Resource, Development
from settings import *

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


    def build_settlement(self, point):

        # resources needed to build a settlement
        settlement_rsrc = [Resource.Wood, Resource.Brick, Resource.Sheep, Resource.Wheat]

        # check that player has required cards
        if not self.check_cards(settlement_rsrc):
            return -1

        self.remove_cards(settlement_rsrc)


    def build_road(self, point1, point2):

        # resources needed to build a road
        road_rsrc = [Resource.Wood, Resource.Brick]

        # check that player has required cards
        if not self.check_cards(road_rsrc):
            return -1

        # check that the location of the road is valid
        if not self.check_road_location(point1, point2):
            return -1

    def check_cards(self, cards):
        for card in self.cards:
            if cards.count(card) == 0:
                return False
        return True

    def check_road_location(self, point1, point2):
        return True

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def remove_cards(self, cards):
        for card in cards:
            del self.cards[self.cards.index(card)]

    def set_colour(self):
        if self.num == 1:
            self.colour = PLAYERCOLOUR1
        if self.num == 2:
            self.colour = PLAYERCOLOUR2
        if self.num == 3:
            self.colour = PLAYERCOLOUR3
        if self.num == 4:
            self.colour = PLAYERCOLOUR4
