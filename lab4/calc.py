from dataclasses import dataclass
from typing import List

from z3 import *

from counter import counter


##################################
# The abstract syntax for the Calc language:
'''
bop ::= + | - | * | /
E   ::= x | E bop E
S   ::= x=E
F   ::= f(x1, ..., xn){S;* return E;}
'''


########################
# expression
@dataclass
class Exp:
    pass


@dataclass
class ExpVar(Exp):
    var: str


@dataclass
class ExpBop(Exp):
    left: Exp
    right: Exp
    bop: str    # "+", "-", "*", "/"

# statement


@dataclass
class Stm:
    pass


@dataclass
class StmAssign(Stm):
    var: str
    exp: Exp

# function:


@dataclass
class Function:
    name: str
    args: List[str]
    stms: List[Stm]
    ret: Exp

###############################################
# to pretty print a program


def pp_bop(op: str) -> str:
    match op:
        case "+" | "-" | "*" | "/":
            return op
        case _:
            raise NotImplementedError(f"unsupported binary operator {op}")


def pp_exp(e: Exp) -> str:
    '''
    E   ::= x | E bop E
    '''
    match e:
        case ExpVar(var):
            return var
        case ExpBop(left, right, bop):
            return pp_exp(left) + pp_bop(bop) + pp_exp(right)
        case _:
            raise NotImplementedError(f"unsupported expression type {type(e)}")


def pp_stm(s: Stm) -> str:
    '''
    S   ::= x=E
    '''
    match s:
        case StmAssign(var, exp):
            return var + "=" + pp_exp(exp)
        case _:
            raise NotImplementedError(f"unsupported statement type {type(s)}")


def pp_func(f: Function) -> str:
    '''
    F   ::= f(x1, ..., xn){S;* return E;}
    '''
    match f:
        case Function(name, args, stms, ret):
            f_name = name
            f_args = ", ".join(args)
            f_stmt = "; ".join(map(lambda s: pp_stm(s), stms)
                               ) + "; " if len(stms) > 0 else ""
            f_ret = "return " + pp_exp(ret) + ";"
            return f_name + "(" + f_args + ")" + "{" + f_stmt + f_ret + "}"


def pp(f: Function):
    print(pp_func(f))


###############################################
# SSA conversion:
# convert expressions:
def to_ssa_exp(exp: Exp, var_map) -> Exp:
    match exp:
        case ExpVar(x):
            return ExpVar(var_map[x])
        case ExpBop(left, right, bop):
            return ExpBop(to_ssa_exp(left, var_map),
                          to_ssa_exp(right, var_map),
                          bop)

# convert statement:


def to_ssa_stm(s: Stm, var_map, fresh_var) -> Stm:
    match s:
        case StmAssign(x, e):
            new_exp = to_ssa_exp(e, var_map)
            new_var = next(fresh_var)
            var_map[x] = new_var
            return StmAssign(new_var, new_exp)

# take a function 'func', convert it to SSA


def to_ssa_func(f: Function) -> Function:
    # a map from variable to new variable:
    # init it by putting every argument into the map
    var_map = {arg: arg for arg in f.args}
    # fresh variable generator
    fresh_var = counter(prefix=f"calc_{f.name}")
    # to convert each statement one by one:
    new_stmts = [to_ssa_stm(stmt, var_map, fresh_var) for stmt in f.stms]
    # we always return a fresh variable
    new_ret_exp = to_ssa_exp(f.ret, var_map)
    new_ret_var = next(fresh_var)
    new_stmts.append(StmAssign(new_ret_var, new_ret_exp))
    return Function(f.name, f.args, new_stmts, ExpVar(new_ret_var))


###############################################
# Generate Z3 constraints:
def gen_cons_exp(exp: Exp) -> BoolRef:
    match exp:
        case ExpVar(var):
            return Const(var, DeclareSort('S'))
        case ExpBop(left, right, bop):
            def _gen_cons_bop(bop: str) -> str:
                match bop:
                    case "+":
                        return "add"
                    case "-":
                        return "minus"
                    case "*":
                        return "mul"
                    case "/":
                        return "div"
                    case _:
                        raise NotImplementedError(
                            f"Unsupported binary operator {bop}")
            func_name = "f_" + _gen_cons_bop(bop)
            left = gen_cons_exp(left)
            right = gen_cons_exp(right)
            return z3.Function(func_name,
                               DeclareSort('S'),
                               DeclareSort('S'),
                               DeclareSort('S')).__call__(left, right)

# generate constraint for statements:


def gen_cons_stm(s: Stm) -> BoolRef:
    match s:
        case StmAssign(x, e):
            return Const(x, DeclareSort('S')).__eq__(gen_cons_exp(e))


# generate constraint for function:
def gen_cons_func(f) -> List[BoolRef]:
    return [gen_cons_stm(stm) for stm in f.stms]


###############################################
# unit tests:
# a sample program:
sample_f = Function('f',
                    ['s1', 's2', 't1', 't2'],
                    [StmAssign('z', ExpBop(ExpBop(ExpVar('s1'), ExpVar('t1'), "+"),
                                           ExpBop(ExpVar('s2'),
                                                  ExpVar('t2'), "+"),
                                           "*")),
                     StmAssign('z', ExpBop(ExpVar('z'), ExpVar('s1'), "*"))],
                    ExpVar('z'))

if __name__ == '__main__':
    # print the original program
    pp(sample_f)
    # convert the program to SSA
    new_f = to_ssa_func(sample_f)
    # print the converted program
    pp(new_f)
    # generate and print Z3 constraints
    print(gen_cons_func(new_f))
