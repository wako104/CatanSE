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

    def check_cards(self, cards):
        for card in cards:
            if self.cards.count(card) == 0:
                return False
        return True

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def remove_cards(self, cards):
        for card in cards:
            del self.cards[self.cards.index(card)]
