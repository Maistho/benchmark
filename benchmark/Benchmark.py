# Copyright 2012 Jeffrey R. Spies
# License: Apache License, Version 2.0
# Website: http://jspi.es/benchmark

import time
import random
import re
import operator
import math
import string
import sys
import os

class Benchmark(object):
    def __init__(self, each=5, prefix="test_", 
        setUp="setUp", tearDown="tearDown",
        eachSetUp="eachSetUp", eachTearDown="eachTearDown", 
        **kwargs):
        
        try:
            self.label = self.label
        except:
            self.label = None
        
        try:
            self.__n = self.each
        except:
            self.__n = each
            
        if sys.platform == "win32":
            # On Windows, the best timer is time.clock()
            self.__timer = time.clock
        else:
            # On most other platforms the best timer is time.time()
            self.__timer = time.time
        
        self.__prefix = prefix
        self.__setUp = setUp
        self.__tearDown = tearDown
        self.__eachSetUp = eachSetUp
        self.__eachTearDown = eachTearDown
        
    def __collectTests(self):
        return [test for test in dir(self) if test.startswith(self.__prefix)]
    
    def __runTest(self, name):
        tick = self.__timer()
        tResult = getattr(self, name)()
        tTime = self.__timer()-tick
        self.results[name]['total'] += tTime
        self.results[name]['sumOfSq'] += pow(tTime, 2)
        return tTime, tResult
    
    def __runFn(self, name):
        getattr(self, name)()
    
    def __testAndRunFn(self, name):
        if name in dir(self):
            self.__runFn(name)
    
    def run(self, previousResults=None):
        # TODO Add previous results
        
        self.__testAndRunFn(self.__setUp)
        
        tests = self.__collectTests()
        testQueue = []
        
        self.results = {}
        for number, testname in enumerate(tests):
            self.results[testname] = {'total':0, 'sumOfSq':0}
            testQueue.extend([number for i in range(0, self.__n)])
        
        random.shuffle(testQueue)
        
        dirSelf = dir(self)
        
        # Why the following?  Checks to see if eachSetUp and eachTearDown
        # functions would have to be done "each" number of times; this
        # checks once, and then, if there, runs them accordingly.
        if self.__eachSetUp in dirSelf and self.__eachTearDown in dirSelf:
            for testId in testQueue:
                self.__runFn(self.__eachSetUp)
                self.__runTest(tests[testId])
                self.__runFn(self.__eachTearDown)
        elif self.__eachSetUp in dirSelf:
            for testId in testQueue:
                self.__runFn(self.__eachSetUp)
                self.__runTest(tests[testId])
        elif self.__eachTearDown in dirSelf:
            for testId in testQueue:
                self.__runTest(tests[testId])
                self.__runFn(self.__eachTearDown)
        else:
            for testId in testQueue:
                self.__runTest(tests[testId])
        
        self.table = []

        for key in self.results.keys():
            row = {}
            row['name'] = key.replace(self.__prefix, '').replace('_', ' ')
            row['runs'] = self.__n
            row['mean'] = self.results[key]['total']/row['runs']
            row['total'] = self.results[key]['total']
            row['sumOfSquares'] = self.results[key]['sumOfSq']
            if row['runs'] > 1:
                row['var'] = (row['sumOfSquares']-pow(row['total'], 2)/row['runs'])/(row['runs']-1)
                row['sd'] = math.sqrt(row['var'])
            else:
                row['var'] = 'NA'
                row['sd'] = 'NA'            
            self.table.append(row)
        
        self.table = sorted(self.table, key=operator.itemgetter('mean'))
        for i, v in enumerate(self.table):
            v['rank'] = i+1
            v['timesBaseline'] = str(float(v['mean'])/float(self.table[0]['mean']))
        
        self.__testAndRunFn(self.__tearDown)
    
    def getTotalRuns(self):
        return self.__n*len(self.table)
    
    def __asMarkdown(self, header, table):
        maxSize = self.__columnWidths(header, table)
        lines = []
        lines.append(' | '.join([string.rjust(v, maxSize[i]) for i, v in enumerate(header)]))
        lines.append('-|-'.join(['-'*size for size in maxSize]))
        for row in table:
            lines.append(' | '.join([string.rjust(v, maxSize[i]) for i, v in enumerate(row)]))
        return os.linesep.join(lines)
    
    def __asRst(self, header, table):
        maxSize = self.__columnWidths(header, table)
        lines = []
        lines.append('+-' + '-+-'.join(['-'*size for size in maxSize]) + '-+')
        lines.append('| ' + ' | '.join([string.rjust(v, maxSize[i]) for i, v in enumerate(header)]) + ' |')
        lines.append('+=' + '=+='.join(['='*size for size in maxSize]) + '=+')
        for row in table:
            lines.append('| ' + ' | '.join([string.rjust(v, maxSize[i]) for i, v in enumerate(row)]) + ' |')
            lines.append('+-' + '-+-'.join(['-'*size for size in maxSize]) + '-+')
        return os.linesep.join(lines)
    
    def __asCsv(self, header, table):
        lines = []
        lines.append(','.join(header))
        for row in table:
            lines.append(','.join(row))
        return os.linesep.join(lines)
    
    def __columnWidths(self, header, table):
        sizes = []
        for h in header:
            sizes.append(len(h))
        for row in table:
            for j, v in enumerate(row):
                if len(v) > sizes[j]:
                    sizes[j] = len(v)
        return sizes
    
    def getTable(self, format="markdown", sort_by="mean", 
        order=['name', 'rank', 'runs', 'mean', 'sd', 'timesBaseline'], 
        header=None,
        formats=None, 
        numberFormat = "%.4g",
        **kwargs):
        
        # format = ['%s', '%s', '%d', "%.4g", "%.4g", "%.4g"]
        
        self.table = sorted(self.table, key=operator.itemgetter(sort_by))
        
        header = header if header else order

        reducedTable = []
        for i in self.table:
            row = []
            for o in order:
                value = i[o]
                try:
                    float(value)
                    value = numberFormat % value
                except: pass
                value = str(value)
                row.append(value)
            reducedTable.append(row)
        
        if format.lower() in ['markdown']:
            return self.__asMarkdown(header, reducedTable)
        elif format.lower() in ['csv', 'comma']:
            return self.__asCsv(header, reducedTable)
        else:
            return self.__asRst(header, reducedTable)