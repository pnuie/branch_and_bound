import gurobipy as gp
from gurobipy import GRB
import heapq
import math

def relaxed(model):
    global iteration
    model.optimize()
    if model.status == GRB.OPTIMAL:
        sol = [v.x for v in model.getVars()]
        obj = model.ObjVal
    else:
        return False
    return (obj, iteration, sol, model)

def initialize():
    initial_model = gp.Model("Minimize Example")
    initial_model.setParam('Outputflag', 0)
    v = [45, 48, 35]
    w = [5, 8, 3]
    K = 28
    x = initial_model.addVars(range(3), vtype=GRB.CONTINUOUS, name="x")
    initial_model.setObjective(gp.quicksum(v[i] * x[i] for i in range(3)), GRB.MINIMIZE)
    initial_model.addConstr(gp.quicksum(w[i] * x[i] for i in range(3)) >= K)
    return initial_model

def lower_node(obj, sol, model, idx, isfraction):
    global iteration
    lower_model = model.copy()
    x = lower_model.getVars()
    lower_model.addConstr(x[idx] == math.floor(isfraction), name="Lower Branch")
    return (obj, iteration, sol, lower_model)

def upper_node(obj, sol, model, idx, isfraction):
    global iteration
    upper_model = model.copy()
    x = upper_model.getVars()
    upper_model.addConstr(x[idx] == math.ceil(isfraction), name="Upper Branch")
    return (obj, iteration, sol, upper_model)

iteration = 0
initial_node = relaxed(initialize())
best_obj = 0
pq = []
heapq.heappush(pq, initial_node)

while pq:
    flag = False
    node = heapq.heappop(pq)
    print(node[2])
    temp = relaxed(node[3])
    if temp == False:
        print('There is no feasible solution.')
        continue
    if best_obj > 0: # 현재 Z_lp가 Best_Obj보다 크면 Prouning
        if temp[0] > best_obj : continue # 현재 Z_lp가 Best_Obj보다 크면 Prouning
    for i in range(len(temp[2])):
        idx, isfraction = i, temp[2][i]
        if isfraction%1 == 0: # 만약 int라면
            continue
        else:
            iteration += 1
            heapq.heappush(pq, lower_node(temp[0], temp[2], temp[3], idx, isfraction))
            iteration += 1
            heapq.heappush(pq, upper_node(temp[0], temp[2], temp[3], idx, isfraction))
            flag = True
    if flag == False: #다 정수일 때만 갱신해라
        best_obj, best_sol = temp[0], temp[2]

print(f"목적함수 값: {best_obj}\n최적해: {best_sol}")