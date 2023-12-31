""" The subset problem

The subset problem is a well-known satisfiability problem: given
a multiset (a multiset is like a normal set, expect for the
elements can be duplicated) S, whether or not there is a
non-empty subset T of S, such that:
  \\sum T = 0

For example, given this set
  {-7, -3, -2, 9000, 5, 8}
the answer is yes because the subset
  {-3, -2, 5}
sums to zero.

This problem is NPC, and for more background information of the
subset problem, please refer to:
https://en.wikipedia.org/wiki/Subset_sum_problem

"""

from z3 import *
import time


# LA-based solution
def subset_sum_la(target_set: list):
    solver = Solver()
    flags = [Int(f"x_{i}") for i in range(len(target_set))]

    # 0-1 ILA
    for flag in flags:
        solver.add(Or(flag == 0, flag == 1))

    # the selected set must be non-empty
    solver.add(sum(flags) != 0)

    # @Exercise 9: please fill in the missing src to add
    # the following constraint into the solver.
    #       \sum_i flags[i]*target_set[i] = 0
    solver.add(sum([f*r for (f, r) in zip(flags, target_set)]) == 0)

    start = time.time()
    result = solver.check()
    print(f"time used in LA: {(time.time() - start):.6f}s")

    if result == sat:
        return True, [target_set[index] for index, flag in enumerate(flags) if solver.model()[flag] == 1]
    return False, result


# LA-based optimized solution
def subset_sum_la_opt(target_set: list):
    solver = Solver()

    # enable Pseudo-Boolean solver
    # to get more information about Pseudo-Boolean constraints
    # refer to https://theory.stanford.edu/~nikolaj/programmingz3.html
    solver.set("sat.pb.solver", "solver")

    # use Pseudo-Boolean constraints for each flag
    flags = [Bool(f"x_{i}") for i in range(len(target_set))]

    # the selected set must be non-empty
    solver.add(PbGe([(flags[i], 1) for i in range(len(target_set))], 1))

    # selected set must sum to zero
    solver.add(PbEq([(flags[i], target_set[i])
               for i in range(len(target_set))], 0))

    start = time.time()
    result = solver.check()
    print(f"time used in LA optimized: {(time.time() - start):.6f}s")

    if result == sat:
        return True, [target_set[index] for index, flag in enumerate(flags) if solver.model()[flag]]
    return False, result


# dynamic programming-based (DP) solution (don't confuse DP with LP):
def subset_sum_dp(target_set) -> bool:
    '''
    use cache to optimize dfs.
    '''
    from functools import cache

    @cache
    def subset_sum_dp_do(target, index) -> bool:
        if index == 0:
            return False
        if target == target_set[index - 1]:
            return True
        return True if subset_sum_dp_do(target - target_set[index - 1], index - 1) \
            else subset_sum_dp_do(target, index - 1)

    start = time.time()
    result = subset_sum_dp_do(0, len(target_set))
    print(f"time used in DP: {(time.time() - start):.6f}s")
    return result


def subset_sum_dp_opt(tartget_set) -> bool:
    '''
    bfs impl with hash-set to prune branches
    '''
    def _subset_sum_dp_opt() -> bool:
        dp = {}
        queue = [(-1, 0)]
        l = len(tartget_set)
        while len(queue) > 0:
            curr = queue.pop(0)
            for i in range(curr[0]+1, l):
                sum = curr[1] + tartget_set[i]
                if dp.get(sum):
                    continue
                if sum == 0:
                    return True
                queue.append((i, curr[1]))
                queue.append((i, sum))
                dp[sum] = True

        return False

    start = time.time()
    result = _subset_sum_dp_opt()
    end = time.time()
    print(f"time used in non-recursive DP: {end - start:.6f}s")

    return result


def gen_large_test(n):
    nums = [10000] * n
    nums[len(nums) - 2] = 1
    nums[len(nums) - 1] = -1
    # print(nums)
    return nums


if __name__ == '__main__':
    # a small test case
    print("---------------small true case---------------")
    small_set = [-7, -3, -2, 9000, 5, 8]
    print(subset_sum_dp(small_set))
    print(subset_sum_dp_opt(small_set))
    print(subset_sum_la(small_set))
    print(subset_sum_la_opt(small_set))

    '''
    time used in DP: 0.000032s
    True
    time used in non-recursive DP: 0.000051s
    True
    time used in LA: 0.021428s
    (True, [-3, -2, 5])
    time used in LA optimized: 0.010312s
    (True, [-3, -2, 5])
    '''

    print("---------------small false case---------------")
    small_set = [-7, -3, -2, 9000, 8]
    print(subset_sum_dp(small_set))
    print(subset_sum_dp_opt(small_set))
    print(subset_sum_la(small_set))
    print(subset_sum_la_opt(small_set))

    '''
    time used in DP: 0.000392s
    False
    time used in non-recursive DP: 0.000205s
    False
    time used in LA: 0.015244s
    (False, unsat)
    time used in LA optimized: 0.011689s
    (False, unsat)
    '''

    # @Exercise 10: compare the efficiency of the DP and the
    # LP algorithm, by changing the value of "max_nums" to other
    # values, say, 200, 2000, 20000, 200000, ...
    # what's your observation? What conclusion you can draw from these data?

    print("---------------max_nums = 20---------------")
    max_nums = 20
    large_set = gen_large_test(max_nums)
    print(subset_sum_dp(large_set))
    print(subset_sum_dp_opt(large_set))
    print(subset_sum_la(large_set))
    print(subset_sum_la_opt(large_set))

    '''
    time used in DP: 0.000006s
    True
    time used in non-recursive DP: 0.000039s
    True
    time used in LA: 0.038829s
    (True, [1, -1])
    time used in LA optimized: 0.011110s
    (True, [1, -1])
    '''

    print("---------------max_nums = 200--------------")
    max_nums = 200
    large_set = gen_large_test(max_nums)
    print(subset_sum_dp(large_set))
    print(subset_sum_dp_opt(large_set))
    print(subset_sum_la(large_set))
    print(subset_sum_la_opt(large_set))

    '''
    time used in DP: 0.000004s
    True
    time used in non-recursive DP: 0.000094s
    True
    time used in LA: 0.205076s
    (True, [1, -1])
    time used in LA optimized: 0.021183s
    (True, [1, -1])
    '''

    print("---------------max_nums = 2000-------------")
    max_nums = 2000
    large_set = gen_large_test(max_nums)
    print(subset_sum_dp(large_set))
    print(subset_sum_dp_opt(large_set))
    print(subset_sum_la(large_set))
    print(subset_sum_la_opt(large_set))

    '''
    time used in DP: 0.000005s
    True
    time used in non-recursive DP: 0.000648s
    True
    time used in LA: 44.152249s
    (True, [1, -1])
    time used in LA optimized: 1.293954s
    (True, [1, -1])
    '''

    print("---------------max_nums = 200000-------------")
    max_nums = 200000
    large_set = gen_large_test(max_nums)
    print(subset_sum_dp(large_set))
    print(subset_sum_dp_opt(large_set))
    print(subset_sum_la(large_set))
    print(subset_sum_la_opt(large_set))

    '''
    time used in DP: 0.000005s
    True
    time used in non-recursive DP: 0.093668s
    True
    Killed
    '''

    # Conclusion:
    # I optimized the first version DP, so that it can quit much earlier with the specific test data.
    # Thanks to DP's early pruning search tree's branches strategy, DP is much more efficient than LA.
