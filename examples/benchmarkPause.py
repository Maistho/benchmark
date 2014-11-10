import benchmark

import time

class BenchmarkPause(benchmark.Benchmark):
    
    def test_one_hundredth(self):
        time.sleep(.01)
    
    def test_one_tenth(self):
        time.sleep(.1)
    
if __name__ == '__main__':
    benchmark.main(each=10)

#  Benchmark Report
#  ================
#  
#  BenchmarkPause
#  --------------
#  
#           name | rank | runs |            mean |                sd
#  --------------|------|------|-----------------|------------------
#  one hundredth |    1 |   10 | 0.0107804536819 | 0.000254526626128
#      one tenth |    2 |   10 |  0.100682234764 | 0.000341868954907
#  
#  Each of the above 20 runs were run in random, non-consecutive order by
#  `benchmark` v0.1.0 (http://jspi.es/benchmark) with Python 2.7.1
#  Darwin-11.3.0-x86_64 on 2012-04-16 19:49:17.