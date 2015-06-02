'''
Created on Jun 2, 2015

@author: Greg Silverman
'''

class Pool(object):
    
    def __init__(self,n):
        self.__n = n
        self.__available = n
        self.__pool = [i for i in xrange(1,n+1)]
        self.__index = 0
        
    def get_id(self):
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
        if anId<1 or anId>self.__n:
            raise ValueError(str(anId)+" is an invalid id")
        else:
            self.__available += 1
            self.__pool[anId-1] = anId
    
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

tests.append(t3)

'''
test that ids can be freed in any order.

1. remove all odd ids
2. verify only even ids are left
3. free odd ids in reverse order

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
    for t in tests:
        t()