import gurobipy as gp
from gurobipy import GRB


class BB_TestCase:
    def __init__(self, test_case):
        self._build_model(test_case)

    def _build_model(self, test_case):
        model = gp.Model()
        model.setParam('OutputFlag', 0)
        if test_case == 1:
            v = [4, 6, 9, 11, 13, 18, 24, 37]
            w = [3, 5, 8, 10, 12, 17, 21, 32]
            K = 100
            num_vars = len(v)
            x = model.addVars(range(len(v)), vtype=GRB.INTEGER, name="x")
            model.addConstr(gp.quicksum(w[i] * x[i] for i in range(len(v))) >= K)
            model.setObjective(gp.quicksum(v[i] * x[i] for i in range(len(v))), GRB.MINIMIZE)
            self.sense = GRB.MINIMIZE
        elif test_case == 2:
            profit = [2, 4, 6, 7, 8, 14, 17, 44]
            weights = [3, 5, 8, 10, 12, 17, 21, 52]
            W = 100
            x = model.addVars(len(profit), vtype=GRB.INTEGER, name='x')
            num_vars = len(profit)
            model.addConstr(gp.quicksum(weights[i] * x[i] for i in range(len(profit))) <= W)
            model.setObjective(gp.quicksum(profit[i] * x[i] for i in range(len(profit))), GRB.MAXIMIZE)
            self.sense = GRB.MAXIMIZE
        self.model = model
        model.optimize()
        self.objVal = model.ObjVal
        vars = model.getVars()
        self.sol = [vars[i].X for i in range(num_vars)]

        self.relax_model = model.copy()
        vars = self.relax_model.getVars()
        for var in vars:
            var.vtype = GRB.CONTINUOUS
        self.relax_model.update()
        self.relax_model.optimize()
        self.relax_objVal = self.relax_model.ObjVal
        self.relax_sol = [vars[i].X for i in range(num_vars)]

    def print_origin(self):
        print(f"Origin - {self.objVal}, sol : {self.sol}")

    def print_relax(self):
        print(f"Relax - {self.relax_objVal}, sol : {self.relax_sol}")