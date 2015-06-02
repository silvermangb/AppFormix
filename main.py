'''
Created on Jun 2, 2015

@author: Greg Silverman
'''

class Pool(object):
    
    def __init__(self,n):
        self.__n = n
        self.__available = n
        self.pool = set([i for i in xrange(1,n+1)])
        
    def get_id(self):
        if self.pool:
            self.__available -= 1
            return self.pool.pop()
        else:
            return 0
        
    def free_id(self,anId):
        if anId<1 or anId>self.__n:
            raise ValueError(str(anId)+" is an invalid id")
        else:
            self.__available += 1
            self.pool.add(anId)
    
    def available(self):
        return self.__available
    
    def size(self):
        return self.__n

tests = []   
        
def t1():
    p = Pool(0);
    assert p.get_id()==0
    
tests.append(t1)

def t2():
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

def t3():
    n = 256
    p = Pool(n)
    for i in xrange(1,n+1):
        assert p.get_id()==i 
    assert p.available()==0
    

if __name__=="__main__":
    for t in tests:
        t()