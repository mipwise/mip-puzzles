"""
Solution to the Digits Tracking puzzle.

This version uses Gurobi as a solver.

Created by Eric Zettermann and Aster Santana (Oct 2021), MipWise.com.
"""

import gurobipy as gp

# region Input Data

# columns
I = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
# digits
K = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

# keys for decision variables x
keys = [(i, k) for i in I for k in K]
# endregion

# region Define the model
mdl = gp.Model('digits_tracking')

# add variables
x = mdl.addVars(keys, vtype=gp.GRB.BINARY, name='x')

# add constraints
# exactly one digit is assigned to each cell
for i in I:
    mdl.addConstr(sum(x[(i, k)] for k in K) == 1, name=f'One-digit-per-cell-{i}')

# If the digit k is assigned to cell i, then i must appear k times in the grid.
for i in I:
    mdl.addConstr(sum(k * x[(i, k)] for k in K) == sum(x[(k, i)] for k in K), name=f'rep-condition-{i}')

# set the objective function
mdl.setObjective(x[1, 1], sense=gp.GRB.MAXIMIZE)  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.optimize()

# retrieve and print out the solution
x_sol = {i: sum(k * x[i, k].X for k in K) for i in I}
print(f'x = {x_sol}')
# endregion
