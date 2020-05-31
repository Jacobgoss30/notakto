"""Utils for noughty"""
import numpy as np

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
