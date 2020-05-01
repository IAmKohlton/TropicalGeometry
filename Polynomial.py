import Variable
import math


class Polynomial(object):
    """ A tropical polynomial. This is a polynomial where addition is done with min(), and multiplication is done with +.
    """

    def __init__(self, input=None):
        """ initialize the polynomial.
        """
        if input is None:
            self.poly = None
            # it will be convention that this is a list [op, x_1, x_2, ...] which will correspond to something like
            # x_1 + x_2 + ... or x_1 * x_2 * ...
        elif isinstance(input, Polynomial):
            self.poly = input.poly
        else:
            assert isinstance(input, int) or isinstance(input, float) or isinstance(input, Variable.Variable)
            self.poly = input

        if isinstance(self.poly, Polynomial):
            raise Exception("Did something bad")
        elif isinstance(self.poly, Variable.Variable):
            self.vars = {self.poly}
        else:
            self.vars = set()

    def operate(self, input, op):
        """ A generalized version of addition, multiplication, and exponentiation
        """
        assert isinstance(input, int) or isinstance(input, float) or \
            isinstance(input, Polynomial) or isinstance(input, Variable.Variable)

        if self.poly is None:
            return Polynomial(input=input)
        else:
            newPoly = Polynomial()
            # newPoly.poly = (self, op, input)

            # cast the input to a Polynomial
            if isinstance(input, int) or isinstance(input, float) or isinstance(input, Variable.Variable):
                input = Polynomial(input=input)

            # these first three cases deal with when one of them is a basic type
            if not isinstance(self.poly, list) and not isinstance(input.poly, list):
                newPoly.poly = [op, self, input]
            elif not isinstance(self.poly, list):
                if op == input.poly[0]:
                    newPoly.poly = input.poly + [self]
            elif not isinstance(input.poly, list):
                if op == self.poly[0]:
                    newPoly.poly = self.poly + [input]

            # next four cases deal with when both are polynomials already
            elif op == self.poly[0] and op == input.poly[0]:
                newPoly.poly = self.poly + input.poly[1:]
            elif op == self.poly[0]:
                newPoly.poly = self.poly
                newPoly.poly.append(input)
            elif op == input.poly[0]:
                newPoly.poly = input.poly
                newPoly.poly.append(self)
            else:
                newPoly.poly = [op, self, input]

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
        if self.poly is None:
            return ""
        elif not isinstance(self.poly, list):
            return str(self.poly)
        else:
            outString = "("
            operation = self.poly[0]
            for term in self.poly[1:]:
                outString += str(term) + operation
            outString = outString[:-1] + ")"
            return outString

    def evalRecurse(self, x):
        if isinstance(self.poly, Variable.Variable):
            return x[self.poly.name]
        elif isinstance(self.poly, int) or isinstance(self.poly, float):
            return self.poly
        elif isinstance(self.poly, list):
            resultList = [branch.evalRecurse(x) for branch in self.poly[1:]]
            if self.poly[0] == "+":
                return min(resultList)
            if self.poly[0] == "*":
                return sum(resultList)
            if self.poly[0] == "^":
                return math.prod(resultList)

    def eval(self, x):
        if self.poly is None:
            return None

        varNameSet = {y.name for y in self.vars}
        if not isinstance(x, dict):
            if len(self.vars) != 1:
                raise Exception("Tried to evaluate polynomial %s with a single variable, but there is more than one variable that needs to be assigned" % str(self))
        elif varNameSet != set(x.keys()):
            raise Exception("Didn't assign all of the variables in the polynomial")
        result = self.evalRecurse(x)
        return result
