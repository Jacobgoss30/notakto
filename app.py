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

startBoxColor = (240, 240, 240)
red = (239, 57, 57)
blue = (46, 121, 232)

wn = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)


endImg = pygame.image.load(ASSET_PATH + "ClickToContinue.png")

images = {
    "r": pygame.image.load(ASSET_PATH + "RedWon.png"),
    "b": pygame.image.load(ASSET_PATH + "BlueWon.png"),
    "draw": pygame.image.load(ASSET_PATH + "Draw.png")
}

mice = {
    "r": pygame.image.load(ASSET_PATH + "RedMouse.png"),
    "b": pygame.image.load(ASSET_PATH + "BlueMouse.png")
}

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

    wn.blit(mice[turn], (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
    pygame.display.update()


def check_winner(data):
    for row in data:
        if row == ["r", "r", "r"]:
            return "r"
        if row == ["b", "b", "b"]:
            return "b"

    for i in range(3):
        if data[0][i] == "r":
            if data[1][i] == "r":
                if data[2][i] == "r":
                    return "r"

        if data[0][i] == "b":
            if data[1][i] == "b":
                if data[2][i] == "b":
                    return "b"

    if data[0][0] == "r":
        if data[1][1] == "r":
            if data[2][2] == "r":
                return "r"
    if data[0][2] == "r":
        if data[1][1] == "r":
            if data[2][0] == "r":
                return "r"

    if data[0][0] == "b":
        if data[1][1] == "b":
            if data[2][2] == "b":
                return "b"

    if data[0][2] == "b":
        if data[1][1] == "b":
            if data[2][0] == "b":
                return "b"

    if not any("d" in x for x in data):
        return "draw"

def initialise_match():
    """Initialises the playing grid data and visual grid"""
    grid_data = [["d", "d", "d"],
                 ["d", "d", "d"],
                 ["d", "d", "d"]]
    grid = []
    for j in range(3):
        y_coord = BOX_SIZE * j + OFFSET * (j + 1)
        for i in range(3):
            x_coord = BOX_SIZE * i + OFFSET * (i + 1)
            grid.append(GridBox((x_coord, y_coord), BOX_SIZE, "d", (i, j)))
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
                    if box.data == "d":
                        box.data = turn
                        grid_data[box.index[0]][box.index[1]] = turn
                        turn = "b" if turn == "r" else "r"

        outcome = check_winner(grid_data)
        if outcome is not None:
            break
        render_screen(grid, turn)

    return outcome

def end_match(outcome):
    """Prints winner to screen"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        wn.fill(WIN_COLOUR)

        img = images[outcome]
        wn.blit(img, (WIN_WIDTH / 2 - img.get_width() / 2,
                      WIN_HEIGHT / 2 - img.get_height() / 2))

        wn.blit(endImg, (WIN_WIDTH / 2 - endImg.get_width() / 2, 350))
        mouse_pos = pygame.mouse.get_pos()
        wn.blit(mice[outcome], (mouse_pos[0], mouse_pos[1]))

        pygame.display.update()

def run():
    """runs the game"""
    while True:
        turn = "r"
        grid, grid_data = initialise_match()
        outcome = play(turn, grid, grid_data)
        end_match(outcome)

if __name__ == '__main__':
    run()
