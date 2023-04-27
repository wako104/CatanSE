import pygame
import math
import pygame_gui

from settings import *
import sys
from board import Board
from player import Player
from dice import Dice
from building import Settlement


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
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.dice_count = 0
        self.placed_init_settlement = False
        self.placed_init_road = False

    # main function to run the game
    def run(self):
        self.board.draw()

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
            turn_number_text = self.font.render("Turn Number: " + str(self.turn_number), 1, (255, 255, 255))
            pygame.draw.rect(self.board.screen, BG_COLOUR, (0, 0, 200, 50))
            self.board.screen.blit(turn_number_text, (10, 10))
            self.draw_resources()
            current_player_text = self.font.render("Player : " + str(self.current_player.num), 1, (255, 255, 255))
            pygame.draw.rect(self.board.screen, BG_COLOUR, (10, HEIGHT - 180, 150, 30))
            self.board.screen.blit(current_player_text, (10, HEIGHT - 180))
            self.draw_end_turn_button()
            self.draw_settlement_button()
            self.draw_road_button()
            self.clock.tick(FPS)
            self.visual()
            self.events()
            self.update()

    def menu(self):
        self.visual()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Main Menu")

        background_image = pygame.image.load("../resources/catan.jpg")
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

        logo_image = pygame.image.load("../resources/the_settlers.png")
        logo_rect = logo_image.get_rect()
        logo_rect.centerx = WIDTH // 2
        logo_rect.y = 60

        manager = pygame_gui.UIManager((WIDTH, HEIGHT))

        text = self.font.render("Select the number of players.", 1, WHITE)
        shadow_text = self.font.render("Select the number of players.", 1, (50, 50, 50))

        drop_down_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 40)
        drop_down_button = pygame_gui.elements.UIDropDownMenu(
            options_list=['Select players', '1 Player', '2 Players', '3 Players', '4 Players'],
            starting_option='Select players',
            relative_rect=drop_down_button_rect,
        )

        running = True
        while running:
            time_delta = pygame.time.Clock().tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == drop_down_button:
                            if event.text != 'Select players':
                                self.num_players = int(event.text[0])
                                self.run()
                                running = False

                manager.process_events(event)

            screen.blit(background_image, (0, 0))
            screen.blit(logo_image, logo_rect)

            shadow_text_rect = shadow_text.get_rect()
            shadow_text_rect.center = (WIDTH // 2 + 2, HEIGHT // 2 + 2)
            screen.blit(shadow_text, shadow_text_rect)

            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, text_rect)

            manager.update(time_delta)
            manager.draw_ui(screen)

            pygame.display.update()

    # initialises some visual stuff like the title and icon
    def visual(self):
        pygame.display.set_caption(TITLE)
        icon = pygame.image.load('../resources/logo.png')
        pygame.display.set_icon(icon)

    def draw_resources(self):
        pygame.draw.rect(self.board.screen, WHITE, (0, HEIGHT - 150, WIDTH, 150))
        posx = 20
        posy = HEIGHT - 135
        r_clay2 = pygame.transform.scale(r_clay, (56.8, 87.8))
        self.board.screen.blit(r_clay2, (posx, posy))
        r_ore2 = pygame.transform.scale(r_ore, (56.8, 87.8))
        self.board.screen.blit(r_ore2, (posx + 66.8, posy))
        r_sheep2 = pygame.transform.scale(r_sheep, (56.8, 87.8))
        self.board.screen.blit(r_sheep2, (posx + (66.8 * 2), posy))
        r_wheat2 = pygame.transform.scale(r_wheat, (56.8, 87.8))
        self.board.screen.blit(r_wheat2, (posx + (66.8 * 3), posy))
        r_wood2 = pygame.transform.scale(r_wood, (56.8, 87.8))
        self.board.screen.blit(r_wood2, (posx + (66.8 * 4), posy))

        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        clay_text = font.render(str(self.current_player.resources[CLAY]), 1, BLACK)
        ore_text = font.render(str(self.current_player.resources[ORE]), 1, BLACK)
        sheep_text = font.render(str(self.current_player.resources[SHEEP]), 1, BLACK)
        wheat_text = font.render(str(self.current_player.resources[WHEAT]), 1, BLACK)
        wood_text = font.render(str(self.current_player.resources[WOOD]), 1, BLACK)

        posx2 = 40.8
        self.board.screen.blit(clay_text, (posx2, HEIGHT - 37.8))
        self.board.screen.blit(ore_text, (posx2 + 67, HEIGHT - 37.8))
        self.board.screen.blit(sheep_text, (posx2 + (67*2), HEIGHT - 37.8))
        self.board.screen.blit(wheat_text, (posx2 + (67*3), HEIGHT - 37.8))
        self.board.screen.blit(wood_text, (posx2 + (67*4), HEIGHT - 37.8))

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

    def draw_settlement_button(self):
        pos_x = 20 + (66.8*5)
        pos_y = HEIGHT - 135
        button_width, button_height = 100, 87.8
        self.settlement_button_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, (200, 150, 200), self.settlement_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Settlement", 1, (100, 50, 100))
        text_pos = text.get_rect(center=self.settlement_button_rect.center)
        self.board.screen.blit(text, text_pos)

    def draw_road_button(self):
        pos_x = 20 + (66.8*7)
        pos_y = HEIGHT - 135
        button_width, button_height = 100, 87.8
        self.road_button_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, (200, 150, 200), self.road_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Road", 1, (100, 50, 100))
        text_pos = text.get_rect(center=self.road_button_rect.center)
        self.board.screen.blit(text, text_pos)

    # ends turn
    def end_turn(self):
        player_count = len(self.players)
        current_player_index = self.players.index(self.current_player)
        if current_player_index == player_count -1:
            for player in self.players:
                print("Player " + str(player.num) + " has " + str(player.resources))
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
            while self.turn_number < 3:
                self.update()
                self.handle_settlement(self.current_player)
                self.handle_road(self.current_player)
                self.end_turn()
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if self.end_turn_button_rect.collidepoint(location):
                    if self.can_end_turn(self.current_player):
                        self.dice_count = 0
                        self.end_turn()
                    else:
                        print("Cannot end turn")
                        return -1
                if self.turn_number < 3:
                    self.handle_settlement(self.current_player)
                elif self.settlement_button_rect.collidepoint(location):
                    self.handle_settlement(self.current_player)
                elif self.road_button_rect.collidepoint(location):
                    self.handle_road(self.current_player)
                if self.dice.dice_rect.collidepoint(location):
                    if self.turn_number > 2:
                        if not self.dice_count > 0:
                            self.dice.roll()
                            self.board.harvest_resource(self.dice.total_dice_num())
                            print(self.dice.total_dice_num())
                            self.dice_count += 1
                        else:
                            print("Player: " + str(self.current_player.num) + " has already rolled on this turn.")
                    else:
                        print("Cannot roll dice until initial placements have been made.")

    def handle_settlement(self, player):
        count = self.player_settlement_count(player)

        if self.turn_number == 1:
            if count == 0:
                self.board.place_settlement(player, True)
            else:
                print("Cannot place another settlement on this turn")
                return -1
        elif self.turn_number == 2:
            if count == 1:
                self.board.place_settlement(player, True)
            else:
                print("Cannot place another settlement on this turn")
                return -1
        else:
            self.board.place_settlement(player, False)

    def handle_road(self, player):
        count = self.player_road_count(player)

        if self.turn_number == 1:
            if count == 0:
                self.board.place_road(player, True)
            else:
                print("Cannot place another road on this turn")
                return -1
        elif self.turn_number == 2:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
            if count == 1:
                self.board.place_road(player, True)
            else:
                print("Cannot place another road on this turn")
                return -1
        else:
            self.board.place_road(player, False)

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
        elif self.dice_count < 1:
            return False
        else:
            return True

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
