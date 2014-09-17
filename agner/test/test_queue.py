import pytest

from redis import Redis
import agner

TEST_QUEUE_NAME = "test_queue"

@pytest.fixture(scope="module")
def redis(request):
  redis = Redis()
  def finalizer():
    redis.delete(TEST_QUEUE_NAME)
  request.addfinalizer(finalizer)
  return redis

def test_create(redis):
  """product.create returns id of newly created item
  """
  q = agner.Queue(TEST_QUEUE_NAME, redis)
  assert q.queue_name.endswith(TEST_QUEUE_NAME), "queue should know its name"
  assert len(q) == 0, "there should be no jobs in the queue"

def test_enqueue(redis):
  job = agner.Job(string_key='string_value')
  q = agner.Queue(TEST_QUEUE_NAME, redis)
  new_len = q.enqueue(job)
  assert new_len == 1, "This should be the only job in the queue"

def test_double_enqueue(redis):
  q = agner.Queue(TEST_QUEUE_NAME, redis)
  job = agner.Job(foo=10)
  q.enqueue(job)
  with pytest.raises(agner.errors.EnqueueError):
    q.enqueue(job)

def test_ordering(redis):
  q = agner.Queue(TEST_QUEUE_NAME, redis)
  q.empty()
  job1 = agner.Job(foo=1)
  job2 = agner.Job(foo=2)
  q.enqueue(job1)
  q.enqueue(job2)
  # check loop
  for j in q:
    assert j.job_id == job1.job_id
    break
  # check one-off
  assert q.next_job().job_id == job2.job_id

def test_existing_jobs(redis):
  """New queue objects should repect already queued jobs
  """
  q = agner.Queue(TEST_QUEUE_NAME, redis)
  q.empty()
  job1 = agner.Job(foo=1)
  q.enqueue(job1)

  del q
  q2 = agner.Queue(TEST_QUEUE_NAME, redis)
  assert q2.next_job().job_id == job1.job_id

def test_payload(redis):
  q = agner.Queue(TEST_QUEUE_NAME, redis)
  q.empty()
  job1 = agner.Job(foo=1, bar={'x':'y'})
  q.enqueue(job1)

  j = q.next_job()
  assert j.payload['foo'] == 1, "payload should survive"
  assert j.payload['bar']['x'] == 'y', "payload should survive"
