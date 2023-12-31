"""N-queens puzzle

The  N-queens problem is about placing N chess queens on an N*N chessboard so that
no two queens threaten each other. A solution requires that no two queens share the
same row, column diagonal or anti-diagonal.The problem's target is try to find how
many solutions exist.

"""

import time
from z3 import *


def n_queen_la(board_size: int, verbose: bool = False) -> int:
    solver = Solver()
    n = board_size

    # Each position of the board is represented by a 0-1 integer variable:
    #   ...    ...    ...    ...
    #   x_2_0  x_2_1  x_2_2  ...
    #   x_1_0  x_1_1  x_1_2  ...
    #   x_0_0  x_0_1  x_0_2  ...
    #
    board = [[Int(f"x_{row}_{col}") for col in range(n)] for row in range(n)]

    # only be 0 or 1 in board
    for row in board:
        for pos in row:
            solver.add(Or(pos == 0, pos == 1))

    # @Exercise 11: please fill in the missing src to add
    # the following constraint into the solver:
    #   each row has just 1 queen,
    for i in range(n):
        solver.add(sum([board[i][j] for j in range(n)]) == 1)
    #   each column has just 1 queen,
    for j in range(n):
        solver.add(sum([board[i][j] for i in range(n)]) == 1)
    #   each diagonal has at most 1 queen,
    for k in range(-n+1, n):
        solver.add(
            sum([board[i][i-k] for i in range(n) if k <= i and i-k < n]) <= 1)
    #   each anti-diagonal has at most 1 queen.
    for k in range(2*n-1):
        solver.add(
            sum([board[i][k-i] for i in range(n) if i <= k and k-i < n]) <= 1)

    # count the number of solutions
    solution_count = 0

    start = time.time()
    while solver.check() == sat:
        solution_count += 1
        model = solver.model()

        if verbose:
            # print the solution
            print([(row_index, col_index) for row_index, row in enumerate(board)
                   for col_index, flag in enumerate(row) if model[flag] == 1])

        # generate constraints from solution
        solution_cons = [(flag == 1)
                         for row in board for flag in row if model[flag] == 1]

        # add solution to the solver to get new solution
        solver.add(Not(And(solution_cons)))

    print(
        f"n_queen_la solve {board_size}-queens by {(time.time() - start):.6f}s")
    return solution_count


def n_queen_bt(board_size: int, verbose: bool = False) -> int:
    n = board_size
    solutions = [[]]

    def is_safe(col, solution):
        same_col = col in solution
        same_diag = any(abs(col - j) == (len(solution) - i)
                        for i, j in enumerate(solution))

        return not (same_col or same_diag)

    start = time.time()
    for row in range(n):
        solutions = [solution + [col]
                     for solution in solutions for col in range(n) if is_safe(col, solution)]
    print(
        f"n_queen_bt solve {board_size}-queens by {(time.time() - start):.6f}s")

    if verbose:
        # print the solutions
        for solution in solutions:
            print(list(enumerate(solution)))

    return len(solutions)


def n_queen_dfs(board_size: int):
    n = board_size
    col: list[bool] = [False] * n
    diag: list[bool] = [False] * (2*n - 1)
    anti_diag: list[bool] = [False] * (2*n - 1)
    cnt = 0

    def _dfs(x: int, y: int):
        nonlocal cnt
        if x >= n:
            if y == 0:
                cnt += 1
            return
        _diag = x - y + n - 1
        _anti_diag = x+y
        if col[y] or diag[_diag] or anti_diag[_anti_diag]:
            return

        col[y] = True
        diag[_diag] = True
        anti_diag[_anti_diag] = True
        for _y in range(n):
            _dfs(x+1, _y)
        anti_diag[_anti_diag] = False
        diag[_diag] = False
        col[y] = False

    start = time.time()
    for _y in range(n):
        _dfs(0, _y)
    end = time.time()

    print(f"n_queen_dfs solve {board_size}-queens by {(end - start):.6f}s")

    return cnt


def n_queen_la_opt(board_size: int, verbose: bool = False) -> int:
    solver = Solver()
    n = board_size

    # We know each queen must be in a different row.
    # So, we represent each queen by a single integer: the column position
    # the q_i = j means queen in the row i and column j.
    queens = [Int(f"q_{i}") for i in range(n)]

    # each queen is in a column {0, ... 7 }
    solver.add([And(0 <= queens[i], queens[i] < n) for i in range(n)])

    # one queen per column
    solver.add([Distinct(queens)])

    # at most one for per anti-diagonal & diagonal
    solver.add([If(i == j, True, And(queens[i] - queens[j] != i - j, queens[i] - queens[j] != j - i))
                for i in range(n) for j in range(i)])

    # count the number of solutions
    solution_count = 0
    start = time.time()

    while solver.check() == sat:
        solution_count += 1
        model = solver.model()

        if verbose:
            # print the solutions
            print([(index, model[queen])
                  for index, queen in enumerate(queens)])

        # generate constraints from solution
        solution_cons = [(queen == model[queen]) for queen in queens]

        # add solution to the solver to get new solution
        solver.add(Not(And(solution_cons)))

    print(
        f"n_queen_la_opt solve {board_size}-queens by {(time.time() - start):.6f}s")

    return solution_count


if __name__ == '__main__':
    # 8-queen problem has 92 solutions
    print("--------------- N = 8 ---------------")
    N = 8
    print(n_queen_bt(N))
    print(n_queen_dfs(N))
    print(n_queen_la(N))
    print(n_queen_la_opt(N))

    '''
    n_queen_bt solve 8-queens by 0.030147s
    92
    n_queen_dfs solve 8-queens by 0.005514s
    92
    n_queen_la solve 8-queens by 4.752979s
    92
    n_queen_la_opt solve 8-queens by 0.366914s
    92
    '''

    # @Exercise 12: Try to compare the backtracking with the LA algorithms,
    # by changing the value of the chessboard size to other values,
    # which one is faster? What conclusion you can draw from the result?
    print("--------------- N = 10 ---------------")
    N = 10
    print(n_queen_bt(N))
    print(n_queen_dfs(N))
    print(n_queen_la(N))
    print(n_queen_la_opt(N))

    '''
    n_queen_bt solve 10-queens by 0.454695s
    724
    n_queen_dfs solve 10-queens by 0.083236s
    724
    n_queen_la solve 10-queens by 64.644696s
    724
    n_queen_la_opt solve 10-queens by 5.702909s
    724
    '''

    # @Exercise 13: Try to compare the efficiency of n_queen_la_opt() method
    # with your n_queen_la() method.
    # What's your observation? What conclusion you can draw?
    print("--------------- N = 16 ---------------")
    N = 16
    print(n_queen_bt(N))
    print(n_queen_dfs(N))
    print(n_queen_la(N))
    print(n_queen_la_opt(N))

    '''
    Killed
    '''

    print("--------------- N = 32 ---------------")
    N = 32
    print(n_queen_bt(N))
    print(n_queen_dfs(N))
    print(n_queen_la(N))
    print(n_queen_la_opt(N))

    '''
    Since N=16 cases are OOM Killed, there's no test result for N=32 :(
    '''

    # Conclusion: As the test result shows, the backtrace version is much faster
    # but it comsumes too much memory and is still slower than pre-allocated flags dfs.
