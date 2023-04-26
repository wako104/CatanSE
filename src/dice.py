import random
import pygame
from settings import *


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
        self.dice_rect = pygame.Rect(WIDTH - 170, HEIGHT / 2, 145, 70)
        self.dice_num1 = 0
        self.dice_num2 = 0

    def roll(self):
        self.dice_num1 = random.choice(self.numbers)
        self.dice_num2 = random.choice(self.numbers)
        self.draw_dice(self.dice_num1, self.dice_num2)

    def draw_dice(self, dice1, dice2):
        pygame.draw.rect(self.screen, BG_COLOUR, (WIDTH - 170, HEIGHT / 2, 200, 100))
        dice1_img = pygame.transform.scale(self.dice_images[dice1-1], (70, 70))
        dice2_img = pygame.transform.scale(self.dice_images[dice2-1], (70, 70))
        self.screen.blit(dice1_img, (WIDTH - 170, HEIGHT / 2))
        self.screen.blit(dice2_img, (WIDTH - 100, HEIGHT / 2))

    def draw_default_dice(self):
        dice1_img = pygame.transform.scale(self.dice_images[5], (70, 70))
        dice2_img = pygame.transform.scale(self.dice_images[5], (70, 70))
        self.screen.blit(dice1_img, (WIDTH - 170, HEIGHT / 2))
        self.screen.blit(dice2_img, (WIDTH - 100, HEIGHT / 2))

    def total_dice_num(self):
        return self.dice_num1 + self.dice_num2
