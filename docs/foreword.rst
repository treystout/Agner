.. _foreward:

A biased opinion on queueing
============================

Most python queueing systems are overkill for smaller web projects. You
generally just want to schedule some form of work for later. Of the most popular
solutions we have: 

 * enqueue executable code, and run it elsewhere later
 * enqueue data only, and rely on the consumer to know what to do with it 
   
Agner uses the second option. This allows your consumers to be written in whatever
language is suitable, and relieves the producing code of having to care about things
like variable scope, and imports.

