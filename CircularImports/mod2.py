from CircularImports import mod1

class B:
    y = "b"

    def __init__(self, y=None):
        if y is not None:
            self.y = y
            self._thing = mod1.A.x