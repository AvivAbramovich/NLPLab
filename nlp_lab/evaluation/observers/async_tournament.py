from nlp_lab.evaluation.observers.tournament import TournamentDebatesObserver
from uuid import uuid1
from random import randint
from nlp_lab.extra.jobs_executor import JobsExecutorBase, QueueIsFullError


class TournamentDebatesAsyncObserver(TournamentDebatesObserver):
    class __JobExecutor__(JobsExecutorBase):
        def __init__(self, delegate, num_threads, sleeping_time_in_seconds=1, queue_limit=500, debug_print=False):
            super(TournamentDebatesAsyncObserver.__JobExecutor__, self)\
                .__init__(num_threads, sleeping_time_in_seconds, queue_limit)
            self.__delegate__ = delegate

        def generate_id(self):
            start_index = randint(0, 15)
            return str(uuid1()).replace('-', '')[start_index:start_index + 10]

        def on_job_finished(self, _id, job, args, description, result):
            self.__delegate__.__on_finish_debate__(args, result)

    def __init__(self, features_extractors, labeling_system, alternative_labeling_systems=None, debug_print=False):
        super(TournamentDebatesAsyncObserver, self)\
            .__init__(features_extractors, labeling_system, alternative_labeling_systems, debug_print)

        self.__jobs_executor__ = self.__JobExecutor__(self, 20, debug_print=debug_print)
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
        return super(TournamentDebatesAsyncObserver, self).digest()
