import numpy as np
import math
import copy
from collections import deque

class State:
    
    """
    Contructeur d'un état initial
    """
    def __init__(self, pos):
        """
        pos donne la position de la voiture i dans sa ligne ou colonne (première case occupée par la voiture);
        """
        self.pos = np.array(pos)
        
        """
        c,d et prev premettent de retracer l'état précédent et le dernier mouvement effectué
        """
        self.c = self.d = self.prev = None
        
        self.nb_moves = 0
        self.score = 0
        
        # Adaptee dans le print
        self.rock = None

    """
    Constructeur d'un état à partir du mouvement (c,d)
    """
    def move(self, c, d):
        s = State(self.pos)
        s.prev = self
        s.pos[c] += d
        s.c = c
        s.d = d
        s.nb_moves = self.nb_moves + 1
        # TODO
        s.rock = self.rock
        return s

    def put_rock(self, rock_pos):
        # TODO
        s = State(self.pos)
        s.prev = self
        
        s.c = self.c
        s.d = self.d
        s.nb_moves = self.nb_moves
        
        s.rock = rock_pos
        
        return s
            
    def score_state(self, rh, is_max=True, is_single_player=True):
        self.old_score_state(rh, is_max, is_single_player)
        
        
    def old_score_state(self, rh, is_max=True, is_single_player=True):
        # TODO
        # Best score if red car closer to exit
        self.score = -(4 - self.pos[0])
#         print('self.score: ', self.score)
        
        nb_cars_blocking_red = 0
        length_cars_blocking_vert_cars_infront_red = 0
        
        for car in range(1, rh.nbcars): # 1 : Don't need to start with the red car
            if not rh.horiz[car] and (rh.move_on[car] >= rh.length[0] + self.pos[0]): # Check if it is between the red car and exit
                for row in range(self.pos[car], self.pos[car] + rh.length[car]):
                    if row == 2: # Means a car crosses the red car
                        nb_cars_blocking_red += 1
                        
                if rh.length[car] == 3 and self.c == car and self.d == -1:
                    self.score -= 1
                    
            elif rh.horiz[car]: # Check if an horizontal car could be blocking a vertical car crossing the red car
                if self.pos[car] + rh.length[car] > self.pos[0] + rh.length[0]:
                    length_cars_blocking_vert_cars_infront_red += self.pos[car] + rh.length[car] - (self.pos[0] + rh.length[0])
        
        # Best score if the number of cars blocking the red car and cars in front of it is smaller
        self.score -= 2 * nb_cars_blocking_red + length_cars_blocking_vert_cars_infront_red
        
        ###
#         print('nb_cars_blocking_red : ', nb_cars_blocking_red )
#         print('length_cars_blocking_vert_cars_infront_red : ', length_cars_blocking_vert_cars_infront_red )
#         print('self.score : ', self.score )
        ###
    
        if self.prev and self.prev.c == self.c and self.prev.d != self.d:
            self.score -= 6
        # Best score if we avoid repeating the previous move
#         if not is_single_player and self.prev and self.prev.prev and self.prev.prev.c == self.c and self.prev.prev.d != self.d:
#             self.score -= 6
#             print('REPEATING: self.score : ', self.score )
        
        # TODO: Necessary ??
        # Remove score for the number of moves
        # self.score -= self.nb_moves
        
        # 
        if self.rock and not is_max:
            for car in range(1, rh.nbcars):
                if rh.horiz[car] and rh.move_on[car] == self.rock[0]:
                    if (self.pos[car] - 1) == self.rock[1] or self.pos[car] + rh.length[car] == self.rock[1]:
#                         print('ROCK BLOCK HORZ')
                        self.score -= 1
                elif not rh.horiz[car] and rh.move_on[car] == self.rock[1]:
                    if (self.pos[car] - 1) == self.rock[0] or self.pos[car] + rh.length[car] == self.rock[0]:
                        self.score -= 1
#                         print('ROCK BLOCK VERT')
#             print('ROCK: self.score : ', self.score )
        

    def success(self):
        return self.pos[0] == 4
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        if len(self.pos) != len(other.pos):
            print("les états n'ont pas le même nombre de voitures")
        
        return np.array_equal(self.pos, other.pos)
    
    def __hash__(self):
        h = 0
        for i in range(len(self.pos)):
            h = 37*h + self.pos[i]
        return int(h)
    
    def __lt__(self, other):
        return (self.score) < (other.score)
