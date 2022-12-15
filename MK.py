import mss
import numpy as np

import psutil

import cv2

import gym
from gym import spaces

import pygame
from pygame.locals import *

# a faire :
# - Reset(self)
# - reverse engineer MK pour grab les variables (indipensable pour faire le système de récompense)
# - implèmentation de tensorboard
# - choix de l'Algo PPO ou DQN (préf PPO)
# - Optuna
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
        
        self.addr_map = {
            "Player": 0x01234567,
            "PV": 0x01234567,
            "Time": 0x01234567,
            "Position_X": 0x01234567,
            "Position_Y": 0x01234567,
        }
        
        self.game_process_id = self.scan_process("MKII")
        self.game_process = psutil.Process(self.game_process_id)
        self.memory_maps = self.game_process.memory_maps()
        
        self.addresses = {}
        
        for key, value in self.addr_map.items():
            addr = self.save_memory_for_read(value)
            self.addresses[key] = addr
        
        self.action_space = spaces.Discrete(len(self.action_map))
        self.observation_space = spaces.Box(low=0, high=255, shape=(64,64,1))
        self.monitor = {'top':200,'left':0, 'width':1895, "height":580}
    
    def scan_process(self, name_process):
        for proc in psutil.process_iter():
            proc_name = proc.name()
            
            if proc_name == name_process:
                process_id = proc.pid
                return process_id
        return
    
    def save_memory_for_read(self, addr_map_valeur):
        for map in self.memory_maps:
            offset  = map.find(addr_map_valeur)
            if offset != -1:
                addr = map.addr + offset
                return addr
        return
           
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
    
    def get_observation(self):
        obs = np.asarray(mss.mss().grab(self.monitor))
        Gray = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
        Resize = cv2.resize(Gray, (64,64))
        channel = np.reshape(Resize, (64,64,1))
        return channel
        
    
    def render(self):
        pass
    
    def reset(self):
        pass
    
    def step(self, action):
        self.read_inputs()
        state, observation, done = self.step(action)
        if done:
            self.reset()
        return state, observation, done
            
if __name__ == "__main__":
    env = RLMK()
    
        
        
        
        
