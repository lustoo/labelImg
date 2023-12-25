class A(object):
    def __init__(self) -> None:
        self.a='4567'
        pass


class B(A):
    def __init__(self) -> None:
        super().__init__()
        print(self.a)


dir={
    'adsf':1,
    'ddfd':45,
    'kojahj':22
}

print(str(dir.keys())+','+str(dir.values()))
