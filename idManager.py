'''
Created on Jun 2, 2015

@author: Greg Silverman

get_id: requesting an id from an empty pool is not considered an error. 0 is
returned, since 0 is not a valid id the client can test if a valid id was returned.

ids are returned in integer order, modulo n. 

free_id: 

freeing an invalid id value is an exception, clients can query the object for the
valid range of ids, i.e., 1 through pool.size().

freeing an id that is available in the pool is not treated as an error or exception, although
it could be.

data structure:

a list of integers 1 through n. a value of i at index i indicates i is an available id, 0
indicates it is taken.

'''

class Pool(object):
    '''
    a pool of integer ids, 1 through self.__n, represented
    as a list of the integers, 1 through self.__n.
    
    when an id is taken its slot in the array is set to 0.
    
    '''
    
    def __init__(self,n):
        self.__n = n
        self.__available = n
        self.__pool = [i for i in xrange(1,n+1)]
        self.__index = 0
        
    def get_id(self):
        '''
        if the pool is not empty, find the next
        non-zero list entry and return that value.
        
        if the list is empty, return 0, which is not a
        valid id.
        '''
        if self.available():
            self.__available -= 1
            while self.__pool[self.__index]==0:
                self.__index += 1
                if self.__index==self.__n:
                    self.__index = 0
            v = self.__pool[self.__index]
            self.__pool[self.__index] = 0
            self.__index += 1
            if self.__index==self.__n:
                self.__index = 0
            return v
        else:
            return 0
        
    def free_id(self,anId):
        '''
        for a valid id, put it in its slot, otherwise, raise an exception.
        
        Note: freeing an id that was not taken could be considered an exceptional
        condition, but, is not at this time.
        
        '''
        if anId<1 or anId>self.__n:
            raise ValueError(str(anId)+" is an invalid id")
        else:
            self.__available += 1
            self.__pool[anId-1] = anId
    
    def available(self):
        return self.__available
    
    def size(self):
        return self.__n


'''
create a list of unit tests
'''
tests = []   
        
def t1():
    '''
    simplest test, an empty pool returns 0
    '''
    p = Pool(0);
    assert p.get_id()==0
    
tests.append(t1)

def t2():
    '''
    tests of getting and freeing from a size 1 pool, and,
    freeing invalid values.
    '''
    p = Pool(1)
    assert p.get_id()==1
    assert p.get_id()==0
    p.free_id(1)
    assert p.available()==1
    p.get_id()
    assert p.available()==0
    try:
        p.free_id(0)
        assert False
    except ValueError:
        pass
    try:
        p.free_id(p.size()+1)
        assert False
    except ValueError:
        pass
    
tests.append(t2)

'''
a "stress" test :)
'''
def t3():
    n = 256
    p = Pool(n)
    for i in xrange(1,n+1):
        assert p.get_id()==i 
    assert p.available()==0

tests.append(t3)

'''
test that ids can be freed in any order.

1. remove all odd ids
2. verify only even ids are left
3. free odd ids in reverse order
4. verify odd ids are there
'''
def t4():
    p = Pool(8)
    for i in xrange(p.size()):
        anId = p.get_id()
        if anId%2==0:
            p.free_id(anId)
    assert p.available()==p.size()/2
    for i in xrange(p.size()):
        anId = p.get_id()
        if i<=p.size()/2:
            assert anId%2==0
        else:
            assert anId==0
    for i in xrange(p.size()-1,0,-2):
        p.free_id(i)
        
    for i in xrange(p.size(),2):
        assert p.get_id()==i+1
    
tests.append(t4)    

if __name__=="__main__":
    #run the regression tests
    failureCount = 0
    try:
        for t in tests:
            t()
    except Exception as e:
        print e
        failureCount += 1
    print len(tests)-failureCount,'successes',failureCount,'failures'