import threading
from queue import Queue
import time

'''
ThreadQueue class limits the amount of running threads and the lifespan of each one
by keeping track of how many 'jobs' each thread executed, after X jobs, the thread
dies and the main thread will create a new thread to continue executing the jobs.
'''
class ThreadQueue:
    def __init__(self,MAX_RUNNING_THREADS,THREAD_JOB_LIMIT):
        self.MAX_RUNNING_THREADS = MAX_RUNNING_THREADS
        self.THREAD_JOB_LIMIT = THREAD_JOB_LIMIT

        self.queue = Queue()
        self.active_threads = []
        
    def _threadJob(self,num):
        print(f"Thread {num} running")
        time.sleep(num)

    def _threadHandler(self):
        counter = 0 # to keep track of job limit

        while not self.queue.empty() and counter < self.THREAD_JOB_LIMIT:
            # get the job from the front of the queue
            self._threadJob(self.queue.get())
            self.queue.task_done()
            counter += 1

    def create_jobs(self,numbers_of_jobs):

        for job in range(0,numbers_of_jobs):
            self.queue.put(job)

    def _start_threads(self):

        for thread in self.active_threads:
            thread.start()

    def run_threads(self):
        """This function is responsible for new threads creation when a thread
            finished his lifespan, this is done by constantly checking 
            the jobs queue and the lifespan of each thread.
        Args:
            None
        Returns:
            None
        """
        #create 5 initial threads
        self.active_threads = [threading.Thread(target=self._threadHandler) for _ in range(self.MAX_RUNNING_THREADS)]

        while not self.queue.empty():
            # while there are more jobs
            for thread in self.active_threads:
                # if a thread finished his lifetime, create a new one
                if not thread.is_alive():
                    self.active_threads.remove(thread)
                    t = threading.Thread(target=self._threadHandler)
                    t.start()
                    self.active_threads.append(t)

def main():
    MAX_RUNNING_THREADS = 5
    THREAD_JOB_LIMIT = 1
    JOBS = 25

    thread_queue = ThreadQueue(MAX_RUNNING_THREADS,THREAD_JOB_LIMIT)
    thread_queue.create_jobs(JOBS)
    thread_queue.run_threads()


if __name__ == "__main__":
    main()