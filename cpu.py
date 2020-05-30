"""Module for all cpu turn operations"""
import numpy as np

def cpu_turn(grid, grid_data, turns, mdp):
    """Plays the cpu turn and returns updated grid and grid data"""
    coords = cpu_play(grid_data, turns, mdp)
    grid_data[coords] = True
    for box in grid:
        if box.index == coords:
            box.filled = True
    return grid, grid_data

def cpu_play(grid_data, turns, mdp):
    """Returns coords of the played box"""
    action = None
    for state in mdp[turns]:
        if check_array_equal(grid_data, np.array(state['state']).astype(bool)):
            action = mdp[turns + 1][state['policy']]['state']
            if action == 'cpu lose':
                return cpu_lose(grid_data)
            action = np.array(action).astype(bool)
            break
    coords = None
    rows, cols = np.where(~grid_data)
    for i, row in enumerate(rows):
        tmp = np.zeros((3, 3)).astype(bool)
        tmp[row, cols[i]] = True
        if check_array_equal(grid_data + tmp, action):
            coords = (row, cols[i])
            break
    return coords

def cpu_lose(grid_data):
    """Plays any losing square"""
    emptys = np.where(~grid_data)
    return (emptys[0][0], emptys[1][0])

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
