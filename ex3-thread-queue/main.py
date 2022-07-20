import threading
from queue import Queue
import time

# limit the number of jobs each thread can execute in its lifetime
# When the thread has finished that many jobs it will quit 
# and the main thread will create a new worker thread
MAX_RUNNING_THREADS = 5
THREAD_JOB_LIMIT = 1

q = Queue()

def threadJob(num):
    # when this exits, the print_lock is released
    print(f"Thread {num} running")
    time.sleep(num)

def threadHandler():
    counter = 0 # to keep track of job limit
    while not q.empty() and counter < THREAD_JOB_LIMIT:
        # get the job from the front of the queue
        threadJob(q.get())
        q.task_done()
        counter += 1

def main():
    # Add jobs to queue
    for job in range(0,25):
        q.put(job)

    # create 5 initial threads
    active_threads = [threading.Thread(target=threadHandler) for i in range(MAX_RUNNING_THREADS)]

    #start them
    for thread in active_threads:
        thread.start()

    # check whenever the queue is not empty
    while not q.empty():
        for thread in active_threads:
            # if a thread finished his lifetime, create a new one
            if not thread.is_alive():
                active_threads.remove(thread)
                t = threading.Thread(target=threadHandler)
                t.start()
                active_threads.append(t)

if __name__ == "__main__":
    main()