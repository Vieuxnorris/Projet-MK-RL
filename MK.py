import mss
import numpy as np
import gym
from gym import spaces

import pygame
from pygame.locals import *

# a faire :
# - get_obsersation(self)
# - Reset(self)
# - Optuna
# - reverse engineer MK pour grab les variables (indipensable pour faire le système de récompense)
# - implèmentation de tensorboard
# - choix de l'Algo PPO ou DQN (préf PPO)
# - go train !


# template 
class RLMK(gym.Env):
    def __init__(self):
        super(RLMK, self).__init__()
        pygame.init()
        pygame.key.set_repeat(200,100)
        
        self.action_map = {
            0: pygame.K_LEFT,
            1: pygame.K_RIGHT,
            2: pygame.K_UP,
            3: (pygame.K_UP, pygame.K_RIGHT),
        }
        
        self.action_space = spaces.Discrete(len(self.action_map))
        self.observation_space = spaces.Box(low=0, high=255, shape=(64,64,3))
        self.monitor = {}
    
    def read_inputs(self):
        # Lire les entrées du clavier
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Récupérer le tableau des touches enfoncées
                keys = pygame.key.get_pressed()

                # Parcourir les combinaisons de touches de la map d'actions
                for key_tuple in self.action_map.values():
                    # Vérifier si la combinaison de touches est enfoncée
                    if all(keys[key] for key in key_tuple):
                        # Récupérer l'action associée à la combinaison de touches
                        action = list(self.action_map.keys())[list(self.action_map.values()).index(key_tuple)]

                        # Effectuer l'action dans l'environnement Gym
                        self.step(action)
    
    def step(self, action):
        self.read_inputs()
        state, observation, done = self.step(action)
        if done:
            self.reset()
        return state, observation, done
    
    def get_observation(self):
        pass
            
if __name__ == "__main__":
    env = RLMK()
    
        
        
        
        
