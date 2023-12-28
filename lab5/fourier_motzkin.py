import unittest
from typing import List

import pandas as pd

from tableau import Tableau
from constraint import Rel, Constraint, IllegalConstraintError


def eli_equations(table: Tableau) -> Tableau:
    # Challenge : finish the equation elimination step for the
    # fourier_motzkin  algorithm
    #
    # Your src here
    raise NotImplementedError('TODO: Your code here!') 


def eli_unbounded_vars(table: Tableau) -> Tableau:
    # Challenge : finish the unbounded variable elimination step for the
    # fourier_motzkin  algorithm
    #
    # Your src here
    raise NotImplementedError('TODO: Your code here!') 

def eli_vars(table: Tableau) -> Tableau:
    # Challenge : finish the bounded variable elimination step for the
    # fourier_motzkin  algorithm
    #
    # Your src here
    raise NotImplementedError('TODO: Your code here!') 

def solve_one_var(table: Tableau) -> float:
    # Challenge : finish the solve the last variable step for the
    # fourier_motzkin  algorithm
    #
    # Your src here
    raise NotImplementedError('TODO: Your code here!') 


def fourier_motzkin(la_prop: List[Constraint]) -> dict | str:
    # Challenge : finish the fourier_motzkin  algorithm by assembling the
    # four steps above
    #
    # Your src here
    result = {}
    
    raise NotImplementedError('TODO: Your code here!') 
    
    print(f"===>Solving result is {result}")
    return result


class TestFourierMotzkin(unittest.TestCase):
    def test_fourier_motzkin_sat(self):
        case = [Constraint([1, 1], 0.8), Constraint([1, -1], 0.2)]
        result = fourier_motzkin(case)
        self.assertDictEqual(result, {"x0": 0.5, "x1": 0.3})

    def test_fourier_motzkin_unsat(self):
        case = [Constraint([-1, -1], 0.8), Constraint([-1, -5], 0.2), Constraint([1, 3], 0)]
        result = fourier_motzkin(case)
        self.assertEqual(result, "no solution")
        
    def test_fourier_motzkin_unsat_2(self):
        case = [Constraint([1, -1, 0], 0), Constraint([1, 0, -1], 0), Constraint([-1, 1, 2], 0), Constraint([0, 0, -1], -1)]
        result = fourier_motzkin(case)
        self.assertEqual(result, "no solution")


if __name__ == '__main__':
    unittest.main()
    