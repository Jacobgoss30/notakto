"""Notakto vs Computer"""
import sys
import os.path
from time import sleep
import numpy as np
import pygame


pygame.init()

ASSET_PATH = os.path.abspath(os.path.dirname(__file__)) + "/assets/"

WIN_WIDTH = 490
WIN_HEIGHT = 590
BOX_SIZE = 150
OFFSET = 10
WIN_COLOUR = (30, 30, 30)
TITLE = "Notakto"

empty = (240, 240, 240)
red = (239, 57, 57)

font = pygame.font.Font(pygame.font.get_default_font(), 20)

wn = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)


endImg = pygame.image.load(ASSET_PATH + "ClickToContinue.png")

images = {
    "r": pygame.image.load(ASSET_PATH + "RedWon.png"),
    "b": pygame.image.load(ASSET_PATH + "BlueWon.png"),
}

mice = {
    "r": pygame.image.load(ASSET_PATH + "RedMouse.png"),
    "b": pygame.image.load(ASSET_PATH + "BlueMouse.png")
}

class GridBox:
    """Class for grid boxes"""
    def __init__(self, position, size, filled, index):
        self.rect = (position[0], position[1], size, size)
        self.filled = filled
        self.index = index

    def draw(self):
        """Draws grid box to screen"""
        if self.filled:
            colour = red
        else:
            colour = empty
        pygame.draw.rect(wn, colour, self.rect)

    def touching_mouse(self):
        """Returns true if mouse is touching grid box"""
        mouse_pos = pygame.mouse.get_pos()
        return pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1])

def render_screen(grid, turn, scores):
    """Blits the grid boxes and mouse to the screen"""
    wn.fill(WIN_COLOUR)

    for box in grid:
        box.draw()

    blit_scores(scores)
    wn.blit(mice[turn], (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
    pygame.display.update()

def check_dead(grid):
    """Checks if the grid is dead"""
    for i in range(3):
        if sum(grid[:, i]) == 3: # Check columns
            return True
        if sum(grid[i, :]) == 3: # Check rows
            return True
    if (np.trace(grid) == 3 or np.trace(np.fliplr(grid)) == 3): # Check diags
        return True
    return False

def initialise_match():
    """Initialises the playing grid data and visual grid"""
    grid_data = np.zeros((3, 3)).astype(bool)
    grid = []
    for j in range(3):
        y_coord = BOX_SIZE * j + OFFSET * (j + 1)
        for i in range(3):
            x_coord = BOX_SIZE * i + OFFSET * (i + 1)
            grid.append(GridBox((x_coord, y_coord), BOX_SIZE, False, (i, j)))
    return grid, grid_data

def play(turn, grid, grid_data, scores):
    """Plays a match and returns outcome"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if turn == 'r':
                for box in grid:
                    if (event.type == pygame.MOUSEBUTTONDOWN and
                            box.touching_mouse() and
                            not box.filled):
                        box.filled = True
                        grid_data[box.index] = True
                        turn = "b"
            else:
                grid, grid_data = cpu_turn(grid, grid_data)
                turn = "r"

        render_screen(grid, turn, scores)

        if check_dead(grid_data):
            sleep(0.5)
            return turn

def cpu_turn(grid, grid_data):
    """Plays the cpu turn and returns updated grid and grid data"""
    sleep(0.1)
    emptys = np.where(~grid_data)
    ind = np.random.randint(len(emptys))
    coords = (emptys[0][ind], emptys[1][ind])
    grid_data[coords] = True
    for box in grid:
        if box.index == coords:
            box.filled = True
    return grid, grid_data

def end_match(winner):
    """Prints winner to screen"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        wn.fill(WIN_COLOUR)

        img = images[winner]
        wn.blit(img, (WIN_WIDTH / 2 - img.get_width() / 2,
                      WIN_HEIGHT / 2 - img.get_height() / 2))

        wn.blit(endImg, (WIN_WIDTH / 2 - endImg.get_width() / 2, 350))
        mouse_pos = pygame.mouse.get_pos()
        wn.blit(mice[winner], (mouse_pos[0], mouse_pos[1]))

        pygame.display.update()

def blit_scores(scores):
    """Blits the scores to the bottom of the screen"""
    textsurface = font.render(f'Player {scores[0]} - {scores[1]} CPU',
                              True, (255, 255, 255))
    wn.blit(textsurface, (10, 500))

def update_scores(scores, winner):
    """Updates the scores with the winner"""
    if winner == 'r':
        scores[0] += 1
    else:
        scores[1] += 1
    return scores

def run():
    """runs the game"""
    scores = [0, 0]
    turn = "r"
    while True:
        grid, grid_data = initialise_match()
        winner = play(turn, grid, grid_data, scores)
        end_match(winner)
        scores = update_scores(scores, winner)
        turn = "b" if turn == "r" else "r"

if __name__ == '__main__':
    run()
