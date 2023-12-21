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
def pp_exp(e: Exp):
    raise NotImplementedError('TODO: Your code here!') 

def pp_stm(s: Stm):
    raise NotImplementedError('TODO: Your code here!') 

def pp_func(f):
    match f:
        case Function(name, args, stms, ret):
            raise NotImplementedError('TODO: Your code here!') 

def pp(f: Function):
    pp_func(f)



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
            func_name = "f_" + bop
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
                                                      ExpBop(ExpVar('s2'), ExpVar('t2'), "+"),
                                                      "*")),
                     StmAssign('z', ExpBop(ExpVar('z'), ExpVar('s1'), "*"))],
                    ExpVar('z'))

if __name__ == '__main__':
    # print the original program
    pp_func(sample_f)
    # convert the program to SSA
    new_f = to_ssa_func(sample_f)
    # print the converted program
    pp_func(new_f)
    # generate and print Z3 constraints
    print(gen_cons_func(new_f))

