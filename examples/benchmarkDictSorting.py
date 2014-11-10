import benchmark

import random
from operator import itemgetter

# Source
# http://writeonly.wordpress.com/2008/08/30/sorting-dictionaries-by-value-in-python-improved/

def fnouter(x):
    return x[1]

class SortDictByValue(benchmark.Benchmark):
    
    label = "Sort Dict with 100 Keys by Value"
    each = 10000
    
    def setUp(self):
        self.d = dict(zip(range(100),range(100)))
    
    def eachSetUp(self):
        random.shuffle(self.d)
    
    def test_pep265(self):
        return sorted(self.d.iteritems(), key=itemgetter(1))
    
    def test_stupid(self):
        return [(k,v) for v,k in sorted([(v,k) for k,v in self.d.iteritems()])]
    
    def test_listExpansion(self):
        L = [(k,v) for (k,v) in self.d.iteritems()]
        return sorted(L, key=lambda x: x[1])
    
    def test_generator(self):
        L = ((k,v) for (k,v) in self.d.iteritems())
        return sorted(L, key=lambda x: x[1])
    
    def test_lambda(self):
        return sorted(self.d.iteritems(), key=lambda x: x[1])
    
    def test_formalFnInner(self):
        def fninner(x):return x[1]
        return sorted(self.d.iteritems(), key=fninner)
    
    def test_formalFnOuter(self):
        return sorted(self.d.iteritems(), key=fnouter)

class SortLargerDictByValue(SortDictByValue):
    
    label = "Sort Dict with 1000 Keys by Value"
    each = 1000
    
    def setUp(self):
        self.d = dict(zip(range(1000),range(1000)))

if __name__ == '__main__':
    benchmark.main() # each is a variable in the above classes

#  Benchmark Report
#  ================
#  
#  Sort Dict with 100 Keys by Value
#  --------------------------------
#  
#           name | rank |  runs |              mean |                sd
#  --------------|------|-------|-------------------|------------------
#         pep265 |    1 | 10000 | 5.30271053314e-05 | 1.32238298129e-05
#         lambda |    2 | 10000 | 6.49063587189e-05 | 1.62878955883e-05
#  formalFnInner |    3 | 10000 | 6.51606559753e-05 | 1.58921554292e-05
#  formalFnOuter |    4 | 10000 | 6.51744127274e-05 | 1.60679178962e-05
#  listExpansion |    5 | 10000 | 7.95884609222e-05 | 1.82228267913e-05
#      generator |    6 | 10000 | 8.46118688583e-05 |  1.9538229455e-05
#         stupid |    7 | 10000 | 0.000104244446754 | 2.17782310661e-05
#  
#  Sort Dict with 1000 Keys by Value
#  ---------------------------------
#  
#           name | rank | runs |              mean |                sd
#  --------------|------|------|-------------------|------------------
#         pep265 |    1 | 1000 | 0.000632953643799 | 0.000121171492027
#         lambda |    2 | 1000 | 0.000742829084396 | 0.000135560592706
#  formalFnOuter |    3 | 1000 |  0.00075030708313 | 0.000139851859294
#  formalFnInner |    4 | 1000 | 0.000758862733841 | 0.000144369829001
#  listExpansion |    5 | 1000 | 0.000893526315689 | 0.000153910494397
#      generator |    6 | 1000 | 0.000928285598755 | 0.000168435308868
#         stupid |    7 | 1000 |  0.00131661295891 | 0.000193817650395
#  
#  Each of the above 77000 runs were run in random, non-consecutive order by
#  `benchmark` v0.0.1 (http://jspi.es/benchmark) with Python 2.7.1 
#  Darwin-11.3.0-x86_64 on 2012-04-16 16:01:17.