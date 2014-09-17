import redis
from agner import Queue, Job

r = redis.StrictRedis()
q = Queue("test_queue", r)

# you can clear a queue of all work with empty(), generally you won't want to do
# that so that you can restart a crashed consumer, and still see the existing
# jobs
q.empty()

# produce some "work"...
for word in ['these', 'are', 'some', 'words']:
  j = Job(word=word, something_else="whatever")
  print "job before queue %r" % j
  new_count = q.enqueue(j)
  print "job after queue %r" % j
  print "new queue count: %d" % new_count

# you can see the number of jobs in the queue with len()
print "jobs in queue", len(q)

# you can get the next job without looping by calling next_job
next_job = q.next_job()

# that job you got should match the payload of what was inserted
print next_job.payload



