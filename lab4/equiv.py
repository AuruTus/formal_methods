from z3 import *


# program equivalence:
# in the class, we present two implementation of the same algorithms, one
# is:
'''
int power3(int in){
  int i, out_a;
  out_a = in;
  for(i = 0; i < 2; i++)
    out_a = out_a * in;
  return out_a;
}
'''
# and the other one is:
'''
int power3_new(int in){
  int out_b;
  out_b = (in*in)*in;
  return out_b;
}

'''
# and with EUF, we can prove that these two algorithms are equivalent,
# that is:
# P1/\P2 -> out_a==out_b

# Exercise 2: try to prove the algorithm 'power3' and 'power3_new'
# are equivalent by using EUF theory
# Please construct, manually, the propositions P1 and P2, and let Z3
# prove the above implication. (Note that you don't need to generate
# P1 or P2 automatically, just write down them manually.)

ist = IntSort()
multi = Function("multi", ist, ist, ist)
_in, _out_a_1, _out_a_2, _out_b = Consts(
    "_in, _out_a_1, _out_a_2, _out_b", ist)

power3 = And(_out_a_1 == multi(_in, _in), And(
    _out_a_2 == multi(_out_a_1, _in)))
power3_new = _out_b == multi(_in, multi(_in, _in))

solve(Implies(And(power3, power3_new), _out_a_2 == _out_b))
