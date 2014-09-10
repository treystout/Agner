rjob
====

[![Build Status](https://travis-ci.org/treystout/rjob.svg?branch=master)](https://travis-ci.org/treystout/rjob)

Simple redis-backed queue that does not rely on eval or code insertion, only data.

## Install ##

    pip install rjob

## Basic Usage ##

Both your product and consumers of queued content will need an instance of
``RJobQueue``

    # first make a Redis Connection
    r = Redis(your_connection_info)

    # construct the queue, by giving it a reference to connected Redis client
    q = RJobQueue('some_name', r)

    # flush the queue by removing anything in there
    q.empty()

    # create a couple of jobs
    job1 = RJob(foo=1)
    job2 = RJob(foo=2)

    # insert them into the queue
    q.enqueue(job1)
    q.enqueue(job2)

    # you can either iterate the queue for jobs...
    for job in q:
      assert j.job_id == job1.job_id
      break

    # or get them 1 at a time in your own loop
    job = q.next_job()
