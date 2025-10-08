# File: USN_Week7_FOL_Unification.py
# Program: Unification in First Order Logic

def is_variable(x):
    return isinstance(x, str) and x[0].islower()

def occur_check(var, expr):
    if var == expr:
        return True
    elif isinstance(expr, list):
        return any(occur_check(var, subexpr) for subexpr in expr)
    return False

def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    if theta == "FAIL":
        return "FAIL"
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        if not x:
            return theta
        first_unify = unify(x[0], y[0], theta)
        return unify(x[1:], y[1:], first_unify)
    else:
        return "FAIL"

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif is_variable(x) and x in theta:
        return unify(var, theta[x], theta)
    elif occur_check(var, x):
        return "FAIL"
    else:
        theta_new = theta.copy()
        theta_new[var] = x
        return theta_new

# ----------- Example Test -----------
if __name__ == "__main__":
    # Example 1
    x = ['Knows', 'John', 'x']
    y = ['Knows', 'John', 'Mary']
    print("Unifying:", x, "and", y)
    print("Result:", unify(x, y))

    # Example 2
    x = ['Knows', 'x', ['Mother', 'y']]
    y = ['Knows', 'John', 'z']
    print("\nUnifying:", x, "and", y)
    print("Result:", unify(x, y))
