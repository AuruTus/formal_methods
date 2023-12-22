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
    def compile_return_exp(e: calc.Exp):
        match e:
            case calc.ExpVar(var):
                return var
            case _:
                raise NotImplementedError(f"Unsupported return expression {e}")

    def compile_exp(e: calc.Exp) -> tac.Exp | list[tac.StmAssign]:
        match e:
            case calc.ExpVar(var):
                return tac.ExpVar(var)
            case calc.ExpBop(_):
                new_stmt = []

                def _compile_exp(curr: calc.Exp):
                    match curr:
                        case calc.ExpVar(var):
                            return var
                        case calc.ExpBop(left, right, bop):
                            new_x = _compile_exp(left)
                            new_y = _compile_exp(right)
                            new_var = next(fresh_var)
                            new_stmt.append(tac.StmAssign(
                                new_var, tac.ExpBop(new_x, new_y, bop)))
                            return new_var
                _compile_exp(e)
                return new_stmt

    def compile_stm(s: calc.Stm):
        match s:
            case calc.StmAssign(x, e):
                new_s = compile_exp(e)
                match new_s:
                    case tac.ExpVar(_):
                        tac_stms.append(tac.StmAssign(x, new_s))
                    case _:
                        new_s[-1] = tac.StmAssign(x, new_s[-1].e)
                        tac_stms.extend(new_s)

    for s in f.stms:
        compile_stm(s)
    ret_var = compile_return_exp(f.ret)
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

    calc_ret_var, tac_ret_var = Consts(
        " ".join([calc_func_ssa.ret.var, tac_func_ssa.ret]), DeclareSort("S"))

    solver = Solver()

    solver.add(
        Not(Implies(And(*calc_cons, *tac_cons), calc_ret_var == tac_ret_var)))
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
        tac.pp_func(self.tac_func)
        print(str(tac.to_ssa_func(self.tac_func)))
        self.assertEqual(str(
            tac.to_ssa_func(self.tac_func
                            )), res)

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
