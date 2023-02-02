def foo():
    pass


class Bar:
    def fuzz(self):
        pass

    def buzz(self, f):
        def g(self):
            f(self)

        return g(self)


Bar().buzz(foo)
