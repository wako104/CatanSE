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
        self.currentPlayer = 0
        self.num_players = 0

    # main function to run the game
    def run(self):
        self.board.draw()
        pygame.display.flip()
        self.running = True

        # loop to create list of objects of players
        players = []
        for i in range(self.num_players):
            player = Player()
            players.append(player)
        print(players)

        # loops to keep game running and updating until it is closed
        while self.running:
            self.clock.tick(FPS)
            self.visual()
            self.events()
            self.update()

    def menu(self):
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
                self.board.place_settlement(location)

    # quits game
    def quit(self):
        sys.exit()


m = Main()
while True:
    m.menu()
