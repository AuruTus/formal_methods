"""Applications of SAT via Z3

In the previous part we've discussed how to obtain solutions and prove
the validity for propositions.
In this part, we will try to use Z3 to solve some practical problems.
Hints:
 You can reuse the `sat_all` function that you've implemented in exercise 1
 if you think necessary."""

from z3 import *

# Exercise 4: Circuit Layout
# Usually When EE-Engineers design a circuit layout, they will verify it to
# make sure that the layout will not only output a single electrical level
# since it's useless.
# Now let's investigate the Circuit Layout we provide you.
# According to the requirement, what we should do is to convert the circuit layout
# into a proposition expression, let's say 'F', and try to obtains the solutions
# for F and Not(F).
# And then make sure that both F and Not(F) can be satisfied.
# First we convert it into proposition


def circuit_layout():
    from z3_solver import _sat_all

    def _assert_solution_number(props: list[ExprRef], f: ExprRef, expected: int, error: str):
        assert len(_sat_all(props, f)) == expected, error

    a, b, c, d = Bools('a b c d')
    A_B = And(a, b)
    A_B_D = And(A_B, d)
    NC = Not(c)
    A_B_NC = And(A_B, NC)
    F = Or(A_B_D, A_B_NC)

    _assert_solution_number([a, b, c, d], F, 3, "wrong solution number for F")
    _assert_solution_number([a, b, c, d], Not(F), 13,
                            "wrong solution number for Not(F)")

    print("assertion succeededs")


if __name__ == '__main__':
    # circuit_layout should have 3 solutions for F and 13 solutions for Not(F)
    circuit_layout()
