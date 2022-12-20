import mss
import numpy as np

import sys
import pyMeow as pm

import cv2

import gym
from gym import spaces

import pygame
from pygame.locals import *

# a faire :
# - reverse engineer MK pour grab les variables (indipensable pour faire le système de récompense)
# - Reset(self)
# - choix de l'Algo PPO ou DQN (préf PPO)
# - implèmentation de tensorboard
# - Optuna
# - go train !

# pour les test des methodes et autre, je prend GeometryDash comme setup de test

# template 
class RLMK(gym.Env):
    def __init__(self, game="GeometryDash.exe"):
        super(RLMK, self).__init__()
        pygame.init()
        pygame.key.set_repeat(200,100)
        
        self.action_map = {
            0: pygame.K_UP,
            1: None,
        }
        
        self.addr_map = {
            "Score": 0x00322290,
            "Time": 0x003222DC,
            #"Death":0x01234567,
        }
        
        self.addr_map_offset = {
            "Score": [0xD0, 0x20, 0x28, 0x0, 0x4C0],
            "Time": [0xCC, 0x28, 0x0, 0x8, 0x2BC],
            #"Death": [0x01, 0x02],
        }
        
        self.game_process_id = pm.get_process_id(game)
        self.game_process_handle = None
        
        if self.game_process_id is not None:
            self.game_process_handle = pm.open_process(self.game_process_id)
            self.baseAddr = pm.get_module(self.game_process_handle, game)["base"]
        else:
            self.game_process_handle = None
            
        self.addresses = {}
        self.read_addr_map()
        
        self.action_space = spaces.Discrete(len(self.action_map))
        self.observation_space = spaces.Box(low=0, high=255, shape=(160,160,1))
        self.monitor = {'top':50,'left':0, 'width':640, "height":430}
    
    def read_memory(self, valeur_map_base, name_map_base):
        Final_addr = pm.pointer_chain_32(self.game_process_handle, self.baseAddr + valeur_map_base, self.addr_map_offset[name_map_base])
        self.addresses[name_map_base] = Final_addr

    def read_addr_map(self):
        for key, value in self.addr_map.items():
            self.read_memory(value, key)
    
    def get_observation(self):
        obs = np.asarray(mss.mss().grab(self.monitor))
        Gray = cv2.cvtColor(obs, cv2.COLOR_BGR2GRAY)
        Resize = cv2.resize(Gray, (160,160))
        channel = np.reshape(Resize, (160,160,1))
        return channel
        
    
    def render(self):
        while True:
            cv2.imshow("test",self.get_observation())
            if cv2.waitKey(10) == 27: # touche echap pour quitter
                break
        cv2.destroyAllWindows()
    
    def press_key(self, key):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key))
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=key))
    
    def reset(self):
        pass
    
    def step(self, action):
        reward_Time = pm.r_int(self.game_process_handle, self.addresses["Time"])
        reward_Score = pm.r_int(self.game_process_handle, self.addresses["Score"])
        #reward_Death = pm.r_int(self.game_process_handle, self.addresses["Death"])
        key = self.action_map[action]
        if key is not None:
            self.press_key(key)
        else:
            print("Action inconnue")

    
if __name__ == "__main__":
    env = RLMK()
    env.render()
