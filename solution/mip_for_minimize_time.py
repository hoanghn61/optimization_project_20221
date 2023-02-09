#MIP model opt time
from ortools.linear_solver import pywraplp

from itertools import combinations
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

def main():
  solver = pywraplp.Solver.CreateSolver('SCIP')
  if not solver:
    return
    
  #decision variables
  num_task, num_worker, timee, worker_for_task, start_time, presequisite, cost = input_data(input())
  print(timee)
  x = {}
  infinity = solver.infinity()
  for worker in range(num_worker):
    for task in range(num_task):
      x[worker, task] = solver.IntVar(0,1,'')
  st = {}
  for i in range(num_task):
    st[i] = solver.IntVar(0.0, solver.infinity() ,'')
  y = {}
  for i in range(num_task):
    y[i] = solver.IntVar(0,num_worker-1, '')
  finish_time = solver.IntVar(0, infinity, '')
  M = 100000

  #constraints
  #if the worker is not able to do the job then x[k,i] = 0
  for task in range(num_task):
    for worker in range(num_worker):
      if worker not in worker_for_task[task]:
        solver.Add(x[worker,task] == 0)
  #presequisite time
  for pair in presequisite:
    solver.Add(st[pair[0]]+ timee[pair[0]] <= st[pair[1]])
  #the task must be done by one worker
  for task in range(num_task):
    solver.Add(solver.Sum([x[worker,task] for worker in range(num_worker)]) == 1)
  #the start time requirement
  for task in range(num_task):
    for worker in range(num_worker):
      solver.Add(st[task] >= start_time[worker]+M*(x[worker,task]-1))

  #the obvious
  for task in range(num_task):
    for worker in range(num_worker):
      gamma = solver.BoolVar('')
      solver.Add(y[task]-worker <= M*(1-x[worker, task]))
      solver.Add(worker-y[task] <= M*(1-x[worker,task]))
      solver.Add(y[task] >= worker + 1 - M*gamma - M*x[worker,task])
      solver.Add(y[task] <= worker - 1 +M*(1-gamma) +M*x[worker,task])
  #if two tasks are performed by the same worker, they have to be non-overlapping

  for i in range(num_task-1):
    for j in range(i+1,num_task):
      x1 = solver.BoolVar('')
      x2 = solver.BoolVar('')
      solver.Add(st[i] + timee[i] <= st[j] + M*(1-x1))
      solver.Add(st[j] + timee[j] <= st[i] + M*(1-x2))

      b = solver.BoolVar('')
      solver.Add(x1 + x2 <= b*M)
      solver.Add(x1 + x2 +(1-b)*M >= 1)

      t0 = solver.IntVar(0,1,'')
      t1 = solver.IntVar(0,1,'')
      t2 = solver.IntVar(0,1,'')

      solver.Add(y[i] + t0 <= y[j] + M*t1)
      solver.Add(y[j] + t0 <= y[i] + M*t2)
      solver.Add(t1 + t2 == t0)

      solver.Add(b == 1 - t0)


  #salary = max salary among k workers

  h = {}
  U = max(start_time) + sum(timee)
  L = max(timee) +min(start_time)
  for task in range(num_task):
    h[task] = solver.BoolVar('')
    solver.Add(st[task] + timee[task] >= L)
    solver.Add(st[task] + timee[task] <= U)
    solver.Add(finish_time >= st[task] + timee[task])
    solver.Add(finish_time <= st[task] + timee[task] + M*(1-h[task]))
  solver.Add(sum([h[task] for task in range(num_task)]) == 1)

  #objective function
  solver.Minimize(finish_time)
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
  else:
    print('The problem does not have an optimal solution')
  print('\nAdvanced usage:')
  print('Problem solved in %f milliseconds' % solver.wall_time())
  print('Problem solved in %d iterations' % solver.iterations())
  print('Problem solved in %d branch-and-bound nodes' % solver.nodes())

  
if __name__ == '__main__':
  main()
