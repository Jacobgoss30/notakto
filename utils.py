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
