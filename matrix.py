import random 
import threading 
import time 
 
SIZE = 100 
LOW = 1 
HIGH = 10 
 
 
def make_matrix(): 
    return [[random.randint(LOW, HIGH) for _ in range(SIZE)] for _ in range(SIZE)] 
 
 
def sequential_product(left, right): 
    answer = [[0] * SIZE for _ in range(SIZE)] 
    for r in range(SIZE): 
        for c in range(SIZE): 
            answer[r][c] = sum(left[r][k] * right[k][c] for k in range(SIZE)) 
    return answer 
 
 
def threaded_product(left, right): 
    answer = [[0] * SIZE for _ in range(SIZE)] 
    guards = [[threading.Lock() for _ in range(SIZE)] for _ in range(SIZE)] 
    jobs = [] 
 
    def add_contribution(r, c, k): 
        contribution = left[r][k] * right[k][c] 
        with guards[r][c]: 
            answer[r][c] += contribution 
 
    started = time.perf_counter() 
 
    for r in range(SIZE): 
        for c in range(SIZE): 
            for k in range(SIZE): 
                job = threading.Thread(target=add_contribution, args=(r, c, k)) 
                jobs.append(job) 
                job.start() 
 
    for job in jobs: 
        job.join() 
 
    elapsed = time.perf_counter() - started 
    return answer, len(jobs), elapsed 
 
 
def main(): 
    first = make_matrix() 
    second = make_matrix() 
 
    expected = sequential_product(first, second) 
    actual, thread_count, seconds = threaded_product(first, second) 
 
    print("Threaded matrix multiplication finished.") 
    print(f"Matrix size: {SIZE} x {SIZE}") 
    print(f"Worker threads created: {thread_count}") 
    print(f"Elapsed time: {seconds:.4f} seconds") 
    print(f"Threaded result is correct: {actual == expected}") 
    print(f"Sample result [0][0]: {actual[0][0]}") 
 
 
if __name__ == "__main__": 
    main()