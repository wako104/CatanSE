import pygame
import math
import pygame_gui
from pygame import MOUSEBUTTONDOWN

from settings import *
import sys
from board import Board
from player import Player
from dice import Dice
import random
from building import Settlement


class Main:

    def __init__(self):
        self.winner = None
        self.yes_button_rect = pygame.Rect(WIDTH - 250 + 30 - 20, 450, 50, 25)
        self.no_button_rect = pygame.Rect(WIDTH - 250 + 30 + 40, 450, 50, 25)
        self.player4_rect = None
        self.player3_rect = None
        self.player2_rect = None
        self.player1_rect = None
        self.send_trade_rect = None
        self.reset_rect = None
        self.clay_t = 0
        self.ore_t = 0
        self.sheep_t = 0
        self.wheat_t = 0
        self.wood_t = 0
        self.clay_r = 0
        self.ore_r = 0
        self.sheep_r = 0
        self.wheat_r = 0
        self.wood_r = 0
        self.counter_box_s = None
        self.counter_box_l = None
        self.counter_box_w = None
        self.counter_box_o = None
        self.counter_box_c = None
        self.resource_box_l = None
        self.resource_box_w = None
        self.resource_box_s = None
        self.resource_box_o = None
        self.resource_box_c = None
        self.counter_box_s2 = None
        self.counter_box_l2 = None
        self.counter_box_w2 = None
        self.counter_box_o2 = None
        self.counter_box_c2 = None
        self.resource_box_l2 = None
        self.resource_box_w2 = None
        self.resource_box_s2 = None
        self.resource_box_o2 = None
        self.resource_box_c2 = None
        self.resource_positions = None
        pygame.init()
        self.board = Board(WIDTH, HEIGHT)
        self.clock = pygame.time.Clock()
        self.count = 0
        self.num_players = 0
        self.players = []
        self.turn_number = 1
        self.dice = Dice()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)
        self.font2 = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.dice_count = 0
        self.receive_resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD:0}
        self.give_resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD:0}
        self.red_counter = 0
        self.blue_counter = 0
        self.green_counter = 0
        self.orange_counter = 0
        self.colour1 = (241,140,140)
        self.colour2 = (170,235,255)
        self.colour3 = (173,228,206)
        self.colour4 = (255, 235, 150)
        self.trade_with = None
        self.placed_init_settlement = False
        self.placed_init_road = False
        self.settlement_button_colour = (200, 150, 200)
        self.road_button_colour = (200, 150, 200)

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
            self.check_for_winner()
            turn_number_text = self.font.render("Turn Number: " + str(self.turn_number), 1, (255, 255, 255))
            pygame.draw.rect(self.board.screen, BG_COLOUR, (0, 0, 200, 50))
            self.board.screen.blit(turn_number_text, (10, 10))
            self.draw_resources()
            self.draw_development()
            self.draw_trade_button()
            current_player_text = self.font.render("Player : " + str(self.current_player.num), 1, (255, 255, 255))
            pygame.draw.rect(self.board.screen, BG_COLOUR, (10, HEIGHT - 180, 150, 30))
            self.board.screen.blit(current_player_text, (10, HEIGHT - 180))
            self.draw_end_turn_button()
            self.draw_development_button()
            self.draw_settlement_button()
            self.draw_road_button()
            self.draw_city_button()
            self.draw_exit_button()
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

    def draw_trade_button(self):
        # Define the colors for the button and text
        button_colour = (200, 200, 200)
        text_colour = (0, 0, 0)
        resource_colour = (0, 200, 0)

        xpos = WIDTH - 250
        xpos2 = xpos + 30
        ypos = 120
        ypos2 = 145

        ypos3 = ypos + 90
        ypos4 = ypos2 + 90

        # Define the positions and sizes of the button and text
        button_rect = pygame.Rect(xpos, 60, 200, 315)
        button_rect_border = pygame.Rect(xpos - 5, 60 - 5, 200 + 10, 315 + 10)
        text_rect = pygame.Rect(xpos2 - 20, 95, 20, 20)

        # Draw the button and text
        pygame.draw.rect(self.board.screen, WHITE, button_rect_border)
        pygame.draw.rect(self.board.screen, button_colour, button_rect)
        self.board.screen.blit(self.font.render("Send", True, text_colour), text_rect)
        self.board.screen.blit(self.font.render("Receive", True, text_colour), (xpos2 - 20, 185))

        # Define the positions and sizes of the resource counters
        self.resource_positions = {
            "C": (xpos2, ypos),
            "O": (xpos2 + 30, ypos),
            "S": (xpos2 + (30 * 2), ypos),
            "W": (xpos2 + (30 * 3), ypos),
            "P": (xpos2 + (30 * 4), ypos)
        }

        self.resource_box_c = pygame.Rect(xpos2, ypos, 20, 20)
        self.resource_box_o = pygame.Rect(xpos2 + 30, ypos, 20, 20)
        self.resource_box_s = pygame.Rect(xpos2 + (30*2), ypos, 20, 20)
        self.resource_box_w = pygame.Rect(xpos2 + (30*3), ypos, 20, 20)
        self.resource_box_l = pygame.Rect(xpos2 + (30*4), ypos, 20, 20)

        self.counter_box_c = pygame.Rect(xpos2, ypos2, 20, 20)
        self.counter_box_o = pygame.Rect(xpos2 + 30, ypos2, 20, 20)
        self.counter_box_s = pygame.Rect(xpos2 + (30*2), ypos2, 20, 20)
        self.counter_box_w = pygame.Rect(xpos2 + (30*3), ypos2, 20, 20)
        self.counter_box_l = pygame.Rect(xpos2 + (30*4), ypos2, 20, 20)

        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_c)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_o)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_s)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_w)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_l)

        self.board.screen.blit(self.font.render(str(self.clay_t), 1, text_colour), self.counter_box_c)
        self.board.screen.blit(self.font.render(str(self.ore_t), 1, text_colour), self.counter_box_o)
        self.board.screen.blit(self.font.render(str(self.sheep_t), 1, text_colour), self.counter_box_s)
        self.board.screen.blit(self.font.render(str(self.wheat_t), 1, text_colour), self.counter_box_w)
        self.board.screen.blit(self.font.render(str(self.wood_t), 1, text_colour), self.counter_box_l)

        self.board.screen.blit(self.font.render("C", 1, text_colour), self.resource_box_c)
        self.board.screen.blit(self.font.render("O", 1, text_colour), self.resource_box_o)
        self.board.screen.blit(self.font.render("S", 1, text_colour), self.resource_box_s)
        self.board.screen.blit(self.font.render("W", 1, text_colour), self.resource_box_w)
        self.board.screen.blit(self.font.render("L", 1, text_colour), self.resource_box_l)

        self.resource_box_c2 = pygame.Rect(xpos2, ypos3, 20, 20)
        self.resource_box_o2 = pygame.Rect(xpos2 + 30, ypos3, 20, 20)
        self.resource_box_s2 = pygame.Rect(xpos2 + (30 * 2), ypos3, 20, 20)
        self.resource_box_w2 = pygame.Rect(xpos2 + (30 * 3), ypos3, 20, 20)
        self.resource_box_l2 = pygame.Rect(xpos2 + (30 * 4), ypos3, 20, 20)

        self.counter_box_c2 = pygame.Rect(xpos2, ypos4, 20, 20)
        self.counter_box_o2 = pygame.Rect(xpos2 + 30, ypos4, 20, 20)
        self.counter_box_s2 = pygame.Rect(xpos2 + (30 * 2), ypos4, 20, 20)
        self.counter_box_w2 = pygame.Rect(xpos2 + (30 * 3), ypos4, 20, 20)
        self.counter_box_l2 = pygame.Rect(xpos2 + (30 * 4), ypos4, 20, 20)

        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_c2)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_o2)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_s2)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_w2)
        pygame.draw.rect(self.board.screen, resource_colour, self.resource_box_l2)

        self.board.screen.blit(self.font.render(str(self.clay_r), 1, text_colour), self.counter_box_c2)
        self.board.screen.blit(self.font.render(str(self.ore_r), 1, text_colour), self.counter_box_o2)
        self.board.screen.blit(self.font.render(str(self.sheep_r), 1, text_colour), self.counter_box_s2)
        self.board.screen.blit(self.font.render(str(self.wheat_r), 1, text_colour), self.counter_box_w2)
        self.board.screen.blit(self.font.render(str(self.wood_r), 1, text_colour), self.counter_box_l2)

        self.board.screen.blit(self.font.render("C", 1, text_colour), self.resource_box_c2)
        self.board.screen.blit(self.font.render("O", 1, text_colour), self.resource_box_o2)
        self.board.screen.blit(self.font.render("S", 1, text_colour), self.resource_box_s2)
        self.board.screen.blit(self.font.render("W", 1, text_colour), self.resource_box_w2)
        self.board.screen.blit(self.font.render("L", 1, text_colour), self.resource_box_l2)

        trade_with_rect = pygame.Rect(xpos2 - 20, ypos3 + 55, 140, 25)
        self.board.screen.blit(self.font.render("Trade with:", True, text_colour), trade_with_rect)

        self.reset_rect = pygame.Rect(xpos2 + 90, 70, 70, 25)
        pygame.draw.rect(self.board.screen, (255, 255, 255), self.reset_rect)
        self.board.screen.blit(self.font.render("Reset", True, text_colour), self.reset_rect)

        self.send_trade_rect = pygame.Rect(xpos2 - 20, ypos3 + 130, 140, 25)
        pygame.draw.rect(self.board.screen, (255, 255, 255), self.send_trade_rect)
        self.board.screen.blit(self.font.render("Offer Trade", True, text_colour), self.send_trade_rect)

        # Define the positions and sizes of the player text and rectangles
        player_rect_width = 30
        player_rect_height = 30
        y_pos_player = 272 + 25
        self.player1_rect = pygame.Rect(xpos2-20, y_pos_player, player_rect_width, player_rect_height)
        self.player2_rect = pygame.Rect(xpos2-20 + player_rect_width + 10, y_pos_player, player_rect_width, player_rect_height)
        self.player3_rect = pygame.Rect(xpos2-20 + (player_rect_width + 10) * 2, y_pos_player, player_rect_width, player_rect_height)
        self.player4_rect = pygame.Rect(xpos2-20 + (player_rect_width + 10) * 3, y_pos_player, player_rect_width, player_rect_height)

        # Determine how many players to display
        if self.num_players == 4:
            pygame.draw.rect(self.board.screen, self.colour1, self.player1_rect)
            pygame.draw.rect(self.board.screen, self.colour2, self.player2_rect)
            pygame.draw.rect(self.board.screen, self.colour3, self.player3_rect)
            pygame.draw.rect(self.board.screen, self.colour4, self.player4_rect)
            self.board.screen.blit(self.font.render("P1", True, BLACK), self.player1_rect)
            self.board.screen.blit(self.font.render("P2", True, BLACK), self.player2_rect)
            self.board.screen.blit(self.font.render("P3", True, BLACK), self.player3_rect)
            self.board.screen.blit(self.font.render("P4", True, BLACK), self.player4_rect)
        elif self.num_players == 3:
            pygame.draw.rect(self.board.screen, self.colour1, self.player1_rect)
            pygame.draw.rect(self.board.screen, self.colour2, self.player2_rect)
            pygame.draw.rect(self.board.screen, self.colour3, self.player3_rect)
            self.board.screen.blit(self.font.render("P1", True, BLACK), self.player1_rect)
            self.board.screen.blit(self.font.render("P2", True, BLACK), self.player2_rect)
            self.board.screen.blit(self.font.render("P3", True, BLACK), self.player3_rect)
        elif self.num_players == 2:
            pygame.draw.rect(self.board.screen, self.colour1, self.player1_rect)
            pygame.draw.rect(self.board.screen, self.colour2, self.player2_rect)
            self.board.screen.blit(self.font.render("P1", True, BLACK), self.player1_rect)
            self.board.screen.blit(self.font.render("P2", True, BLACK), self.player2_rect)
        else:
            pygame.draw.rect(self.board.screen, self.colour1, self.player1_rect)
            self.board.screen.blit(self.font.render("P1", True, BLACK), self.player1_rect)

    def check_for_winner(self):
        for i, player in enumerate(self.players):
            if player.get_victory_points() == 10:
                winner = player
                print("Game over. Player " + str(i + 1) + " has reached 10 victory points and won the game")
                self.end_game_screen(winner)

    def end_game_screen(self, winner):
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

        text = self.font.render("PLAYER " + str(winner.num) + " HAS WON!", 1, WHITE)
        shadow_text = self.font.render("PLAYER " + str(winner.num) + " HAS WON!", 1, (50, 50, 50))

        running = True

        while running:
            time_delta = pygame.time.Clock().tick(60) / 1000.0

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

            self.events()

            pygame.display.update()

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

    def draw_development(self):
        pos_x = 20
        pos_y = HEIGHT - 700

        vp_card = pygame.Rect(pos_x, pos_y, 56.8, 87.8)
        vp = pygame.transform.scale(d_victory_point, (35, 55))
        vp_rect = vp.get_rect()
        vp_rect.center = vp_card.center
        pygame.draw.rect(self.board.screen, VICTORYPOINT, vp_card)
        self.board.screen.blit(vp, vp_rect)

        knight_card = pygame.Rect(pos_x, pos_y + 100, 56.8, 87.8)
        knight = pygame.transform.scale(d_knight, (40, 55))
        knight_rect = knight.get_rect()
        knight_rect.center = knight_card.center
        pygame.draw.rect(self.board.screen, KNIGHT, knight_card)
        self.board.screen.blit(knight, knight_rect)

        road_card = pygame.Rect(pos_x, pos_y + (100 * 2), 56.8, 87.8)
        road = pygame.transform.scale(d_road, (35, 55))
        road_rect = road.get_rect()
        road_rect.center = road_card.center
        pygame.draw.rect(self.board.screen, DEVELOPMENTROAD, road_card)
        self.board.screen.blit(road, road_rect)

        monopoly_card = pygame.Rect(pos_x, pos_y + (100 * 3), 56.8, 87.8)
        monopoly = pygame.transform.scale(d_monopoly, (35, 55))
        monopoly_rect = monopoly.get_rect()
        monopoly_rect.center = monopoly_card.center
        pygame.draw.rect(self.board.screen, MONOPOLY, monopoly_card)
        self.board.screen.blit(monopoly, monopoly_rect)

        yofp_card = pygame.Rect(pos_x, pos_y + (100 * 4), 56.8, 87.8)
        yofp = pygame.transform.scale(d_yofp, (40, 55))
        yofp_rect = yofp.get_rect()
        yofp_rect.center = yofp_card.center
        pygame.draw.rect(self.board.screen, YEAROFPLENTY, yofp_card)
        self.board.screen.blit(yofp, yofp_rect)

        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        vp_text = font.render(str(self.current_player.cards[VICTORYPOINT]), 1, BLACK)
        vp_text_rect = vp_text.get_rect()
        vp_text_rect.center = (vp_card.centerx + 50, vp_card.centery)
        pygame.draw.rect(self.board.screen, BG_COLOUR3, vp_text_rect)
        self.board.screen.blit(vp_text, vp_text_rect)

        knight_text = font.render(str(self.current_player.cards[KNIGHT]), 1, BLACK)
        knight_text_rect = knight_text.get_rect()
        knight_text_rect.center = (knight_card.centerx + 50, knight_card.centery)
        pygame.draw.rect(self.board.screen, BG_COLOUR2, knight_text_rect)
        self.board.screen.blit(knight_text, knight_text_rect)
        
        road_text = font.render(str(self.current_player.cards[DEVELOPMENTROAD]), 1, BLACK)
        road_text_rect = road_text.get_rect()
        road_text_rect.center = (road_card.centerx + 50, road_card.centery)
        pygame.draw.rect(self.board.screen, BG_COLOUR2, road_text_rect)
        self.board.screen.blit(road_text, road_text_rect)

        monopoly_text = font.render(str(self.current_player.cards[MONOPOLY]), 1, BLACK)
        monopoly_text_rect = monopoly_text.get_rect()
        monopoly_text_rect.center = (monopoly_card.centerx + 50, monopoly_card.centery)
        pygame.draw.rect(self.board.screen, BG_COLOUR2, monopoly_text_rect)
        self.board.screen.blit(monopoly_text, monopoly_text_rect)
        
        yofp_text = font.render(str(self.current_player.cards[YEAROFPLENTY]), 1, BLACK)
        yofp_text_rect = yofp_text.get_rect()
        yofp_text_rect.center = (yofp_card.centerx + 50, yofp_card.centery)
        pygame.draw.rect(self.board.screen, BG_COLOUR3, yofp_text_rect)
        self.board.screen.blit(yofp_text, yofp_text_rect)

    # creates end turn button
    def draw_end_turn_button(self):
        button_width, button_height = 100, 50
        button_x = WIDTH - button_width - 10
        button_y = HEIGHT - button_height - 50
        self.end_turn_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, (255, 0, 0), self.end_turn_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("End Turn", 1, (255, 255, 255))
        text_pos = text.get_rect(center=self.end_turn_button_rect.center)
        self.board.screen.blit(text, text_pos)

    def draw_settlement_button(self):
        pos_x = WIDTH - 350
        pos_y = HEIGHT - 120
        button_width, button_height = 100, 87.8
        self.settlement_button_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        self.settlement_button_colour = (200, 65, 200)
        pygame.draw.rect(self.board.screen, self.settlement_button_colour, self.settlement_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Settlement", 1, (100, 50, 100))
        text_pos = text.get_rect(center=self.settlement_button_rect.center)
        self.board.screen.blit(text, text_pos)

    def draw_road_button(self):
        pos_x = WIDTH - 230
        pos_y = HEIGHT - 120
        button_width, button_height = 100, 87.8
        self.road_button_colour = (200, 65, 200)
        self.road_button_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, self.road_button_colour, self.road_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Road", 1, (100, 50, 100))
        text_pos = text.get_rect(center=self.road_button_rect.center)
        self.board.screen.blit(text, text_pos)

    def draw_city_button(self):
        pos_x = WIDTH - 470
        pos_y = HEIGHT - 120
        button_width, button_height = 100, 87.8
        self.city_button_colour = (200, 65, 200)
        self.city_button_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, self.city_button_colour, self.city_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("City", 1, (100, 50, 100))
        text_pos = text.get_rect(center=self.city_button_rect.center)
        self.board.screen.blit(text, text_pos)

    def draw_development_button(self):
        pos_x = WIDTH - 600
        pos_y = HEIGHT - 120
        button_width, button_height = 110, 87.8
        self.development_button_colour = (230, 131, 32)
        self.development_button_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, self.development_button_colour, self.development_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Buy\nDevelopment\nCard", True, (100, 50, 100))
        text_pos = text.get_rect(center=self.development_button_rect.center)
        self.board.screen.blit(text, text_pos)

    def draw_exit_button(self):
        pos_x = WIDTH - 230
        pos_y = HEIGHT - 220
        button_width, button_height = 60, 60
        self.exit_button_colour = (255, 0, 0)
        self.exit_button_rect = pygame.Rect(pos_x, pos_y, button_width, button_height)
        pygame.draw.rect(self.board.screen, self.exit_button_colour, self.exit_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render("Exit", 1, (100, 50, 100))
        text_pos = text.get_rect(center=self.exit_button_rect.center)
        self.board.screen.blit(text, text_pos)

    # ends turn
    def end_turn(self):
        player_count = len(self.players)
        current_player_index = self.players.index(self.current_player)
        if current_player_index == player_count -1:
            for player in self.players:
                if self.turn_number == 2:
                    second_settlement = self.board.existing_settlements[current_player_index + len(self.players)]
                    self.board.initial_resource_collection(player, second_settlement)
                print("Player " + str(player.num) + " has " + str(player.resources))
            self.turn_number += 1
        self.current_player = self.players[(current_player_index + 1) % player_count]
        self.colour1 = (241, 140, 140)
        self.colour2 = (170, 235, 255)
        self.colour3 = (173, 228, 206)
        self.colour4 = (255, 235, 150)
        self.clay_t = 0
        self.ore_t = 0
        self.sheep_t = 0
        self.wheat_t = 0
        self.wood_t = 0
        self.clay_r = 0
        self.ore_r = 0
        self.sheep_r = 0
        self.wheat_r = 0
        self.wood_r = 0
        print("Player " + str(self.current_player.num))

    # checks for game updates
    def update(self):
        pygame.display.update()

    # checks events, checks if the game is closed
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if self.turn_number < 3:
                selected = False
                self.update()
                while not selected:
                    pygame.mouse.set_cursor(pygame.cursors.ball)
                    wait = pygame.event.wait()
                    if wait.type == pygame.QUIT:
                        self.quit()
                    if wait.type == MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        for option in self.board.unique_v:
                            if mouse_position[0] in range(option[0] - 15, option[0] + 15):
                                if mouse_position[1] in range(option[1] - 15, option[1] + 15):
                                    self.handle_settlement(self.current_player, option)
                                    selected = True
                        if not selected:
                            print("Select an initial settlement location.")
                    elif wait.type == pygame.QUIT:
                        self.quit()
                self.update()
                selected = False
                while not selected:
                    pygame.mouse.set_cursor(pygame.cursors.ball)
                    wait = pygame.event.wait()
                    if wait.type == pygame.QUIT:
                        self.quit()
                    if wait.type == MOUSEBUTTONDOWN:
                        mouse_position = pygame.mouse.get_pos()
                        for option in self.board.centre_edge:
                            print("test123")
                            if mouse_position[0] in range(option[0][0] - 15, option[0][0] + 15):
                                if mouse_position[1] in range(option[0][1] - 15, option[0][1] + 15):
                                    print("found edge")
                                    self.handle_road(self.current_player, option)
                                    selected = True
                        if not selected:
                            print("Select an initial road location")
                    elif wait.type == pygame.QUIT:
                        self.quit()
                self.update()
                self.end_turn()
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if self.turn_number > 2:
                    if not self.dice.dice_rect.collidepoint(location):
                        if self.dice_count < 1:
                            print("Roll dice first")
                            return -1
                if self.end_turn_button_rect.collidepoint(location):
                    if self.can_end_turn(self.current_player):
                        self.dice_count = 0
                        self.end_turn()
                    else:
                        print("Cannot end turn")
                        return -1
                if self.settlement_button_rect.collidepoint(location):
                    self.handle_settlement(self.current_player, None)
                elif self.road_button_rect.collidepoint(location):
                    self.handle_road(self.current_player, None)
                elif self.city_button_rect.collidepoint(location):
                    self.handle_city(self.current_player)
                elif self.development_button_rect.collidepoint(location):
                    self.handle_get_development(self.current_player)
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

                if self.reset_rect.collidepoint(location):
                    self.clay_t = 0
                    self.ore_t = 0
                    self.sheep_t = 0
                    self.wheat_t = 0
                    self.wood_t = 0
                    self.clay_r = 0
                    self.ore_r = 0
                    self.sheep_r = 0
                    self.wheat_r = 0
                    self.wood_r = 0
                    self.give_resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD: 0}
                    self.receive_resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD: 0}
                    self.colour1 = (241, 140, 140)
                    self.colour2 = (170, 235, 255)
                    self.colour3 = (173, 228, 206)
                    self.colour4 = (255, 235, 150)
                    self.trade_with = None

                if self.resource_box_c.collidepoint(location):
                    self.clay_t += 1
                if self.resource_box_o.collidepoint(location):
                    self.ore_t += 1
                if self.resource_box_s.collidepoint(location):
                    self.sheep_t += 1
                if self.resource_box_w.collidepoint(location):
                    self.wheat_t += 1
                if self.resource_box_l.collidepoint(location):
                    self.wood_t += 1
                if self.resource_box_c2.collidepoint(location):
                    self.clay_r += 1
                if self.resource_box_o2.collidepoint(location):
                    self.ore_r += 1
                if self.resource_box_s2.collidepoint(location):
                    self.sheep_r += 1
                if self.resource_box_w2.collidepoint(location):
                    self.wheat_r += 1
                if self.resource_box_l2.collidepoint(location):
                    self.wood_r += 1

                if self.send_trade_rect.collidepoint(location):
                    if self.trade_with != None:
                        req = {CLAY: self.clay_r, ORE: self.ore_r, SHEEP: self.sheep_r, WHEAT: self.wheat_r, WOOD: self.wood_r}
                        give = {CLAY: self.clay_t, ORE: self.ore_t, SHEEP: self.sheep_t, WHEAT: self.wheat_t, WOOD: self.wood_t}

                        req_zero = all(val == 0 for val in req.values())
                        give_zero = all(val == 0 for val in give.values())

                        if req_zero and give_zero:
                            pass

                        elif all(req[key] <= self.trade_with.resources[key] for key in req) and all(give[key] <= self.current_player.resources[key] for key in give):
                            self.request_trade(req, give)
                            self.colour1 = (241, 140, 140)
                            self.colour2 = (170, 235, 255)
                            self.colour3 = (173, 228, 206)
                            self.colour4 = (255, 235, 150)
                            self.draw_accept_trade_offer()

                        else:
                            print("Players do not have required resources to trade!")
                    else:
                        pass

                if self.player1_rect.collidepoint(location):
                    if self.red_counter == 1:
                        self.colour1 = (241,140,140)
                        self.red_counter = 0
                        self.trade_with = None
                    else:
                        self.colour1 = PLAYERCOLOUR1
                        self.colour2 = (170, 235, 255)
                        self.colour3 = (173, 228, 206)
                        self.colour4 = (255, 235, 150)
                        self.red_counter = 1
                        self.trade_with = self.players[0]

                if self.player2_rect.collidepoint(location):
                    if self.blue_counter == 1:
                        self.colour2 = (170,235,255)
                        self.blue_counter = 0
                        self.trade_with = None
                    else:
                        self.colour1 = (241, 140, 140)
                        self.colour2 = PLAYERCOLOUR2
                        self.colour3 = (173, 228, 206)
                        self.colour4 = (255, 235, 150)
                        self.blue_counter = 1
                        self.trade_with = self.players[1]

                if self.player3_rect.collidepoint(location):
                    if self.green_counter == 1:
                        self.colour3 = (173,228,206)
                        self.green_counter = 0
                        self.trade_with = None
                    else:
                        self.colour1 = (241, 140, 140)
                        self.colour2 = (170, 235, 255)
                        self.colour3 = PLAYERCOLOUR3
                        self.colour4 = (255, 235, 150)
                        self.green_counter = 1
                        self.trade_with = self.players[2]

                if self.player4_rect.collidepoint(location):
                    if self.orange_counter == 1:
                        self.colour4 = (255, 235, 150)
                        self.orange_counter = 0
                        self.trade_with = None
                    else:
                        self.colour1 = (241, 140, 140)
                        self.colour2 = (170, 235, 255)
                        self.colour3 = (173, 228, 206)
                        self.colour4 = PLAYERCOLOUR4
                        self.orange_counter = 1
                        self.trade_with = self.players[3]

                if self.no_button_rect.collidepoint(location):
                    accept_box_rect = pygame.Rect(WIDTH - 250, 400, 200, 85)
                    pygame.draw.rect(self.board.screen, BG_COLOUR, accept_box_rect)
                    self.trade_with = None
                    self.clay_t = 0
                    self.ore_t = 0
                    self.sheep_t = 0
                    self.wheat_t = 0
                    self.wood_t = 0
                    self.clay_r = 0
                    self.ore_r = 0
                    self.sheep_r = 0
                    self.wheat_r = 0
                    self.wood_r = 0

                if self.yes_button_rect.collidepoint(location):
                    self.accept_trade(self.current_player, self.trade_with)
                    print("trade complete")
                    accept_box_rect = pygame.Rect(WIDTH - 250, 400, 200, 85)
                    pygame.draw.rect(self.board.screen, BG_COLOUR, accept_box_rect)
                    self.trade_with = None

    def draw_accept_trade_offer(self):
        player_rect_width = 30
        player_rect_height = 30
        y_pos_player = 272 + 25

        xpos = WIDTH - 250
        xpos2 = xpos + 30
        ypos = 120
        ypos2 = 145

        ypos3 = ypos + 90
        ypos4 = ypos2 + 90

        player_rects = [
            pygame.Rect(xpos2 - 20, 410, player_rect_width, player_rect_height)
            for _ in range(len(self.players))
        ]

        print(self.players[0])
        print(self.trade_with)

        xpos = WIDTH - 250

        button_colour = (200, 200, 200)
        text_colour = (0, 0, 0)

        accept_text_rect = pygame.Rect(xpos + 48, 415, 200, 50)
        accept_box_rect = pygame.Rect(xpos, 400, 200, 85)
        self.yes_button_rect = pygame.Rect(xpos2 - 20, 450, 50, 25)
        self.no_button_rect = pygame.Rect(xpos2 + 40, 450, 50, 25)

        pygame.draw.rect(self.board.screen, button_colour, accept_box_rect)
        self.board.screen.blit(self.font2.render("Do you accept?", True, text_colour), accept_text_rect)
        pygame.draw.rect(self.board.screen, (255, 255, 255), self.yes_button_rect)
        pygame.draw.rect(self.board.screen, (255, 255, 255), self.no_button_rect)
        self.board.screen.blit(self.font2.render("Yes", True, text_colour), self.yes_button_rect)
        self.board.screen.blit(self.font2.render("No", True, text_colour), self.no_button_rect)

        player_colours = [PLAYERCOLOUR1, PLAYERCOLOUR2, PLAYERCOLOUR3, PLAYERCOLOUR4]

        for i, player in enumerate(self.players):
            if self.trade_with == player:
                pygame.draw.rect(self.board.screen, player_colours[i], player_rects[i])
                self.board.screen.blit(self.font.render(f"P{i + 1}", True, BLACK), player_rects[i])

    def handle_get_development(self, player):
        for required in DEVELOPMENT:
            if required not in player.resources.keys() or player.resources[required] < 1:
                print("Not enough resources to get development card")
                return -1
        else:
            dev_cards = [VICTORYPOINT, KNIGHT, DEVELOPMENTROAD, MONOPOLY, YEAROFPLENTY]
            choice = random.choice(dev_cards)
            player.get_development(choice)
            for required in DEVELOPMENT:
                player.resources[required] -= 1

    def handle_settlement(self, player, location):
        count = self.player_settlement_count(player)
        if location is not None:
            if self.turn_number == 1:
                if count == 0:
                    self.board.place_settlement(player, True, location, False, self.exit_button_rect)
                else:
                    print("Cannot place another settlement on this turn")
                    return -1
            elif self.turn_number == 2:
                if count == 1:
                    self.board.place_settlement(player, True, location, False, self.exit_button_rect)
                else:
                    print("Cannot place another settlement on this turn")
                    return -1
        else:
            self.board.place_settlement(player, False, None, False, self.exit_button_rect)

        pygame.mouse.set_cursor(pygame.cursors.arrow)

    def handle_road(self, player, location):
        count = self.player_road_count(player)
        if self.turn_number == 1:
            if count == 1:
                print("Cannot place another road this turn")
                return -1
        elif self.turn_number == 2:
            if count == 2:
                print("Cannot place another road this turn")
                return -1
        print("test")
        pygame.mouse.set_cursor(pygame.cursors.ball)
        if location is None:
            wait = pygame.event.wait()
            while wait.type != MOUSEBUTTONDOWN:
                wait = pygame.event.wait()
            if wait.type == MOUSEBUTTONDOWN:
                mouse_loc = pygame.mouse.get_pos()
                for option in self.board.centre_edge:
                    if mouse_loc[0] in range(option[0][0] - 10, option[0][0] + 10):
                        if mouse_loc[1] in range(option[0][1] - 10, option[0][1] + 10):
                            selected = option
        else:
            selected = location
        print(selected)
        print("hello")
        print("Edge")
        if self.turn_number == 1:
            if count == 0:
                if self.player_settlement_count(self.current_player) == 1:
                    print("test")
                    print(selected)
                    if not self.board.place_road(player, selected, True, False):
                        print("testing")
                        self.handle_road(player, location)
                        return -1
                else:
                    print("Place settlement before road")
            else:
                print("Cannot place another road on this turn")
                pygame.mouse.set_cursor(pygame.cursors.arrow)
                return -1
        elif self.turn_number == 2:

            if count == 1:
                if self.player_settlement_count(self.current_player) == 2:
                    player_settlements = self.player_settlements(self.current_player)
                    required_locations = []

                    for edge in self.board.centre_edge:
                        if player_settlements[1].location in edge[1]:
                            required_locations.append(edge[0])

                    current_location = selected[0]
                    if current_location in required_locations:
                        if not self.board.place_road(player, selected, True, False):
                            self.handle_road(player, location)
                            return -1
                        print("Must place next to your most recent settlement")
                        self.handle_road(player, location)
                        return -1
                else:
                    print("Place settlement before road")
                    pygame.mouse.set_cursor(pygame.cursors.arrow)
                    return -1
            else:
                print("Cannot place another road on this turn")
                pygame.mouse.set_cursor(pygame.cursors.arrow)
                return -1
        else:
            self.board.place_road(player, selected, False, False)
        pygame.mouse.set_cursor(pygame.cursors.arrow)

    def handle_city(self, player):
        self.board.build_city(player)

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
            print("Roll dice first")
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

    def player_settlements(self, player):
        player_settlements = []
        for settlement in self.board.existing_settlements:
            if settlement.player == self.current_player:
                player_settlements.append(settlement)
        return player_settlements

    def request_trade(self, receive, give):
        for resource, amount in receive.items():
            self.receive_resources[resource] += amount
        for resource, amount in give.items():
            self.give_resources[resource] += amount

    def accept_trade(self, player1, player2):
        player1.send_trade(self.give_resources)
        player1.receive_trade(self.receive_resources)
        player2.send_trade(self.receive_resources)
        player2.receive_trade(self.give_resources)
        self.give_resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD:0}
        self.receive_resources = {CLAY: 0, ORE: 0, SHEEP: 0, WHEAT: 0, WOOD:0}

    # quits game
    def quit(self):
        sys.exit()


m = Main()
while True:
    m.menu()
