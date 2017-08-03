__a = 30

class C:
    __a = 5
    
    def __init__(self):
        self.__a = 10
        print (C.__a)
       
    def getA(self):
        global __a
        __a = 40
        return __a
     
    def setA(self, b):
        C.__a = b
        
           
c = C()
print (c.getA())
c.setA(11)  

c1 = C()
print (c1.getA())

def f():
    def g():
        def k():
            global v1
            print (v1)
            v1 = 23      
                  
        global v1
        v1 = 10
        print ("v1 em g()", v1)
        k()
        print ("v1 em k()", v1)
        
    def h():
        nonlocal v1
        v1 = 15
        print ("v1 em h()", v1)

    v1 = 2
    print ("v1 antes g():", v1)
    g()
    print ("v1 depois g():", v1)
    h()
    print ("v1 depois g():", v1)

def f1():    
    print (v1)
    v1=15
   
    
v1 = 5
print ("v1 antes f():",  v1)
f()
print ("v1 depois f():",  v1)
print (v1)
f1()