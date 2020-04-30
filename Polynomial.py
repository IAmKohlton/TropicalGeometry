import Variable


class Polynomial(object):
    def __init__(self, input=None):
        if input is None:
            self.poly = (None, None, None)
        else:
            assert isinstance(input, int) or isinstance(input, float) or isinstance(input, Polynomial) or isinstance(input, Variable.Variable)
            self.poly = input

        if isinstance(self.poly, Polynomial):
            self.vars = self.poly.vars
        elif isinstance(self.poly, Variable.Variable):
            self.vars = {self.poly}
        else:
            self.vars = set()

    def operate(self, input, op):
        assert isinstance(input, int) or isinstance(input, float) or isinstance(input, Polynomial) or isinstance(input, Variable.Variable)
        if self.poly == (None, None, None):
            return Polynomial(input=input)
        else:
            newPoly = Polynomial()
            newPoly.poly = (self, op, input)
            if isinstance(input, Polynomial):
                newPoly.vars = input.vars | self.vars
            elif isinstance(input, Variable.Variable):
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

    def __pow__(self, input):
        assert isinstance(input, int)
        return self.operate(input, "^")

    def __str__(self):
        if self.poly is (None, None, None):
            return ""
        elif not isinstance(self.poly, tuple):
            return str(self.poly)
        else:
            return "(" + str(self.poly[0]) + self.poly[1] + str(self.poly[2]) + ")"

    def evalRecurse(self, x):
        if isinstance(self.poly, Variable):
            return x[self.poly.name]
        elif isinstance(self.poly, int) or isinstance(self.poly, float):
            return self.poly
        elif isinstance(self.poly, tuple):
            if self.poly[1] == "+":
                return min(self.poly[0].evalRecurse(x), self.poly[2].evalRecurse(x))
            if self.poly[1] == "*":
                return self.poly[0].evalRecurse(x) + self.poly[2].evalRecurse(x)
            if self.poly[1] == "^":
                return self.poly[0].evalRecurse(x) * self.poly[2].evalRecurse(x)

    def eval(self, x):
        if self.poly is (None, None, None):
            return None

        varNameSet = {x.name for x in self.vars}
        if not isinstance(x, dict):
            if len(self.vars) != 1:
                raise Exception("Tried to evaluate polynomial %s with a single variable, but there is more than one variable that needs to be assigned" % str(self))
        elif varNameSet != x.keys:
            raise Exception("Didn't assign all of the variables in the polynomial")

        return self.evalRecurse(x)
