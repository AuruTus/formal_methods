from typing import List
import unittest

from z3 import *

import calc
import tac
from counter import counter


###############################################
# a compiler from Calc to Tac.
def compile_func(f: calc.Function) -> tac.Function:
    tac_stms = []
    fresh_var = counter(f"tmp_{f.name}")

    # Exercise 9: Finish the compiler implementation by filling in the 
    # missing code in compile_exp()
    def compile_exp(e: calc.Exp) -> str:
        raise NotImplementedError('TODO: Your code here!') 

    def compile_stm(s: calc.Stm):
        match s:
            case calc.StmAssign(x, e):
                y = compile_exp(e)
                new_s = tac.StmAssign(x, tac.ExpVar(y))
                tac_stms.append(new_s)

    for s in f.stms:
        compile_stm(s)
    ret_var = compile_exp(f.ret)
    return tac.Function(f.name, f.args, tac_stms, ret_var)


# Exercise 10: do the translation validation by proving this condition: orig_cons /\ result_cons -> x1==x2"
# recall that the z3.And() can accept list of constraints
def translation_validation(calc_func: calc.Function, tac_func: tac.Function) -> Solver:
    # for the compiler to be correct, you should prove this condition:
    #      orig_cons /\ result_cons -> x1==x2
    # is always validity
    calc_func_ssa = calc.to_ssa_func(calc_func)
    tac_func_ssa = tac.to_ssa_func(tac_func)

    calc_cons: List[BoolRef] = calc.gen_cons_func(calc_func_ssa)
    tac_cons: List[BoolRef] = tac.gen_cons_func(tac_func_ssa)

    solver = Solver()

    raise NotImplementedError('TODO: Your code here!') 
    return solver


###############################################
# Tests


class TestTV(unittest.TestCase):

    tac_func = compile_func(calc.sample_f)

    def test_compile(self):
        res = ("f(s1, s2, t1, t2){\n\t_tac_f_0 = s1 + t1;\n\t_tac_f_1 = s2 + t2;\n\t"
               "_tac_f_2 = _tac_f_0 * _tac_f_1;\n\t_tac_f_3 = _tac_f_2;\n\t_tac_f_4 = _tac_f_3 * s1;\n\t"
               "_tac_f_5 = _tac_f_4;\n\treturn _tac_f_5;\n}")

        # f(s1, s2, t1, t2){
        #   _tac_f_0 = s1 + t1;
        #   _tac_f_1 = s2 + t2;
        #   _tac_f_2 = _tac_f_0 * _tac_f_1;
        #   _tac_f_3 = _tac_f_2;
        #   _tac_f_4 = _tac_f_3 * s1;
        #   _tac_f_5 = _tac_f_4;
        #   return _tac_f_5;
        # }
        # self.assertEqual(str(tac.to_ssa_func(self.tac_func)), res)

    def test_tv(self):
        solver = translation_validation(calc.sample_f, self.tac_func)

        # [Not(Implies(And(_calc_f_0 ==
        #                  f_mul(f_add(s1, t1), f_add(s2, t2)),
        #                  _calc_f_1 == f_mul(_calc_f_0, s1),
        #                  _tac_f_0 == f_add(s1, t1),
        #                  _tac_f_1 == f_add(s2, t2),
        #                  _tac_f_2 == f_mul(_tac_f_0, _tac_f_1),
        #                  _tac_f_3 == _tac_f_2,
        #                  _tac_f_4 == f_mul(_tac_f_3, s1),
        #                  _tac_f_5 == _tac_f_4),
        #              _calc_f_1 == _tac_f_5))]
        print(solver)
        self.assertEqual(str(solver.check()), "unsat")


if __name__ == '__main__':
    unittest.main()
