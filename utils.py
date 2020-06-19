"""Utils for notakto"""
import os
from pygame.image import load
import numpy as np

ASSET_PATH = os.path.abspath(os.path.dirname(__file__)) + "/assets/"

IMAGES = {
    "mouse": load(ASSET_PATH + "RedMouse.png"),
    "continue": load(ASSET_PATH + "ClickToContinue.png"),
    "p": load(ASSET_PATH + "YOUWON.png"),
    "c": load(ASSET_PATH + "YOULOSE.png")
}

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

def check_array_equal(arr1, arr2):
    """Checks if the arrays are equal, accounting for the 8 fold symmetry"""
    return (np.array_equal(arr1, arr2) |
            np.array_equal(np.flipud(arr1), arr2) |
            np.array_equal(np.fliplr(arr1), arr2) |
            np.array_equal(np.rot90(arr1), arr2) |
            np.array_equal(np.rot90(arr1, 2), arr2) |
            np.array_equal(np.rot90(arr1, -1), arr2) |
            np.array_equal(arr1.T, arr2) |
            np.array_equal(arr1[::-1, ::-1].T, arr2))
