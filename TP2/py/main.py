from rushhour import Rushhour
from state import State 
from minimax import  MiniMaxSearch 


# Recherche adverserielle 

def moves_9():
    # Solution optimale: 9 moves
    rh = Rushhour([True, False, False, False, True],
                    [2, 3, 2, 3, 3],
                    [2, 4, 5, 1, 5],
                    ["rouge", "vert", "bleu", "orange", "jaune"])
    s = State([1, 0, 1, 3, 2])
    algo = MiniMaxSearch(rh, s,3)
    algo.rushhour.init_positions(s)

    print('Init: ')
    # print(algo.rushhour.free_pos)
    algo.rushhour.print_pretty_grid(s)
    print('===')

    algo.solve(s, False)
    print('\nEND - Nb moves: ', algo.nb_moves_tot,'\n')
    # %time

def moves_16():

    # solution optimale: 16 moves
    rh = Rushhour([True, True, False, False, True, True, False, False],
                    [2, 2, 3, 2, 3, 2, 3, 3],
                    [2, 0, 0, 0, 5, 4, 5, 3],
                    ["rouge", "vert", "mauve", "orange", "emeraude", "lime", "jaune", "bleu"])
    s = State([1, 0, 1, 4, 2, 4, 0, 1])
    algo = MiniMaxSearch(rh, s, 3) 
    algo.rushhour.init_positions(s)

    print('Init: ')
    # print(algo.rushhour.free_pos)
    algo.rushhour.print_pretty_grid(s)
    print('===')

    algo.solve(s, False) 
    # %time


moves_16()