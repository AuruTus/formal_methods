from z3 import *


def pretty_print(expr):
    print(trans_pretty(expr))


def trans_pretty(expr, var_mapping=None, depth=0, top_level=True):
    if var_mapping is None:
        var_mapping = {}
    if is_quantifier(expr):
        num_vars = expr.num_vars()
        bound_vars = [expr.var_name(i) for i in range(num_vars)]
        body = expr.body()
        new_var_mapping = var_mapping.copy()
        for i, var in enumerate(bound_vars):
            new_var_mapping[f'Var({depth + i})'] = var
        body_str = trans_pretty(body, new_var_mapping, depth + num_vars, False)
        quantifier_str = "∀" if expr.is_forall() else "∃"
        return f"{quantifier_str}{', '.join(bound_vars)}.({body_str})" if body_str.startswith("¬") and depth == 0 else \
            f"{quantifier_str}{', '.join(bound_vars)}.{body_str}"
    elif is_iff(expr):
        left, right = expr.children()
        if is_implies(left) and is_implies(right) and is_implies_equivalent(left, right):
            antecedent, consequent = left.children()
            antecedent_str = trans_pretty(
                antecedent, var_mapping, depth, False)
            consequent_str = trans_pretty(
                consequent, var_mapping, depth, False)
            if (top_level == True):
                return f"{antecedent_str} <-> {consequent_str}"
            else:
                return f"({antecedent_str} <-> {consequent_str})"
    elif is_implies(expr):
        antecedent, consequent = expr.children()
        antecedent_str = trans_pretty(antecedent, var_mapping, depth, False)
        consequent_str = trans_pretty(consequent, var_mapping, depth, False)
        if (top_level == True):
            return f"{antecedent_str} -> {consequent_str}"
        else:
            return f"({antecedent_str} -> {consequent_str})"
    elif is_and(expr):
        conjuncts = expr.children()
        conjuncts_str = " /\ ".join(trans_pretty(c,
                                    var_mapping, depth, False) for c in conjuncts)
        if (top_level == True):
            return f"{conjuncts_str}"
        else:
            return f"({conjuncts_str})"
    elif is_or(expr):
        disjuncts = expr.children()
        disjuncts_str = " \/ ".join(trans_pretty(c,
                                    var_mapping, depth, False) for c in disjuncts)
        if (top_level == True):
            return f"{disjuncts_str}"
        else:
            return f"({disjuncts_str})"
    elif is_not(expr):
        operand = expr.children()[0]
        operand_str = trans_pretty(operand, var_mapping, depth, False) if not isinstance(operand, QuantifierRef) else \
            f"({trans_pretty(operand, var_mapping, depth, False)})"
        return f"¬{operand_str}"
    elif is_app(expr) and expr.num_args() > 0:
        decl_name = expr.decl().name()
        if "=" == decl_name or "<" == decl_name or ">" == decl_name:
            arg_1_str = trans_pretty(
                expr.children()[0], var_mapping, depth, False)
            arg_2_str = trans_pretty(
                expr.children()[1], var_mapping, depth, False)
            return f"{arg_1_str} {decl_name} {arg_2_str}"
        args_str = ", ".join(trans_pretty(arg, var_mapping, depth, False)
                             for arg in expr.children())
        return f"{decl_name}({args_str})"
    elif is_var(expr):
        var_name = var_mapping.get(str(expr), str(expr))
        return var_name
    else:
        return str(expr)


def is_implies_equivalent(impl1, impl2):
    antecedent1, consequent1 = impl1.children()
    antecedent2, consequent2 = impl2.children()

    return antecedent1 == consequent2 and antecedent2 == consequent1


def is_iff(expr):
    if is_and(expr):
        conjuncts = expr.children()
        if len(conjuncts) == 2:
            left, right = conjuncts
            return is_implies(left) and is_implies(right) and is_implies_equivalent(left, right)
    return False
