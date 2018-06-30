from nlp_lab.evaluation.observers.tournament import TournamentDebatesObserver
from uuid import uuid1
from random import randint
from nlp_lab.extra.jobs_executor import JobsExecutorBase, QueueIsFullError


class JobExecutor(JobsExecutorBase):
    def __init__(self, num_threads, on_success_method, sleeping_time_in_seconds=3, queue_limit=500):
        super(JobExecutor, self).__init__(num_threads, sleeping_time_in_seconds, queue_limit)
        self.__on_success_method = on_success_method

    def generate_id(self):
        start_index = randint(0, 15)
        return str(uuid1()).replace('-', '')[start_index:start_index+10]

    def on_job_finished(self, _id, job, args, description, result):
        self.__on_success_method(args, result)


class TournamentDebatesAsyncObserver(TournamentDebatesObserver):
    def __init__(self, features_extractors, labeling_system, alternative_labeling_systems=None):
        super(TournamentDebatesAsyncObserver, self).__init__(features_extractors, labeling_system, alternative_labeling_systems)

        self.__jobs_executor__ = JobExecutor(10, self.__on_finish_debate__)
        self.__jobs_executor__.start()

    def observe(self, debate, name=None):
        # start new job
        try:
            self.__jobs_executor__.add_job(self.__observe_job__, (debate, name), name)
        except QueueIsFullError:
            return False
        return True

    def digest(self):
        self.__jobs_executor__.wait_and_end()
        return super(self).digest()
