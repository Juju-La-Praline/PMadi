from mdpmadi22_class import Display
from ProjectCore import *
import gurobipy as gp
from gurobipy import GRB
import numpy as np

# S : set of states
# A : set of actions
# T : S x A -> L(S) transition function
# (s, a) -> T(s, a) probability on the states of the nature
# R : S x A -> R reward function
# (s, a) -> R(s, a) reward of the state s and the action a

# max fi(x) = sum sum R(s, a) * x(s, a)
# s.t. sum x(s, a) - gamma * sum s' sum a T(s, a, s') * x(s', a) = mu(s)
# x(s, a) >= 0

nb_lines = 10
nb_columns = 20

weights = [np.array([1,1]), 2, np.array([2,0]), np.array([0,2]), 16, np.array([-1000, -1000])]

p_tiles_type = {'pwall': 0.15, 'pwhite': 0.45, 'pgreen': 0.0, 'pblue': 0.2, 'pred': 0.2}

e = Env(nb_columns, nb_lines, weights, 1, p_tiles_type, 0)
e.create_rnd_map()

m = gp.Model("bi-objective mdp")

# Create variables
var_names = []
for s in e.listAllStates:
    for a in s.dictNextStates:
        var_names.append((s.coords, a))
x = m.addVars(var_names, vtype=GRB.CONTINUOUS, name="x")

z = m.addVar(vtype=GRB.CONTINUOUS, name="z")

# Set objective
m.setObjective(z, GRB.MAXIMIZE)

# Décommenter si le modèle est unbouded ou infeasible
# m.Params.DualReductions = 0
# m.Params.InfUnbdInfo = 1

nb_states = len(e.listAllStates)

gamma = 0.9

# Add constraint

c = m.addConstrs((gp.quicksum(x[s.coords, a] for a in s.dictNextStates) - gamma * gp.quicksum(e.T(sp, a, s) * x[sp.coords, a] for sp in e.get_previous_states(s) for a in sp.dictNextStates) == 1/nb_states for s in e.listAllStates), name="c")
# sum[a] x((i,j),a) - gamma * sum[i',j'] sum[a] T((i',j'),a,(i,j)) * x((i',j'),a) = 1/nb_states for all (i,j)

m.addConstrs((x[s.coords, a] >= 0 for s in e.listAllStates for a in s.dictNextStates), name="c")
# x((i,j),a) >= 0 for all (i,j) and all a
m.addConstr(gp.quicksum(x[s.coords, a] * e.get_state(s.dictNextStates[a][0], s.dictNextStates[a][1]).reward[0] for s in e.listAllStates for a in s.dictNextStates) >= z, name="c")
# sum[(i,j)] sum[a] x((i,j),a) * R((i,j),a)[0] <= z
m.addConstr(gp.quicksum(x[s.coords, a] * e.get_state(s.dictNextStates[a][0], s.dictNextStates[a][1]).reward[1] for s in e.listAllStates for a in s.dictNextStates) >= z, name="c")
# sum[(i,j)] sum[a] x((i,j),a) * R((i,j),a)[1] <= z

# Optimize model
m.optimize()
# Décommenter si le modèle est infeasible
# m.computeIIS()
# m.write("model.ilp")

# Décommenter si le modèle est unbouded
# print(m.UnbdRay)

display = Display(2, e, m.getVars()[:-1])
display.initialize()

display.run()


