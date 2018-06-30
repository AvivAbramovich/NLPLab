from threading import Thread, Lock
from time import sleep
from abc import ABCMeta, abstractmethod


class QueueIsFullError(Exception):
    def __init__(self, job_executor, job, args, description):
        self.job_executor = job_executor
        self.job = job
        self.args = args
        self.description = description
        self.message = 'The queue for the Jobs is full'

    def __str__(self):
        return self.message


class Locker:
    def __init__(self):
        self.lock = Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()


class JobsExecutorBase:
    __metaclass__ = ABCMeta

    def __init__(self, num_threads, sleeping_time_in_seconds=1, queue_limit=500):
        self.num_threads = num_threads
        self.waiting_queue = []
        self.working = {}
        self.lock = Locker()
        self.sleeping_time = sleeping_time_in_seconds
        self.should_terminate = False
        self.is_working = False
        self.threads = []
        self.queue_limit = queue_limit  # Note: the default value is just a magic number, better configure it after testing properly!

    @abstractmethod
    def generate_id(self):
        pass

    def on_job_start(self, _id, job, args, description):
        pass

    def on_job_finished(self, _id, job, args, description, result):
        pass

    def on_job_failed(self, _id, job, args, description, exception):
        pass

    def add_job(self, func, args, description=None):
        with self.lock:
            if len(self.waiting_queue) >= self.queue_limit:
                raise QueueIsFullError(self, func, args, description)

            _id = self.generate_id()
            self.waiting_queue.append((func, args, description, _id))
            return _id

    def start(self):
        if self.is_working:
            return
        else:
            self.is_working = True

        self.threads = []

        # Create new threads
        for i in range(self.num_threads):
            self.threads.append(self.ManagedThread(self))

        # Start new Threads
        for thread in self.threads:
            thread.start()

    def wait_and_end(self):
        if self.is_working:
            self.should_terminate = True
        else:
            return

        # Wait for all threads to complete
        for thread in self.threads:
            thread.join()

        self.should_terminate = False
        self.is_working = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait_and_end()

    def list_running(self):
        with self.lock:
            return self.working.items()

    def list_waiting(self):
        with self.lock:
            return [(_id, desc) for _, _, desc, _id in self.waiting_queue]

    class ManagedThread(Thread):
        def __init__(self, manager):
            Thread.__init__(self)
            self.manager = manager

        def run(self):
            result = None
            exception = None
            while True:
                with self.manager.lock:
                    if len(self.manager.waiting_queue) > 0:
                        job, args, desc, _id = self.manager.waiting_queue.pop()
                        self.manager.working[_id] = desc
                    else:
                        job = None
                        args = None
                        _id = None
                        desc = None
                if job:
                    self.manager.on_job_start(_id, job, args, desc)

                    # run the job and save the result (or exception), pop from working dict, and call callbacks
                    try:
                        result = job(*args)
                    except Exception as e:
                        exception = e

                    with self.manager.lock:
                        self.manager.working.pop(_id)

                    if result:
                        self.manager.on_job_finished(_id, job, args, desc, result)
                    else:
                        self.manager.on_job_failed(_id, job, args, desc, exception)

                    result = None
                    exception = None
                else:
                    if self.manager.should_terminate:
                        return
                    else:
                        sleep(self.manager.sleeping_time)
