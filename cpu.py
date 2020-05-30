"""Module for all cpu turn operations"""
import numpy as np

def cpu_turn(grid, grid_data, play_info, mdp):
    """Plays the cpu turn and returns updated grid and grid data"""
    coords, play_info = cpu_play(grid_data, play_info, mdp)
    print(coords)
    grid_data[coords] = True
    for box in grid:
        if box.index == coords:
            box.filled = True
    return grid, grid_data, play_info

def cpu_play(grid_data, play_info, mdp):
    """Returns coords of the played box"""
    action = None
    for state_no, state in enumerate(mdp[play_info['turns']]):
        if check_array_equal(grid_data, np.array(state['state']).astype(bool)):
            policy = state['policy']
            new_play_info = get_play_info(play_info, state_no, policy)
            update_counts(mdp, state, play_info, new_play_info)
            action = mdp[play_info['turns'] + 1][policy]['state']
            if action == 'cpu lose':
                return cpu_lose(grid_data), new_play_info
            action = np.array(action).astype(bool)
            break
    return coords_of_action(action, grid_data), new_play_info

def get_play_info(play_info, state_no, policy):
    """Returns updated play info dict"""
    new_play_info = play_info.copy()
    new_play_info['state_no'] = state_no
    new_play_info['cpu_policy'] = policy
    return new_play_info

def update_counts(mdp, state, play_info, new_play_info):
    """Updates the counts in the mdp"""
    state['actions'][new_play_info['cpu_policy']]['count'] += 1
    turns = play_info['turns'] - 2
    if turns >= 0:
        mdp[turns][play_info['state_no']]['actions'][play_info['cpu_policy']][
            'next_state_count'][new_play_info['state_no']]['count'] += 1

def coords_of_action(action, grid_data):
    """Returns the coords of the action"""
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
