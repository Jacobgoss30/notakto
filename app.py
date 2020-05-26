"""Notakto vs Computer"""
import sys
import os.path
import numpy as np
import pygame


pygame.init()

ASSET_PATH = os.path.abspath(os.path.dirname(__file__)) + "/assets/"

WIN_WIDTH = 490
WIN_HEIGHT = 490
BOX_SIZE = 150
OFFSET = 10
WIN_COLOUR = (30, 30, 30)
TITLE = "Notakto"

empty = (240, 240, 240)
red = (239, 57, 57)

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
    def __init__(self, position, size, filled, index):
        self.rect = (position[0], position[1], size, size)
        self.filled = filled
        self.index = index

    def draw(self):
        if self.filled:
            colour = red
        else:
            colour = empty
        pygame.draw.rect(wn, colour, self.rect)

    def touching_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        return pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1])


def render_screen(grid, turn):
    wn.fill(WIN_COLOUR)

    for box in grid:
        box.draw()

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

def play(turn, grid, grid_data):
    """Plays a match and returns outcome"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            for box in grid:
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        box.touching_mouse()):
                    if not box.filled:
                        box.filled = True
                        grid_data[box.index[0], box.index[1]] = True
                        turn = "b" if turn == "r" else "r"

        render_screen(grid, turn)

        if check_dead(grid_data):
            return turn

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

def run():
    """runs the game"""
    while True:
        turn = "r"
        grid, grid_data = initialise_match()
        winner = play(turn, grid, grid_data)
        end_match(winner)

if __name__ == '__main__':
    run()
