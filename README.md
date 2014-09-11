Agner
=====

[![Build Status](https://travis-ci.org/treystout/Agner.svg?branch=master)](https://travis-ci.org/treystout/Agner)
[![Documentation Status](https://readthedocs.org/projects/agner/badge/?version=latest)](https://readthedocs.org/projects/agner/?badge=latest)


Simple redis-backed queue that does not rely on eval or code insertion, only data.

## Install ##

```shell
$ pip install agner
```

## Basic Usage ##

Full Documentation can be found at http://agner.readthedocs.org/en/latest/

Both your product and consumers of queued content will need an instance of
``agner.Queue``

```python
import redis
import agner

# first make a Redis Connection
r = redis.Redis(your_connection_info)

# construct the queue, by giving it a reference to connected Redis client
q = agner.Queue('some_name', r)

# flush the queue by removing anything in there
q.empty()

# create a couple of jobs
job1 = agner.Job(foo=1)
job2 = agner.Job(foo=2)

# insert them into the queue
q.enqueue(job1)
q.enqueue(job2)

# you can either iterate the queue for jobs...
for job in q:
  assert j.job_id == job1.job_id
  break

# or get them 1 at a time in your own loop
job = q.next_job()
```
