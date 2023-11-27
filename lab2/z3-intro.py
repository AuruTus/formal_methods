from z3 import *
from pro_print import *

# Z3 is an SMT solver. In this lecture, we'll discuss
# the basis usage of Z3 through some working example, the
# primary goal is to introduce how to use Z3 to solve
# the satisfiability problems we've discussed in the past
# several lectures.
# We must emphasize that Z3 is just one of the many such SMT
# solvers, and by introducing Z3, we hope you will have a
# general understanding of what such solvers look like, and
# what they can do.

########################################
# Basic propositional logic

# In Z3, we can declare two propositions just as booleans, this
# is rather natural, for propositions can have values true or false.
# To declare two propositions P and Q:
P = Bool('P')
Q = Bool('Q')
# or, we can use a more compact shorthand:
P, Q = Bools('P Q')


# We can build propositions by writing Lisp-style abstract
# syntax trees, for example, the disjunction:
# P \/ Q
# can be encoded as the following AST:
F = Or(P, Q)
# Output is : Or(P, Q)
print(F)

# Note that the connective '\/' is called 'Or' in Z3, we'll see
# several other in the next.

# We have designed the function 'pretty_print(expr)' for you,
# As long as we input the expression defined by z3, we can output
# propositions that are suitable for us to read.
# Here‘s an example:

P, Q = Bools('P Q')
F = Or(P, Q)

# Output is : P \/ Q
pretty_print(F)


def assert_expression(expr, expected: str):
    prove(expr)
    if not isinstance(expr, str):
        expr = trans_pretty(expr)
    assert expr.lower().replace(' ', '') == expected.lower().replace(' ', ''), \
        f"incorrect expression: {expr}, expected: {expected}"

################################################################
##                           Part A                           ##
################################################################


# exercises 1 : P -> (Q -> P)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
P, Q = Bools('P Q')
assert_expression(
    Implies(P, Implies(Q, P)),
    "P -> (Q -> P)",
)

# exercise 2 : (P -> Q) -> ((Q -> R) -> (P -> R))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
P, Q, R = Bools("P Q R")
assert_expression(
    Implies(
        Implies(P, Q),
        Implies(Implies(Q, R), Implies(P, R))),
    "(P -> Q) -> ((Q -> R) -> (P -> R))",
)

# exercise 3 : (P /\ (Q /\ R)) -> ((P /\ Q) /\ R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
P, Q, R = Bools("P Q R")
assert_expression(
    Implies(
        And(P, And(Q, R)),
        And(And(P, Q), R),
    ),
    "(P /\ (Q /\ R)) -> ((P /\ Q) /\ R)",
)

# exercise 4 : (P \/ (Q \/ R)) -> ((P \/ Q) \/ R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
P, Q, R = Bools("P Q R")
assert_expression(
    Implies(
        Or(P, Or(Q, R)),
        Or(Or(P, Q), R)
    ),
    "(P \/ (Q \/ R)) -> ((P \/ Q) \/ R)",
)

# exercise 5 : ((P -> R) /\ (Q -> R)) -> ((P /\ Q) -> R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
P, Q, R = Bools("P Q R")
assert_expression(
    Implies(
        And(Implies(P, R), Implies(Q, R)),
        Implies(And(P, Q), R)
    ),
    "((P -> R) /\ (Q -> R)) -> ((P /\ Q) -> R)"
)

# exercise 6 : ((P /\ Q) -> R) <-> (P -> (Q -> R))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
P, Q, R = Bools("P Q R")
assert_expression(
    And(
        Implies(
            Implies(And(P, Q), R),
            Implies(P, Implies(Q, R)),
        ),
        Implies(
            Implies(P, Implies(Q, R)),
            Implies(And(P, Q), R),
        )
    ),
    "((P /\ Q) -> R) <-> (P -> (Q -> R))",
)


# exercise 7 : (P -> Q) -> (¬Q -> ¬P)
# Please use z3 to define the proposition
# Note that you need to define the proposition, and prove it.
P, Q = Bools("P Q")
assert_expression(
    Implies(
        Implies(P, Q),
        Implies(Not(Q), Not(P)),
    ),
    "(P -> Q) -> (¬Q -> ¬P)",
)


################################################################
##                           Part B                           ##
################################################################

# Before writing the code first, we need to understand the
# quantifier. ∀ x.P (x) means that for any x, P (x) holds,
# so both x and P should be a sort types. IntSort() and BoolSort()
# are given in Z3
# IntSort(): Return the integer sort in the given context.
# BoolSort(): Return the Boolean Z3 sort.
isort=IntSort()
bsort=BoolSort()

# Declare a Int variable x
x=Int('x')

# Declare a function P with input of isort type and output
# of bsort type
P=Function('P', isort, bsort)

# It means ∃x.P(x)
F=Exists(x, P(x))
print(F)
pretty_print(F)

# Now you can complete the following exercise based on the example above

# exercise 8 : # ∀x.(¬P(x) /\ Q(x)) -> ∀x.(P(x) -> Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.

x = Int("x")
P = Function("P", IntSort(), BoolSort())
Q = Function("Q", IntSort(), BoolSort())
F_1 = ForAll(x, And(Not(P(x)), Q(x)))
F_2 = ForAll(x, Implies(P(x), Q(x)))
assert_expression(
    Implies(F_1, F_2),
    "∀x.(¬P(x) /\ Q(x)) -> ∀x.(P(x) -> Q(x))",
)

# exercise 9 : ∀x.(P(x) /\ Q(x)) <-> (∀x.P(x) /\ ∀x.Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
x = Int("x")
P = Function("P", IntSort(), BoolSort())
Q = Function("Q", IntSort(), BoolSort())
F_1 = ForAll(x, And(P(x), Q(x)))
F_2 = ForAll(x, P(x))
F_3 = ForAll(x, Q(x))
assert_expression(
    And(
        Implies(F_1, And(F_2, F_3)),
        Implies(And(F_2, F_3), F_1),
    ),
    "∀x.(P(x) /\ Q(x)) <-> (∀x.P(x) /\ ∀x.Q(x))",
)

# exercise 10 : ∃x.(¬P(x) \/ Q(x)) -> ∃x.(¬(P(x) /\ ¬Q(x)))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
x = Int("x")
P = Function("P", IntSort(), BoolSort())
Q = Function("Q", IntSort(), BoolSort())
F_1 = Exists(x, Or(Not(P(x)), Q(x)))
F_2 = Exists(x, Not(And(P(x), Not(Q(x)))))
assert_expression(
    Implies(F_1, F_2),
    "∃x.(¬P(x) \/ Q(x)) -> ∃x.(¬(P(x) /\ ¬Q(x)))",
)

# exercise 11 : ∃x.(P(x) \/ Q(x)) <-> (∃x.P(x) \/ ∃x.Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
x = Int("x")
P = Function("P", IntSort(), BoolSort())
Q = Function("Q", IntSort(), BoolSort())
F_1 = Exists(x, Or(P(x), Q(x)))
F_2 = Exists(x, P(x))
F_3 = Exists(x, Q(x))
assert_expression(
    And(
        Implies(F_1, Or(F_2, F_3)),
        Implies(Or(F_2, F_3), F_1),
    ),
    "∃x.(P(x) \/ Q(x)) <-> (∃x.P(x) \/ ∃x.Q(x))",
)

# exercise 12 : ∀x.(P(x) -> ¬Q(x)) -> ¬(∃x.(P(x) /\ Q(x)))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
x = Int("x")
P = Function("P", IntSort(), BoolSort())
Q = Function("Q", IntSort(), BoolSort())
F_1 = ForAll(x, Implies(P(x), Not(Q(x))))
F_2 = Exists(x, And(P(x), Q(x)))
assert_expression(
    Implies(
        F_1,
        Not(F_2),
    ),
    "∀x.(P(x) -> ¬Q(x)) -> ¬(∃x.(P(x) /\ Q(x)))",
)


# exercise 13 : (∃x.(P(x) /\ Q(x)) /\ ∀x.(P(x) -> R(x))) -> ∃x.(R(x) /\ Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
x = Int("x")
P = Function("P", IntSort(), BoolSort())
Q = Function("Q", IntSort(), BoolSort())
R = Function("R", IntSort(), BoolSort())
F_1 = Exists(x, And(P(x), Q(x)))
F_2 = ForAll(x, Implies(P(x), R(x)))
F_3 = Exists(x, And(R(x), Q(x)))
assert_expression(
    Implies(
        And(F_1, F_2),
        F_3,
    ),
    "(∃x.(P(x) /\ Q(x)) /\ ∀x.(P(x) -> R(x))) -> ∃x.(R(x) /\ Q(x))",
)

# exercise 14 : ∃x.∃y.P(x, y) -> ∃y.∃x.P(x, y)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
x = Int("x")
y = Int("y")
P = Function("P", IntSort(), IntSort(), BoolSort())
# !BUG(z3py): WTF the z3 treats the inner variable as Var{0} and the outer one as Var{1}
# for z3:       var(1)          var(0)   P(var(0), var(1))
#         Exists(x,        Exists(y, P(y, x)))
# for our map   var(0)         var(1)
# seems no z3 api for us to get the ast context for such continuous quantifier expression, sadly
F_1 = Exists(x, Exists(y, P(y, x)))
F_2 = Exists(y, Exists(x, P(y, x)))
assert_expression(
    Implies(
        F_1, F_2,
    ),
    "∃x.∃y.P(x, y) -> ∃y.∃x.P(x, y)",
)

# exercise 15 : (P(b) /\ ∀x.∀y.(P(x) /\ (P(y) -> x = y))) -> ∀x.(P(x) <-> x = b)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
x = Int("x")
y = Int("y")
b = Int("b")
P = Function("P", IntSort(), BoolSort())
F_1 = P(b)
F_2 = ForAll(x, ForAll(y, And(P(y), Implies(P(x), y==x))))
F_3 = ForAll(x, And(
    Implies(P(x), x==b),
    Implies(x==b, P(x)),
))
assert_expression(
    Implies(
        And(F_1, F_2),
        F_3,
    ),
    "(P(b) /\ ∀x.∀y.(P(x) /\ (P(y) -> x = y))) -> ∀x.(P(x) <-> x = b)",
)


################################################################
##                           Part C                           ##
################################################################

# Challenge:
# We provide the following two rules :
#     ----------------(odd_1)
#           odd 1
#
#           odd n
#     ----------------(odd_ss)
#         odd n + 2
#
# Please prove that integers 9, 25, and 99 are odd numbers.

# declare sorts: isort and bsort
isort=IntSort()
bsort=BoolSort()

raise NotImplementedError('TODO: Your code here!')
