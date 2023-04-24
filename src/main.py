import pygame
from settings import *
import sys
from board import Board
from player import Player


class Main:

    def __init__(self):
        pygame.init()
        self.board = Board(WIDTH, HEIGHT)
        self.clock = pygame.time.Clock()
        self.count = 0
        self.num_players = 0
        self.players = []

    # main function to run the game
    def run(self):
        self.board.draw()
        self.draw_end_turn_button()
        pygame.display.flip()
        self.running = True

        # loop to create list of objects of players
        for i in range(self.num_players):
            player = Player(i+1)
            self.players.append(player)
        self.currentPlayer = self.players[0]
        print(self.players)
        print("Player " + str(self.currentPlayer.num))

        # loops to keep game running and updating until it is closed
        while self.running:
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
    def endTurn(self):
        player_count = len(self.players)
        current_player_index = self.players.index(self.currentPlayer)
        self.currentPlayer = self.players[(current_player_index + 1) % player_count]
        print("Player " + str(self.currentPlayer.num))

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
                    self.endTurn()
                else:
                    self.board.place_settlement(self.currentPlayer, location)

    # quits game
    def quit(self):
        sys.exit()


m = Main()
while True:
    m.menu()
