import random
import itertools 

n = int(input('The number of tasks: '))
m = int(input('The number of workers: '))
k = int(input('The number of pairs of prerequisites: '))

def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    j = len(pool)
    indices = sorted(random.sample(range(j), r))
    return tuple(pool[i] for i in indices)

def get_random_pairs(numbers, y): 
  # Generate all possible non-repeating pairs 
  pairs = list(itertools.combinations(numbers, 2)) 
 
  # Randomly shuffle these pairs 
  x = random.sample(pairs, y) 
  return x


def main():
    worker_list = list(range(m))
    f = open(f'{n} x {m} x {k}', 'w')
    time_and_capa = {}
    for i in range(n):
        time_and_capa[i] = [random.randint(1, 30)]
        num_cap = random.randint(1, m)
        cap_list = random_combination(worker_list, num_cap)
        for j in range(len(cap_list)):
            time_and_capa[i].append(cap_list[j])
    start_time = []
    for i in range(m):
        start_time.append(random.randint(0,20))
    presequisite = get_random_pairs(list(range(n)),k)
    cost_matrix = []
    for i in range(n):
        cost_worker = [random.randint(1,20) for i in range(m)]
        cost_matrix.append(cost_worker)

    f.write(f'{n} {m}\n')
    for i in range(n):
        f.write(' '.join(map(str,time_and_capa[i]))+'\n')
    f.write(' '.join(map(str,start_time))+'\n')
    f.write(str(k)+'\n')
    for i in range(k):
        f.write(' '.join(map(str,presequisite[i]))+'\n')
    for i in range(n):
        f.write(' '.join(map(str,cost_matrix[i])) + '\n')

main()
