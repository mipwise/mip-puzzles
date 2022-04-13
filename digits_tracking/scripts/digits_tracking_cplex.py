"""
Solution to the Digits Tracking puzzle.

This version uses CPLEX as a solver.

Created by Eric Zettermann and Aster Santana (Oct 2021).
"""

import docplex.mp.model as cpl

# Input data
# columns
I = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
# digits
K = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
keys = [(i, k) for i in I for k in K]

# Build the optimization model
mdl = cpl.Model('digits_tracking')
x = mdl.var_dict(keys, vartype=mdl.binary_vartype, name='x')
mdl.add_constraints((sum(x[i, k] for k in K) == 1 for i in I), names='C1')
mdl.add_constraints((sum(k * x[i, k] for k in K) == sum(x[k, i] for k in K) for i in I), names='C2')
mdl.minimize(x[1, 1])
mdl.solve()

# Optimize and retrieve the solution
x_sol = {i: sum(k * x[i, k].solution_value for k in K) for i in I}
print(f'x = {x_sol}')




