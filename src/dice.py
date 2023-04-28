import random
import pygame
from settings import *

'''
Author: Rob
Class: Creates a dice that can be rolled by a player
'''

class Dice:

    def __init__(self):
        self.numbers = [1, 2, 3, 4, 5, 6]
        self.dice_images = [
            pygame.image.load("../resources/dice1.png"),
            pygame.image.load("../resources/dice2.png"),
            pygame.image.load("../resources/dice3.png"),
            pygame.image.load("../resources/dice4.png"),
            pygame.image.load("../resources/dice5.png"),
            pygame.image.load("../resources/dice6.png"),
        ]
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.height = (HEIGHT / 2) + 150
        self.width = WIDTH - 150
        self.dice_rect = pygame.Rect(self.width, self.height, 145, 70)
        self.dice_num1 = 0
        self.dice_num2 = 0

    def roll(self):
        self.dice_num1 = random.choice(self.numbers)
        self.dice_num2 = random.choice(self.numbers)
        self.draw_dice(self.dice_num1, self.dice_num2)

    def draw_dice(self, dice1, dice2):
        pygame.draw.rect(self.screen, BG_COLOUR, (self.width, self.height, 200, 70))
        dice1_img = pygame.transform.scale(self.dice_images[dice1-1], (70, 70))
        dice2_img = pygame.transform.scale(self.dice_images[dice2-1], (70, 70))
        self.screen.blit(dice1_img, (self.width, self.height))
        self.screen.blit(dice2_img, (self.width + 70, self.height))

    def draw_default_dice(self):
        dice1_img = pygame.transform.scale(self.dice_images[5], (70, 70))
        dice2_img = pygame.transform.scale(self.dice_images[5], (70, 70))
        self.screen.blit(dice1_img, (self.width, self.height))
        self.screen.blit(dice2_img, (self.width + 70, self.height))

    def total_dice_num(self):
        return self.dice_num1 + self.dice_num2
