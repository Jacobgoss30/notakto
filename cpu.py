"""Module for all cpu turn operations"""
from time import sleep
import numpy as np

def cpu_turn(grid, grid_data):
    """Plays the cpu turn and returns updated grid and grid data"""
    coords = cpu_play(grid_data)
    grid_data[coords] = True
    for box in grid:
        if box.index == coords:
            box.filled = True
    return grid, grid_data

def cpu_play(grid_data):
    """Returns coords of the played box"""
    sleep(0.1)
    emptys = np.where(~grid_data)
    ind = np.random.randint(len(emptys))
    return (emptys[0][ind], emptys[1][ind])
