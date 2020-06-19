"""Notakto vs Computer"""
import sys
import time
import numpy as np
import pygame
from utils import check_dead, IMAGES
from cpu import cpu_turn
from mdp import load_mdp, save_mdp, update_data


pygame.init()


WIN_WIDTH = 490
WIN_HEIGHT = 790
BOX_SIZE = 150
OFFSET = 10
WIN_COLOUR = (30, 30, 30)
TITLE = "Notakto"

EMPTY = (240, 240, 240)
RED = (239, 57, 57)

FONT = pygame.font.Font(pygame.font.get_default_font(), 20)

WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)

MDP = load_mdp()

class GridBox:
    """Class for grid boxes"""
    def __init__(self, position, size, filled, index):
        self.rect = (position[0], position[1], size, size)
        self.filled = filled
        self.index = index

    def draw(self):
        """Draws grid box to screen"""
        if self.filled:
            colour = RED
        else:
            colour = EMPTY
        pygame.draw.rect(WINDOW, colour, self.rect)

    def touching_mouse(self):
        """Returns true if mouse is touching grid box"""
        mouse_pos = pygame.mouse.get_pos()
        return pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1])

def render_screen(grid, scores, turn=None, winner=None):
    """Blits the grid boxes and mouse to the screen"""
    WINDOW.fill(WIN_COLOUR)

    for box in grid:
        box.draw()

    blit_scores(scores)
    if winner is None:
        blit_turn(turn)
    else:
        blit_winner(winner)
    WINDOW.blit(IMAGES['mouse'],
                (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
    pygame.display.update()

def blit_scores(scores):
    """Blits the scores to the bottom of the screen"""
    textsurface = FONT.render(f'Player {scores[0]} - {scores[1]} CPU',
                              True, (255, 255, 255))
    WINDOW.blit(textsurface, (10, 700))

def blit_turn(turn):
    """Blits the current turn to the top of the screen"""
    if turn == 'p':
        text = 'Your Turn'
    else:
        text = 'CPU Turn'
    textsurface = FONT.render(text, True, (255, 255, 255))
    WINDOW.blit(textsurface, (10, 180))


def blit_winner(winner):
    """Blits the winner image to screen"""
    img = IMAGES[winner]
    WINDOW.blit(img, (WIN_WIDTH / 2 - img.get_width() / 2, 10))
    WINDOW.blit(IMAGES['continue'],
                (WIN_WIDTH / 2 - IMAGES['continue'].get_width() / 2, 150))

def initialise_match():
    """Initialises the playing grid data and visual grid"""
    grid_data = np.zeros((3, 3)).astype(bool)
    grid = []
    for j in range(3):
        y_coord = 200 + BOX_SIZE * j + OFFSET * (j + 1)
        for i in range(3):
            x_coord = BOX_SIZE * i + OFFSET * (i + 1)
            grid.append(GridBox((x_coord, y_coord), BOX_SIZE, False, (i, j)))
    return grid, grid_data

def play(turn, grid, grid_data, scores):
    """Plays a match and returns outcome"""
    play_info = {
        'turns': 0,
        'state_no': None,
        'cpu_policy': None
    }
    time_end = 0
    while True:
        pygame.time.wait(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if turn == 'p':
                for box in grid:
                    if (event.type == pygame.MOUSEBUTTONDOWN and
                            box.touching_mouse() and
                            not box.filled):
                        box.filled = True
                        grid_data[box.index] = True
                        turn = "c"
                        play_info['turns'] += 1
                time_end = time.time() + 0.5

        if turn == 'c':
            if time.time() > time_end:
                grid, grid_data, play_info = cpu_turn(grid, grid_data,
                                                      play_info, MDP)
                turn = "p"
                play_info['turns'] += 1

        render_screen(grid, scores, turn=turn)

        if check_dead(grid_data):
            return turn, grid

def end_match(winner, grid, scores):
    """Prints winner to screen"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        render_screen(grid, scores, winner=winner)

def update_scores(scores, winner):
    """Updates the scores with the winner"""
    if winner == 'p':
        scores[0] += 1
    else:
        scores[1] += 1
    return scores

def run():
    """runs the game"""
    scores = [0, 0]
    turn = "p"
    while True:
        grid, grid_data = initialise_match()
        winner, grid = play(turn, grid, grid_data, scores)
        update_data(winner, turn, MDP)
        scores = update_scores(scores, winner)
        end_match(winner, grid, scores)
        turn = "c" if turn == "p" else "p"

if __name__ == '__main__':
    run()
