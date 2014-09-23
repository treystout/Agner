import logging

from pkg_resources import resource_string

from .job import Job
from .errors import EnqueueError

QUEUE_PREFIX = "AGNER:"
BLOCK_SECONDS = 1

class Queue(object):
  def __init__(self, queue_name, redis_connection):
    """Queues are responsible for both producing and consuming work
    You must pass in a connected Redis object as well as a string queue_name
    """
    self.redis = redis_connection
    self.__raw_queue_name = queue_name
    self.__should_run = True # set this to false to break consumer loops
    self.log = logging.getLogger("%s.%s" % (__name__, queue_name))

    # load the lua scripts and bind them to registered functions
    self.lua_next = self.redis.register_script(resource_string(__name__,
      'lua/next_job.lua'))

  def __len__(self):
    """Returns the number of jobs currently sitting in the queue
    """
    return self.redis.llen(self.queue_name)

  @property
  def queue_name(self):
    return "%s%s" % (QUEUE_PREFIX, self.__raw_queue_name)

  def enqueue(self, job):
    """Enqueue a job for later processing, returns the new length of the queue
    """
    if job.queue_name():
      raise EnqueueError("job %s already queued!" % job.job_id)
    new_len = self.redis.lpush(self.queue_name, job.serialize())
    job.notify_queued(self)
    return new_len

  def next_job(self, timeout_seconds=None):
    """Retuns the next job in the queue, or None if is nothing there
    """
    if timeout_seconds is not None:
      timeout = timeout_seconds
    else:
      timeout = BLOCK_SECONDS

    response = self.lua_next(keys=[self.queue_name])
    if not response:
      return

    job = Job.from_serialized(response)
    if not job:
      self.log.warn("could not deserialize job from: %s", serialized_job)
    return job

  def finish(self, job_id):
    """Notify the queue that a worker has completed work on a job_id. This
    removes the record from the queue as well as the holding area
    """
    pass


  def __iter__(self):
    """Generator interface that will block on a queue and return items as they
    become available
    """
    while self.__should_run:
      job = self.next_job()
      if job is not None:
        yield job
    raise StopIteration

  def empty(self):
    """Empties the queue, you rarely want this other than for testing
    """
    self.redis.delete(self.queue_name)
