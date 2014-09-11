.. _tutorial:

Tutorial
========

A Simple Producer of Work
-------------------------

The following is an example script that finds all the words in a file,
then enqueues a job to look up the definition of each word

.. code-block:: python
  :linenos:

  # it's up to you to provide a configured redis connection to rjob
  from redis import StrictRedis()
  from agner import Queue, Job

  r = StrictRedis() # configure however you like
  # setup a queue keyed on the first argument, using the redis connection
  q = Queue('words_to_lookup', r)

  for word in "this is a sentence".split():
    # create a job
    job = Job(word=w)
    q.enqueue(job)

On the other side of this, we'll have a consumer script that will process our enqueued jobs::      

    from

    

