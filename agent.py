from typing import get_args
from lux.game import Game
from data_processing.data_access import *
from evaluation import *

game_state = None
gs = None
data = None
    
def agent(observation, configuration):
    global game_state
    global gs
    global data
    
    actions = []
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])
    gs = game_state
    
    data = get_game_data(gs)
    actions = evaluate(data)
    
    return actions