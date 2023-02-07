#greedy alg
import random
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
class Job:
  def __init__(self, cap_worker,exe_time, possible_start_time):
    self.cap_worker = cap_worker
    self.possible_start_time = possible_start_time
    self.exe_time = exe_time

  def set_st_ed(self, amount):
    self.start_time = amount
    self.end_time = self.start_time + self.exe_time

  def set_worker(self, worker):
    self.worker = worker

  def change_pos_st(self, amount):
    self.possible_start_time = amount

def transpose(matrix):
    trans = []
    for i in range(len(matrix[0])):
        col = [matrix[j][i] for j in range(len(matrix))]
        trans.append(col)
    return trans

def executable(matrix, i):
  matrix1 = transpose(matrix)
  if 1 not in matrix1[i]:
    return True

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v = list(d.values())
     k = list(d.keys())
     return k[v.index(max(v))]

def keywithminval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v = list(d.values())
     k = list(d.keys())
     return k[v.index(min(v))]

def keywithsatval(d, pos):
    v = list(d.values())
    k = list(d.keys())
    lst = []
    for i in v:
        if i >= pos:
            lst.append(i)
        else:
            lst.append(100000)
    if min(lst) == 100000:
        return None
    else:
        return k[lst.index(min(lst))]

def main():
    num_task, num_worker, time, worker_for_task, start_time, prerequisite, cost = input_data(input())

    adj_matrix = [[0]*num_task for task in range(num_task)]
    for i,j in prerequisite:
        adj_matrix[i][j] = 1

    tasks = {}
    for task in range(num_task):
        workers = worker_for_task[task][:]
        min_st = min([start_time[i] for i in workers])
        tasks[task] = Job(worker_for_task[task],time[task],min_st)
    cost_for_worker = {}
    for worker in range(num_worker):
        cost_for_worker[worker] = 0
    avai_time = {}
    for worker in range(num_worker):
        avai_time[worker] = start_time[worker]
  
    sorted = []
    while len(sorted) != num_task:
        frontier = {}
        for task in range(num_task):
            if executable(adj_matrix, task) and task not in sorted:
                frontier[task] = tasks[task].exe_time
        while True:
            sort_now = keywithmaxval(frontier)
            avai_ver = {}
            for worker in tasks[sort_now].cap_worker:
                avai_ver[worker] = avai_time[worker]
    
            if keywithsatval(avai_ver, tasks[sort_now].possible_start_time) == None:
                worker_index = random.sample(tasks[sort_now].cap_worker)
                tasks[sort_now].set_st_ed(tasks[sort_now].possible_start_time)
            else:
                worker_index = keywithsatval(avai_ver, tasks[sort_now].possible_start_time)
                tasks[sort_now].set_st_ed(avai_time[worker_index])
    
            
            tasks[sort_now].set_worker(worker_index)
            cost_for_worker[worker_index] += cost[sort_now][worker_index]
            avai_time[worker_index] = tasks[sort_now].end_time


            for task in range(num_task):
                if adj_matrix[sort_now][task] == 1:
                    tasks[task].change_pos_st(tasks[sort_now].end_time)

            del frontier[sort_now]

            adj_matrix[sort_now] = [-1 for i in range(num_task)]
            sorted.append(sort_now)
            if frontier == {}:
                break

    return tasks, cost_for_worker


tasks, cost_for_worker = main()
for key, value in tasks.items():
  print(f'task {key}:')
  print(f'worker: {value.worker}')
  print(f'start time {value.start_time}')
  print(f'end time: {value.end_time} \n')

for key,value in cost_for_worker.items():
  print(f'The amount of money to pay for worker {key} is: {cost_for_worker[key]}')

