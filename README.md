=========
benchmark
=========

``benchmark`` is a Python benchmarking framework, similar to Steve Purcell's 
``unittest`` in basic structure. It's as simple as::

    import benchmark

    import math
    
    class Benchmark_Sqrt(benchmark.Benchmark):

        each = 100 # allows for differing number of runs

        def setUp(self):
            # Only using setUp in order to subclass later
            # Can also specify tearDown, eachSetUp, and eachTearDown
            self.size = 25000

        def test_pow_operator(self):
            for i in xrange(self.size):
                z = i**.5

        def test_pow_function(self):
            for i in xrange(self.size):
                z = pow(i, .5)

        def test_sqrt_function(self):
            for i in xrange(self.size):
                z = math.sqrt(i)

    class Benchmark_Sqrt2(Benchmark_Sqrt):
        # Subclass the previous benchmark to change input using
        # self.setUp()

        label = "Benchmark Sqrt on a larger range"
        # The above label comes from the class name, this oen
        # comes from the label attribute

        each = 50

        def setUp(self):
            self.size = 750000
    
    if __name__ == '__main__':
        benchmark.main(format="markdown", numberFormat="%.4g")
        # could have written benchmark.main(each=50) if the
        # first class shouldn't have been run 100 times.

which produces::

    Benchmark Report
    ================

    Benchmark Sqrt
    --------------

             name | rank | runs |     mean |        sd | timesBaseline
    --------------|------|------|----------|-----------|--------------
     pow operator |    1 |  100 | 0.004163 | 0.0001469 |           1.0
    sqrt function |    2 |  100 | 0.004584 |  0.000379 | 1.10126499627
     pow function |    3 |  100 | 0.005496 | 0.0002709 | 1.32031909568

    Benchmark Sqrt on a larger range
    --------------------------------

             name | rank | runs |   mean |       sd | timesBaseline
    --------------|------|------|--------|----------|--------------
     pow operator |    1 |   50 | 0.1265 | 0.004772 |           1.0
    sqrt function |    2 |   50 | 0.1375 | 0.004729 |    1.08705384
     pow function |    3 |   50 | 0.1649 | 0.003935 | 1.30357975885

    Each of the above 450 runs were run in random, non-consecutive order by
    `benchmark` v0.1.4 (http://jspi.es/benchmark) with Python 2.7.1
    Darwin-11.3.0-x86_64 on 2012-04-17 19:43:01.

More examples are available in the example folder or visit 
http://jspi.es/benchmark for more information.