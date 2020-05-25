"""2 Player noughts and crosses"""
import sys
import os.path
import pygame


pygame.init()

ASSET_PATH = os.path.abspath(os.path.dirname(__file__)) + "/assets/"

WIN_WIDTH = 490
WIN_HEIGHT = 490
BOX_SIZE = 150
OFFSET = 10
WIN_COLOUR = (30, 30, 30)
TITLE = "Noughts and Crosses"

wn = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(TITLE)

blueMouse = pygame.image.load(ASSET_PATH + "BlueMouse.png")
redMouse = pygame.image.load(ASSET_PATH + "RedMouse.png")
pygame.mouse.set_visible(False)

startBoxColor = (240, 240, 240)
red = (239, 57, 57)
blue = (46, 121, 232)

redWon = pygame.image.load(ASSET_PATH + "RedWon.png")
blueWon = pygame.image.load(ASSET_PATH + "BlueWon.png")
drawImg = pygame.image.load(ASSET_PATH + "Draw.png")
endImg = pygame.image.load(ASSET_PATH + "ClickToContinue.png")

class GridBox:
    def __init__(self, pos, size, data, index):
        self.rect = (pos[0], pos[1], size, size)
        self.data = data
        self.index = index

    def draw(self):
        if self.data == "r":
            colour = red
        elif self.data == "b":
            colour = blue
        else:
            colour = startBoxColor

        pygame.draw.rect(wn, colour, self.rect)

    def touching_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        return pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1])


def render_screen(grid, turn):
    wn.fill(WIN_COLOUR)

    for box in grid:
        box.draw()

    wn.blit(
        redMouse if turn is "r" else blueMouse, (pygame.mouse.get_pos()[0],
                                                 pygame.mouse.get_pos()[1]))

    pygame.display.update()


def check_winner(data):
    for row in data:
        if row == ["r", "r", "r"]:
            # red got three horizontal at any row
            return "r"
        if row == ["b", "b", "b"]:
            # blue got three horizontal at any row
            return "b"

    for i in range(3):
        if data[0][i] == "r":
            if data[1][i] == "r":
                # middle column is occupies by red
                if data[2][i] == "r":
                    # right column is occupies by red
                    return "r"

        # -------------------------------------------
        if data[0][i] == "b":
            # left column is occupied by blue
            if data[1][i] == "b":
                # middle column is occupied by blue
                if data[2][i] == "b":
                    # right column is occupied by blue
                    return "b"

    # -----------------------------------------------
    if data[0][0] == "r":
        if data[1][1] == "r":
            if data[2][2] == "r":
                # red has gotten top left to bottom right
                return "r"
    if data[0][2] == "r":
        if data[1][1] == "r":
            if data[2][0] == "r":
                # red has gotten top right to bottom left
                return "r"

    # ------------------------------------------------
    if data[0][0] == "b":
        if data[1][1] == "b":
            if data[2][2] == "b":
                # blue has gotten top left to bottom right
                return "b"
    if data[0][2] == "b":
        if data[1][1] == "b":
            if data[2][0] == "b":
                # blue has gotten top right to bottom left
                return "b"

    if not any("d" in x for x in data):
        return "draw"

def initialise_match():
    """Initialises the playing grid data and visual grid"""
    gridData = [["d", "d", "d"],
                ["d", "d", "d"],
                ["d", "d", "d"]]
    grid = []
    for j in range(3):
        y = BOX_SIZE * j + OFFSET * (j + 1)
        for i in range(3):
            x = BOX_SIZE * i + OFFSET * (i + 1)
            grid.append(GridBox((x, y), BOX_SIZE, "d", (i, j)))
    return grid, gridData

def play(turn, grid, gridData):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            for box in grid:
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        box.touching_mouse()):
                    if box.data == "d":
                        box.data = turn
                        gridData[box.index[0]][box.index[1]] = turn
                        turn = "b" if turn == "r" else "r"

        outcome = check_winner(gridData)
        if outcome is not None:
            break
        render_screen(grid, turn)

    return outcome

while True:
    turn = "r"

    grid, gridData = initialise_match()
    outcome = play(turn, grid, gridData)

    pressed = False
    tick = 0

    while not pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tick > 60:
                    pressed = True

        wn.fill(WIN_COLOUR)

        if outcome  == "r":
            # RED HAS WON!
            wn.blit(redWon, (WIN_WIDTH / 2 - redWon.get_width() / 2,
                             WIN_HEIGHT / 2 - redWon.get_height() / 2))
        elif outcome == "b":
            # BLUE HAS WON!
            wn.blit(blueWon, (WIN_WIDTH / 2 - blueWon.get_width() / 2,
                              WIN_HEIGHT / 2 - blueWon.get_height() / 2))
        else:
            # DRAW!
            wn.blit(drawImg, (WIN_WIDTH / 2 - drawImg.get_width() / 2,
                              WIN_HEIGHT / 2 - drawImg.get_height() / 2))

        if tick > 60:
            wn.blit(endImg, (WIN_WIDTH / 2 - endImg.get_width() / 2, 350))

        mousePos = pygame.mouse.get_pos()
        wn.blit(blueMouse if outcome == "b" else redMouse,
                (mousePos[0], mousePos[1]))

        pygame.display.update()

        tick += 1
