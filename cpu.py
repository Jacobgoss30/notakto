"""Module for all cpu turn operations"""
import numpy as np
from utils import check_array_equal

def cpu_turn(grid, grid_data, play_info, mdp):
    """Plays the cpu turn and returns updated grid and grid data"""
    coords, play_info = cpu_play(grid_data, play_info, mdp)
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
            new_play_info = get_play_info(play_info, state_no, state['policy'])
            update_counts(mdp, state, play_info, new_play_info)
            action = mdp[play_info['turns'] + 1][state['policy']]['state']
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
    """Plays the first losing square"""
    emptys = np.where(~grid_data)
    return (emptys[0][0], emptys[1][0])
