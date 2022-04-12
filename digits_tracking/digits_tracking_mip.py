"""
Solution to the Digits Tracking puzzle.

This version uses Python-MIP as a modeling language and CBC as a solver.

Created by Aster Santana (Nov, 2021), MipWise.com.
"""

import mip

# region Input Data

# columns
I = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
# digits
K = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

# keys for decision variables x
keys = [(i, k) for i in I for k in K]
# endregion

# region Define the model
mdl = mip.Model()

# add variables
x = {key: mdl.add_var(var_type=mip.BINARY, name='x') for key in keys}

# add constraints
# exactly one digit is assigned to each cell
for i in I:
    mdl.add_constr(mip.xsum(x[(i, k)] for k in K) == 1, name=f'One-digit-per-cell-{i}')

# If the digit k is assigned to cell i, then i must appear k times in the grid.
for i in I:
    mdl.add_constr(mip.xsum(k * x[(i, k)] for k in K) == mip.xsum(x[(k, i)] for k in K), name=f'rep-condition-{i}')

# set the objective function
mdl.objective = mip.minimize(x[1, 1])  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.optimize()

# retrieve and print out the solution
x_sol = {i: sum(k * x[i, k].x for k in K) for i in I}
print(f'x = {x_sol}')
# endregion
