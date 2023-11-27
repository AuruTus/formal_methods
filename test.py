from z3 import *

x = Int("x")
odd = Function("odd", IntSort(), BoolSort())
prove(Implies(ForAll(x, odd(x) == odd(x-2)), odd(29) == odd(1)))
