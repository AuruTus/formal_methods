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

################################################################
##                           Part A                           ##
################################################################

# exercises 1 : P -> (Q -> P)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
F = Implies(P, Implies(Q, P))
trans_pretty(F)

# exercise 2 : (P -> Q) -> ((Q -> R) -> (P -> R))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 3 : (P /\ (Q /\ R)) -> ((P /\ Q) /\ R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 4 : (P \/ (Q \/ R)) -> ((P \/ Q) \/ R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 5 : ((P -> R) /\ (Q -> R)) -> ((P /\ Q) -> R)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 6 : ((P /\ Q) -> R) <-> (P -> (Q -> R))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 7 : (P -> Q) -> (¬Q -> ¬P)
# Please use z3 to define the proposition
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')


################################################################
##                           Part B                           ##
################################################################

# Before writing the code first, we need to understand the
# quantifier. ∀ x.P (x) means that for any x, P (x) holds,
# so both x and P should be a sort types. IntSort() and BoolSort()
# are given in Z3
# IntSort(): Return the integer sort in the given context.
# BoolSort(): Return the Boolean Z3 sort.
isort = IntSort()
bsort = BoolSort()

# Declare a Int variable x
x = Int('x')

# Declare a function P with input of isort type and output
# of bsort type
P = Function('P', isort, bsort)

# It means ∃x.P(x)
F = Exists(x, P(x))
print(F)
pretty_print(F)

# Now you can complete the following exercise based on the example above

# exercise 8 : # ∀x.(¬P(x) /\ Q(x)) -> ∀x.(P(x) -> Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 9 : ∀x.(P(x) /\ Q(x)) <-> (∀x.P(x) /\ ∀x.Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 10 : ∃x.(¬P(x) \/ Q(x)) -> ∃x.(¬(P(x) /\ ¬Q(x)))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 11 : ∃x.(P(x) \/ Q(x)) <-> (∃x.P(x) \/ ∃x.Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 12 : ∀x.(P(x) -> ¬Q(x)) -> ¬(∃x.(P(x) /\ Q(x)))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 13 : ∃x.(P(x) /\ Q(x)) /\ ∀x.(P(x) -> R(x)) -> ∃x.(R(x) /\ Q(x))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 14 : ∃x.∃y.P(x, y) -> ∃y.∃x.P(x, y)
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')

# exercise 15 : P(b) /\ (∀x.∀y.(P(x) /\ P(y) -> x = y)) -> (∀x.(P(x) <-> x = b))
# Please use z3 to define the proposition.
# Note that you need to define the proposition, and prove it.
raise NotImplementedError('TODO: Your code here!')


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
isort = IntSort()
bsort = BoolSort()

raise NotImplementedError('TODO: Your code here!')
