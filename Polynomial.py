from Variable import Variable


class Polynomial(object):
    def __init__(self, input=None):
        if input is None:
            self.poly = (None, None, None)
        else:
            assert isinstance(input, int) or isinstance(input, float) or isinstance(input, Polynomial) or isinstance(input, Variable)
            self.poly = input

        if isinstance(self.poly, Polynomial):
            self.vars = self.poly.vars
        elif isinstance(self.poly, Variable):
            self.vars = {self.poly}
        else:
            self.vars = set()

    def operate(self, input, op):
        assert isinstance(input, int) or isinstance(input, float) or isinstance(input, Polynomial) or isinstance(input, Variable)
        if self.poly == (None, None, None):
            return Polynomial(input=input)
        else:
            newPoly = Polynomial()
            newPoly.poly = (self, op, input)
            if isinstance(input, Polynomial):
                newPoly.vars = input.vars | self.vars
            elif isinstance(input, Variable):
                newPoly.vars = {input} | self.vars
            else:
                newPoly.vars = self.vars
            return newPoly

    def __add__(self, input):
        return self.operate(input, "+")

    def __radd__(self, input):
        return self.operate(input, "+")

    def __mul__(self, input):
        return self.operate(input, "*")

    def __rmul__(self, input):
        return self.operate(input, "*")

    def __str__(self):
        if self.poly is (None, None, None):
            return ""
        elif not isinstance(self.poly, tuple):
            return str(self.poly)
        else:
            return "(" + str(self.poly[0]) + self.poly[1] + str(self.poly[2]) + ")"

    def eval(self, x):
        if self.poly is (None, None, None):
            return None
        elif isinstance(self.poly, Variable):
            return None
