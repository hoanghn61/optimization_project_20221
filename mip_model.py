from ortools.linear_solver import pywraplp
import sys
def input_data(file_name):
  with open(file_name) as f:
    n,m = [int(x) for x in f.readline().split()]
    time = []
    worker_for_task = []
    for _ in range(n):
      text = f.readline().split()
      time.append(float(text[0]))
      worker_for_task.append([int(i) for i in text[1:]])
    start_time = [float(t) for t in f.readline().split()]
    k = int(f.readline().split()[0])
    presequisite = []
    for _ in range(k):
      presequisite.append([int(c) for c in f.readline().split()])
    cost = []
    for _ in range(n):
      cost.append([float(x) for x in f.readline().split()])
    return n, m, time, worker_for_task, start_time, presequisite, cost

#MIP model

def main():
  solver = pywraplp.Solver.CreateSolver('SCIP')
  if not solver:
    return
    
  #decisions variables
  num_task, num_worker, timee, worker_for_task, start_time, presequisite, cost = input_data(input())
  infinity = solver.infinity()
  x = {}
  for worker in range(num_worker):
    for task in range(num_task):
      x[worker, task] = solver.IntVar(0,1,'')
  st = {}
  for i in range(num_task):
    st[i] = solver.NumVar(0.0, infinity,'')
  y = {}
  for i in range(num_task):
    y[i] = solver.IntVar(0,num_worker, '')
  salary = solver.NumVar(0.0, max([sum(row_cost) for row_cost in cost]),'')
  M = 100000

  #constraints
  #if the worker is not able to do the job then x[k,i] = 0
  for task in range(num_task):
    for worker in range(num_worker):
      if worker not in worker_for_task[task]:
        solver.Add(x[worker,task] == 0)
  #presequisite time
  for pair in presequisite:
    solver.Add(st[pair[0]]+timee[pair[0]] <= st[pair[1]])
  #the task must be done by one worker
  for task in range(num_task):
    solver.Add(solver.Sum([x[worker,task] for worker in range(num_worker)]) == 1)
  #the start time requirement
  for task in range(num_task):
    for worker in range(worker):
      solver.Add(st[task] >= start_time[worker]+M*(x[worker,task]-1))
  #the obvious
  for task in range(num_task):
    for worker in range(num_worker):
      solver.Add(y[task]-worker <= M*(1-x[worker, task]))
      solver.Add(worker-y[task] <= M*(1-x[worker,task]))
  #if two tasks are performed by the same worker, they have to be non-overlapping
  alpha = {}
  delta = {}
  for i in range(num_task-1):
    alpha[i] = []
    delta[i] = []
    for j in range(i+1,num_task):
      alpha[i].append(solver.IntVar(0,1,''))
      delta[i].append(solver.IntVar(0,1,''))
      solver.Add(y[i]-y[j] <= M*(1-alpha[i][j-i-1]))
      solver.Add(y[j]-y[i] <= M*(1-alpha[i][j-i-1]))
      solver.Add(st[i] >= st[j] + timee[j] - M*delta[i][j-i-1] - M*(1-alpha[i][j-i-1]))
      solver.Add(st[i] <= st[j] - timee[i] + M*(1-delta[i][j-i-1]) + M*(1-alpha[i][j-i-1]))
  #salary = max salary among k workers
  L = 0
  U = max([sum([cost[i][j] for i in range(num_task)]) for j in range(num_worker)])
  print(U)
  d = {}
  for worker in range(num_worker):
    d[worker] = solver.IntVar(0,1,'')
    #solver.Add(solver.Sum([x[worker,task]*cost[task][worker]]) <= U)
    #solver.Add(solver.Sum([x[worker,task]*cost[task][worker]]) >= L)
    solver.Add(salary >= solver.Sum([x[worker,task]*cost[task][worker] for task in range(num_task)]))
    solver.Add(salary <= solver.Sum([x[worker,task]*cost[task][worker] for task in range(num_task)]) + (U-L)*(1-d[worker]))
  solver.Add(solver.Sum([d[worker] for worker in range(num_worker)])==1)

  #objective function
  solver.Minimize(salary)
  solver.set_time_limit(300*1000)

  #initialize the solver
  status = solver.Solve()

  if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print(f'Objective value ={solver.Objective().Value()}')
    for task in range(num_task):
      print(f'task {task} is performed by worker {y[task].solution_value()} at time {st[task].solution_value()}')
    for worker in range(num_worker):
      print(f'money to pay for worker {worker} is {sum([x[worker,task].solution_value()*cost[task][worker] for task in range(num_task)])}')
      print(d[worker].solution_value())
  else:
    print('The problem does not have an optimal solution')
  print('\nAdvanced usage:')
  print('Problem solved in %f milliseconds' % solver.wall_time())
  print('Problem solved in %d iterations' % solver.iterations())
  print('Problem solved in %d branch-and-bound nodes' % solver.nodes())

  
if __name__ == '__main__':
  main()

  

  




