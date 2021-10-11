"""
Solution to the Continuous Line.

This version uses Gurobi as a solver.

Created by Aster (Oct 2021), MipWise.com.
"""

import gurobipy as gp

# region Input Data
num_rows = 6
num_cols = 6
# holes
H = [(1, 3), (2, 5), (4, 3), (4, 4), (5, 1), (5, 4), (5, 6), (6, 1), (6, 6)]

num_digits = num_rows*num_cols-len(H)
# rows
I = [i for i in range(1, num_rows+1)]
# columns
J = [j for j in range(1, num_cols+1)]

# cells
C = [(i, j) for i in I for j in J if (i, j) not in H]

# keys for decision variables x
x_keys = list()
for i, j in C:
    if j > 1:
        if (i, j-1) not in H:
            x_keys.append(((i, j), (i, j-1)))
    if j < num_cols:
        if (i, j+1) not in H:
            x_keys.append(((i, j), (i, j+1)))
    if i > 1:
        if (i-1, j) not in H:
            x_keys.append(((i, j), (i-1, j)))
    if i < num_rows:
        if (i+1, j) not in H:
            x_keys.append(((i, j), (i+1, j)))
dummy = (0, 0)
x_keys = [(dummy, (i, j)) for i, j in C] + x_keys
x_keys = x_keys + [((i, j), dummy) for i, j in C]
C.append(dummy)
# endregion

# region Define the model
mdl = gp.Model('continuous_line')

# add variables
x = mdl.addVars(x_keys, vtype=gp.GRB.BINARY, name='x')
u = mdl.addVars(C, vtype=gp.GRB.INTEGER, lb=0, ub=27, name='u')

# add constraints
# exactly one origin
for i in C:
    mdl.addConstr(sum(x[i, j] for i_, j in x_keys if i_ == i) == 1, name=f'single_origin_{i}')
# exactly one destination
for j in C:
    mdl.addConstr(sum(x[i, j] for i, j_ in x_keys if j_ == j) == 1, name=f'single_dest_{j}')
# sequence
for i, j in x_keys:
    if i != dummy and j != dummy:
        mdl.addConstr(u[i] - u[j] + 1 <= (num_digits+1) * (1 - x[i, j]), name=f'seq_{i}_{j}')
# set the objective function
mdl.setObjective(x.sum(), sense=gp.GRB.MINIMIZE)  # not required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.optimize()

# retrieve and print out the solution
u_sol = {(i, j): int(round(u[i, j].X)) for (i, j) in C if (i, j) != dummy}
for i in I:
    row = [u_sol[i, j] if (i, j) in u_sol else 'X' for j in J]
    print(row)
# endregion

