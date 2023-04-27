import unittest
import math

import pygame
import pygame.font

import cards

pygame.font.init()
from settings import*
from board import Board
from player import Player
from building import Settlement
from tile import Tile
from road import Road
from cards import Resource
from dice import Dice



class MyTestCase(unittest.TestCase):


    def test1(self):
        #test board class sets width correctly

        player1 = Player(1)
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        #need to set up locations to test
        location1 =board1.unique_v[0]

        #player1 = new player object // location1 = position at a tile corner
        board1.place_settlement(player1, location1,False)

        self.assertEqual(board1.screen.get_width(),WIDTH)  # add assertion here

    def test2(self):
        # test board class sets height correctly

        player1 = Player(1)
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        # need to set up locations to test??
        location1 = board1.unique_v[0]

        # player1 = new player object // location1 = position at a tile corner
        #NEED INITIAL PLACEMENT

        board1.place_settlement(player1, location1, False)

        self.assertEqual(board1.screen.get_height(), HEIGHT)



    def test3(self):
        #test building class assigns player correctly

        player1 = Player(1)
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]
        #adjacent = array of adjacent tile corners
        adjacent1 = []
        adjacentHC1 =[]

        #NEEDS 1-ADJACENT HEX CENTRES, 2-Board
        settlement1 = Settlement(player1, location1, adjacent1,adjacentHC1,board1)
        self.assertEqual(settlement1.player, player1)  # add assertion here

    def test4(self):
        #test building class assigns location correctly

        player1 = Player(1)
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]
        #adjacent = array of adjacent tile corners
        adjacent1 = []
        adjacentHC1 = []

        settlement1 = Settlement(player1, location1, adjacent1,adjacentHC1,board1)
        self.assertEqual(settlement1.location, location1)  # put this in own test

    def test5(self):
        #test building class assigns adjacent correctly
        #assuming centre of 1st hexagon is (170,150)
        #tileSize = 50,
        #angle_deg = 60*(j:0-5) - 30

        #works out top left vertex from 1st tile centre
        angle_deg = 60*0 - 30
        angle_rad = math.pi / 180*angle_deg
        x = math.floor(170 + 50* math.cos((angle_rad)))
        y = math.floor(150 + 50* math.sin((angle_rad)))
        #adjacent = array of adjacent tile corners
        adjacentVertex = (x,y)
        adjacent1 = [adjacentVertex] #put an adjacent corner into array
        adjacentHC1 = []

        player1 = Player(1)

        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]
        settlement1 = Settlement(player1, location1, adjacent1,adjacentHC1,board1)
        self.assertEqual(settlement1.adjacent_vertices[0], adjacentVertex)  # put this in own test


    def test6(self):
        #test player class constructor num
        player1 = Player(1)
        self.assertEqual(player1.num, 1)  # add assertion here

    """
    def test7(self):
        #test player class build settlement removes appropriate cards from player
        player1 = Player(1)
        #need cards in inv to build settlement
        #cards=[wood,brick,sheep,wheat]
        wood1 = Resource(0)
        brick1 = Resource(1)
        sheep1 = Resource(2)
        wheat1 = Resource(3)
        player1.add_cards([wood1,brick1,sheep1,wheat1]) #array of card objects
        player1.build_settlement() #POINT param??? not used
        self.assertEqual(player1.check_cards(player1.cards), False)  # checkcards returns false if array empty
    """
    """
    def test8(self):
        #test player class build road
        player1 = Player(1)
        wood1 = Resource(0)
        brick1 = Resource(1)
        player1.add_cards([wood1,brick1])
        player1.build_road() # NEED 2 points ends of roads ??
        self.assertEqual(player1.check_cards(player1.cards), False)  # add assertion here
    """
    def test9(self):
        #test player class check cards method when cards present
        player1 = Player(1)
        wood1 = Resource(0)
        player1.add_cards([wood1])
        self.assertEqual(player1.check_cards(player1.cards), True)  # add assertion here

    def test10(self):
        #test player class check cards method when no cards in player
        player1 = Player(1)

        self.assertEqual(player1.check_cards(player1.cards), False)  # add assertion here
        #returns true == error with code to improve == returns true even tho deck is empty because for loop never starts


    def test11(self):
        #test player class add cards method with 1 card
        player1 = Player(1)
        wood1 = Resource(0)
        player1.add_cards([wood1])
        self.assertEqual(player1.cards[0], wood1)  # add assertion here
    def test12(self):
        #test player class add cards method with 2 cards
        player1 = Player(1)
        wood1 = Resource(0)
        brick1 = Resource(1)
        player1.add_cards([wood1,brick1])
        self.assertEqual(player1.cards[1], brick1)  # add assertion here
    def test13(self):
        #test player class add cards method with 3 of the same card
        player1 = Player(1)
        wood1 = Resource(0)
        player1.add_cards([wood1,wood1,wood1])
        self.assertEqual(player1.cards[2], wood1)  # add assertion here
    def test14(self):
        #test player class add cards method with 5 cards of different types
        player1 = Player(1)
        wood1 = Resource(0)
        brick1 = Resource(1)
        sheep1 = Resource(2)
        wheat1 = Resource(3)
        ore1 = Resource(4)
        player1.add_cards([wood1,brick1,sheep1,wheat1,ore1])
        self.assertEqual(player1.cards[4], ore1)  # add assertion here

    def test15(self):
        #test player class remove cards method
        player1 = Player(1)
        wood1 = Resource(0)
        player1.add_cards([wood1])
        player1.remove_cards([wood1])

        #self.assertEqual(player1.check_cards(player1.cards), False)  # add assertion here
        self.assertEqual(player1.cards.__len__(), 0)  # add assertion here

    def test16(self):
        #test player class remove cards method with 5 cards
        player1 = Player(1)
        wood1 = Resource(0)
        brick1 = Resource(1)
        sheep1 = Resource(2)
        wheat1 = Resource(3)
        ore1 = Resource(4)
        player1.add_cards([wood1,brick1,sheep1,wheat1,ore1])
        player1.remove_cards([wood1,brick1,sheep1,wheat1,ore1])
        self.assertEqual(player1.cards.__len__(), 0)  # add assertion here


    def test17(self):
        #test tile class add road method
        player1 = Player
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]

        tile1 = Tile()
        road1 = Road(player1,location1)
        tile1.add_road(1,road1) #(tileEdgePosition(1-6 ttb ltr), road object)
        self.assertEqual(tile1.roads[1], road1)  # add assertion here

    def test18(self):
        #test tile class add building method

        tile1 = Tile()
        player1 = Player(1)
        board1 = Board(WIDTH,HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]
        adjacentHC1 = []

        # assuming centre of 1st hexagon is (170,150)
        # tileSize = 50,
        # angle_deg = 60*(j:0-5) - 30
        # works out top left vertex from 1st tile centre
        angle_deg = 60 * 0 - 30
        angle_rad = math.pi / 180 * angle_deg
        x = math.floor(170 + 50 * math.cos((angle_rad)))
        y = math.floor(150 + 50 * math.sin((angle_rad)))
        # adjacent = array of adjacent tile corners
        adjacentVertex = (x, y)
        adjacent1 = [adjacentVertex]  # put an adjacent corner into array

        #NEEDS 1-ADJACENT HEX CENTRES, 2-BOARD
        settlement1 = Settlement(player1,location1,adjacent1,adjacentHC1,board1) #player,location,adjacent
        tile1.add_building(1,settlement1) #(TileVertexPosition(1-6 ttb ltr), building object)
        self.assertEqual(tile1.buildings[1], settlement1)  # add assertion here


    """
    def test19(self):
        #test player class check road location
        player1 = Player(1)
        player1.check_road_location()
        self.assertEqual(True, True)  # add assertion here
    """

    """
    #def test20(self):
        #test road class ?? currently empty ??
        #self.assertEqual(True, True)  # add assertion here
    """

    def test21(self):
        player1 = Player(1)

        #BRICK/CLAY RESOURCE PROBLEM ??????????????????????????????????????????????

        wood1 = cards.Resource.Wood
        brick1 = cards.Resource.Brick
        player1.add_cards([wood1,brick1])
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.centre_edge[0]
        #player option initialplacement
        board1.place_road(player1, location1, False)
        self.assertEqual(board1.centre_edge,location1)

    def test22(self):
        #test board class harvest_resource method
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()

        board1.harvest_resource(1)
        #TOO COMPLICATED ?????????????????????????????????????????????


    def test23(self):
        #test board class build_city method
        tile1 = Tile()
        player1 = Player(1)
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]
        adjacentHC1 = []

        # assuming centre of 1st hexagon is (170,150)
        # tileSize = 50,
        # angle_deg = 60*(j:0-5) - 30
        # works out top left vertex from 1st tile centre
        angle_deg = 60 * 0 - 30
        angle_rad = math.pi / 180 * angle_deg
        x = math.floor(170 + 50 * math.cos((angle_rad)))
        y = math.floor(150 + 50 * math.sin((angle_rad)))
        # adjacent = array of adjacent tile corners
        adjacentVertex = (x, y)
        adjacent1 = [adjacentVertex]  # put an adjacent corner into array

        # NEEDS 1-ADJACENT HEX CENTRES, 2-BOARD
        settlement1 = Settlement(player1, location1, adjacent1, adjacentHC1, board1)  # player,location,adjacent
        tile1.add_building(1, settlement1)  # (TileVertexPosition(1-6 ttb ltr), building object)
        board1.existing_settlements.append(settlement1)
        board1.build_city(player1,settlement1.location)
        #SPELLING MISTAKE ERROR W EXISITING BOARDS VS EXISTING BOARDS
        self.assertEqual(board1.exisiting_cities.__len__(),1)

    def test24(self):
        #test dice class roll method
        dice1 = Dice()
        dice1.roll()
        self.assertNotEqual(dice1.dice_num1,0)
    def test25(self):
        #test dice class roll method
        dice1 = Dice()
        dice1.roll()
        self.assertNotEqual(dice1.dice_num2,0)


    #main untestable until some way to quit/terminate game
    """
    def test26(self):
        #test main class handle_settlement method
        main1 = Main()
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        player1 = Player
        location1 = board1.unique_v[0]

        main1.handle_settlement(player1,location1)

    def test27(self):
        #test main class handle_road method
        main1 = Main()
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        player1 = Player
        location1 = board1.unique_v[0]

        main1.handle_road(player1,location1)

        pass
    
        
    def test28(self):
        #test main class can_end_turn method
        pass


    def test29(self):
        #test main class player_road_count method
        pass
    def test30(self):
        #test main class player_settlement method
        pass

    """



    def test31(self):
        #test player class add_victory_point method
        player1 = Player(1)
        player1.add_victory_point()
        self.assertEqual(player1.victory_points,1)
    def test32(self):
        #test player class add_victory_point method
        player1 = Player(1)
        for i in range(10):
            player1.add_victory_point()
        self.assertEqual(player1.victory_points,10)
    def test33(self):
        #test player class get_victory_points method
        player1 = Player(1)
        player1.add_victory_point()

        self.assertEqual(player1.get_victory_points(),1)
    def test34(self):
        #test player class get_victory_points method
        player1 = Player(1)
        for i in range(10):
            player1.add_victory_point()
        self.assertEqual(player1.get_victory_points(),10)

    def test35(self):
        #test player class get_resource method for CLAY
        player1 = Player(1)
        player1.get_resource(CLAY)
        self.assertEqual(player1.resources[CLAY],1)

    def test36(self):
        #test player class get_resource method for ORE
        player1 = Player(1)
        player1.get_resource(ORE)
        self.assertEqual(player1.resources[ORE],1)

    def test37(self):
        #test player class get_resource method for SHEEP
        player1 = Player(1)
        player1.get_resource(SHEEP)
        self.assertEqual(player1.resources[SHEEP],1)

    def test38(self):
        #test player class get_resource method for WHEAT
        player1 = Player(1)
        player1.get_resource(WHEAT)
        self.assertEqual(player1.resources[WHEAT],1)

    def test39(self):
        #test player class get_resource method for WOOD
        player1 = Player(1)
        player1.get_resource(WOOD)
        self.assertEqual(player1.resources[WOOD],1)

    def test40(self):
        #test player class get_resource method for 10 CLAY resources
        player1 = Player(1)
        for i in range(10):
            player1.get_resource(CLAY)
        self.assertEqual(player1.resources[CLAY],10)
    def test41(self):
        #test road class constructor
        player1 = Player(1)
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]
        road1 = Road(player1,location1)
        self.assertEqual(road1.player,player1)
    def test42(self):
        #test road class constructor
        player1 = Player(1)
        board1 = Board(WIDTH, HEIGHT)
        board1.draw()
        location1 = board1.unique_v[0]
        road1 = Road(player1,location1)
        self.assertEqual(road1.location,location1)


if __name__ == '__main__':
    unittest.main()
