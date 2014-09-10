class Error(Exception):
  """Base exception for rjob package, all other exceptions in this package
  will inherit from this.
  """
  pass

class EnqueueError(Error):
  """An error happened during enqueueing of a job
  """
  pass

