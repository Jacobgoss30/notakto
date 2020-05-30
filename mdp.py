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

def update_info(winner, mdp):
    return
