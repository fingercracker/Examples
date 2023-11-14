from CircularImports import mod2

class A(mod2.B):
    x = "a"
    
    def __init__(self, a=None):
        if a is not None:
            self.a = a
