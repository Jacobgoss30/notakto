"""Module for updating the mdp"""
import pickle

def load_mdp():
    """Loads in the mdp from pickle"""
    with open('data/mdp.pkl', 'rb') as mdp_fp:
        mdp = pickle.load(mdp_fp)
    return mdp

def save_mdp(mdp):
    """Saves the current mdp to pickle file"""
    with open('data/mdp.pkl', 'wb') as mdp_fp:
        pickle.dump(mdp, mdp_fp)

def update_data(winner, turn, mdp):
    """Updates general info and mdp if required"""
    if update_general(winner, turn):
        update_mdp(mdp)
    save_mdp(mdp)

def update_general(winner, turn):
    """Updates the general.pkl file and returns True if mdp needs updating"""
    with open('data/general.pkl', "rb") as file_path:
        general = pickle.load(file_path)
    general['total_trials'] += 1
    general['rolling_trials'] += 1
    general['outcomes'] += [{turn: winner}]
    if general['rolling_trials'] == general['update_after']:
        general['rolling_trials'] = 0
        with open('data/general.pkl', 'wb') as file_path:
            pickle.dump(general, file_path)
        return True
    with open('data/general.pkl', 'wb') as file_path:
        pickle.dump(general, file_path)
    return False

def update_mdp(mdp):
    """Updates psa, performs value iteration then optimum policy evaluation"""
    print('Updating Markov Decision Process...')
    update_psa(mdp)
    apply_value_iteration(mdp)
    update_policies(mdp)
    print('Done')

def update_psa(mdp):
    """Updates the probability state action for all states and actions"""
    for turn in mdp.values():
        for state in turn:
            for action in state['actions'].values():
                update_psa_action(action)

def update_psa_action(action):
    """Updates psa for an action"""
    if 'next_state_count' in action.keys():
        if action['count'] == 0:
            avg = 1 / len(action['next_state_count'].values())
            for next_state in action['next_state_count'].values():
                next_state['psa'] = avg
        else:
            for next_state in action['next_state_count'].values():
                next_state['psa'] = next_state['count'] / action['count']
    else:
        action['psa'] = 1

def apply_value_iteration(mdp):
    """Performs value iteration until convergence"""
    for _ in range(10**4):
        if value_iterate(mdp) == 0:
            break

def value_iterate(mdp):
    """Performs one iteration of the value iteration algorithm"""
    num_changes = 0
    for turn, states in mdp.items():
        for state in states:
            new_value = update_state_value(turn, state, mdp)
            if new_value != state['value']:
                state['value'] = new_value
                num_changes += 1
    return num_changes

def update_state_value(turn, state, mdp):
    """Returns updated value for a specific state"""
    value = 0
    if 'reward' in state.keys():
        value += state['reward']
    actions_results = calc_sum_psa_v(turn, state, mdp)
    if len(actions_results) > 0:
        value += max(actions_results.values())
    return value

def calc_sum_psa_v(turn, state, mdp):
    """Returns dictionary of next states and product of their psa and V"""
    actions_copy = state['actions'].copy()
    for key, action in state['actions'].items():
        if key == -1:
            actions_copy[key] = mdp[turn + 1][key]['value']
        else:
            next_values = 0
            for next_key, next_action in action['next_state_count'].items():
                next_values += (mdp[turn + 2][next_key]['value'] *
                                next_action['psa'])
            actions_copy[key] = next_values
    return actions_copy

def update_policies(mdp):
    """Updates the policies for every state in mdp to the optimum policy"""
    for turn, states in mdp.items():
        for state in states:
            policy = optimum_policy(turn, state, mdp)
            if policy is not None:
                state['policy'] = policy

def optimum_policy(turn, state, mdp):
    """Returns the optimum polocy for a state, or None if no policy required"""
    actions_results = calc_sum_psa_v(turn, state, mdp)
    if len(actions_results) > 0:
        argmax = max(actions_results.keys(),
                     key=(lambda key: actions_results[key]))
        return argmax
    return None

