"""
Solution to the Even-odd Sudoku.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Luiz Suzana (Jul 6, 2021), MipMaster.org.
"""

import pulp

# region Input Data
# rows, columns, and digits
I = {1, 2, 3, 4, 5, 6, 7, 8, 9}
# even cells
EC = {(2, 1), (3, 2), (3, 5), (2, 6), (2, 7), (2, 8), (3, 8), (4, 8), (5, 7), (8, 7), (8, 9)}
# odd cells
OC = {(1, 2), (2, 3), (4, 4), (5, 3), (6, 2), (6, 6), (7, 2), (8, 2), (8, 3), (8, 4), (7, 5), (7, 8), (9, 8)}
# given digits
GD = {(1, 6): 4, (1, 7): 6, (1, 9): 9, (2, 5): 5, (3, 4): 1, (3, 9): 7, (4, 3): 4, (4, 9): 8, (5, 2): 2, (5, 8): 9,
      (6, 1): 1, (6, 7): 3, (7, 1): 9, (7, 6): 8, (8, 5): 6, (9, 1): 8, (9, 3): 5, (9, 4): 7}
# bold regions
BR = {1: [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)],
      2: [(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6)],
      3: [(1, 7), (1, 8), (1, 9), (2, 7), (2, 8), (2, 9), (3, 7), (3, 8), (3, 9)],
      4: [(4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3), (6, 1), (6, 2), (6, 3)],
      5: [(4, 4), (4, 5), (4, 6), (5, 4), (5, 5), (5, 6), (6, 4), (6, 5), (6, 6)],
      6: [(4, 7), (4, 8), (4, 9), (5, 7), (5, 8), (5, 9), (6, 7), (6, 8), (6, 9)],
      7: [(7, 1), (7, 2), (7, 3), (8, 1), (8, 2), (8, 3), (9, 1), (9, 2), (9, 3)],
      8: [(7, 4), (7, 5), (7, 6), (8, 4), (8, 5), (8, 6), (9, 4), (9, 5), (9, 6)],
      9: [(7, 7), (7, 8), (7, 9), (8, 7), (8, 8), (8, 9), (9, 7), (9, 8), (9, 9)]
      }
# keys for decision variables x
keys = [(i, j, k) for i in I for j in I for k in I]
# endregion

# region Define the model
mdl = pulp.LpProblem('Even-odd-sudoku', sense=pulp.LpMaximize)

# Add Variables
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpBinary, name='x')

# Add constraints
# Each cell must have exactly one digit
for i in I:
    for j in I:
        mdl.addConstraint(pulp.lpSum(x[(i, j, k)] for k in I) == 1, name=f'One-digit-per-cell-{(i,j)}')

# Digits can't repeat in each row
for i in I:
    for k in I:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for j in I) == 1, name=f'No-repeat-row-{i}-value-{k}')

# Digits can't repeat in each column
for j in I:
    for k in I:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for i in I) == 1, name=f'No-repeat-col-{j}-value-{k}')

# Digits can't repeat in each bold region
for region in BR:
    for k in I:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for (i, j) in BR[region]) == 1, name=f'No-repeat-region-{region}-value-'
                                                                                     f'{k}')

# Some cells must have the given digits
for i, j in GD:
    value = GD[i, j]
    x[i, j, value].lowBound = 1

# Some cells must have an even digit
for i, j in EC:
    mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in I if k % 2 == 0) == 1, name=f'Even-digit-cell-{(i, j)}')

# Some cells must have an odd digit
for i, j in OC:
    mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in I if k % 2 == 1) == 1, name=f'Odd-digit-cell-{(i, j)}')

# Set Objective function
mdl.setObjective(x[1, 1, 1])  # we could choose any other non-constant function
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# Retrieve the solution (first option)
# x_sol = {key: int(var.value()) for key, var in x.items() if var.value() > 0.5}
# print(f'x = {x_sol}')

# Retrieve the solution (second option)
# x_sol = {(i, j): round(sum(k * x[i, j, k].value() for k in I)) for i in I for j in I}
# print(f'x = {x_sol}')

# Retrieve the solution (third option)
for i in I:
    print([int(sum(k * x[i, j, k].value() for k in I)) for j in I])
# endregion
