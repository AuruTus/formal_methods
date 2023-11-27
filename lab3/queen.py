import time
from z3 import *


def four_queen():
    solver = Solver()
    # the basic data structure:
    N = 4
    board = [[Bool('b_{}_{}'.format(i, j)) for i in range(N)]
             for j in range(N)]

    # constraint 1: each row has just one queen:
    for i in range(N):
        rows = []
        for j in range(N):
            current_row = []
            current_row.append(board[i][j])
            for k in range(N):
                if k != j:
                    current_row.append(Not(board[i][k]))
            rows.append(And(current_row))
        solver.add(Or(rows))

    # Challenge: add constraints which describe each column has just one queen
    # constraint 2: each column has just one queen:
    raise NotImplementedError('TODO: Your code here!') 
        
    # Challenge: add constraints which describe each diagonal has at most one queen
    # constraint 3: each diagonal has at most one queen:
    raise NotImplementedError('TODO: Your code here!') 
    
    # Challenge: add constraints which describe each anti-diagonal has at most one queen
    # constraint 4: each anti-diagonal has at most one queen:
    raise NotImplementedError('TODO: Your code here!') 

    count = 0
    while solver.check() == sat:
        m = solver.model()
        print(m)
        count += 1
        block = []
        for i in range(N):
            for j in range(N):
                if m.eval(board[i][j], True):
                    board[i][j] = board[i][j]
                else:
                    board[i][j] = Not(board[i][j])
                block.append(board[i][j])
        new_prop = Not(And(block))
        solver.add(new_prop)
        
    print("number of result: ",count)


if __name__ == '__main__':
    # Four Queen should have 2 set of solutions
    four_queen()

