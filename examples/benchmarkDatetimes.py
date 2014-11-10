import benchmark

import time
import datetime

class TimeTests(benchmark.Benchmark):
    label = 'datetime vs. time'
    def test_utcnow(self):
        return datetime.datetime.utcnow().isoformat()[:-6]+'000Z'
    
    def test_gmtime(self):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

if __name__ == '__main__':
    benchmark.main(
        each=100, 
        format='rst', 
        order = ['rank', 'name', 'runs', 'mean'], # no sd
        header=["Rank", "Name","Runs", "Mean (s)"]
    )

#  Benchmark Report
#  ================
#  
#  datetime vs. time
#  -----------------
#  
#  +--------+------+------+-------------------+
#  |   Name | Rank | Runs |          Mean (s) |
#  +========+======+======+===================+
#  | utcnow |    1 |  100 | 4.78744506836e-06 |
#  +--------+------+------+-------------------+
#  | gmtime |    2 |  100 | 9.05752182007e-06 |
#  +--------+------+------+-------------------+
#  
#  Each of the above 200 runs were run in random, nonconsecutive order by 
#  `benchmark` v0.0.1 (http://jspi.es/benchmark) with Python 2.7.1
#  Darwin-11.3.0-x86_64 on 2012-04-16 16:03:12.