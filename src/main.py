import pygame
import math

from settings import *
import sys
from board import Board
from player import Player
from dice import Dice


class Main:

    def __init__(self):
        pygame.init()
        self.board = Board(WIDTH, HEIGHT)
        self.clock = pygame.time.Clock()
        self.count = 0
        self.num_players = 0
        self.players = []
        self.turn_number = 1
        self.dice = Dice()

    # main function to run the game
    def run(self):
        self.board.draw()
        self.draw_end_turn_button()
        pygame.display.flip()
        self.running = True
        self.dice.draw_default_dice()

        # loop to create list of objects of players
        for i in range(self.num_players):
            player = Player(i+1)
            self.players.append(player)
        self.current_player = self.players[0]
        print(self.players)
        print("Player " + str(self.current_player.num))

        # loops to keep game running and updating until it is closed
        while self.running:
            font = pygame.font.Font(None, 24)
            text = font.render("Turn Number: " + str(self.turn_number), 1, (255, 255, 255))
            pygame.draw.rect(self.board.screen, BG_COLOUR, (0, 0, 200, 50))
            self.board.screen.blit(text, (10, 10))
            self.clock.tick(FPS)
            self.visual()
            self.events()
            self.update()

    def menu(self):
        self.visual()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Main Menu")
        screen.fill(BG_COLOUR)
        font = pygame.font.Font("../resources/Retro Gaming.ttf", 22)
        text = font.render("Press 1-4 for the number of players.", 1, WHITE)

        # ask user how many players will be in the game and store the value
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        self.num_players = 1
                        self.run()
                    elif event.key in [pygame.K_2, pygame.K_KP2]:
                        self.num_players = 2
                        self.run()
                    elif event.key in [pygame.K_3, pygame.K_KP3]:
                        self.num_players = 3
                        self.run()
                    elif event.key in [pygame.K_4, pygame.K_KP4]:
                        self.num_players = 4
                        self.run()

            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, text_rect)
            pygame.display.update()

    # initialises some visual stuff like the title and icon
    def visual(self):
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load('../resources/logo.png')
        pygame.display.set_icon(icon)

    # creates end turn button
    def draw_end_turn_button(self):
        button_width, button_height = 100, 50
        button_x = WIDTH - button_width - 10
        button_y = HEIGHT - button_height - 10
        self.end_turn_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, (255, 0, 0), self.end_turn_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("End Turn", 1, (255, 255, 255))
        text_pos = text.get_rect(center=self.end_turn_button_rect.center)
        self.board.screen.blit(text, text_pos)

    # ends turn
    def end_turn(self):
        player_count = len(self.players)
        current_player_index = self.players.index(self.current_player)
        if current_player_index == player_count -1:
            self.turn_number += 1
        self.current_player = self.players[(current_player_index + 1) % player_count]
        print("Player " + str(self.current_player.num))

    # checks for game updates
    def update(self):
        pygame.display.update()

    # checks events, checks if the game is closed
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if self.end_turn_button_rect.collidepoint(location):
                    if self.can_end_turn(self.current_player):
                        self.end_turn()
                    else:
                        print("Cannot end turn")
                        return -1
                for option in self.board.unique_v:
                    if location[0] in range(option[0] - 10, option[0] + 10):
                        if location[1] in range(option[1] - 10, option[1] + 10):
                            self.handle_settlement(self.current_player, location)
                for option in self.board.centre_edge:
                    if location[0] in range(option[0][0] - 10, option[0][0] + 10):
                        if location[1] in range(option[0][1] - 10, option[0][1] + 10):
                            self.handle_road(self.current_player, option)
                if self.dice.dice_rect.collidepoint(location):
                    self.dice.roll()
                    print(self.dice.total_dice_num())

    def handle_settlement(self, player, location):
        count = self.player_settlement_count(player)

        if self.turn_number == 1:
            if count == 0:
                self.board.place_settlement(player, location, True)
            else:
                print("Cannot place another settlement on this turn")
                return -1
        elif self.turn_number == 2:
            if count == 1:
                self.board.place_settlement(player, location, True)
            else:
                print("Cannot place another settlement on this turn")
                return -1
        else:
            self.board.place_settlement(player, location, False)

    def handle_road(self, player, location):
        count = self.player_road_count(player)

        if self.turn_number == 1:
            if count == 0:
                self.board.place_road(player, location, True)
            else:
                print("Cannot place another settlement on this turn")
                return -1
        elif self.turn_number == 2:

            if count == 1:
                self.board.place_road(player, location, True)
            else:
                print("Cannot place another settlement on this turn")
                return -1
        else:
            self.board.place_road(player, location, False)

    def can_end_turn(self, player):
        road_count = self.player_road_count(player)
        settlement_count = self.player_settlement_count(player)
        if self.turn_number == 1:
            if road_count == 1 & settlement_count == 1:
                return True
            else:
                return False
        elif self.turn_number == 2:
            if road_count == 2 & settlement_count == 2:
                return True
            else:
                return False

    def player_road_count(self, player):
        count = 0
        for road in self.board.existing_roads:
            if road.player == player:
                count += 1
        return count

    def player_settlement_count(self, player):
        count = 0
        for settlement in self.board.existing_settlements:
            if settlement.player == player:
                count += 1
        return count

    # quits game
    def quit(self):
        sys.exit()


m = Main()
while True:
    m.menu()
