import uuid


def foo():
    return uuid.uuid4()


class Bar:
    def fuzz(self):
        pass

    def buzz(self, f):
        def g(self):
            f(self)

        return g(self)


Bar().buzz(foo)
