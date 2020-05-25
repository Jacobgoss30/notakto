"""2 Player noughts and crosses"""
import sys
import os.path
import pygame

ASSET_PATH = os.path.abspath(os.path.dirname(__file__)) + "/assets/"

pygame.init()

wnWidth = 500
wnHeight = 430
wnColor = (30, 30, 30)
wnTitle = "Tic-Tac-Toe"

wn = pygame.display.set_mode((wnWidth, wnHeight))
pygame.display.set_caption(wnTitle)

boxSize = 100

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

while True:
    turn = "r"

    gridData = [["d", "d", "d"],
                ["d", "d", "d"],
                ["d", "d", "d"]]

    wn = pygame.display.set_mode((wnWidth, wnHeight))
    pygame.display.set_caption(wnTitle)
    grid = []
    run = True

    """
    Red vs Blue
    Tic-Tac-Toe
    """


    class GridBox:
        def __init__(self, pos, expand, color, data, vert, hor):
            self.color = color
            self.rect = (pos[0], pos[1], expand, expand)
            self.data = data
            self.vert = vert
            self.hor = hor

        def draw(self):
            if self.data == "r":
                self.color = red
            elif self.data == "b":
                self.color = blue
            else:
                self.color = startBoxColor

            pygame.draw.rect(wn, self.color, self.rect)

        def touching_mouse(self):
            mouse_pos = pygame.mouse.get_pos()
            return pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1])


    def add_row(y, color, grid_index):
        global grid

        grid.append(GridBox((85, y), 100, color, "d", grid_index, 0))
        grid.append(GridBox((195, y), 100, color, "d", grid_index, 1))
        grid.append(GridBox((305, y), 100, color, "d", grid_index, 2))


    add_row(50, startBoxColor, 0)
    add_row(160, startBoxColor, 1)
    add_row(270, startBoxColor, 2)


    def render_screen():
        global grid, box, blueMouse, redMouse, turn
        wn.fill(wnColor)

        for box in grid:
            box.draw()

        wn.blit(redMouse if turn is "r" else blueMouse, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

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


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # checking if a box is clicked
            for box in grid:
                if event.type == pygame.MOUSEBUTTONDOWN and box.touching_mouse():
                    # a box is pressed
                    if box.data == "d":
                        # no side has occupied the box
                        box.data = turn
                        gridData[box.vert][box.hor] = turn
                        turn = "b" if turn == "r" else "r"

        if check_winner(gridData) == "r":
            # red has won
            run = False
        if check_winner(gridData) == "b":
            # blue has won
            run = False

        inList = True if "d" in gridData[0] or "d" in gridData[1] or "d" in gridData[2] else False

        if not inList:
            run = False

        render_screen()

    #######################################

    pressed = False
    tick = 0

    while not pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tick > 60:
                    pressed = True

        wn.fill(wnColor)

        if check_winner(gridData) == "r":
            # RED HAS WON!
            wn.blit(redWon, (wnWidth / 2 - redWon.get_width() / 2, wnHeight / 2 - redWon.get_height() / 2))
        elif check_winner(gridData) == "b":
            # BLUE HAS WON!
            wn.blit(blueWon, (wnWidth / 2 - blueWon.get_width() / 2, wnHeight / 2 - blueWon.get_height() / 2))
        else:
            # DRAW!
            wn.blit(drawImg, (wnWidth / 2 - drawImg.get_width() / 2, wnHeight / 2 - drawImg.get_height() / 2))

        if tick > 60:
            wn.blit(endImg, (wnWidth / 2 - endImg.get_width() / 2, 350))

        mousePos = pygame.mouse.get_pos()
        wn.blit(blueMouse if check_winner(gridData) == "b" else redMouse, (mousePos[0], mousePos[1]))

        pygame.display.update()

        tick += 1
