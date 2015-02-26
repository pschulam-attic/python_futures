import math

from concurrent.futures import ProcessPoolExecutor, as_completed


def factorize_naive(n):
    """A naive factorization method. Take integer 'n', return list of
    factors.
    """
    if n < 2:
        return []
    
    factors = []
    p = 2

    while True:
        if n == 1:
            return factors

        r = n % p
        if r == 0:
            factors.append(p)
            n = n // p
        elif p * p >= n:
            factors.append(n)
            return factors
        elif p > 2:
            # Advance in steps of 2 over odd numbers
            p += 2
        else:
            # If p == 2, get to 3
            p += 1
            
    assert False, "unreachable"


def chunked_worker(nums):
    """Factorize a list of numbers, returning a num:factors mapping."""
    return {n: factorize_naive(n) for n in nums}


def pool_factorizer_chunked(nums, nprocs):
    """Manually divide the task to chunks of equal length, submitting each
    chunk to the pool.
    """
    chunksize = int(math.ceil(len(nums) / float(nprocs)))
    futures = []

    with ProcessPoolExecutor() as executor:
        for i in range(nprocs):
            chunk = nums[(chunksize * i) : (chunksize * (i + 1))]
            futures.append(executor.submit(chunked_worker, chunk))

    resultdict = {}
    for f in as_completed(futures):
        resultdict.update(f.result())
    return resultdict


def chunked_worker2(nums, my_id, nprocs):
    """Chop up the list more intelligently than the first."""
    return {n: factorize_naive(n) for i, n in enumerate(nums) if i % nprocs == my_id}


def pool_factorizer_chunked2(nums, nprocs):
    """Call the chunked_worker2 worker function."""
    futures = []

    with ProcessPoolExecutor() as executor:
        for i in range(nprocs):
            futures.append(executor.submit(chunked_worker2, nums, i, nprocs))

    resultdict = {}
    for f in as_completed(futures):
        resultdict.update(f.result())
    return resultdict


def pool_factorizer_map(nums, nprocs):
    """Let the executor divide the work among processes by using 'map'."""
    with ProcessPoolExecutor(max_workers=nprocs) as executor:
        return {num:factors for num, factors in
                                zip(nums,
                                    executor.map(factorize_naive, nums))}


if __name__ == '__main__':
    import sys, random

    strategy = int(sys.argv[1])
    nums = list(range(int(sys.argv[2])))
    nprocs = int(sys.argv[3])

    if strategy == 1:
        pool_factorizer_chunked(nums, nprocs)
    elif strategy == 2:
        random.shuffle(nums)
        pool_factorizer_chunked(nums, nprocs)
    elif strategy == 3:
        pool_factorizer_chunked2(nums, nprocs)
    elif strategy == 4:
        pool_factorizer_map(list(range(int(sys.argv[1]))), int(sys.argv[2]))
    else:
        raise RuntimeError('Strategy {} not recognized'.format(strategy))
