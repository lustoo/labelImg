class A(object):
    def __init__(self) -> None:
        self.a='4567'
        pass


class B(A):
    def __init__(self) -> None:
        super().__init__()
        print(self.a)

b=B()