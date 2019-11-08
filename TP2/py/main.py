from rushhour import Rushhour
from state import State 
from minimax import  MiniMaxSearch 


# Recherche adverserielle 

def moves_9(depth=1, is_single=True):
    # Solution optimale: 9 moves
    rh = Rushhour([True, False, False, False, True],
                    [2, 3, 2, 3, 3],
                    [2, 4, 5, 1, 5],
                    ["rouge", "vert", "bleu", "orange", "jaune"])
    s = State([1, 0, 1, 3, 2])
    algo = MiniMaxSearch(rh, s,depth)
    algo.rushhour.init_positions(s)

    print('Init: ')
    # print(algo.rushhour.free_pos)
    algo.rushhour.print_pretty_grid(s)
    print('===')

    algo.solve(s, is_single)
    print('\nEND - Nb moves: ', algo.nb_moves_tot,'\n')
    # %time

def moves_16(depth=1, is_single=True):

    # solution optimale: 16 moves
    rh = Rushhour([True, True, False, False, True, True, False, False],
                    [2, 2, 3, 2, 3, 2, 3, 3],
                    [2, 0, 0, 0, 5, 4, 5, 3],
                    ["rouge", "vert", "mauve", "orange", "emeraude", "lime", "jaune", "bleu"])
    s = State([1, 0, 1, 4, 2, 4, 0, 1])
    algo = MiniMaxSearch(rh, s, depth) 
    algo.rushhour.init_positions(s)

    print('Init: ')
    # print(algo.rushhour.free_pos)
    algo.rushhour.print_pretty_grid(s)
    print('===')

    algo.solve(s, is_single) 
    print("===")
    print('Last grid:')
    algo.rushhour.print_pretty_grid(algo.state)
    print('\nEND - Nb moves: ', algo.nb_moves_tot,'\n')
    # %time

def moves_14(depth=1, is_single=True):
    # solution optimale: 14 moves
    rh = Rushhour([True, False, True, False, False, False, True, True, False, True, True],
                    [2, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2],
                    [2, 0, 0, 3, 4, 5, 3, 5, 2, 5, 4],
                    ["rouge", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    s = State([0, 0, 3, 1, 2, 1, 0, 0, 4, 3, 4])
    algo = MiniMaxSearch(rh, s,depth)
    algo.rushhour.init_positions(s)
    
    print('Init: ')
    # print(algo.rushhour.free_pos)
    algo.rushhour.print_pretty_grid(s)
    print('===')

    algo.solve(s, is_single)
    print("===")
    print('Last grid:')
    algo.rushhour.print_pretty_grid(algo.state)
    print('\nEND - Nb moves: ', algo.nb_moves_tot,'\n')
    # %time

depth = 3
is_single = False
moves_9(depth, is_single)