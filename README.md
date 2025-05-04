# Branch and Bound with Custom Priority Strategies

## Overview

This repository implements a basic Branch and Bound (B&B) algorithm to solve simple Integer Programming (IP) problems.  
The approach relaxes the original IP into a Linear Programming (LP) problem, then dynamically generates branching constraints on decision variables during the search.  
Additionally, it explores different priority queue strategies to investigate how node selection order impacts search efficiency and the number of explored nodes.

![image](https://github.com/user-attachments/assets/b59251f7-defe-4bd2-a9ae-fabdf8d9fe5d)

![image](https://github.com/user-attachments/assets/31815ff0-67d6-404a-9920-60636c9dab4a)

---

## Problem Description

The goal is to solve a simple IP optimization problem, such as a knapsack-type problem, by:
- Relaxing integer constraints to continuous constraints.
- Branching on fractional decision variables.
- Finding an optimal integer solution through systematic exploration.

---

## Approach

1. **LP Relaxation**  
   - Solve the relaxed LP to get a fractional solution.

2. **Branching**  
   - Select a decision variable with a fractional value and create two subproblems by adding integer constraints (floor and ceil).

3. **Node Exploration**  
   - Use a priority queue to determine the next node to explore.
   - Different strategies are tested:
     - Explore nodes in the order they are created.
     - Prioritize nodes where the fractional part is closest to 0.5.

4. **Termination**  
   - The algorithm terminates when an integer-feasible solution is found with no better candidate remaining.

---

## Key Features

- **Custom Branch and Bound implementation** using Gurobi for solving LP relaxations.
- **Flexible Priority Queue strategies** to guide branching order.
- **Experiments comparing different strategies** on node counts and convergence speed.
- **Modular Class Design** (`BB`, `BB_ver2`, `BB_ver3`) for different queueing logics.

---

## File Structure

```
/branch-and-bound
├── BranchandBound.py    # Basic standalone B&B implementation
├── bb_algorithm.py      # BB class: explore by creation order
├── bb_ver2.py           # BB_ver2 class: explore by 0.5-fraction closeness
├── bb_ver3.py           # BB_ver3 class: explore by objective value
├── test_case.py         # Test case generator (e.g., knapsack examples)
├── run.py               # Runner script to test and compare different versions
├── README.md            # Project documentation
```

---

## Requirements

- Python 3.x
- Gurobi Optimizer (with `gurobipy`)

Install Gurobi Python API:
```bash
pip install gurobipy
```

---

This README were prepared with assistance from ChatGPT.
