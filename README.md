# Python Futures Experiments

This is a small set of scripts used to experiment with the `concurrent.futures` Python 3 module. The code is adapted from Eli Bendersky's blog post [here](http://eli.thegreenplace.net/2013/01/16/python-paralellizing-cpu-bound-tasks-with-concurrent-futures). To run the experiments, change the variables in `run_experiments.sh` and launch it on the command line:

```
bash run_experiments.sh
```

You can place the call to the script within the body of a set of nested for-loops to obtain timing results across a variety of experimental settings.

## Conclusions

I found that for small, simple computations where there are many tasks (i.e. factorizing 500,000 numbers) manually dividing the tasks and distributing across the pool works best (this is Strategy 1). The map solution was *very* slow (Strategy 4). I believe that Python creates a new `Futures` object for each task, and so the overhead completely overwhelms the benefits gained from parallelization.

If running many small tasks, I recommend that you manually allocate chunks of the input to different workers. If your tasks are larger, however, then the `map` method of the Executor subclasses allows for elegant code and the overhead of creating futures for each task should be acceptable.
