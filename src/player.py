from cards import Resource, Development


class Player:

    def __init__(self, num):
        # player number
        self.num = num
        # initial road placements
        self.initial_placements = []
        # the cards a player has
        self.cards = []
        # players victory points
        self.victory_points = 0

    def build_settlement(self, point):
        settlement_rsrc = [Resource.Wood, Resource.Brick, Resource.Sheep, Resource.Wheat]

        if not self.check_cards(settlement_rsrc):
            return -1

    def build_road(self, point1, point2):
        road_rsrc = {
            Resource.Wood,
            Resource.Brick
        }

    def check_cards(self, cards):
        for card in self.cards:
            if cards.count(card) == 0:
                return False
        return True
