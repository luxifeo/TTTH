import math
import sys  
from docplex.mp.model import Model
#
Ewce = 40000.0
U = 5.0
Ptravel = 1.0
Emin = 540.0
Emax = 10800.0
M = 10000.0
#
class Problem:
    def __init__(self, input_file):
        f = open(input_file, 'r')
        path_str = f.readline().split(' ')
        self.path = [int(x) for x in path_str]
        self.pos = [self.path.index(i) for i in range(1, len(self.path) + 1)]
        self.data = []
        for node in f:
            self.data.append([float(x) for x in node.split(' ')])
        f.close()
        self.N = len(self.path)
        assert self.N == len(self.data)
#
# Distance function

def distance(node1, node2):
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


# Initialize data
def solve(prob):
    node = [[0, 0]]
    P = []
    Tnode = []
    e_remain = []
    Ttsp = 0
    Tchar = 0
    N = prob.N
    for x in prob.path:
        node.append([prob.data[x - 1][0], prob.data[x - 1][1]])
        P.append(prob.data[x - 1][2])
        e_remain.append(prob.data[x - 1][3])
    # Calculate traveling time
    for i in range(N):
        length = distance(node[i], node[i+1])
        Ttsp += length / U
        Tnode.append(round(Ttsp, 3))
    Ttsp += distance(node[-1], node[0]) / U
    Tchar = (Ewce - Ttsp * Ptravel) / U
    # print(Ttsp)
    # print(Tchar)
    # print(P)
    # print(prob.path)
    # print(e_remain)
    # print(Tnode)
    # modeling
    model = Model(name='Phase 2')
    T = model.continuous_var_list(N, name='Time')
    F = model.binary_var_list(N, name='F')
    X = model.binary_var_list(N, name='X')
    Y = model.binary_var_list(N, name='Y')
    # Objective
    model.minimize(model.sum(F))
    # Constraint
    for i in range(N):
        model.add_constraint(Emin - e_remain[i] + (Tnode[i] + model.sum(T[:i])) * P[i] <= M * X[i])

        model.add_constraint(Emin - e_remain[i] + (Tnode[i] + model.sum(T[:i])) * P[i] >= M * (X[i] - 1))

        model.add_constraint(Emin - T[i] * U - e_remain[i] + (Ttsp - Tnode[i] + model.sum(T[i+1:])) * P[i] <= M * Y[i])

        model.add_constraint(Emin - T[i] * U - e_remain[i] + (Ttsp - Tnode[i] + model.sum(T[i+1:])) * P[i] >= M * (Y[i] - 1))

        model.add_constraint(F[i] >= X[i])

        model.add_constraint(F[i] >= Y[i])

        model.add_constraint(F[i] <= X[i] + Y[i])

        model.add_constraint(F[i] <= 1)

        model.add_constraint(T[i] >= 0)

        model.add_constraint(T[i] <= Tchar)

        model.add_constraint(T[i] * (U - P[i]) <= Emax - Emin)

    model.add_constraint(model.sum(T) == Tchar)

    if model.solve():
        model.print_solution()
        print('Dead node minimized: {}'.format(model.objective_value))
        for i in range(N):
            print('{:.3f}'.format(T[i].solution_value), end=' ')
        print()
        # for i in range(len(prob.pos)):
        #     print('Node {:d} charge time: {:.3f}'.format(i+1, T[prob.pos[i]].solution_value))
        print()
        for i in range(N):
            if F[i].solution_value == 1:
                print('Node {} is the dead node'.format(prob.path[i]))
        return (T, F)
    else:
        print('Problem not solved successfully')
        sys.exit(2)
#
def writeToFile(T, F, prob, output_file):
    print('Dump output to {}'.format(output_file))
    f = open(output_file, 'w+')
    for i in range(prob.N):
        f.write('{:.3f} '.format(T[prob.pos[i]].solution_value))
    dead_list = []
    for i in range(prob.N):
        if F[i].solution_value == 1:
            dead_list.append(prob.path[i])
    f.write('\n')
    dead_list.sort()
    for i in dead_list:
        f.write('{:d} '.format(i))
    f.write('\n{:d}'.format(len(dead_list)))
    f.close()
#

if __name__ == "__main__":
    try:
        input_file, output_file = sys.argv[1], sys.argv[2]
    except IndexError:
        print('python3 solve.py <inputfile> <outputfile>')
        sys.exit(2)
    prob = Problem(input_file)
    (T, F) = solve(prob)
    writeToFile(T, F, prob, output_file)
    