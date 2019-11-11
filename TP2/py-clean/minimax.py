import numpy as np
import enum
import random
import math

class Algorithm(enum.Enum):
    MINIMAX_SINGLE = 1
    MINIMAX_MULTI = 2
    PRUNING = 3
    EXPECTIMAX = 4

class ExpectimaxProbability(enum.Enum):
    RANDOM = 1
    OPTIMISTIC = 2
    PESSIMISTIC = 3


class MiniMaxSearch:
    def __init__(self, rushHour, initial_state, search_depth):
        self.rushhour = rushHour
        self.state = initial_state
        self.search_depth = search_depth
        self.nb_moves_tot = 0
        self.nb_state_searched = 0
        self.expectimax_probability = ExpectimaxProbability.RANDOM

    #  Un seul joueur et retourne le meilleur coup à prendre à partir de l'état courant
    def minimax_1(self, current_depth, current_state): 
        #TODO
        self.nb_state_searched += 1

        best_score = None
        possible_states = self.rushhour.possible_moves(current_state)
        
        if current_depth == self.search_depth:
            current_state.score_state(self.rushhour)
            return current_state.score
        
        for state in possible_states:
            score = self.minimax_1(current_depth + 1, state)        

            if best_score is None:
                best_score = score

            best_score = max(best_score, score)

        return best_score
        
    
    def minimax_2(self, current_depth, current_state, is_max, is_rock_turn): 
        #TODO
        self.nb_state_searched += 1

        if current_depth == self.search_depth:
            current_state.score_state(self.rushhour, is_rock_turn)
            return current_state.score

        best_score = None

        if is_max:
            possible_states = self.rushhour.possible_moves(current_state)
        else:
            possible_states = self.rushhour.possible_rock_moves(current_state)
        
        for state in possible_states:
            score = self.minimax_2(current_depth + 1, state, not is_max, is_rock_turn)        

            if best_score is None:
                best_score = score

            if is_max:
                best_score = max(best_score, score)
            else:
                best_score = min(best_score, score)

        return best_score

    def minimax_pruning(self, current_depth, current_state, is_max, alpha, beta, is_rock_turn):

        self.nb_state_searched += 1
        best_score = None

        if current_depth == self.search_depth:
            current_state.score_state(self.rushhour, is_rock_turn)
            return current_state.score

        if is_max:
            possible_states = self.rushhour.possible_moves(current_state)
        else:
            possible_states = self.rushhour.possible_rock_moves(current_state)
        
        for state in possible_states:
            score = self.minimax_pruning(current_depth + 1, state, not is_max, alpha, beta, is_rock_turn)        

            if best_score is None:
                best_score = score

            if is_max:
                best_score = max(best_score, score)
                if score >= beta:
                    return best_score
                
                alpha = max(alpha, score)
            else:
                best_score = min(best_score, score)
                
                if score <= alpha:
                    return best_score
                
                beta = min(beta, score)
                
        return best_score

    def expectimax(self, current_depth, current_state, is_max, is_rock_turn):
        #TODO
        self.nb_state_searched += 1

        if current_depth == self.search_depth:
            current_state.score_state(self.rushhour, is_rock_turn)
            return current_state.score

        best_score = None

        if is_max:
            possible_states = self.rushhour.possible_moves(current_state)

            for state in possible_states:
                score = self.expectimax(current_depth + 1, state, not is_max, is_rock_turn)        

                if best_score is None:
                    best_score = score

                if is_max:
                    best_score = max(best_score, score)
                else:
                    best_score = min(best_score, score)

            return best_score
        else:
            possible_states = self.rushhour.possible_rock_moves(current_state)

            scores = []
            for state in possible_states:
                scores.append(self.expectimax(current_depth + 1, state, not is_max, is_rock_turn)) 

            p = 1
            scores_len = len(scores)
            p = p / scores_len
            p_arr = []

            if self.expectimax_probability == ExpectimaxProbability.RANDOM:
                for idx in range(0, scores_len):
                    p_arr.append(p)

            else:
                mid = math.floor(scores_len / 2)
                
                for idx in range(0, scores_len):
                    p_arr.append(p + (idx - mid) * p / scores_len)

                if sum(p_arr) != 1.0:
                    p_left = 1.0 - sum(p_arr)

                    for idx in range(0, scores_len):
                        p_arr[idx] = p_arr[idx] + p_left / scores_len

                if self.expectimax_probability == ExpectimaxProbability.OPTIMISTIC: # probability higher for lower scores
                    scores.sort(reverse=True)

                elif self.expectimax_probability == ExpectimaxProbability.PESSIMISTIC: # probability higher for higher scores
                    scores.sort()

            scores = [a*b for a,b in zip(scores,p_arr)]

            return sum(scores)

        return best_score

    # Trouve et exécute le meilleur coup pour une partie à un joueur (apelle version de mininmax)
    def decide_best_move_1(self):
        #TODO
        
        best_move = None

        possible_states = self.rushhour.possible_moves(self.state)
        for state in possible_states:
            state.score = self.minimax_1(1, state)

            if best_move is None:
                best_move = state

            best_move = max(best_move, state)
        
        return best_move

    def decide_best_move_2(self, is_max, is_rock_turn):
        #TODO
        best_move = None

        if is_max:
            possible_states = self.rushhour.possible_moves(self.state)
        else:
            possible_states = self.rushhour.possible_rock_moves(self.state)
            
        for state in possible_states:
            state.score = self.minimax_2(1, state, not is_max, is_rock_turn)

            if best_move is None:
                best_move = state

            if is_max:
                best_move = max(best_move, state)
            else:
                best_move = min(best_move, state)

        
        return best_move

    def decide_best_move_pruning(self, is_max, is_rock_turn):
        #TODO
        best_move = None
        alpha = -1000000
        beta = 1000000

        if is_max:
            possible_states = self.rushhour.possible_moves(self.state)
        else:
            possible_states = self.rushhour.possible_rock_moves(self.state)
            
        for state in possible_states:
            state.score = self.minimax_pruning(1, state, not is_max, alpha, beta, is_rock_turn)

            if best_move is None:
                best_move = state

            if is_max:
                best_move = max(best_move, state)
                if state.score >= beta:
                    return best_move
                
                alpha = max(alpha, state.score)
            else:
                best_move = min(best_move, state)
                
                if state.score <= alpha:
                    return best_move
                
                beta = min(beta, state.score)
        
        return best_move

    def decide_best_move_expectimax(self, is_max, is_rock_turn):
        #TODO
        best_move = None

        if is_max:
            possible_states = self.rushhour.possible_moves(self.state)
        else:
            possible_states = self.rushhour.possible_rock_moves(self.state)
            return random.choice(possible_states)
            
        for state in possible_states:
            state.score = self.expectimax(1, state, not is_max, is_rock_turn)

            if best_move is None:
                best_move = state

            if is_max:
                best_move = max(best_move, state)
            else:
                best_move = min(best_move, state)

        
        return best_move

    def solve(self, state, algorithm): # apelle plusieurs fois decide_best_move
        #TODO
        self.nb_moves_tot = 1

        if algorithm == Algorithm.MINIMAX_SINGLE:
            self.state = self.decide_best_move_1()
            while not self.state.success():
                print('final move: ', end='')
                self.print_move(True, self.state)
                # self.rushhour.print_pretty_grid(self.state)

                self.state = self.decide_best_move_1()
                self.nb_moves_tot += 1
                
        elif algorithm == Algorithm.MINIMAX_MULTI:
            is_max = True
            self.state = self.decide_best_move_2(is_max, is_rock_turn=is_max)
            while not self.state.success():

                print('final move: ', end='')
                self.print_move(is_max, self.state)
                # self.rushhour.print_pretty_grid(self.state)
                
                is_max = not is_max
                self.state = self.decide_best_move_2(is_max, is_rock_turn=is_max)
                
                if is_max:
                    self.nb_moves_tot += 1
                
                if self.nb_moves_tot == 80:
                    print('FAIL')
                    break
        
        elif algorithm == Algorithm.PRUNING:
            is_max = True
            self.state = self.decide_best_move_pruning(is_max, is_rock_turn=is_max)
            while not self.state.success():

                print('final move: ', end='')
                self.print_move(is_max, self.state)
                # self.rushhour.print_pretty_grid(self.state)
                
                is_max = not is_max
                self.state = self.decide_best_move_pruning(is_max, is_rock_turn=is_max)
                
                if is_max:
                    self.nb_moves_tot += 1
                
                if self.nb_moves_tot == 80:
                    print('FAIL')
                    break

        else:
            is_max = True
            self.state = self.decide_best_move_expectimax(is_max, is_rock_turn=is_max)
            while not self.state.success():

                print('final move: ', end='')
                self.print_move(is_max, self.state)
                # self.rushhour.print_pretty_grid(self.state)
                
                is_max = not is_max
                self.state = self.decide_best_move_expectimax(is_max, is_rock_turn=is_max)
                
                if is_max:
                    self.nb_moves_tot += 1
                
                if self.nb_moves_tot == 80:
                    print('FAIL')
                    break

            
    def print_move(self, is_max, state):
        #TODO
        # Is_max : player
        # Not is_max : adversary
        
        if is_max:
            print('Voiture {} vers '.format(self.rushhour.color[state.c]), end='')
            
            if self.rushhour.horiz[state.c] and state.d == -1:
                print('la gauche')
            
            if self.rushhour.horiz[state.c] and state.d == 1:
                print('la droite')
            
            if (not self.rushhour.horiz[state.c]) and state.d == -1:
                print('le haut')
            
            if (not self.rushhour.horiz[state.c]) and state.d == 1:
                print('le bas')
        
        else:
            print('Roche dans la case {}-{}'.format(state.rock[0], state.rock[1]))
        
        pass
          
