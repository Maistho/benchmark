import benchmark

import tempfile
import os
from glob import iglob
import fnmatch
import re

# Source
# http://www.reddit.com/r/Python/comments/de2xp/dae_need_this_in_a_lot_of_projects/c0zj813?context=3

class BenchmarkGlobs(benchmark.Benchmark):
    
    label = "Glob Tests"
    
    def setUp(self):
        self.walk_root = tempfile.gettempdir()
        for i in xrange(0, 100):
            tempfile.mkstemp(suffix=".txt")
    
    def test_glob(self):
        items = []
        for root, dirs, files in os.walk(self.walk_root):
            for item in iglob(os.path.join(root, '*.txt')):
                items.append(item)
    
    def test_fnmatch(self):
        items = []
        for root, dirs, files in os.walk(self.walk_root):
            for item in fnmatch.filter(files, '*.txt'):
                items.append(os.path.join(root, item))
    
    def test_re(self):
        items = []
        rex = re.compile(".*\.txt$")
        for root, dirs, files in os.walk(self.walk_root):
            for item in files:
                if rex.match(item):
                    items.append(os.path.join(root, item))

if __name__ == '__main__':
    benchmark.main(each=50)

#  Benchmark Report
#  ================
#  
#  Glob Tests
#  ----------
#  
#     name | rank | runs |           mean |              sd
#  --------|------|------|----------------|----------------
#       re |    1 |   50 | 0.262927365303 | 0.0152220841337
#  fnmatch |    2 |   50 | 0.265928983688 | 0.0218745928887
#     glob |    3 |   50 | 0.274979395866 | 0.0158716836404
#  
#  Each of the above 150 runs were run in random, non-consecutive order by
#  `benchmark` v0.0.1 (http://jspi.es/benchmark) with Python 2.7.1 
#  Darwin-11.3.0-x86_64 on 2012-04-16 15:54:58.