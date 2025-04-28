import heapq
from math import ceil, floor

from gurobipy import GRB


class BB_ver2:
    def __init__(self, model, sense=GRB.MINIMIZE):
        """
        :param model: gp.Model
        :param sense: Minimize or Maximize

        objVal : objective value
        sol : optimal solution
        """
        self.model = model
        self.num_vars = len(self.model.getVars())
        self.sense = 1 if sense == GRB.MINIMIZE else -1
        self.current_best = 1e9 if self.sense == 1 else -1e9
        self.objVal = None
        self.sol = []
        self.optimal_sol = None
        self.cnt_node = 0
        self.pq = []
        self.flag = None

    def relaxed(self, model):
        model.optimize()
        if model.status == GRB.OPTIMAL:
            vars = model.getVars()
            self.objVal = model.ObjVal
            self.sol = [vars[i].X for i in range(self.num_vars)]
            self.cnt_node += 1
            return 0, self.objVal, self.cnt_node, model, self.sol  # (목적함수값, n번째 node, model, 해)
        else:
            return 'Cannot find feasible solution'

    def prouning(self, model, idx, isfraction):
        upper_model = model.copy()
        lower_model = model.copy()
        y = upper_model.getVars()
        x = lower_model.getVars()
        upper_model.addConstr(y[idx] >= ceil(isfraction), name="Upper Branch")
        lower_model.addConstr(x[idx] <= floor(isfraction), name="Lower Branch")
        self.cnt_node += 1
        heapq.heappush(self.pq, (0.5-(isfraction%1), self.objVal, self.cnt_node, upper_model, self.sol))
        self.cnt_node += 1
        heapq.heappush(self.pq, (0.5-(isfraction%1), self.objVal, self.cnt_node, lower_model, self.sol))

    def solve(self):
        initial_node = self.relaxed(self.model)
        heapq.heappush(self.pq, initial_node)
        while self.pq:
            there_is_fraction_value = False
            node = self.relaxed(heapq.heappop(self.pq)[3])
            if node == 'Cannot find feasible solution':
                continue
            if self.sense == 1:
                if node[1] > self.current_best:
                    continue
            if self.sense == -1:
                if node[1] < self.current_best:
                    continue
            for i in range(self.num_vars):
                idx, isfraction = i, node[4][i]
                if isfraction % 1 == 0:  # 만약 int라면
                    continue
                else:
                    self.prouning(node[3], idx, isfraction)
                    there_is_fraction_value = True
            if not there_is_fraction_value:
                self.current_best, self.optimal_sol = self.objVal, self.sol

    def print_result(self):
        print(f"BB - {self.current_best}, sol : {self.optimal_sol}")
        print(self.cnt_node)