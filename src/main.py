import pygame
from settings import *
import sys
from src.board import Board


class Main:

    def __init__(self):
        pygame.init()
        self.board = Board(WIDTH, HEIGHT)
        self.clock = pygame.time.Clock()
        self.count = 0


    # main function to run the game
    def run(self):
        self.board.draw()
        pygame.display.flip()
        self.running = True

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
        font = pygame.font.Font("../resources/Retro Gaming.ttf", 30)
        text = font.render("Click to start.", 1, WHITE)

        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.run()

            screen.blit(text, (250, 250))

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
