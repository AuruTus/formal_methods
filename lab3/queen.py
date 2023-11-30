import time
from z3 import *


def four_queen():
    solver = Solver()
    # the basic data structure:
    N = 100
    board = [[Bool('b_{}_{}'.format(i, j)) for j in range(N)]
             for i in range(N)]

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
    for i in range(N):
        cols = []
        for j in range(N):
            current_col = []
            current_col.append(board[j][i])
            for k in range(N):
                if k != j:
                    current_col.append(Not(board[k][i]))
            cols.append(And(current_col))
        solver.add(Or(cols))

    # Challenge: add constraints which describe each diagonal has at most one queen
    # constraint 3: each diagonal has at most one queen:

    # NOTE: diagnoal_hash(x, y) = x-y
    # the first diagonal starts from (0, N-1)
    diag = []
    for i in range(2*N-1):
        diagonals = []
        for x in range(N):
            y = x - i + N-1
            if y < 0 or y >= N:
                continue
            current_diagonal = []
            current_diagonal.append(board[x][y])
            for _x in range(N):
                if _x == x:
                    continue
                _y = _x - i + N-1
                if _y < 0 or _y >= N:
                    continue
                current_diagonal.append(Not(board[_x][_y]))
            diagonals.append(And(current_diagonal))
        current_diagonal = []
        for x in range(N):
            y = x - i + N-1
            if y < 0 or y >= N:
                continue
            current_diagonal.append(Not(board[x][y]))
        diagonals.append(And(current_diagonal))
        solver.add(Or(diagonals))

    # Challenge: add constraints which describe each anti-diagonal has at most one queen
    # constraint 4: each anti-diagonal has at most one queen:

    # NOTE: anti_diagnoal_hash(x, y) = x+y
    # the first anti_diagonal starts from (0, 0)
    anti_diag = []
    for i in range(2*N-1):
        anti_diagonals = []
        for x in range(N):
            y = i - x
            if y < 0 or y >= N:
                continue
            current_anti_diagonal = []
            current_anti_diagonal.append(board[x][y])
            for _x in range(N):
                if _x == x:
                    continue
                _y = i - _x
                if _y < 0 or _y >= N:
                    continue
                current_anti_diagonal.append(Not(board[_x][_y]))
            anti_diagonals.append(And(current_anti_diagonal))
        current_anti_diagonal = []
        for x in range(N):
            y = i - x
            if y < 0 or y >= N:
                continue
            current_anti_diagonal.append(Not(board[x][y]))
        anti_diagonals.append(And(current_anti_diagonal))
        solver.add(Or(anti_diagonals))

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

    print("number of result: ", count)


if __name__ == '__main__':
    # Four Queen should have 2 set of solutions
    four_queen()
