

class B(object):
    def __init__(self):
        self._bar = None

    def getbar(self):
        print("getter")
        return self._bar

    def setbar(self, value):
        print("setter")
        self._bar = value
    def delbar(self):
        print("delete")
        del self._bar

    bar = property(getbar, setbar, delbar)



if __name__ == '__main__':
    b = B()
    print(b.bar)
    print(b._bar)
    b.bar = 5
    print(b._bar)
    del b.bar
    print(b._bar)
