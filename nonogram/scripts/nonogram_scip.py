"""
Solution to the Nonogram puzzle.

This version uses SCIP as a solver.

Created by Aster Santana and Éder Pinheiro (Aug, 2021), Mip Wise.
"""

from pyscipopt import Model, quicksum

# region Input Data
# row strings
RS = {
  1: {1: 3, 2: 3},
  2: {1: 4, 2: 4},
  3: {1: 2, 2: 4, 3: 2},
  4: {1: 2, 2: 2, 3: 2},
  5: {1: 2, 2: 1, 3: 2, 4: 2},
  6: {1: 2, 2: 2, 3: 1, 4: 2},
  7: {1: 2, 2: 2, 3: 2},
  8: {1: 2, 2: 4, 3: 2},
  9: {1: 4, 2: 4},
  10: {1: 3, 2: 3}
  }
# column strings
CS = {
  1: {1: 10},
  2: {1: 10},
  3: {1: 2, 2: 2},
  4: {1: 2, 2: 2, 3: 2},
  5: {1: 2, 2: 3},
  6: {1: 3, 2: 2},
  7: {1: 2, 2: 2, 3: 2},
  8: {1: 2, 2: 2},
  9: {1: 10},
  10: {1: 10}
  }
# rows
I = list(RS.keys())
# columns
J = list(CS.keys())
# keys for decision variables
x_keys = [(i, j) for i in I for j in J]
y_keys = [(i, j, k) for i in I for j in J for k in RS[i]]
z_keys = [(i, j, k) for i in I for j in J for k in CS[j]]
# endregion

# region Define the model
mdl = Model('nonogram')

# add variables
x, y, z = dict(), dict(), dict()
for key in x_keys:
    x[key] = mdl.addVar(vtype='B', name=f'x_{key}')
for key in y_keys:
    y[key] = mdl.addVar(vtype='B', name=f'y_{key}')
for key in z_keys:
    z[key] = mdl.addVar(vtype='B', name=f'z_{key}')

# add constraints
# OBS: We could have combined the loops below to gain efficiency, but we kept them separated for clarity.
# each row string begins in exactly one column
for i in I:
    for k in RS[i]:
        mdl.addCons(quicksum(y[i, j, k] for j in J) == 1, name=f'str_row{i}_{k}')
# each column string begins in exactly one row
for j in J:
    for k in CS[j]:
        mdl.addCons(quicksum(z[i, j, k] for i in I) == 1, name=f'str_col{j}_{k}')
# row strings length
for i in I:
    for j in J:
        for k in RS[i]:
            for t in range(RS[i][k]):
                mdl.addCons(y[i, j, k] <= x.get((i, j+t), 0), name=f'row_len_{i}_{j}_{k}_{t}')
# column strings length
for i in I:
    for j in J:
        for k in CS[j]:
            for t in range(CS[j][k]):
                mdl.addCons(z[i, j, k] <= x.get((i+t, j), 0), name=f'col_len_{i}_{j}_{k}_{t}')
# row strings disjunction and precedence
for i in I:
    for j in J:
        for k in RS[i]:
            for jp in range(1, j + RS[i][k]+1):  # the +1 ensures disjunction, i.e., an empty cell between strings
                mdl.addCons(y.get((i, jp, k+1), 0) <= 1 - y[i, j, k], name=f'row_pre_{i}_{j}_{k}_{jp}')
# column strings disjunction and precedence
for i in I:
    for j in J:
        for k in CS[j]:
            for ip in range(1, i + CS[j][k]+1):  # the +1 ensures disjunction, i.e., an empty cell between strings
                mdl.addCons(z.get((ip, j, k+1), 0) <= 1 - z[i, j, k], name=f'col_pre_{i}_{j}_{k}_{ip}')
# set the objective function
mdl.setObjective(quicksum(x[key] for key in x_keys))
# endregion

# region Optimize and retrieve the solution
mdl.optimize()

# retrieve and print out the solution
for i in I:
    row = [int(mdl.getVal(x[i, j])) for j in J]
    print(row)
# endregion
